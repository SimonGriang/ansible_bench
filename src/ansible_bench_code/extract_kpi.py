from collections import defaultdict
import csv
import os
import re
from typing import Dict
from utils.config import Config, load_config


def load_in_files():
    config = load_config()
    input_dir = config.dataset_dir / "benchmark100"
    print("\nInput_Directory:", input_dir, "\n")

    # finde alle relevanten YAML-Dateien
    in_files = scan_tasks(('.yml', '.yaml'), input_dir)

    # ignoriere assert.yml / assert.yaml
    in_files = [
        f for f in in_files
        if os.path.basename(f) not in ("assert.yml", "assert.yaml")
    ]

    file_info = {}

    print("\nInput-Files:")
    for rel_path in in_files:
        abs_path = os.path.join(input_dir, rel_path)
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
                file_info[rel_path] = {"file_size": len(content)}
        except Exception as e:
            print(f"⚠️ Fehler beim Lesen von {abs_path}: {e}")
            file_info[rel_path] = 0
    return file_info


def scan_tasks(file_extension, directory):
    result = []
    for root, _, files in os.walk(directory):
        if os.path.basename(root) == "tasks":
            yml_files = [f for f in files if f.endswith(file_extension)]
            for f in yml_files:
                rel_dir = os.path.relpath(root, directory)
                result.append(os.path.join(rel_dir, f))
    return result

