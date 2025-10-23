from datetime import datetime
from io import TextIOWrapper
from langchain.schema import AIMessage
import os
import re
import traceback
import shutil
from typing import Tuple
from dotenv import load_dotenv
import time
import argparse
from ollama import ResponseError
from tqdm import tqdm
from pathlib import Path
from quality_assurance import check_yamllint, check_playbook_syntax, check_ansible_lint, check_molecule
from llm_abstraction import LLMSettings, llm_wrapper
import llm_chain
from utils.cli_abstraction import CLIArgumentsBase, CLIArgumentsPrompt, CLIArgumentsBenchmark, CLIArgumentsGeneration
from utils.config import Config, load_config
from utils.metadata import GenerationMetadata
from utils.logging_utilities import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


class BaseOperationManager:
    def __init__(self, args: CLIArgumentsBase, config: Config):
        self.args = args
        self.config = config
        self.set_model_name_engine()

    def set_model_name_engine(self):
        if "llamafile" in self.args.engine:
            self.model_name = self.args.model
            print("Name for the llamafile model:", self.model_name)
            logger.info(f"Name for the llamafile model: {self.model_name}")
            self.model_engine = "llamafile"
        elif "ollama" in self.args.engine:
            self.model_name = self.args.model
            print("Name for the ollama model:", self.model_name)
            logger.info(f"Name for the ollama model: {self.model_name}")
            self.model_engine = "ollama"
        elif "langchain" in self.args.engine:
            self.model_name = self.args.model
            print("Name for the langchain model:", self.model_name)
            logger.info(f"Name for the langchain model: {self.model_name}")
            self.model_engine = "torch"
        else:
            raise NotImplementedError("The given model was not implemented.")
            logger.error("The given model was not implemented.")
        return self.model_name, self.model_engine

    def scan_tasks(self, file_extension, directory):
        logger.info(f"Scanning directory {directory} for files with extension {file_extension}")
        result = []
        for root, _, files in os.walk(directory):
            if os.path.basename(root) == "tasks":
                yml_files = [f for f in files if f.endswith(file_extension)]
                for f in yml_files:
                    rel_dir = os.path.relpath(root, directory)
                    result.append(os.path.join(rel_dir, f))
        logger.info(f"Found {len(result)} files with extension {file_extension} in {directory}")
        for r in result:
            logger.info(f"Found file: {r}")
        return result

    def setup_llm(self):
        llm_settings = LLMSettings(
            top_k=self.args.top_k,
            top_p=self.args.top_p,
            temperature=self.args.temperature,
            repeat_penalty=1,
        )
        logger.info(f"Setup LLM: {llm_settings}")
        self.llm = llm_wrapper(self.model_name, self.model_engine, llm_settings=llm_settings)
        self.save_model_metadata(llm_settings)

    def save_model_metadata(self, llm_settings):
        logger.info("Saving model metadata")
        tm = GenerationMetadata(self.args.operation_mode, self.model_name, self.model_engine, llm_settings, [self.args.template_type], self.args.language)
        tm.save_to_file(self.main_output_path / "metadata.yml")

    def setup_files(self):
        raise NotImplementedError
    
    def run(self):
        raise NotImplementedError
    
    def clean_text(self, raw_output: str) -> str:
        raise NotImplementedError

    def create_prompt_validate_context(self, input_str, stage):
        logger.info(f"Creating prompt for stage: {stage}")
        templates = llm_chain.create_prompt_template_for_model(self.model_name, self.args.operation_mode, self.args.language, self.args.template_type, stage)
        logger.info(f"Filling prompt template: {templates[0]}")
        prompt = llm_chain.fillin_prompt_template(
            templates[0],
            input_str,
        )
        logger.info(f"Created prompt: {prompt}")
        print("\n\nPrompt: " + prompt)
        logger.info(f"Checking context size for model: {self.model_name}")
        max_output_tokens = llm_chain.check_context_size(prompt, self.model_name)
        if max_output_tokens <= 0:
            logger.info(f"The tokens exceeded the maximum size of the context window by {max_output_tokens} tokens.")
            return f"# Token size exceeded by {-max_output_tokens} tokens"
        logger.info(f"Context size is within limits. Max output tokens: {max_output_tokens}")
        return templates[0], input_str, None
    
    def create_recursive_prompt_validate_context(self, input_str, recursive_str, error_str, stage):
        logger.info(f"Creating recursive prompt for stage: {stage}")
        templates = llm_chain.create_prompt_template_for_model(self.model_name, self.args.operation_mode, self.args.language, self.args.template_type, stage)
        logger.info(f"Filling recursive prompt template: {templates[0]}")
        prompt = llm_chain.fillin_prompt_template(
            templates[0],
            input_str,
            recursive_str,
            error_str,
        )
        logger.info(f"Created recursive prompt: {prompt}")
        print("Prompt: " + prompt)

        max_output_tokens = llm_chain.check_context_size(prompt, self.model_name)
        if max_output_tokens <= 0:
            logger.info(f"The tokens exceeded the maximum size of the context window by {max_output_tokens} tokens.")
            return f"# Token size exceeded by {-max_output_tokens} tokens"
        logger.info(f"Context size is within limits. Max output tokens: {max_output_tokens}")
        return templates[0], input_str, recursive_str, error_str, None

    #def create_prompt_validate_context_recursive selbe methode nur um weitere Felder im prompt erweitert
    
    def invoke_prompt_chain(self, template, input_str):
        logger.info("Invoking prompt chain")
        return llm_chain.create_and_invoke_prompt_chain(
            template,
            self.llm,
            input_str,
        )
    
    def invoke_recursive_chain(self, template, input_str, recursive_str, error_str):
        logger.info("Invoking recursive prompt chain")
        return llm_chain.create_and_invoke_recursive_chain(
            template,
            self.llm,
            input_str,
            recursive_str,
            error_str,
        ) 
    
