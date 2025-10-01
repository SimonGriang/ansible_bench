import re
import subprocess
from pathlib import Path
from typing import Tuple
#import re
#import yaml
from yamllint import linter
from yamllint.config import YamlLintConfig


# -------------------------------
# YAML-Lint Checking
# -------------------------------
def check_yamllint(yaml_file: Path) -> Tuple[bool, str]:
    #return True, ""
    """
    Validates that the cleaned string is non-empty YAML. (not yamllint specific)
    Validates a YAML file using yamllint via the Python API.
    Returns (True, "passed") if no errors or warnings are found,
    otherwise returns (False, output containing errors/warnings).
    """
    try:
        # Standard-Konfiguration von yamllint verwenden
        config = YamlLintConfig('extends: default')

        with open(yaml_file, 'r') as f:
            content = f.read()

        if not content or content == "---":
            raise ValueError("Ansible-YAML is empty after cleaning.")
            
        #yaml.safe_load(content)

        # Linting ausführen
        problems = list(linter.run(content, config))

        if not problems:
            return True, "passed"
        else:
            # Ausgabe als Text zusammenfassen
            output = "\n".join(str(p) for p in problems)
            return False, output

    except FileNotFoundError:
        return False, f"{yaml_file} not found."
 #   except yaml.YAMLError as e:
 #       return False, """The generated Ansible-YAML did not pass pre-validation.  
 #                       This means that after cleaning, the output was invalid YAML.  
 #                       Most likely, the error occurred because the previous output included unnecessary text, explanations, comments, or extra characters like '...' or '```', instead of outputting only the YAML content.
 #                       CLEANING STEPS TAKEN:
 #                       1. Removed any text before the first '---' line.
 #                       2. Removed any text following '```'.
 #                       3. Removed any text following '...'.
 #                       4. Removed all occurrences of the '</s>' token.
 #                       5. Stripped leading and trailing whitespace and ensured a newline at the end."""
    except ValueError:
        return False, """The generated Ansible-YAML did not pass pre-validation.  
                This means that after cleaning, the output was empty.  
                Most likely, the error occurred because the previous output included unnecessary text, explanations, comments, or extra characters like '...' or '```', instead of outputting only the YAML content.
                CLEANING STEPS TAKEN:
                1. Removed any text before the first '---' line.
                2. Removed any text following '```'.
                3. Removed any text following '...'.
                4. Removed all occurrences of the '</s>' token.
                5. Stripped leading and trailing whitespace and ensured a newline at the end.""" 
    except Exception as e:
        return False, "Something with yamllint went wrong:\n" + str(e)


    """
    TODO: checks Ansible Playbook Syntax via `yamllint`.
    """
    raise NotImplementedError("Yamllint Check not implemented yet.")


#def check_yamllint(yaml_file: Path) -> Tuple[bool, str]:
#    """
#    Führt yamllint auf der angegebenen YAML-Datei aus.
#    Gibt (True, "passed") zurück, wenn keine Fehler/Warnings vorliegen,
#    ansonsten (False, Ausgabe mit Fehler/Warning).
#
#
#    :param yaml_file: Pfad zur YAML Datei
#    :return: Tuple[bool, str]
#    """
#    try:
#        result = subprocess.run(
#            ["yamllint", str(yaml_file)],
#            capture_output=True,
#            text=True,
#            check=False
#        )
#
#
#        stdout = result.stdout.strip()
#        stderr = result.stderr.strip()
#        output = (stdout + "\n" + stderr).strip()
#
#
#        if result.returncode == 0 and not output:
#            return True, "passed"
#        else:
#            return False, output
#
#
#    except FileNotFoundError:
#        return False, "yamllint command not found. Bitte sicherstellen, dass yamllint installiert ist."
# -------------------------------
# Alternative for check_yamllint
# -------------------------------
#from yamllint import linter
#from yamllint.config import YamlLintConfig
#
#def check_yamllint(yaml_file: Path) -> Tuple[bool, str]:
#    """
#    Prüft eine YAML-Datei mit yamllint über die Python-API.
#    Gibt (True, "passed") zurück, wenn keine Fehler/Warnings vorliegen,
#    ansonsten (False, Ausgabe mit Fehler/Warning).
#    """
#    try:
#        # Standard-Konfiguration von yamllint verwenden
#        config = YamlLintConfig(fileconfig=None)
#
#        with open(yaml_file, 'r') as f:
#            content = f.read()
#
#        # Linting ausführen
#        problems = list(linter.run(content, config))
#
#        if not problems:
#            return True, "passed"
#        else:
#            # Ausgabe als Text zusammenfassen
#            output = "\n".join(str(p) for p in problems)
#            return False, output
#
#    except FileNotFoundError:
#        return False, f"{yaml_file} not found."
#    except Exception as e:
#        return False, str(e)

