"""collects the CLI arguments in an object"""

import argparse
from dataclasses import dataclass

@dataclass
class CLIArgumentsBase(argparse.Namespace):
    operation_mode:str
    engine: str
    model: str
    top_k: int
    top_p: float
    temperature: float

@dataclass
class CLIArgumentsPrompt(CLIArgumentsBase):
    dataset: str
    template_type: str
    language: str

@dataclass
class CLIArgumentsBenchmark(CLIArgumentsBase):
    dataset: str
    template_type: str
    language: str
    prompts: str

@dataclass
class CLIArgumentsGeneration(CLIArgumentsBase):
    pass