#--------------- End of Class

class PromptOperationManager(BaseOperationManager):
    def setup_files(self):
        self.input_dir = self.config.dataset_dir / self.args.dataset
        print("\nInput_Directory: "+str(self.input_dir))
        logger.info(f"Input_Directory: {self.input_dir}")
        if not self.input_dir.exists():
            logger.error(f"Directory {str(self.input_dir)} does not exist.")
            raise FileNotFoundError(f"Directory {str(self.input_dir)} does not exist.")

        self.main_output_path = (
            self.config.dataset_dir/ "prompts" /f"{self.model_engine}_{self.model_name}_{self.args.language}_{self.args.template_type}" / self.args.dataset
        )
        self.main_output_path = self.main_output_path
        os.makedirs(self.main_output_path, exist_ok=True)
        print("\nOutput_Directory: "+str(self.main_output_path))
        logger.info(f"Output_Directory: {self.main_output_path}")
        self.in_files = self.scan_tasks(('.yml', '.yaml'), self.input_dir)

        self.in_files = [
            f for f in self.in_files
            if os.path.basename(f) not in ("assert.yml", "assert.yaml")
        ]

        print("\nInput-Files:")
        logger.info(f"Input-Files: {self.in_files}")
        logger.info(f"Found {len(self.in_files)} input files.")
        for file_name in self.in_files:
            print(file_name)
            logger.info(f"Found input file: {file_name}")
        print(f"Found {len(self.in_files)} inputs\n")

    def run(self):
        logger.info("Starting prompt generation run")
        for f in tqdm(self.in_files):
            playbook_file = self.input_dir / f
            logger.info(f"Processing file: {playbook_file}")
            playbook_str = ""
            with open(playbook_file, "r", encoding="UTF-8", errors="ignore") as fin:
                logger.info(f"Reading file: {playbook_file}")
                playbook_str = fin.read()

            try:
                logger.info(f"Start try catch block for file: {playbook_file}")
                t0 = time.perf_counter()
                logger.info("Creating prompt and validating context")
                template, pb_str, error_msg = self.create_prompt_validate_context(playbook_str, "first")
                if error_msg:
                    logger.error(f"Error in creating prompt or validating context: {error_msg}")
                    return error_msg
                
                logger.info("Invoking prompt chain")
                raw_outputs = self.invoke_prompt_chain(template, pb_str)
                
                print(f"___________________________________________LLM Output:___________________________________________ \n{raw_outputs.content}")

                if self.model_name in {"gpt-oss:20b", 
                                       "qwen2.5:14b", 
                                       "granite-code:20b", 
                                       "codestral:22b",
                                       "phi4:14b",
                                       "llama3.1:8b"}:
                    cleaned_outputs = raw_outputs.content
                    logger.info(f"No cleaning applied for {self.model_name}.")
                    logger.info(f"Raw output: {cleaned_outputs}")
                else:
                    cleaned_outputs = self.clean_text(raw_outputs)
                    logger.info(f"Cleaned output for {self.model_name}.")
                    logger.info(f"Cleaned output: {cleaned_outputs}")
                    print(f"___________________________________________Cleaned LLM Output:___________________________________________ \n{cleaned_outputs}")

                t1 = time.perf_counter()

                f_path = Path(f)
                relative_dir = f_path.parent
                target_dir = self.main_output_path / relative_dir
                target_dir.mkdir(parents=True, exist_ok=True)
                base_name = f_path.stem
                out_file = target_dir / f"{base_name}_prompt.txt"

                print(f"\n{time.ctime()}: {out_file} Total generation time:", t1 - t0)
                logger.info(f"Total generation time for {out_file}: {t1 - t0} seconds")
                with open(out_file, "w") as fot:
                    print(cleaned_outputs, file=fot)

            except (ValueError, FileNotFoundError, Exception) as e:
                print(e)

                continue
    
    def clean_text(self, raw_output: str) -> str:
        """
        Cleans text:
        - removes everything in front of the first quotation mark
        - removes everthing following the last quotation mark
        - removes stamp </s>.
        """
        if isinstance(raw_output, AIMessage):
            raw_output = raw_output.content
            logger.info(f"Raw output is an AIMessage. Extracted content: {raw_output}")

        if self.model_name == "deepseek-r1:14b":
            raw_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
            logger.info("Removed <think>...</think> tags for deepseek-r1:14b model.")
            logger.info(f"Output after removing <think> tags: {raw_output}")
            
        if '"' in raw_output:
            raw_output = raw_output.split('"', 1)[1]  
            logger.info("Removed text before the first quotation mark.")
            logger.info(f"Output after removing text before first quotation mark: {raw_output}")
        raw_output = raw_output.lstrip()
        logger.info(f"Output after left stripping whitespace: {raw_output}")

        if '"' in raw_output:
            raw_output = raw_output.rsplit('"', 1)[0]
            logger.info("Removed text after the last quotation mark.")
            logger.info(f"Output after removing text after last quotation mark: {raw_output}")


        raw_output = re.sub(r'</s>', '', raw_output, flags=re.IGNORECASE)
        logger.info("Removed </s> tags.")
        logger.info(f"Output after removing </s> tags: {raw_output}")

        return raw_output.strip()


