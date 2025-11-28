import os
import time
import logging
from baseOperationsManager import BaseOperationManager
from pathlib import Path
from tqdm import tqdm
import post_processing
import shutil
from datetime import datetime
from typing import Tuple
from ollama import ResponseError
from quality_assurance import check_yamllint, check_ansible_lint, check_molecule
from benchmark_reporter import Reporter
import re

logger = logging.getLogger(__name__)

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
        return post_processing.clean_text_yaml(self, raw_output)

    def run(self):
        reporter = Reporter()
        reporter.report_path = self.main_output_path
        molecule_works_flag = False
        reporter.start_time = datetime.now()
        reporter.failed_at_stage_yamllint = []
        reporter.failed_at_stage_ansiblelint = []
        reporter.failed_at_stage_molecule_test = []
        reporter.passed_all_stages = []
        reporter.failed_initial_molecule_test = []
        reporter.failed_with_exception = []

        for f in tqdm(self.prompt_files):
            f_yamllint_runs = 0
            f_yamllint_passed_without_iteration = 0
            f_yamllint_passed_at_first_attempt = 0
            f_ansiblelint_runs = 0
            f_ansiblelint_passed_at_first_attempt = 0
            logger.info(f"Processing prompt file: {f}") 
            reporter.reports()
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
                logger.info(f"Raw LLM output: {raw_outputs}")
                cleaned_outputs = self.clean_text(raw_outputs)
                logger.info(f"Cleaned LLM output: {cleaned_outputs}")
                t1 = time.perf_counter()
                logger.info(f"Total generation time for {yaml_path}: {t1 - t0} seconds")

                logger.info(f"Writing cleaned output to YAML file: {yaml_path}")
                with yaml_path.open("w", encoding="utf-8") as f:
                    f.write(cleaned_outputs)
                
                max_iterations_yamllint = 5
                logger.info(f"setting max iterations for yamllint to {max_iterations_yamllint}")

                max_iterations_ansiblelint = 4
                logger.info(f"setting max iterations for ansiblelint to {max_iterations_ansiblelint}")
                logger.info("setting up error counters")
                errors_ansiblelint = 0

                while True:
                    logger.info("Starting quality assurance while loop")
                    status_flag_yamllint = False
                    logger.info("setting status_flag_yamllint to False")
                    for i in range(1,max_iterations_yamllint+1): 
                        logger.info(f"Yamllint iteration {i}")
                        yamllint_check_results: Tuple[bool, str] = check_yamllint(yaml_path)
                        reporter.yamllint_runs += 1
                        f_yamllint_runs += 1
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
                            t1 = time.perf_counter()
                            logger.info(f"Total generation time for {yaml_path}: {t1 - t0} seconds")

                            with yaml_path.open("w", encoding="utf-8") as f:
                                f.write(cleaned_outputs)
                            logger.info(f"Wrote cleaned output to YAML file: {yaml_path}")
                    else:
                        logger.info(f"Yamllint did not pass after {max_iterations_yamllint} iterations, breaking loop.")

                    if i < 2:
                        logger.info("Yamllint passed without iteration")
                        reporter.yamllint_passed_without_iteration += 1
                        f_yamllint_passed_without_iteration += 1
                        if errors_ansiblelint == 0:
                            reporter.yamllint_passed_at_first_attempt += 1
                            f_yamllint_passed_at_first_attempt += 1

                    if not status_flag_yamllint:
                        logger.error("Yamllint failed, exiting while loop")
                        print(f"\nGeneration of playbook '{yaml_path}' failed at stage 'yamllint'")
                        logger.error(f"Generation of playbook '{yaml_path}' failed at stage 'ansiblelint'")

                        if(errors_ansiblelint>0):
                            reporter.failed_at_stage_ansiblelint.append(yaml_path)
                            logger.error(f"Note: {errors_ansiblelint} ansible-lint iterations were done before!")
                        else:
                            reporter.failed_at_stage_yamllint.append(yaml_path)
                            logger.error(f"added {yaml_path} to failed_at_stage_yamllint list")
                        break
                    
                    print("################################# Quality Gate 'yamllint' passed! ################################")

                    ansiblelint_check: Tuple[bool, str] = check_ansible_lint(yaml_path)
                    reporter.ansiblelint_runs += 1
                    f_ansiblelint_runs += 1
                    if not ansiblelint_check[0]:
                        errors_ansiblelint += 1
                        logger.info(f"Ansiblelint failed at iteration {errors_ansiblelint} with message: {ansiblelint_check[1]}")
                        logger.info(f"Ansiblelint runs so far: {reporter.ansiblelint_runs}")
                        logger.info(f"Ansiblelint errors so far: {errors_ansiblelint}")
                        if errors_ansiblelint > max_iterations_ansiblelint:
                            logger.info(f"Ansiblelint did not pass after {max_iterations_ansiblelint} iterations, breaking loop.")
                            print(f"\nGeneration of playbook '{yaml_path}' failed at stage 'ansiblelint'")
                            reporter.failed_at_stage_ansiblelint.append(yaml_path)
                            logger.info(f"added {yaml_path} to failed_at_stage_ansiblelint list")
                            break
                        logger.info(f"{errors_ansiblelint}. Iteration: Generated Ansible-YAML did not pass quality gate 'ansiblelint'")
                        logger.info("Creating recursive prompt for ansiblelint")
                        template, p_str, recursive_str, error_str, error_msg = self.create_recursive_prompt_validate_context(prompt_str, cleaned_outputs, ansiblelint_check[1], "recursive_ansiblelint")
                        if error_msg:
                            logger.info(f"Error in creating recursive prompt or validating context: {error_msg}")
                            logger.error(f"Error: {error_msg}")
                            return error_msg
                        logger.info("Invoking recursive prompt chain for ansiblelint")
                        raw_outputs = self.invoke_recursive_chain(template, p_str, cleaned_outputs, ansiblelint_check[1])
                        logger.info(f"Raw LLM output after ansiblelint: {raw_outputs}")
                        cleaned_outputs = self.clean_text(raw_outputs)
                        logger.info("Cleaned LLM output after ansiblelint")
                        t1 = time.perf_counter()
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
                    print("################################# Quality Gate 'ansiblelint' passed! ################################")
                    logger.info("Ansiblelint passed, proceeding to molecule test")
                    errors_ansiblelint = 0
                    
                    if check_molecule(yaml_path):
                        logger.info("Molecule test passed")
                        print(f"\n Generation and test of '{yaml_path}' sucessfull!")
                        reporter.passed_all_stages.append(yaml_path)
                        logger.info(f"added {yaml_path} to passed_all_stages list")
                        break
                    else: 
                        logger.info("Molecule test failed")
                        print(f"Error: Generated Ansible-YAML did not pass quality gate 'molecule-test'!")
                        print(f"\nGeneration of playbook '{yaml_path}' failed at stage 'molecule-test'")
                        reporter.failed_at_stage_molecule_test.append(yaml_path)
                        logger.info(f"added {yaml_path} to failed_at_stage_molecule_test list")
                        break
            except (ValueError, FileNotFoundError) as e:
                logger.error(f"Exception occurred: {e}")
                continue
            except (ResponseError, Exception) as e:
                logger.error(f"LLM Exception occurred: {e}")
                reporter.failed_with_exception.append(yaml_path)
                # correct stats:
                reporter.yamllint_runs -= f_yamllint_runs
                reporter.yamllint_passed_without_iteration -= f_yamllint_passed_without_iteration
                reporter.yamllint_passed_at_first_attempt -= f_yamllint_passed_at_first_attempt
                reporter.ansiblelint_runs -= f_ansiblelint_runs
                reporter.ansiblelint_passed_at_first_attempt -= f_ansiblelint_passed_at_first_attempt
                logger.info("Corrected statistics after exception")
                logger.info(f"added {yaml_path} to failed_with_exception list")
                continue
            if tmp_copy.exists():  
                logger.info(f"Restoring original YAML file from temporary location {tmp_copy} to {yaml_path}")
                shutil.copy2(tmp_copy, yaml_path) 
                tmp_copy.unlink()
        logger.info("Benchmark run completed, generating final report.")
        reporter.reports()