def process_report(file_content: str):
    content = file_content

    stage = extract_stage_counts(content)
    if stage["total_entries"] == 0:
        print("⚠️ Keine Stage Counts gefunden oder alle Werte 0.")
    else:
        yamllint_failures = stage["yamllint_failures"]
        ansiblelint_failures = stage["ansiblelint_failures"]
        molecule_failures = stage["molecule_failures"]
        all_passed = stage["all_passed"]
        total_entries = stage["total_entries"]
    total_entries = yamllint_failures + ansiblelint_failures + molecule_failures + all_passed

    details = {
        "Yamllint passed without iteration": 0,
        "Yamllint passed at first attempt": 0,
        "Total yamllint runs": 0,
        "Ansiblelint passed at first attempt": 0,
        "Total ansiblelint runs": 0,
    }

    for key in details.keys():
        match = re.search(rf"{key}:\s*(\d+)", content)
        if match:
            details[key] = int(match.group(1))

    yamllint_passed = ansiblelint_failures + molecule_failures + all_passed
    ansible_lint_passed = molecule_failures + all_passed

    yamllint_score = 1 + (
        (details["Yamllint passed without iteration"] + details["Yamllint passed at first attempt"])
        / (2 * details["Total yamllint runs"])
        if details["Total yamllint runs"] > 0 else 0
    )

    ansiblelint_score = 1 + (
        (details["Ansiblelint passed at first attempt"] / details["Total ansiblelint runs"])
        if details["Total ansiblelint runs"] > 0 else 0
    )

    molecule_passed = all_passed 

    benchmark_score = (
        (yamllint_score * (yamllint_passed / total_entries))
        + 2 * (ansiblelint_score * (ansible_lint_passed / total_entries))
        + 4 * (molecule_passed / total_entries)
    ) / (1 * 2 + 2 * 2 + 4)

    stats_block = f"""
Computed Metrics:
Yamllint passed = {yamllint_passed}
Ansible-lint passed = {ansible_lint_passed}
Molecule passed = {molecule_passed}
YAMLLint Score = {yamllint_score:.4f}
Ansible-Lint Score = {ansiblelint_score:.4f}
Benchmark-Score = {benchmark_score:.4f}
        """.strip()

    updated_content = re.sub(
        r"(=+\s*Run Summary\s*=+.*?\n)(?==+\s*Stage Counts\s*=+)",
        rf"\1====== KPIs ======\n\n{stats_block}\n\n",
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    return updated_content

def extract_stage_counts(content: str) -> dict:
    """
    Extrahiert yamllint/ansiblelint/molecule/all passed Zahlen aus dem Report-Text.
    Liefert ein Dict mit ganzzahligen Werten oder None, falls nicht gefunden.
    """
    # flexibles Pattern: ignoriert Groß/Klein und variable Leerzeichen vor/nach ':'
    patterns = {
        "yamllint_failures": r"yamllint\s+failures\s*:\s*(\d+)",
        "ansiblelint_failures": r"ansiblelint\s+failures\s*:\s*(\d+)",
        "molecule_failures": r"molecule\s+failures\s*:\s*(\d+)",
        "all_passed": r"all\s+passed\s*:\s*(\d+)"
    }

    results = {}
    for key, pat in patterns.items():
        m = re.search(pat, content, flags=re.IGNORECASE)
        if m:
            results[key] = int(m.group(1))
        else:
            # Falls etwas fehlt, setze 0 (oder None, wenn du explizit Fehler willst)
            results[key] = 0

    # Gesamtanzahl nach deinem bisherigen Schema
    results["total_entries"] = (
        results["yamllint_failures"]
        + results["ansiblelint_failures"]
        + results["molecule_failures"]
        + results["all_passed"]
    )
    return results

def parse_report_content(content: str) -> Dict[str, Dict[str, int]]:
    """
    Parst den Inhalt eines Reports und gibt ein Dictionary zurück:
    {
        "pfad/zur/datei.yml": {
            "yamllint_failed": 1,
            "ansiblelint_failed": 0,
            "molecule_failed": 0,
            "molecule_passed": 0,
            "total_runs": 1
        },
        ...
    }
    """
    results = defaultdict(lambda: {
        "yamllint_failed": 0,
        "ansiblelint_failed": 0,
        "molecule_failed": 0,
        "molecule_passed": 0,
        "total_runs": 0
    })

    path_pattern = re.compile(r"/molecule_test/([^\s]*?\.ya?ml)", re.IGNORECASE)
    all_paths = [m.group(1) for m in path_pattern.finditer(content)]


    stages = {
        "yamllint_failed": re.compile(r"Failed at stage 'yamllint':\s*(.*?)(?=\n[A-Z]+ Statistics:|\Z)", re.DOTALL | re.IGNORECASE),
        "ansiblelint_failed": re.compile(r"Failed at stage 'ansiblelint':\s*(.*?)(?=\n[A-Z]+ Statistics:|\Z)", re.DOTALL | re.IGNORECASE),
        "molecule_failed": re.compile(r"failed at stage 'molecule-test':\s*(.*?)(?=\nSuccessfully passed all stages:|\Z)", re.DOTALL | re.IGNORECASE),
        "molecule_passed": re.compile(r"Successfully passed all stages:\s*(.*?)(?=\n======|\Z)", re.DOTALL | re.IGNORECASE),
    }

    for key, pattern in stages.items():
        match = pattern.search(content)
        if match:
            failed_block = match.group(1)
            for path in re.findall(path_pattern, failed_block):
                results[path][key] += 1
                results[path]["total_runs"] += 1
        else:
            continue

    print("\n=== Total Runs pro Datei ===")
    for path, stats in results.items():
        print(f"{path}: total_runs = {stats['total_runs']}")

    return dict(results)


def merge_report_dicts(dict_a: Dict[str, Dict[str, int]],
                       dict_b: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    """
    Merge two report result dictionaries.
    Sum the failure counts and runs per file.
    """
    merged = defaultdict(lambda: {
        "yamllint_failed": 0,
        "ansiblelint_failed": 0,
        "molecule_failed": 0,
        "molecule_passed": 0,
        "total_runs": 0
    })

    for d in (dict_a, dict_b):
        for path, stats in d.items():
            for key in stats:
                merged[path][key] += stats[key]

    return dict(merged)


def format_overall_report(aggregate: Dict[str, Dict[str, int]]) -> str:
    """
    Formatiert das aggregierte Dictionary in lesbarer Textform.
    """
    lines = []
    for path, stats in sorted(aggregate.items()):
        lines.append(f"{path}:")
        lines.append(f"  YAMLLint failed: {stats['yamllint_failed']}")
        lines.append(f"  AnsibleLint failed: {stats['ansiblelint_failed']}")
        lines.append(f"  molecule failed: {stats['molecule_failed']}")
        lines.append(f"  molecule passed: {stats['molecule_passed']}")
        lines.append(f"  Total runs: {stats['total_runs']}\n")
        lines.append(f"  File size (chars): {stats['file_size']}\n")
    return "\n".join(lines)

def merge_file_dicts(dict_a, dict_b):
    merged = {}

    # alle keys aus beiden dicts
    all_keys = set(dict_a.keys()) | set(dict_b.keys())

    for key in all_keys:
        merged[key] = {}
        if key in dict_a:
            merged[key].update(dict_a[key])
        if key in dict_b:
            merged[key].update(dict_b[key])

    return merged


if __name__ == "__main__":
    base_dir = "../../ouput"
    combined_report = {}
    for root, dirs, files in os.walk(base_dir):
        if "report.txt" in files:
            file_path = os.path.join(root, "report.txt")
            print(f"Bearbeite: {file_path}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = process_report(content)
            report = parse_report_content(new_content)
            combined_report = merge_report_dicts(combined_report, report)
            file_sizes = load_in_files()
            overall_report = merge_file_dicts(combined_report, file_sizes)

            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
    
    # format and save overall report
    overall_text = format_overall_report(overall_report)
    print("Overall Report:\n", overall_text)
    with open(os.path.join(base_dir, "overall_report.txt"), "w", encoding="utf-8") as f:
        f.write(overall_text)

    csv_path = os.path.join(base_dir, "overall_report.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        # Headerzeile
        writer.writerow([
            "Datei",
            "Yamllint failed",
            "Ansiblelint failed",
            "Molecule failed",
            "Molecule passed",
            "Total runs",
            "File size (chars)"
        ])

        # Datenzeilen
        for path, stats in overall_report.items():
            writer.writerow([
                path,
                stats["yamllint_failed"],
                stats["ansiblelint_failed"],
                stats["molecule_failed"],
                stats["molecule_passed"],
                stats["total_runs"],
                stats["file_size"]
            ])

    print(f"✅ CSV-Datei erstellt: {csv_path}")