class BenchmarkOperationManager(BaseOperationManager):
    def setup_benchmark_tmp_log(self):
        """
        creates benchmark log file and temp directory
        """
        self.main_output_path.mkdir(parents=True, exist_ok=True)

        self.tmp_dir = self.main_output_path / "tmp"
        if self.tmp_dir.exists():
            shutil.rmtree(self.tmp_dir)
            logger.info(f"Removed existing temporary directory: {self.tmp_dir}")
        self.tmp_dir.mkdir()
        logger.info(f"Created temporary directory: {self.tmp_dir}")
        print(f"\nTemporary directory for benchmark run created: {self.tmp_dir}")

    def setup_test_directory(self):
        """
        copies all ansible-roles
        """
        for role_dir in self.input_dir.iterdir():
            if role_dir.is_dir():
                target = self.main_output_path / "molecule_test" / role_dir.name
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(role_dir, target)
                logger.info(f"Copied role directory {role_dir} to {target}")
                print(f"Copied {role_dir.name} to {target}.")
    
    
    def setup_files(self):
        """
        Setup files:
            - File directory with original Ansible-Roles
            - File directory with the generated prompts
        """
        self.input_dir = self.config.dataset_dir / self.args.dataset
        print("\nInput_Directory: "+str(self.input_dir))
        logger.info(f"Input_Directory: {self.input_dir}")
        self.prompt_dir = self.config.dataset_dir / self.args.prompts
        print("\nPrompts_Directory: "+str(self.prompt_dir)+"\n")
        logger.info(f"Prompts_Directory: {self.prompt_dir}")

        if not self.input_dir.exists():
            logger.error(f"Directory {str(self.input_dir)} does not exist.")
            raise FileNotFoundError(f"Directory {str(self.input_dir)} does not exist.")

        prompt_model = self.extract_prompt_model(str(self.prompt_dir))

        self.main_output_path = (
            self.config.output_dir / f"{self.model_engine}_{self.model_name}_{self.args.language}_{self.args.template_type}" / self.args.dataset / prompt_model
        )
        logger.info(f"Setting main output path: {self.main_output_path} / {self.model_engine}_{self.model_name}_{self.args.language}_{self.args.template_type} / {self.args.dataset} / {prompt_model}")
        logger.info(f"Main output path: {self.main_output_path}")
        os.makedirs(self.main_output_path, exist_ok=True)

        self.setup_test_directory()
        
        self.setup_benchmark_tmp_log()

        print("\nOutput_Directory: "+str(self.main_output_path))
        logger.info(f"Output_Directory: {self.main_output_path}")

        self.prompt_files = self.scan_tasks('.txt', self.prompt_dir)
        print("\nInput-Files:")
        logger.info(f"Prompt files: {self.prompt_files}")
        for file_name in self.prompt_files:
            print(file_name)
            logger.info(f"Found prompt file: {file_name}")
        print(f"found {len(self.prompt_files)} inputs")
        logger.info(f"Found {len(self.prompt_files)} prompt files.")

    def extract_prompt_model(self, path: str) -> str:
        m = re.search(r"(?:ollama|llamafile)_(.*?)_[^_/]+_[^_/]+", path)
        if not m:
            return path
        core = m.group(1)
        return f"prompts_{core}"
    
    def clean_text(self, raw_output: str) -> str:
            """
            Cleans text while preserving line content and line breaks:
            - removes everything in front of '---'
            - removes everything following '```'
            - removes stamp </s>
            - removes everything after two consecutive empty lines
            - removes everything after a single empty line if the next line
            does not contain ':' and is not indented
            - checks output is not empty
            """
            
            if isinstance(raw_output, AIMessage):
                raw_output = raw_output.content
                logger.info(f"Raw output is an AIMessage. Extracted content: {raw_output}")
            
            backup_input = raw_output
            
            if self.model_name == "deepseek-r1:14b":
                raw_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
                logger.info("Removed <think>...</think> tags for deepseek-r1:14b model.")
                logger.info(f"Output after removing <think> tags: {raw_output}")

            # remove everything before '---'
            if '---' in raw_output:
                raw_output = '---' + raw_output.split('---', 1)[1]
                logger.info("Removed text before the first '---'.")
                logger.info(f"Output after removing text before '---': {raw_output}")

            # remove everything after '```'
            if '```' in raw_output:
                raw_output = raw_output.split('```', 1)[0]
                logger.info("Removed text after the first '```'.")
                logger.info(f"Output after removing text after '```': {raw_output}")

            # remove everything after '...'
            if '...' in raw_output:
                raw_output = raw_output.split('...', 1)[0]
                logger.info("Removed text after the first '...'.")
                logger.info(f"Output after removing text after '...': {raw_output}")

            # remove </s>
            raw_output = raw_output.replace("</s>", "")
            logger.info("Removed </s> tags.")
            logger.info(f"Output after removing </s> tags: {raw_output}")

            # remove everything after the last non-empty line
            lines = raw_output.splitlines(keepends=True)
            cleaned_lines = []
            empty_count = 0

            for i, line in enumerate(lines):
                is_empty = line.strip() == ''

                if is_empty:
                    empty_count += 1

                    # check for single empty line
                    if empty_count == 1 and i + 1 < len(lines):
                        next_line = lines[i + 1]
                        stripped_next = next_line.lstrip()
                        # delete rest if ':' not in AND not indented
                        if ':' not in next_line and len(next_line) == len(stripped_next):
                            break

                    # two consecutive empty lines → break
                    if empty_count >= 2:
                        if cleaned_lines and cleaned_lines[-1].strip() == '':
                            cleaned_lines.pop()
                        break
                else:
                    empty_count = 0
                    cleaned_lines.append(line)

                # keep empty lines
                if is_empty:
                    cleaned_lines.append(line)

            # check if output is empty if so return uncleaned output
            if not cleaned_lines:
                logger.warning("Cleaned output is empty, returning uncleaned output.")
                return backup_input.strip() + "\n"

            if self.model_name in {"gpt-oss:20b",
                                   "granite-code:20b",}:
                logger.info("Appending newline to cleaned output for gpt-oss:20b model.")
                return ''.join(cleaned_lines) + "\n"
            logger.info("Returning cleaned output.")
            logger.info(f"Cleaned output: {''.join(cleaned_lines)}")
            return ''.join(cleaned_lines)



    def run(self):
        molecule_works_flag = False
        start_time = datetime.now()
        # loop over input files
        failed_at_stage_yamllint = []
