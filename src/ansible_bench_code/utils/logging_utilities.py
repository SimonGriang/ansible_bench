import logging
from pathlib import Path

def setup_logging():
    log_file = Path.cwd() / "ansible_bench.log"
 
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="a", encoding="utf-8"),
            #logging.StreamHandler()
        ],
    )