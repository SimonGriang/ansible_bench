"""collects the CLI arguments in an object"""

import argparse
from dataclasses import dataclass

@dataclass
class CLIArguments(argparse.Namespace):
    engine: str
    model: str
    dataset: str
    template_type: str

@dataclass
class CLIArgumentsTranslation(CLIArguments):
    top_k: int
    top_p: float
    temperature: float