#        failed_at_stage_syntax = []
        failed_at_stage_ansiblelint = []
        failed_at_stage_molecule_test = []
        passed_all_stages = []
        failed_initial_molecule_test = []
        failed_with_exception = []
        yamllint_runs = 0
        yamllint_passed_without_iteration = 0
        yamllint_passed_at_first_attempt = 0
        ansiblelint_runs = 0
        ansiblelint_passed_at_first_attempt = 0

        for f in tqdm(self.prompt_files):
            f_yamllint_runs = 0
            f_yamllint_passed_without_iteration = 0
            f_yamllint_passed_at_first_attempt = 0
            f_ansiblelint_runs = 0
            f_ansiblelint_passed_at_first_attempt = 0
            logger.info(f"Processing prompt file: {f}") 
            self.reports(start_time, 
                        failed_initial_molecule_test,
                        failed_at_stage_yamllint, 
                        #failed_at_stage_syntax, 
                        failed_at_stage_ansiblelint, 
                        failed_at_stage_molecule_test, 
                        passed_all_stages, 
                        self.main_output_path,
                        yamllint_runs,
                        yamllint_passed_without_iteration,
                        yamllint_passed_at_first_attempt,
                        ansiblelint_runs,
                        ansiblelint_passed_at_first_attempt,
                        failed_with_exception)
            logger.info("Intermediate report generated.")
            prompt_file = self.prompt_dir / f
            if not prompt_file.name.endswith("_prompt.txt"):
                logger.error(f"File {prompt_file} does not end with '_prompt.txt', raised ValueError")
                raise ValueError(f"File {prompt_file} does not end with '_prompt.txt'")

            logger.info(f"Looking for corresponding YAML/YML file for prompt: {prompt_file}")
            yaml_file = f.replace("_prompt.txt", ".yaml")
            yaml_path = self.main_output_path / "molecule_test" / yaml_file
            #yaml_path = prompt_file.with_name(prompt_file.stem.replace("_prompt.txt", "") + ".yaml")
            if not yaml_path.exists():
                logger.info(f"YAML file {yaml_path} not found, trying .yml extension.")
                yaml_path = yaml_path.with_suffix(".yml")
            if not yaml_path.exists():
                logger.error(f"No YAML/YML found for {prompt_file}, raised FileNotFoundError")
                raise FileNotFoundError(f"No YAML/YML found for {prompt_file}")
            
            # This should be used, but molecule takes too much time for all runs 
            #print("\nInitial Molecule Test of original file: ", yaml_path)
            #if not check_molecule(yaml_path):
            #    failed_initial_molecule_test.append(yaml_path)
            #    continue

            tmp_copy = self.tmp_dir / yaml_path.name
            shutil.copy2(yaml_path, tmp_copy)
            logger.info(f"Copied original YAML file {yaml_path} to temporary location {tmp_copy}")

            prompt_str = ""
            with open(prompt_file, "r", encoding="UTF-8", errors="ignore") as fin:
                prompt_str = fin.read()
            logger.info(f"Read prompt file: {prompt_file}")

            try:
                logger.info(f"Start try catch block for file: {yaml_path}")
                t0 = time.perf_counter()
                logger.info("Creating prompt and validating context for benchmark")
                template, p_str, error_msg = self.create_prompt_validate_context(prompt_str, "first_yamllint")
                if error_msg:
                    logger.error(f"Error in creating prompt or validating context: {error_msg}")
                    return error_msg
                logger.info("Invoking prompt chain for benchmark")
                raw_outputs = self.invoke_prompt_chain(template, p_str)
                print(f"___________________________________________LLM Output:___________________________________________ \n{raw_outputs}")
                logger.info(f"Raw LLM output: {raw_outputs}")
                cleaned_outputs = self.clean_text(raw_outputs)
                print(f"_______________________________________Cleaned LLM Output:_______________________________________ \n{cleaned_outputs}")
                logger.info(f"Cleaned LLM output: {cleaned_outputs}")
                t1 = time.perf_counter()
                print(f"\n{time.ctime()}: {yaml_path} Total generation time:", t1 - t0)
                logger.info(f"Total generation time for {yaml_path}: {t1 - t0} seconds")

                # copy generated file into molecule test directory
                logger.info(f"Writing cleaned output to YAML file: {yaml_path}")
                with yaml_path.open("w", encoding="utf-8") as f:
                    f.write(cleaned_outputs)
                
                max_iterations_yamllint = 5
                logger.info(f"setting max iterations for yamllint to {max_iterations_yamllint}")

#                max_iterations_syntax = 5
                max_iterations_ansiblelint = 4
                logger.info(f"setting max iterations for ansiblelint to {max_iterations_ansiblelint}")
