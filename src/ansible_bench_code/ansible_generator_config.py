# print(platform.system())

from pathlib import Path


LLAMAFILE_VERSION = "0.8.17"

TOKENIZER_MODELS_PATH = Path("/home/studgoetsi5301/documents/tokenizer")
"""Path to the base directory of the transformers and pytorch model files."""
LLAMAFILE_PATH = Path("/home/studgoetsi5301/documents/llamafile/llamafile-0.8.17")
"""Path to the llamafile executable."""
GGUF_PATH = Path("/home/studgoetsi5301/documents/llamafile")
"""Path to the directory with the GGUF files of the models."""
LLAMAFILE_OUTPUT_LOG = Path("/home/studgoetsi5301/documents/ansible_bench/output")
"""Path to the directory where the llamafile output log files are stored."""
