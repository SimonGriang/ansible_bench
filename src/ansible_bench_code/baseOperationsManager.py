import os
from utils.cli_abstraction import CLIArgumentsBase, CLIArgumentsPrompt, CLIArgumentsBenchmark, CLIArgumentsGeneration
from utils.config import Config, load_config
from utils.logging_utilities import setup_logging
import logging
import llm_chain
from llm_abstraction import LLMSettings, llm_wrapper
from utils.metadata import GenerationMetadata

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