# -------------------------------
# ansible-playbook --syntax-check Checking
# -------------------------------
def check_playbook_syntax(playbook_path: Path) -> Tuple[bool, str]:
#    return True, ""
#    """
#    TODO: Validate Ansible Playbook syntax via `ansible-playbook --syntax-check`.
#    """
#    raise NotImplementedError("Playbook syntax check not implemented yet.")

    """
    Führt ansible-playbook --syntax-check auf dem angegebenen Playbook aus.
    Gibt (True, "passed") zurück, wenn keine Fehler/Warnings vorliegen,
    ansonsten (False, Ausgabe mit Fehler/Warning).

    :param playbook_path: Pfad zur YAML Playbook-Datei
    :return: Tuple[bool, str]
    """
    try:
        result = subprocess.run(
            ["ansible-playbook", str(playbook_path), "--syntax-check"],
            capture_output=True,
            text=True,
            check=False
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output = (stdout + "\n" + stderr).strip()

        if result.returncode == 0 and not stderr:
            return True, "passed"
        else:
            return False, output

    except FileNotFoundError:
        return False, "ansible-playbook command not found. Bitte sicherstellen, dass Ansible installiert ist."

# -------------------------------
# Ansible-Lint Checking
# -------------------------------
#def check_ansible_lint(yaml_file: Path) -> Tuple[bool, str]:
#    return True, ""
#    
#    """
#    TODO: Validate YAML/Playbook with ansible-lint.
#    """
#    raise NotImplementedError("ansible-lint check not implemented yet.")



def check_ansible_lint(yaml_file: Path) -> Tuple[bool, str]:
    """
    Führt ansible-lint auf der angegebenen YAML-Datei aus.
    Gibt (True, "passed") zurück, wenn keine Fehler/Warnings vorliegen,
    ansonsten (False, Ausgabe mit Fehler/Warning).


    :param yaml_file: Pfad zur YAML Datei
    :return: Tuple[bool, str]
    """
    try:
        result = subprocess.run(
            ["ansible-lint", str(yaml_file)],
            capture_output=True,
            text=True,
            check=False
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output = (stdout + "\n" + stderr).strip()


        if result.returncode == 0:
            return True, "passed"
        else:
            return False, output


    except FileNotFoundError:
        return False, "ansible-lint command not found. Please ensure that Ansible Lint is installed."


# -------------------------------
# Molecule-Testing
# -------------------------------

def check_molecule(task_path: Path) -> bool:
    """
    Runs Molecule tests for all scenarios of the Ansible role that contains the given task YAML file.

    The method executes `molecule test` for each scenario individually.
    Returns True only if ALL scenarios pass (all recap lines report failed=0), otherwise False.

    :param task_path: Path to a YAML file inside the role's `tasks/` folder.
    :return: bool
    """
    role_dir = task_path.parent.parent
    molecule_dir = role_dir / "molecule"  # tasks/../molecule/
    overall_success = True
    try:
        scenarios = [d.name for d in molecule_dir.iterdir() if d.is_dir()]

        if not scenarios:
            print(f"No Molecule scenarios found in '{molecule_dir}'.")
            return False

        for scenario in scenarios:
            print(f"Molecule test role '{role_dir.name}' for Scenario '{scenario}':____________________________\n")
            result = subprocess.run(
                ["molecule", "test", "-s", scenario],
                cwd=str(role_dir),
                capture_output=True,
                text=True,
                check=False
            )
            output = result.stdout + "\n" + result.stderr
            print(output)
            
            failed_matches = re.findall(r"failed=(\d+)", output)
            scenario_success = result.returncode == 0 and all(int(x) == 0 for x in failed_matches)
            print(f"Molecule test role '{role_dir.name}' for Scenario '{scenario}' was {scenario_success}")
            if not scenario_success:
                overall_success = False
                print("Scenario failed, stopping further tests. Overall result will be False.")
                break  # If one scenario fails, no need to continue

        print(f"Overall Molecule test result for role '{role_dir.name}': {overall_success}")        
        return overall_success

    except FileNotFoundError:
        print("Molecule executable not found.")
        return False