#                errors_syntax = 0
                logger.info("setting up error counters")
                errors_ansiblelint = 0

                while True:
                    logger.info("Starting quality assurance while loop")
                    # check yamllint, syntax, ansiblelint from here
                    status_flag_yamllint = False
                    logger.info("setting status_flag_yamllint to False")
                    for i in range(1,max_iterations_yamllint+1): 
                        logger.info(f"Yamllint iteration {i}")
                        print(f"________________________________________Yamllint Run: {i}________________________________________\n")
                        yamllint_check_results: Tuple[bool, str] = check_yamllint(yaml_path)
                        yamllint_runs += 1
                        f_yamllint_runs += 1
                        if yamllint_check_results[0]:
                            logger.info(f"Yamllint passed at iteration {i}")
                            status_flag_yamllint=True
                            break
                        else: 
                            logger.info(f"Yamllint failed at iteration {i} with message: {yamllint_check_results[1]}")
                            print(f"{i}. Iteration in a row: Generated Ansible-YAML did not pass quality gate 'yamllint'")
                            template, p_str, recursive_str, error_str, error_msg = self.create_recursive_prompt_validate_context(prompt_str, cleaned_outputs, yamllint_check_results[1], "recursive_yamllint")
                            logger.info("Created recursive prompt for yamllint")
                            if error_msg:
                                logger.error(f"Error in creating recursive prompt or validating context: {error_msg}")
                                return error_msg
                            raw_outputs = self.invoke_recursive_chain(template, p_str, cleaned_outputs, yamllint_check_results[1])
                            logger.info("Invoked recursive prompt chain for yamllint")
                            print(f"___________________________________________LLM Output:___________________________________________ \n{raw_outputs}")
                            logger.info(f"Raw LLM output after yamllint: {raw_outputs}")
                            cleaned_outputs = self.clean_text(raw_outputs)
                            logger.info("Cleaned LLM output after yamllint")
                            print(f"_______________________________________Cleaned LLM Output:_______________________________________ \n{cleaned_outputs}")
                            t1 = time.perf_counter()
                            print(f"\n{time.ctime()}: {yaml_path} Total generation time:", t1 - t0)
                            logger.info(f"Total generation time for {yaml_path}: {t1 - t0} seconds")

                            # copy generated file into molecule test directory
                            with yaml_path.open("w", encoding="utf-8") as f:
                                f.write(cleaned_outputs)
                            logger.info(f"Wrote cleaned output to YAML file: {yaml_path}")
                    else:
                        logger.info(f"Yamllint did not pass after {max_iterations_yamllint} iterations, breaking loop.")
                        print(f"Error: Generated Ansible-YAML did not pass quality gate 'yamllint' after defined maximum of {max_iterations_yamllint} iterations in a row!")

                    if i < 2:
                        logger.info("Yamllint passed without iteration")
                        yamllint_passed_without_iteration += 1
                        f_yamllint_passed_without_iteration += 1
                        print(f"yamllint_passed_without_iteration increased to {yamllint_passed_without_iteration}")
                        if errors_ansiblelint == 0:
                            yamllint_passed_at_first_attempt += 1
                            f_yamllint_passed_at_first_attempt += 1
                            print(f"yamllint_passed_at_first_attempt increased to {yamllint_passed_at_first_attempt}")


                        
                    if not status_flag_yamllint:
                        logger.error("Yamllint failed, exiting while loop")
                        print(f"\nGeneration of playbook '{yaml_path}' failed at stage 'yamllint'")
                        logger.error(f"Generation of playbook '{yaml_path}' failed at stage 'ansiblelint'")

                        if(errors_ansiblelint>0):
                            print(f"Note: {errors_ansiblelint} ansible-lint iterations were done before!")
                            failed_at_stage_ansiblelint.append(yaml_path)
                            logger.error(f"Note: {errors_ansiblelint} ansible-lint iterations were done before!")
#                        elif(errors_syntax>0):
#                            print(f"Note: {errors_syntax} syntax-check iterations were done before!")
#                            failed_at_stage_syntax.append(yaml_path)
                        else:
                            failed_at_stage_yamllint.append(yaml_path)
                            logger.error(f"added {yaml_path} to failed_at_stage_yamllint list")
                        break
                    
                    print("################################# Quality Gate 'yamllint' passed! ################################")

