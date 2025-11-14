import os
import time
import logging
from baseOperationsManager import BaseOperationManager
from pathlib import Path
from tqdm import tqdm
import post_processing

logger = logging.getLogger(__name__)

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
        return post_processing.clean_text_prompt(self, raw_output)