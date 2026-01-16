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
import post_processing
from utils.cli_abstraction import CLIArgumentsBase, CLIArgumentsPrompt, CLIArgumentsBenchmark, CLIArgumentsGeneration
from utils.config import Config, load_config
from utils.metadata import GenerationMetadata
from utils.logging_utilities import setup_logging
import logging
from benchmarkOperationsManager import BenchmarkOperationManager
from promptOperationManager import PromptOperationManager
from baseOperationsManager import BaseOperationManager
from generationOperationsManager import GenerationOperationManager

setup_logging()
logger = logging.getLogger(__name__)

########################___MAIN___########################
def main(args: CLIArgumentsBase, config: Config):
    if args.operation_mode == "benchmark":
        operationManager = BenchmarkOperationManager(args, config)
    elif args.operation_mode == "generation":
        operationManager = GenerationOperationManager(args, config)
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
        help="Prompt languages available. Possible languages are: english, german. Not all languages are supported, right now only english is fully supported. Default: english",
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
        help="Type of the prompt to use for Ansible-YAML generateion. Template type defines the level of detail in the generated YAML files. Possible types are: exact, precise, approximate. Default: exact",
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
        help="Type of the prompt to use for Ansible-YAML generateion. Template type defines the level of detail in the generated YAML files. Possible types are: exact, precise, approximate. Default: exact",
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
    parser_generation = subparsers.add_parser(
        "generation",
        help = "Generate Ansible YAML files based on user-provided prompts, followed by an automated quality check using YAML-Lint, Ansible Playbook syntax check, and Ansible-Lint."
    )

    parser_generation.add_argument(
        "-y",
        "--max_yamllint_iterations",
        help="Number of maximum iterations for yamllint quality assurance loop. If the generated YAML file does not pass the yamllint check the last generated file will be returned. If no value is provided, yamllint quality assurance will continued until, either a file passes or the process is manually stopped.",
        type=int,
    )

    parser_generation.add_argument(
        "-a",
        "--max_ansiblelint_iterations",
        help="Number of maximum iterations for ansiblelint quality assurance loop. If the generated YAML file does not pass the ansiblelint check the last generated file will be returned. If no value is provided, ansiblelint quality assurance will continued until, either a file passes or the process is manually stopped.",
        type=int,
    )

    parser_generation.add_argument(
        "-s",
        "--max_syntaxcheck_iterations",
        help="Number of maximum iterations for ansible-playbook --syntax-check quality assurance loop. If the generated YAML file does not pass the syntax check the last generated file will be returned. If no value is provided, syntax check quality assurance will continued until, either a file passes or the process is manually stopped. Note that syntax check is only effective for template_type playbook.",
        type=int,
    )

    parser_generation.add_argument(
        "-o",
        "--output_path",
        help="Path to output directory where generated files will be saved. Full path from root directory. Default ",
        type=str,
    )

    parser_generation.add_argument(
        "-tt",
        "--template_type",
        help="Type of the prompt to use for Ansible-YAML generation. Template type defines if the generated YAML files are task files or playbooks. Possible types are: task_file, playbook. Default: task_file",
        required=False,
        default="task_file",
        type=str,
    )

    parser_generation.add_argument(
        "-i",
        "--inventory",
        help="file path to the Ansible inventory file. If not provided, it will be assumed the only inventories in the ansible src/ file will be used. Specification highly recomended.",
        required=False,
        type=str,
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