#                    syntax_check: Tuple[bool, str] = check_playbook_syntax(yaml_path)
#                    if not syntax_check[0]:
#                        errors_syntax += 1
#                        if errors_syntax >= max_iterations_syntax:
#                            print(f"Error: Generated Ansible-YAML did not pass quality gate 'ansible-playbook --syntax-check' after defined maximum of {max_iterations_syntax} iterations!")
#                            print(f"\nGeneration of playbook '{yaml_path}' failed at stage 'ansible-plybook --syntax-check'")
#                            failed_at_stage_syntax.append(yaml_path)
#                            break
#                        print(f"{errors_syntax+1}. Iteration: Generated Ansible-YAML did not pass quality gate 'ansible-playbook --syntax-check'")
#                        template, p_str, recursive_str, error_str, error_msg = self.create_recursive_prompt_validate_context(prompt_str, cleaned_outputs, syntax_check[1], "recursive_syntaxcheck")
#                        if error_msg:
#                            return error_msg
#                        raw_outputs = self.invoke_recursive_chain(template, p_str, cleaned_outputs, syntax_check[1])
#                        print(f"Prompt String: \n{p_str}")
#                        print(f"___________________________________________LLM Output:___________________________________________ \n{raw_outputs}")
#                        cleaned_outputs = self.clean_text(raw_outputs)
#                        print(f"___________________________________________Cleaned LLM Output:___________________________________________ \n{cleaned_outputs}")
#                        t1 = time.perf_counter()
#                        print(f"\n{time.ctime()}: {yaml_path} Total generation time:", t1 - t0)
#
#                        # copy generated file into molecule test directory
#                        with yaml_path.open("w", encoding="utf-8") as f:
#                            f.write(cleaned_outputs)
#                        continue
#                    print("##################### Quality Gate 'ansible-playbook --syntax-check' passed! #####################")
#                    errors_syntax = 0

                    ansiblelint_check: Tuple[bool, str] = check_ansible_lint(yaml_path)
                    ansiblelint_runs += 1
                    f_ansiblelint_runs += 1
                    if not ansiblelint_check[0]:
                        errors_ansiblelint += 1
                        logger.info(f"Ansiblelint failed at iteration {errors_ansiblelint} with message: {ansiblelint_check[1]}")
                        logger.info(f"Ansiblelint runs so far: {ansiblelint_runs}")
                        logger.info(f"Ansiblelint errors so far: {errors_ansiblelint}")
                        if errors_ansiblelint > max_iterations_ansiblelint:
                            logger.info(f"Ansiblelint did not pass after {max_iterations_ansiblelint} iterations, breaking loop.")
                            print(f"Error: Generated Ansible-YAML did not pass quality gate 'ansiblelint' after defined maximum of {max_iterations_ansiblelint} iterations!")
                            print(f"\nGeneration of playbook '{yaml_path}' failed at stage 'ansiblelint'")
                            failed_at_stage_ansiblelint.append(yaml_path)
                            logger.info(f"added {yaml_path} to failed_at_stage_ansiblelint list")
                            break
                        print(f"{errors_ansiblelint}. Iteration: Generated Ansible-YAML did not pass quality gate 'ansiblelint'")
                        logger.info("Creating recursive prompt for ansiblelint")
                        template, p_str, recursive_str, error_str, error_msg = self.create_recursive_prompt_validate_context(prompt_str, cleaned_outputs, ansiblelint_check[1], "recursive_ansiblelint")
                        if error_msg:
                            logger.info(f"Error in creating recursive prompt or validating context: {error_msg}")
                            print(f"Error: {error_msg}")
                            return error_msg
                        logger.info("Invoking recursive prompt chain for ansiblelint")
                        raw_outputs = self.invoke_recursive_chain(template, p_str, cleaned_outputs, ansiblelint_check[1])
                        print(f"___________________________________________LLM Output:___________________________________________ \n{raw_outputs}")
                        logger.info(f"Raw LLM output after ansiblelint: {raw_outputs}")
                        cleaned_outputs = self.clean_text(raw_outputs)
                        print(f"_______________________________________Cleaned LLM Output:_______________________________________ \n{cleaned_outputs}")
                        logger.info("Cleaned LLM output after ansiblelint")
                        t1 = time.perf_counter()
                        print(f"\n{time.ctime()}: {yaml_path} Total generation time:", t1 - t0)
                        logger.info(f"Total generation time for {yaml_path}: {t1 - t0} seconds")
                        # copy generated file into molecule test directory
                        with yaml_path.open("w", encoding="utf-8") as f:
                            f.write(cleaned_outputs)
                        logger.info(f"Wrote cleaned output to YAML file: {yaml_path}")
                        logger.info("Continuing while loop for next ansiblelint iteration")
                        continue
                    if errors_ansiblelint < 1:
                        ansiblelint_passed_at_first_attempt += 1
                        f_ansiblelint_passed_at_first_attempt += 1
                        logger.info(f"Ansiblelint passed at first attempt, total so far: {ansiblelint_passed_at_first_attempt}")
                        print(f"ansiblelint_passed_at_first_attempt increased to {ansiblelint_passed_at_first_attempt}")
                    print("################################# Quality Gate 'ansiblelint' passed! ################################")
                    logger.info("Ansiblelint passed, proceeding to molecule test")
                    errors_ansiblelint = 0
                    
                    if check_molecule(yaml_path):
                        logger.info("Molecule test passed")
                        print(f"\n Generation and test of '{yaml_path}' sucessfull!")
                        passed_all_stages.append(yaml_path)
                        logger.info(f"added {yaml_path} to passed_all_stages list")
                        break
                    else: 
                        logger.info("Molecule test failed")
                        print(f"Error: Generated Ansible-YAML did not pass quality gate 'molecule-test'!")
                        print(f"\nGeneration of playbook '{yaml_path}' failed at stage 'molecule-test'")
                        failed_at_stage_molecule_test.append(yaml_path)
                        logger.info(f"added {yaml_path} to failed_at_stage_molecule_test list")
                        break
            except (ValueError, FileNotFoundError) as e:
                logger.error(f"Exception occurred: {e}")
                print(e)
                continue
            except (ResponseError, Exception) as e:
                logger.error(f"LLM Exception occurred: {e}")
                print(f"LLM Exception: {e}")
                failed_with_exception.append(yaml_path)
                # correct stats:
                yamllint_runs -= f_yamllint_runs
                yamllint_passed_without_iteration -= f_yamllint_passed_without_iteration
                yamllint_passed_at_first_attempt -= f_yamllint_passed_at_first_attempt
                ansiblelint_runs -= f_ansiblelint_runs
                ansiblelint_passed_at_first_attempt -= f_ansiblelint_passed_at_first_attempt
                logger.info("Corrected statistics after exception")
                print(f"{yaml_path} was added to failed_with_exception list")
                logger.info(f"added {yaml_path} to failed_with_exception list")
                continue
            if tmp_copy.exists():  
                logger.info(f"Restoring original YAML file from temporary location {tmp_copy} to {yaml_path}")
                shutil.copy2(tmp_copy, yaml_path) 
                tmp_copy.unlink()
                print(f"Original YAML file '{yaml_path}' was copied from temp into molecule_test directory.")
        logger.info("Benchmark run completed, generating final report.")
        self.reports(start_time, 
                     failed_initial_molecule_test,
                     failed_at_stage_yamllint, 
                     #failed_at_stage_syntax, 
                     failed_at_stage_ansiblelint, 
                     failed_at_stage_molecule_test, 
                     passed_all_stages, 
                     self.main_output_path,
                     yamllint_runs,
                     yamllint_passed_without_iteration,
                     yamllint_passed_at_first_attempt,
                     ansiblelint_runs,
                     ansiblelint_passed_at_first_attempt,
                     failed_with_exception)


    def reports(
        self,
        start_time,
        failed_initial_molecule_test,
        failed_at_stage_yamllint,
        #failed_at_stage_syntax,
        failed_at_stage_ansiblelint,
        failed_at_stage_molecule_test,
        passed_all_stages,
        report_path,
        yamllint_runs,
        yamllint_passed_without_iteration,
        yamllint_passed_at_first_attempt,
        ansiblelint_runs,
        ansiblelint_passed_at_first_attempt,
        failed_with_exception=[],
    ) -> None:
        """
        Creates a report file with start/end time, duration, stage counts,
        total entries and detailed list of results.
        """
        report_file = report_path / "report.txt"

        end_time = datetime.now()
        duration = end_time - start_time

        with report_file.open("w", encoding="utf-8") as f:
            # Header
            f.write("====== Run Summary ======\n")
            f.write(f"Start time : {start_time}\n")
            f.write(f"End time   : {end_time}\n")
            f.write(f"Duration   : {duration}\n\n")

            # Stats
            f.write("====== Stage Counts ======\n")
            if len(failed_initial_molecule_test) > 0:
                f.write(f"Initial molecule failures: {len(failed_initial_molecule_test)}\n")
            if len(failed_with_exception) > 0:
                f.write(f"Failed with exception   : {len(failed_with_exception)}\n")
            f.write(f"yamllint failures   : {len(failed_at_stage_yamllint)}\n")
