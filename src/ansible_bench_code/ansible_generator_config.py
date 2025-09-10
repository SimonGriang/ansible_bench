# print(platform.system())

from pathlib import Path


LLAMAFILE_VERSION = "0.6.2"

TORCH_MODELS_PATH = Path("E:/") / "models" / "pytorch"
"""Path to the base directory of the transformers and pytorch model files."""
# LLAMAFILE_PATH = Path("C:/") / "home" / "bins" / "llamafile-0.6.2.exe"
LLAMAFILE_PATH = Path("C:/") / "home" / "bins" / "llamafile-0.8.6.exe"
"""Path to the llamafile executable."""
GGUF_PATH = Path("E:/") / "models" / "gguf"
"""Path to the directory with the GGUF files of the models."""
LLAMAFILE_OUTPUT_LOG = Path("C:/") / "home" / "ma_simon" / "llamafile_output"
"""Path to the directory where the llamafile output log files are stored."""
