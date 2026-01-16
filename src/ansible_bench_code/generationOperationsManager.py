import logging
from baseOperationsManager import BaseOperationManager
from pathlib import Path
import post_processing
from typing import Tuple
from ollama import ResponseError
from quality_assurance import check_yamllint, check_ansible_lint, check_playbook_syntax

logger = logging.getLogger(__name__)

class GenerationOperationManager(BaseOperationManager):    
    def clean_text(self, raw_output: str) -> str:
        return post_processing.clean_text_yaml(self, raw_output)
    
    def setup_files(self):
        """
        Setup files:
            - File directory with original Ansible-Roles
            - File directory with the generated prompts
        """
        if not self.args.output_path:
            self.main_output_file = Path.cwd().parent / "output.yml" 
            self.main_output_path = Path.cwd().parent   
        else:
            self.main_output_file = Path(self.args.output_path)   
            self.main_output_path = self.main_output_file.parent    

    def run(self):
        print("Chat started. Type your messages below (Ctrl+D or Ctrl+C to exit):")
        print("------------------------------------------------------")

        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                print("Exited.")
                break

            if not user_input.strip():
                continue

            # Nutzeranfrage → LLM soll Ansible-Playbook generieren
            result = self.get_validated_playbook(user_input)
            if result is None:
                continue
            if self.args.template_type == "task_file":
                print(f"\n{self.args.model} (validated task-file):\n")
            else:
                print(f"\n{self.args.model} (validated playbook):\n")
            print(result)
            print(f"Your generated Ansible-YAML is also saved in {self.main_output_file}\n------------------------------------------------------")


    def get_validated_playbook(self, prompt_str: str) -> str:
        output_file = self.main_output_file
        try:
            logger.info("Creating prompt and validating context for benchmark")
            template, p_str, error_msg = self.create_prompt_validate_context(prompt_str, "first_yamllint")
            if error_msg:
                logger.error(f"Error in creating prompt or validating context: {error_msg}")
                return error_msg
            logger.info("Invoking prompt chain for benchmark")
            raw_outputs = self.invoke_prompt_chain(template, p_str)
            logger.info(f"Raw LLM output: {raw_outputs}")
            cleaned_outputs = self.clean_text(raw_outputs)
            logger.info(f"Cleaned LLM output: {cleaned_outputs}")
            with output_file.open("w", encoding="utf-8") as f:
                f.write(cleaned_outputs)
            #if max iterations for yamllint and ansiblelint are defined
            if self.args.max_yamllint_iterations is not None:
                max_iterations_yamllint = self.args.max_yamllint_iterations
                logger.info(f"setting max iterations for yamllint to {max_iterations_yamllint}")

            if self.args.max_ansiblelint_iterations is not None:
                max_iterations_ansiblelint = self.args.max_ansiblelint_iterations
                logger.info(f"setting max iterations for ansiblelint to {max_iterations_ansiblelint}")

            if self.args.max_syntaxcheck_iterations is not None:
                max_iterations_syntax = self.args.max_syntaxcheck_iterations
                logger.info(f"setting max iterations for syntaxcheck to {max_iterations_syntax}")
                
            errors_ansiblelint = 0
            errors_syntax = 0

            while True:
                logger.info("Starting quality assurance while loop")
                status_flag_yamllint = False
                logger.info("setting status_flag_yamllint to False")
                i = 1
                while True:
                    if self.args.max_yamllint_iterations is not None and i > max_iterations_yamllint:
                        logger.info("Breaking yamllint loop due to max iterations reached")
                        print(f"{self.args.model}: Yamllint did not pass after {max_iterations_yamllint} iterations, breaking loop.")
                        print(f"Last generated saved at: {output_file}")
                        print(f"Last generated YAML: \n {cleaned_outputs}")
                        print("------------------------------------------------------")
                        return None
                    logger.info(f"Yamllint iteration {i}")
                    i += 1
                    yamllint_check_results: Tuple[bool, str] = check_yamllint(output_file)
                    if yamllint_check_results[0]:
                        logger.info(f"Yamllint passed at iteration {i}")
                        status_flag_yamllint=True
                        break
                    else: 
                        logger.info(f"Yamllint failed at iteration {i} with message: {yamllint_check_results[1]}")
                        template, p_str, recursive_str, error_str, error_msg = self.create_recursive_prompt_validate_context(prompt_str, cleaned_outputs, yamllint_check_results[1], "recursive_yamllint")
                        logger.info("Created recursive prompt for yamllint")
                        if error_msg:
                            logger.error(f"Error in creating recursive prompt or validating context: {error_msg}")
                            return error_msg
                        raw_outputs = self.invoke_recursive_chain(template, p_str, cleaned_outputs, yamllint_check_results[1])
                        logger.info("Invoked recursive prompt chain for yamllint")
                        logger.info(f"Raw LLM output after yamllint: {raw_outputs}")
                        cleaned_outputs = self.clean_text(raw_outputs)
                        logger.info("Cleaned LLM output after yamllint")
                        with output_file.open("w", encoding="utf-8") as f:
                            f.write(cleaned_outputs)
                        logger.info(f"Wrote cleaned output to YAML file: {output_file}")


                if not status_flag_yamllint:
                    break
                
                if (self.args.template_type == "playbook"):
                    syntax_check: Tuple[bool, str] = check_playbook_syntax(output_file, Path(self.args.inventory))
                    if not syntax_check[0]:
                        errors_syntax += 1
                        if self.args.max_syntaxcheck_iterations is not None and errors_syntax >= max_iterations_syntax:
                            logger.info(f"Syntax check did not pass after {max_iterations_syntax} iterations, breaking loop.")
                            logger.info(f"added {output_file} to failed_at_stage_syntaxcheck list")
                            print(f"{self.args.model}: Syntax check did not pass after {max_iterations_syntax} iterations, breaking loop.")
                            print(f"Last generated saved at: {output_file}")
                            print(f"Last generated YAML: \n {cleaned_outputs}")
                            print("------------------------------------------------------")
                            return None
                        template, p_str, recursive_str, error_str, error_msg = self.create_recursive_prompt_validate_context(prompt_str, cleaned_outputs, syntax_check[1], "recursive_syntaxcheck")
                        if error_msg:
                            return error_msg
                        raw_outputs = self.invoke_recursive_chain(template, p_str, cleaned_outputs, syntax_check[1])
                        cleaned_outputs = self.clean_text(raw_outputs)
                        # copy generated file into molecule test directory
                        with output_file.open("w", encoding="utf-8") as f:
                            f.write(cleaned_outputs)
                        continue
                    errors_syntax = 0

                ansiblelint_check: Tuple[bool, str] = check_ansible_lint(output_file)
                if not ansiblelint_check[0]:
                    errors_ansiblelint += 1
                    logger.info(f"Ansiblelint failed at iteration {errors_ansiblelint} with message: {ansiblelint_check[1]}")
                    logger.info(f"Ansiblelint errors so far: {errors_ansiblelint}")
                    if self.args.max_ansiblelint_iterations is not None and errors_ansiblelint > max_iterations_ansiblelint:
                        logger.info(f"Ansiblelint did not pass after {max_iterations_ansiblelint} iterations, breaking loop.")
                        logger.info(f"added {output_file} to failed_at_stage_ansiblelint list")
                        print(f"{self.args.model}: Ansiblelint did not pass after {max_iterations_ansiblelint} iterations, breaking loop.")
                        print(f"Last generated saved at: {output_file}")
                        print(f"Last generated YAML: \n {cleaned_outputs}")
                        print("------------------------------------------------------")
                        return None
                    logger.info("Creating recursive prompt for ansiblelint")
                    template, p_str, recursive_str, error_str, error_msg = self.create_recursive_prompt_validate_context(prompt_str, cleaned_outputs, ansiblelint_check[1], "recursive_ansiblelint")
                    if error_msg:
                        logger.info(f"Error in creating recursive prompt or validating context: {error_msg}")
                        return error_msg
                    logger.info("Invoking recursive prompt chain for ansiblelint")
                    raw_outputs = self.invoke_recursive_chain(template, p_str, cleaned_outputs, ansiblelint_check[1])
                    logger.info(f"Raw LLM output after ansiblelint: {raw_outputs}")
                    cleaned_outputs = self.clean_text(raw_outputs)
                    logger.info("Cleaned LLM output after ansiblelint")
                    with output_file.open("w", encoding="utf-8") as f:
                        f.write(cleaned_outputs)
                    logger.info(f"Wrote cleaned output to YAML file: {output_file}")
                    logger.info("Continuing while loop for next ansiblelint iteration")
                    continue
                return cleaned_outputs
        except (ValueError, FileNotFoundError) as e:
            logger.error(f"Exception occurred: {e}")
        except (ResponseError, Exception) as e:
            logger.error(f"LLM Exception occurred: {e}")
            logger.info("Corrected statistics after exception")
            logger.info(f"added {output_file} to failed_with_exception list")
    logger.info("Generation and validation process completed")