#            f.write(f"syntax failures     : {len(failed_at_stage_syntax)}\n")
            f.write(f"ansiblelint failures: {len(failed_at_stage_ansiblelint)}\n")
            f.write(f"molecule failures   : {len(failed_at_stage_molecule_test)}\n")
            f.write(f"all passed          : {len(passed_all_stages)}\n")

            total = (
                len(failed_at_stage_yamllint)
#                + len(failed_at_stage_syntax)
                + len(failed_at_stage_ansiblelint)
                + len(failed_at_stage_molecule_test)
                + len(passed_all_stages)
            )
            f.write(f"TOTAL entries       : {total}\n\n")

            # Details
            f.write("====== Detailed Entries ======\n")
            if len(failed_initial_molecule_test) > 0:
                f.write("\nInitial Molecule Test Statistics: \n")
                f.write(f"Initial molecule failures: {len(failed_initial_molecule_test)}\n")
                for entry in failed_initial_molecule_test:
                    f.write(f"Initial molecule failed: {entry}\n")
            if len(failed_with_exception) > 0:
                f.write("\nFailed with Exception Statistics: \n")
                f.write(f"Failed with exception   : {len(failed_with_exception)}\n")
                for entry in failed_with_exception:
                    f.write(f"Failed with exception: {entry}\n")
            f.write("\nYAMLLINT Statistics: \n")
            f.write(f"Total yamllint runs: {yamllint_runs}\n")
            f.write(f"Yamllint passed without iteration: {yamllint_passed_without_iteration}\n")
            f.write(f"Yamllint passed at first attempt: {yamllint_passed_at_first_attempt}\n")
            f.write("Failed at stage 'yamllint': \n")
            for entry in failed_at_stage_yamllint:
                f.write(f"yamllint failed: {entry}\n")
#            f.write("\nFailed at stage 'ansible-playbook --syntax-check':\n")
#            for entry in failed_at_stage_syntax:
#                f.write(f"syntax failed: {entry}\n")
            f.write("\nANSIBLELINT Statistics: \n")
            f.write(f"Total ansiblelint runs: {ansiblelint_runs}\n")
            f.write(f"Ansiblelint passed at first attempt: {ansiblelint_passed_at_first_attempt}\n")
            f.write("Failed at stage 'ansiblelint':\n")
            for entry in failed_at_stage_ansiblelint:
                f.write(f"ansiblelint failed: {entry}\n")

            f.write("\nMOLECULE Statistics: \n")     
            f.write("failed at stage 'molecule-test':\n")
            for entry in failed_at_stage_molecule_test:
                f.write(f"molecule failed: {entry}\n")
            f.write("\nSuccessfully passed all stages:\n")
            for entry in passed_all_stages:
                f.write(f"passed: {entry}\n")

            f.write("\n====== All run roles ======\n")
            for entry in failed_at_stage_yamllint:
                f.write(f"{entry}\n")
            for entry in failed_at_stage_ansiblelint:
                f.write(f"{entry}\n")
            for entry in failed_at_stage_molecule_test:
                f.write(f"{entry}\n")
            for entry in passed_all_stages:
                f.write(f"{entry}\n") 
        print(f"Report written to {report_file}")

