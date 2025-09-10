from io import TextIOWrapper
import os
import re
import logging
import traceback
import shutil
from dotenv import load_dotenv
import time
import argparse
from tqdm import tqdm
from pathlib import Path
from llm_abstraction import LLMSettings, llm_wrapper
import llm_chain
from utils.cli_abstraction import CLIArgumentsBase, CLIArgumentsPrompt, CLIArgumentsBenchmark, CLIArgumentsGeneration
from utils.config import Config, load_config
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
            self.model_engine = "llamafile"
        elif "ollama" in self.args.engine:
            self.model_name = self.args.model
            print("Name for the ollama model:", self.model_name)
            self.model_engine = "ollama"
        elif "langchain" in self.args.engine:
            self.model_name = self.args.model
            print("Name for the langchain model:", self.model_name)
            self.model_engine = "torch"
        else:
            raise NotImplementedError("The given model was not implemented.")
        return self.model_name, self.model_engine

    def scan_tasks(self, file_extension, directory):
        result = []
        for root, _, files in os.walk(directory):
            if os.path.basename(root) == "tasks":
                yml_files = [f for f in files if f.endswith(file_extension)]
                for f in yml_files:
                    rel_dir = os.path.relpath(root, directory)
                    result.append(os.path.join(rel_dir, f))
        return result

    def setup_llm(self):
        llm_settings = LLMSettings(
            top_k=self.args.top_k,
            top_p=self.args.top_p,
            temperature=self.args.temperature,
            repeat_penalty=1,
        )
        self.llm = llm_wrapper(self.model_name, self.model_engine, llm_settings=llm_settings)
        self.save_model_metadata(llm_settings)

    def save_model_metadata(self, llm_settings):
        tm = GenerationMetadata(self.args.operation_mode, self.model_name, self.model_engine, llm_settings, [self.args.template_type], self.args.language)
        tm.save_to_file(self.main_output_path / "metadata.yml")

    #------------------has to be implemented by subclass
    def setup_files(self):
        raise NotImplementedError
    
    def run(self):
        raise NotImplementedError

    def clean_text(self, raw_output: str) -> str:
        raise NotImplementedError
    #------------------necessary independently from run() and setup_files()


    def create_prompt_validate_context(self, input_str, stage):
        templates = llm_chain.create_prompt_template_for_model(self.model_name, self.args.operation_mode, self.args.language, self.args.template_type, stage)

        prompt = llm_chain.fillin_prompt_template(
            templates[0],
            input_str,
        )

        print("Prompt: " + prompt)

        if (self.model_engine == "ollama"):
            print("Ollama applies the template automatically, so we do not need to check the context size.")
        else:
            max_output_tokens = llm_chain.check_context_size(prompt, self.model_name)
            if max_output_tokens <= 0:
                logger.info(f"The tokens exceeded the maximum size of the context window by {max_output_tokens} tokens.")
                return f"# Token size exceeded by {-max_output_tokens} tokens"

        return templates[0], input_str, None

    #def create_prompt_validate_context_recursive selbe methode nur um weitere Felder im prompt erweitert
    
    def invoke_prompt_chain(self, template, input_str):
        return llm_chain.create_and_invoke_prompt_chain(
            template,
            self.llm,
            input_str,
        ) 
    
#--------------- End of Class

class PromptOperationManager(BaseOperationManager):
    def setup_files(self):
        self.input_dir = self.config.dataset_dir / self.args.dataset
        print("\nInput_Directory: "+str(self.input_dir))

        if not self.input_dir.exists():
            raise FileNotFoundError(f"Directory {str(self.input_dir)} does not exist.")

        self.main_output_path = (
            self.config.dataset_dir/ "prompts" /f"{self.model_engine}_{self.model_name}_{self.args.language}_{self.args.template_type}" / self.args.dataset
        )
        self.out_folder = self.main_output_path
        os.makedirs(self.out_folder, exist_ok=True)
        print("\n Output_Directory: "+str(self.out_folder))

        self.in_files = self.scan_tasks(('.yml', '.yaml'), self.input_dir)
        for file_name in self.in_files:
            print(file_name)
        print(f"found {len(self.in_files)} inputs")

    def run(self):
        # loop over input files
        context_window_report = f"context_window_report_{self.args.model}.txt"
        context_window_file = open(context_window_report, "a")
        for f in tqdm(self.in_files):
            playbook_file = self.input_dir / f

            playbook_str = ""
            with open(playbook_file, "r", encoding="UTF-8", errors="ignore") as fin:
                playbook_str = fin.read()

            try:
                t0 = time.perf_counter()
                template, pb_str, error_msg = self.create_prompt_validate_context(playbook_str, "first")
                # Falls ein Fehler vorliegt, gib ihn zurück oder behandle ihn entsprechend
                if error_msg:
                    return error_msg
                
                # Ansonsten invoke_prompt_chain mit den zurückgegebenen Parametern aufrufen
                raw_outputs = self.invoke_prompt_chain(template, pb_str)
                cleaned_outputs = self.clean_text(raw_outputs)
                print(cleaned_outputs)

                t1 = time.perf_counter()

                if "# Token size exceeded" in raw_outputs:
                    context_window_file.write(f"{raw_outputs} for file {f}\n")

                f_path = Path(f)
                relative_dir = f_path.parent
                target_dir = self.out_folder / relative_dir
                target_dir.mkdir(parents=True, exist_ok=True)
                base_name = f_path.stem
                out_file = target_dir / f"{base_name}_prompt.txt"

                print(f"\n{time.ctime()}: {out_file} Total generation time:", t1 - t0)
                with open(out_file, "w") as fot:
                    print(cleaned_outputs, file=fot)

            except (ValueError, FileNotFoundError) as e:
                print(e)
                continue
    
    def clean_text(self, raw_output: str) -> str:
        """
        Cleans text:
        - removes everything in front of the first quotation mark
        - removes everthing following the last quotation mark
        - removes stamp </s>.
        """
        if '"' in raw_output:
            raw_output = raw_output.split('"', 1)[1]  
        raw_output = raw_output.lstrip()

        if '"' in raw_output:
            raw_output = raw_output.rsplit('"', 1)[0]

        raw_output = re.sub(r'</s>', '', raw_output, flags=re.IGNORECASE)

        return raw_output.strip()


