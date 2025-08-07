import logging
import os
import argparse
import time
import regex


from translation.translate_open_source import main as translation_main
from utils.cli_abstraction import (
    CLIArguments,
    CLIArgumentsTranslation,
)
from .utils.config import load_config, Config
from .utils.logging_utilities import setup_logging


logger = logging.getLogger(__name__)


def logged_batch_task(
    config: Config,
    logfile: str,
    task: str,
    batch_function: callable,
    cli_args: CLIArguments,
):

    logger.info(f"Executing command: {task} {cli_args}")

    try:
        batch_function(cli_args, config)
    except Exception as e:
        logger.error(e)
    else:
        with open(logfile, "a") as log:
            log.write(f"{time.ctime()}:\n")
            log.write(f"Executed command: {task} {cli_args}\n")

def iterate_task_over_dataset(
    config: Config,
    model_name: str,
    template_type: str,
    logfile: str,
    datasets: list[str],
    ignore_executed_pairs=False
):
    for ds in datasets:
            cli_args = CLIArgumentsTranslation(
                model_name,
                ds,
                template_type,
                k=50,
                p=0.95,
                temperature=0.7,
            )
            logged_batch_task(config, logfile, translation_main, cli_args)



def setup_environment_variables():
    # This is required to ensure the C# compiler outputs are in English and not in a mixtrue with the current locale of the machine
    os.environ["DOTNET_CLI_UI_LANGUAGE"] = "en"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Name of the model to use.", type=str)
    parser.add_argument(
        "template", help="Name of the prompt template to use.", type=str
    )
    parser.add_argument(
        "-d",
        "--dataset",
        help="Path to CSV Dataset",
        required=False,
        type=str,
    )
    parser.add_argument(
        "-e",
        "--engine",
        help="Path to the model engine to use.",
        required=False,
        type=str,
        default="llamafile",
    )

    args = parser.parse_args()

    model_name = args.model.lower()
    template_type = args.template.lower()
    dataset = args.dataset
    model_engine = args.engine.lower()

    config = load_config()

    #setup_environment_variables() # not necessary for main task, add on or feature

    setup_logging(model=model_name, config=config)

    logfile = f"logfile_for_python_batching_{model_name}.txt"

    datasets = ["huggingface"]
    if dataset and (dataset in datasets):
        datasets = [dataset.lower()]

    ignore_executed_pairs = args.overwrite

    iterate_task_over_dataset(
        config,
        f"{model_engine}_{model_name}",
        template_type,
        logfile,
        datasets,
        args.attempt,
    )