########################___MAIN___########################
def main(args: CLIArgumentsBase, config: Config):
    if args.operation_mode == "benchmark":
        operationManager = BenchmarkOperationManager(args, config)
    elif args.operation_mode == "generation":
        raise NotImplementedError
        #operationManager = GenerationOperationManager(args, config)
    elif args.operation_mode == "prompt":
        operationManager = PromptOperationManager(args, config)
    else:
        raise ValueError(f"The operation_mode='{args.operation_mode}' does not exist. Use a valid operation_mode: prompt, generation, benchmark")

    operationManager.setup_files()

    operationManager.setup_llm()

    operationManager.run()


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Tool for creating benchmarks, executing benchmark runs, and generating Ansible YAML files. The behavior is controlled via the --operation_mode argument; additional parameters vary depending on the selected mode.")
    
    subparsers = parser.add_subparsers(
        dest="operation_mode",
        title="operation_mode",
        description="Specifies the operation mode of the tool:",
        required=True
    )

    parser.add_argument(
        "-m",
        "--model",
        help="model to use for code translation.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-e",
        "--engine",
        help="Name of the model engine to use. Valid values: 'llamafile', 'ollama', 'torch'. Note that there is only a basic implementation for using pytorch and the HuggingFace transformers library. Default: 'llamafile'.",
        required=False,
        type=str,
        default="llamafile",
    )

    parser.add_argument(
        "-tk",
        "--top_k",
        help="The number of highest probability vocabulary tokens to keep for top-k-filtering. Only applies for sampling mode, with range from 1 to 100. Default value is 50.",
        required=False,
        default=50,
        type=int,
    )

    parser.add_argument(
        "-tp",
        "--top_p",
        help="Only the most probable tokens with probabilities that add up to top_p or higher are considered during decoding. The valid range is 0.0 to 1.0. 1.0 is equivalent to disabled and is the default. Only applies to sampling mode. Also known as nucleus sampling. Default value is 0.95.",
        required=False,
        default=0.95,
        type=float,
    )

    parser.add_argument(
        "-t",
        "--temperature",
        help='A value used to warp next-token probabilities in sampling mode. Values less than 1.0 sharpen the probability distribution, resulting in "less random" output. Values greater than 1.0 flatten the probability distribution, resulting in "more random" output. A value of 1.0 has no effect and is the default. The allowed range is 0.0 to 2.0. Default value is 0.7.',
        required=False,
        default=0.7,
        type=float,
    )

    parser.add_argument(
        "-l",
        "--language",
        help="Prompt languages available. Possible languages are: english, german",
        required=False,
        default="english",
        type=str,
    )

    # Parser for Prompt Mode
    parser_prompt = subparsers.add_parser(
        "prompt",
        help = "Generate prompts from Ansible role YAML files. Prompts can be created in three different levels of detail."
    )

    parser_prompt.add_argument(
        "-d",
        "--dataset",
        help="Dataset to use for prompt generation. Note that possible datasets are the files in the directory /dataset/. The folder should contain ansible-roles with out of the box working molecule tests!",
        required=False,
        default="example",
        type=str,
    )

    parser_prompt.add_argument(
        "-tt",
        "--template_type",
        help="Type of the prompt template to use for code translation. Possible types are: exact, precise, approximate. Default: exact",
        required=False,
        default="exact",
        type=str,
    )

    # Parser for Benchmark Mode
    parser_benchmark = subparsers.add_parser(
        "benchmark",
        help = "Run the benchmark by generating Ansible YAML files and validating them using YAML-Lint, Ansible Playbook syntax check Ansible-Lint and Molecule.\n"
    )

    parser_benchmark.add_argument(
        "-d",
        "--dataset",
        help="Dataset to use for benchmark creation (same as for prompt generation). Note that possible datasets are the files in the directory /dataset/. The folder should contain ansible-roles.",
        required=False,
        default="example",
        type=str,
    )

    parser_benchmark.add_argument(
        "-tt",
        "--template_type",
        help="Type of the prompt template to use for code translation. Possible types are: exact, precise, approximate. Default: exact",
        required=False,
        default="exact",
        type=str,
    )

    parser_benchmark.add_argument(
        "-p",
        "--prompts",
        help="Path to generated prompts generated with this tool. Path relative to dataset/ folder. Path construction: dataset/prompts/<engine>_<model>_<language>_<template_type>",
        required=True,
        type=str,
    )

    # Parser for Generation Mode
    parser_benchmark = subparsers.add_parser(
        "generation",
        help = "Generate Ansible YAML files based on user-provided prompts, followed by an automated quality check using YAML-Lint, Ansible Playbook syntax check, and Ansible-Lint."
    )

    # nsp = CLIArgumentsGeneration()
    # args = parser.parse_args(namespace=nsp)

    parsed_args = parser.parse_args()

    if parsed_args.operation_mode == "prompt":
        args: CLIArgumentsBase = CLIArgumentsPrompt(**vars(parsed_args))
    elif parsed_args.operation_mode == "benchmark":
        args: CLIArgumentsBase = CLIArgumentsBenchmark(**vars(parsed_args))
    elif parsed_args.operation_mode == "generation":
        args: CLIArgumentsBase = CLIArgumentsGeneration(**vars(parsed_args))
    else:
        raise ValueError(f"Unbekannter operation_mode: {parsed_args.operation_mode}")


    #args = CLIArgumentsGeneration(**vars(parser.parse_args()))

    config = load_config()
    main(args, config)