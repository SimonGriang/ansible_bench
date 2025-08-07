german_template = """Du bist ein professioneller Entwickler. Nachfolgend erhältst du ein vollständiges Ansible Playbook. Dieses Playbook wurde auf Basis eines Prompts generiert. Deine Aufgabe ist es, den ursprünglichen Prompt zu rekonstruieren, der dieses Playbook hätte erzeugen können.

Der rekonstruierte Prompt muss exakt folgendem Format folgen:

"Du bist professioneller Entwickler. Nachfolgend erhältst du Aufgabenschritte, aus denen du ein Ansible Playbook generieren sollst. Nenne dabei die Tasks genau so, wie ich sie dir in diesem Prompt vorgebe:

Aufgabe 1: ...
Aufgabenbeschreibung Aufgabe 1: ...
Aufgabe 2: ...
Aufgabenbeschreibung Aufgabe 2: ...
Aufgabe 3: ...
Aufgabenbeschreibung Aufgabe 3: ...
..."

Hinweise zur Erstellung:
- Verwende pro Aufgabe eine kurze, präzise Beschreibung der jeweiligen Aktion.
- Die Aufgaben müssen den tatsächlichen Tasks im Playbook **inhaltlich und in der Reihenfolge** entsprechen.
- Verwende möglichst dieselben Begriffe und benutzerdefinierte Namen wie im Playbook (z.B. „nginx installieren“ statt „Webserver installieren“).
- Liefere zu jedem Task eine detaillierte Beschreibung unterhalb des Tasks:

Hier ist das Ansible Playbook:
{playbook}
"""

english_template = """You are a professional developer. Below you will find a complete Ansible Playbook. This playbook was generated based on a prompt. Your task is to reconstruct the original prompt that could have been used to generate this playbook.

Important: The only output follows theh format below. Do not include any explanations or comments before or after nor any quotation marks in your output.

The reconstructed prompt must exactly follow the structure below:

"You are a professional developer. Below you will receive task descriptions from which you should generate an Ansible Playbook. Name the tasks exactly as I provide them here:

Task 1: ...
Description Task 1: ...

Task 2: ...
Description Task 2: ...

Task 3: ...
Description Task 3: ...

..."

Guidelines:
- Each task should be short and clearly describe one specific action.
- The tasks must match the actual tasks in the playbook **both in content and order**.
- Use the exact terminology and labels as used in the playbook (e.g., “install nginx” instead of “install web server”).
- Provide a more detailed description of the task next to each task

Here is the Ansible Playbook:
{playbook}
"""