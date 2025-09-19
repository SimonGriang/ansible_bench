from pathlib import Path
import sys
# Projekt-Root hinzufügen
sys.path.append(str(Path(__file__).resolve().parent.parent))
from quality_assurance import check_yamllint, check_playbook_syntax, check_ansible_lint, check_molecule

if __name__ == "__main__":
    # Beispielpfad – anpassen
    pfad = Path("/home/studgoetsi5301/documents/ansible_bench/dataset/benchmark100/ansible-role-logrotate/tasks/main.yml")
    
    if check_molecule(pfad):
        print(f"{pfad} return is true.")
    else:
        print(f"{pfad} return is false.")