class BenchmarkOperationManager(BaseOperationManager):
    def setup_benchmark_tmp_log(self):
        """
        creates benchmark log file and temp directory
        """
        self.main_output_path.mkdir(parents=True, exist_ok=True)

        self.benchmark_log_file = self.main_output_path / "benchmark.log"
        if not self.benchmark_log_file.exists():
            self.benchmark_log_file.touch()
        print(f"Benchmark-Log-Datei erstellt: {self.benchmark_log_file}")

        self.tmp_dir = self.main_output_path / "tmp"
        if self.tmp_dir.exists():
            shutil.rmtree(self.tmp_dir)
        self.tmp_dir.mkdir()
        print(f"Temporärer Ordner erstellt: {self.tmp_dir}")

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
                print(f"{role_dir.name} in {target} kopiert")
    
    
    def setup_files(self):
        """
        Setup files:
            - File directory with original Ansible-Roles
            - File directory with the generated prompts
            - File directory with the generated YAML files one folder for each exit-point?
                - yamllint
                - ansible-playbook --synthax-check
                - ansible-lint
                - molcule test
                - successfully passed all stages --> perfectly correct YAML
        """
        self.input_dir = self.config.dataset_dir / self.args.dataset
        print("\nInput_Directory: "+str(self.input_dir))
        self.prompt_dir = self.config.dataset_dir / self.args.prompts
        print("\nPrompts_Directory: "+str(self.prompt_dir)+"\n")

        if not self.input_dir.exists():
            raise FileNotFoundError(f"Directory {str(self.input_dir)} does not exist.")

        self.main_output_path = (
            self.config.output_dir / f"{self.model_engine}_{self.model_name}_{self.args.language}_{self.args.template_type}" / self.args.dataset
        )
        self.out_folder = self.main_output_path
        os.makedirs(self.out_folder, exist_ok=True)

        self.setup_test_directory()
        
        self.setup_benchmark_tmp_log()

        print("\nOutput_Directory: "+str(self.out_folder))


        self.prompt_files = self.scan_tasks('.txt', self.prompt_dir)
        for file_name in self.prompt_files:
            print(file_name)
        print(f"found {len(self.prompt_files)} inputs")
    
    def clean_text(self, raw_output: str) -> str:
        """
        Cleans text:
        - removes everything in front of '---'
        - removes everthing following '```'
        - removes stamp </s>.
        """
        if '---' in raw_output:
            raw_output = '---' + raw_output.split('---', 1)[1]

        if '```' in raw_output:
            raw_output = raw_output.split('```', 1)[0]

        return raw_output.strip()


    def run(self):
        # loop over input files
        context_window_report = f"context_window_report_{self.args.model}.txt"
        context_window_file = open(context_window_report, "a")
        for f in tqdm(self.prompt_files):
            prompt_file = self.prompt_dir / f
            if not prompt_file.name.endswith("_prompt.txt"):
                raise ValueError(f"Pfad {prompt_file} endet nicht mit '_prompt.txt'")

            yaml_file = f.replace("_prompt.txt", ".yml")
            yaml_path = self.config.dataset_dir / self.args.dataset / yaml_file
            #yaml_path = prompt_file.with_name(prompt_file.stem.replace("_prompt.txt", "") + ".yaml")
            if not yaml_path.exists():
                yaml_path = yaml_path.with_suffix(".yml")
            if not yaml_path.exists():
                raise FileNotFoundError(f"Keine YAML/YML gefunden zu {prompt_file}")

            tmp_copy = self.tmp_dir / yaml_path.name
            shutil.copy2(yaml_path, tmp_copy)

            prompt_str = ""
            with open(prompt_file, "r", encoding="UTF-8", errors="ignore") as fin:
                prompt_str = fin.read()

            try:
                t0 = time.perf_counter()
                template, p_str, error_msg = self.create_prompt_validate_context(prompt_str, "first_yamllint")
                if error_msg:
                    return error_msg
                raw_outputs = self.invoke_prompt_chain(template, p_str)
                print(p_str)
                print(raw_outputs.content)
                cleaned_outputs = self.clean_text(raw_outputs.content)
                print(cleaned_outputs)

                t1 = time.perf_counter()

                if "# Token size exceeded" in raw_outputs:
                    context_window_file.write(f"{raw_outputs} for file {f}\n")

    #            f_path = Path(f)
    #            relative_dir = f_path.parent
    #            target_dir = self.out_folder / relative_dir
    #            target_dir.mkdir(parents=True, exist_ok=True)
    #            base_name = f_path.stem
    #            out_file = target_dir / f"{base_name}_prompt.txt"
                
                #Alter Stand:
                #base_name = Path(f).stem  # Dateiname ohne Endung, z. B. "rechner" aus "rechner.py"
                #out_file = self.out_folder / f"{base_name}_prompt.txt"


    #            print(f"\n{time.ctime()}: {out_file} Total generation time:", t1 - t0)
    #            with open(out_file, "w") as fot:
    #                print(cleaned_outputs, file=fot)

            except (ValueError, FileNotFoundError) as e:
                print(e)
                continue


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