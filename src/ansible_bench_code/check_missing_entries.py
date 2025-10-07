import os
from pathlib import Path
import re
from utils.config import Config, load_config


def check_missing_entries():
    config = load_config()
    input_dir = config.dataset_dir / "benchmark100"
    print("\nInput_Directory: "+str(input_dir)+"\n")
    in_files = scan_tasks(('.yml', '.yaml'), input_dir)
    in_files = [
        f for f in in_files
        if os.path.basename(f) not in ("assert.yml", "assert.yaml")
    ]
    print("\nInput-Files:")
    for file_name in in_files:
        print(file_name)
    print(f"found {len(in_files)} inputs")
    return in_files


def scan_tasks(file_extension, directory):
    result = []
    for root, _, files in os.walk(directory):
        if os.path.basename(root) == "tasks":
            yml_files = [f for f in files if f.endswith(file_extension)]
            for f in yml_files:
                rel_dir = os.path.relpath(root, directory)
                result.append(os.path.join(rel_dir, f))
    return result

def load_processed_files():
    config = load_config()
    processed_dir = Path(config.output_dir) / "ollama_qwen2.5:14b_english_exact/benchmark100/prompts_qwen2.5:14b"
    report_path = Path(processed_dir) / "report.txt"
    if not report_path.exists():
        raise FileNotFoundError(f"Datei nicht gefunden: {report_path}")

    with report_path.open("r", encoding="utf-8") as f:
        report_text = f.read()

    # Suche den Abschnitt unter '====== All run roles ======'
    pattern = r"====== All run roles ======\n(.*?)(?:\n\n|$)"
    match = re.search(pattern, report_text, re.DOTALL)
    if not match:
        return []

    section = match.group(1).strip()
    # Jede Zeile ist ein Pfad
    files = [line.strip() for line in section.splitlines() if line.strip()]
    print(f"\nLoaded {len(files)} processed files from report.txt")
    cleaned = []
    for path in files:
        if "molecule_test/" in path:
            cleaned.append(path.split("molecule_test/", 1)[1])
        else:
            # Falls 'molecule_test/' nicht vorkommt, Pfad unverändert übernehmen
            cleaned.append(path)
    for file_name in cleaned:
        print(file_name)
    print("\n")
    return cleaned


def get_unprocessed_files(prompt_files: list[str], processed_files: list[str]) -> list[str]:
    """
    Vergleicht zwei Listen und gibt jene Einträge zurück,
    die nur in prompt_files vorkommen, aber nicht in processed_files.
    """
    prompt_set = set(prompt_files)
    processed_set = set(processed_files)

    unprocessed = list(prompt_set - processed_set)

    unprocessed.sort()
    return unprocessed

if __name__ == "__main__":
    prompt_files = check_missing_entries()
    processed_files = load_processed_files()
    unprocessed_files = get_unprocessed_files(prompt_files, processed_files)
    print("\nUnprocessed-Files:")
    for file_name in unprocessed_files:
        print(file_name)
    print(f"\nfound {len(unprocessed_files)} unprocessed files")