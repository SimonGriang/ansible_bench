import subprocess
from pathlib import Path
from typing import Tuple
from yamllint import linter
from yamllint.config import YamlLintConfig

# -------------------------------
# YAML-Lint Prüfung
# -------------------------------

def lint_yaml(yaml_text: str):
    # Standard-Konfiguration laden (du kannst auch eine eigene YAML-Lint-Config übergeben)
    config = YamlLintConfig('extends: default')

    # Linter auf den String anwenden
    problems = linter.run(yaml_text, config)

    # Ergebnisse ausgeben
    return [f"{p.line}:{p.column}: {p.desc} ({p.rule})" for p in problems]

# -------------------------------
# Platzhalter für weitere Checks
# -------------------------------
def check_playbook_syntax(yaml_file: Path) -> Tuple[bool, str]:
    """
    TODO: Prüft Ansible Playbook Syntax via `ansible-playbook --syntax-check`.
    """
    raise NotImplementedError("Playbook Syntax Check noch nicht implementiert.")

def check_ansible_lint(yaml_file: Path) -> Tuple[bool, str]:
    """
    TODO: Prüft YAML/Playbook mit ansible-lint.
    """
    raise NotImplementedError("ansible-lint Prüfung noch nicht implementiert.")

def check_molecule(role_dir: Path) -> Tuple[bool, str]:
    """
    TODO: Führt Molecule Tests auf der Rolle durch.
    """
    raise NotImplementedError("Molecule Test noch nicht implementiert.")


