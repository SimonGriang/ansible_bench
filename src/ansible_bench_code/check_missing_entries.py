import os
from pathlib import Path
import re
import shutil
from utils.config import Config, load_config


def load_in_files():
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

def load_processed_files(path):
    config = load_config()
    processed_dir = Path(config.output_dir) / path
    report_path = Path(processed_dir) / "report.txt"
    if not report_path.exists():
        raise FileNotFoundError(f"File not found: {report_path}")

    with report_path.open("r", encoding="utf-8") as f:
        report_text = f.read()

    # Search for the section under '====== All run roles ======'
    pattern = r"====== All run roles ======\n(.*?)(?:\n\n|$)"
    match = re.search(pattern, report_text, re.DOTALL)
    if not match:
        return []

    section = match.group(1).strip()
    # Each line is a path
    files = [line.strip() for line in section.splitlines() if line.strip()]
    print(f"\nLoaded {len(files)} processed files from report.txt")
    cleaned = []
    for path in files:
        if "molecule_test/" in path:
            cleaned.append(path.split("molecule_test/", 1)[1])
        else:
            # If 'molecule_test/' is not present, keep the path unchanged
            cleaned.append(path)
    for file_name in cleaned:
        print(file_name)
    print("\n")
    return cleaned


def get_unprocessed_files(prompt_files: list[str], processed_files: list[str]) -> list[str]:
    """
    Compare two lists and return the entries that appear
    in prompt_files but not in processed_files.
    """
    prompt_set = set(prompt_files)
    processed_set = set(processed_files)

    unprocessed = list(prompt_set - processed_set)

    unprocessed.sort()
    return unprocessed

def create_missing_dataset(unprocessed_files: list[str], dataset_name: str, model_name: str, prompt_model: str):
    config = load_config()
    prompt_dir = Path(config.dataset_dir) / "prompts" / f"ollama_{prompt_model}_english_exact" / dataset_name
    output_dir = Path(config.dataset_dir) / "prompts" / f"{model_name}_{prompt_model}_{dataset_name}_missing_files_prompts"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nPrompt Directory: {prompt_dir}")
    print(f"Output Directory: {output_dir}")

    if not prompt_dir.exists():
        raise FileNotFoundError(f"Prompt directory {prompt_dir} does not exist.")
    for rel_file in unprocessed_files:
        # Input file (e.g. ansible-role-ansible/tasks/main.yml)
        prompt_file = prompt_dir / rel_file.replace(".yml", "_prompt.txt")

        if not prompt_file.exists():
            print(f"⚠️ No prompt file found: {prompt_file}")
            continue

        # Target directory (relative to the role)
        target_dir = output_dir / Path(rel_file).parent
        target_dir.mkdir(parents=True, exist_ok=True)

        # Target file path
        target_file = target_dir / prompt_file.name

        # Copy file
        shutil.copy2(prompt_file, target_file)

        print(f"✅ Copied: {prompt_file} → {target_file}")


#######################################################################################

if __name__ == "__main__":
    # Configuration
    model = "gpt-oss:20b"
    prompt_model = "qwen2.5:14b"
    create_missing_dataset_flag = False
    dataset_name = "benchmark100"

    processed_files_path = f"ollama_{model}_english_exact/benchmark100/prompts_{prompt_model}"
    prompt_files = load_in_files()
    processed_files = load_processed_files(processed_files_path)
    unprocessed_files = get_unprocessed_files(prompt_files, processed_files)

    print("Unprocessed files:")
    for file_name in unprocessed_files:
        print(file_name)
    print(f"\nFound {len(unprocessed_files)} unprocessed files\n")

    if create_missing_dataset_flag:
        create_missing_dataset(unprocessed_files, dataset_name, model, prompt_model)