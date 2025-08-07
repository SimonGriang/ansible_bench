from io import TextIOWrapper
import os
import logging
import traceback
from dotenv import load_dotenv
import time
import argparse
from tqdm import tqdm
from pathlib import Path
from llm_abstraction import LLMSettings, llm_wrapper
import llm_chain
from utils.cli_abstraction import CLIArgumentsTranslation
from utils.config import Config, load_config
from utils.metadata import TranslationMetadata

logger = logging.getLogger(__name__)


class CodeTranslator:
    def __init__(self, args: CLIArgumentsTranslation, config: Config):
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

    def setup_files(self):
        self.input_dir = self.config.dataset_dir / self.args.dataset
        print("\n Input_Directory: "+str(self.input_dir))

        if not self.input_dir.exists():
            raise FileNotFoundError(f"Directory {str(self.input_dir)} does not exist.")

        self.main_output_path = (
            self.config.output_dir / f"{self.model_engine}_{self.model_name}_{self.args.template_type}" / self.args.dataset
        )
        self.out_folder = self.main_output_path
        os.makedirs(self.out_folder, exist_ok=True)
        print("\n Output_Directory: "+str(self.out_folder))

        self.in_files = os.listdir(self.input_dir)
        print(f"found {len(self.in_files)} inputs")

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
        tm = TranslationMetadata(self.model_name, self.model_engine, llm_settings, [self.args.template_type])
        tm.save_to_file(self.main_output_path / "metadata.yml")

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

                raw_outputs = self.process_playbook(playbook_str)

                t1 = time.perf_counter()

                if "# Token size exceeded" in raw_outputs:
                    context_window_file.write(f"{raw_outputs} for file {f}\n")

                base_name = Path(f).stem  # Dateiname ohne Endung, z. B. "rechner" aus "rechner.py"
                out_file = self.out_folder / f"{base_name}_prompt.txt"


                print(f"\n{time.ctime()}: {out_file} Total generation time:", t1 - t0)
                with open(out_file, "w") as fot:
                    print(raw_outputs, file=fot)

            except (ValueError, FileNotFoundError) as e:
                print(e)
                continue

    def process_playbook(self, playbook_str):
        templates = llm_chain.create_prompt_template_for_model(self.args.template_type, self.model_name)

        prompt = llm_chain.fillin_prompt_template(
            templates[0],
            playbook_str,
        )

        max_output_tokens = llm_chain.check_context_size(prompt, self.model_name)
        if max_output_tokens <= 0:
            logger.info(f"The tokens exceeded the maximum size of the context window by {max_output_tokens} tokens.")
            return f"# Token size exceeded by {-max_output_tokens} tokens"


        result = llm_chain.create_and_invoke_llm_chain(
            templates[0],
            self.llm,
            playbook_str,
        )
        raw_outputs = result["target_prompt"]
        return raw_outputs

def main(args: CLIArgumentsTranslation, config: Config):

    translator = CodeTranslator(args, config)

    translator.setup_files()

    translator.setup_llm()

    translator.run()


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="run translation with open-source models given dataset and languages")
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
        help=" Name of the model engine to use. Valid values: 'llamafile', 'ollama', 'torch'. Note that there is only a basic implementation for using pytorch and the HuggingFace transformers library. Default: 'llamafile'.",
        required=False,
        type=str,
        default="llamafile",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        help="dataset to use for benchmark creation. Note that possible datasets are the files in the directory /dataset/. The file should contain .yaml files one for each playbook. Currently only 'example' possible.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-tt",
        "--template_type",
        help="type of the prompt template to use for code translation. Possible types are: english, german",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-k",
        "--top_k",
        help="The number of highest probability vocabulary tokens to keep for top-k-filtering. Only applies for sampling mode, with range from 1 to 100. Default value is 50.",
        required=False,
        default=50,
        type=int,
    )
    parser.add_argument(
        "-p",
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

    # nsp = CLIArgumentsTranslation()
    # args = parser.parse_args(namespace=nsp)

    args = CLIArgumentsTranslation(**vars(parser.parse_args()))

    config = load_config()
    main(args, config)