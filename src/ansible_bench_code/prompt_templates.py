# Templates for the generation of Prompts
prompt_exact_german_template = """Du bist ein professioneller Entwickler. Nachfolgend erhältst du ein vollständiges Ansible Playbook. Dieses Playbook wurde auf Basis eines Prompts generiert. Deine Aufgabe ist es, den ursprünglichen Prompt zu rekonstruieren, der dieses Playbook hätte erzeugen können.

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
{input_str}
"""

prompt_exact_english_template = """You are a professional developer. Below you will find a complete Ansible Playbook. This playbook was generated based on a prompt. Your task is to reconstruct the original prompt that could have been used to generate this playbook.

Important: The only output follows the format below. Do not include any explanations or comments before or after.

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
{input_str}
"""

prompt_precise_english_template = """You are a professional developer. Below is an Ansible Playbook. Your job is to guess the original prompt that might have led to this playbook.

Provide the result in a semi-structured way:

- List the tasks in the same general order as they appear.
- Each task should include a short title and a 1-2 sentence description of what it does.
- The wording can be slightly paraphrased, but the meaning should stay the same.

Format:

Task 1: <short title> - <short description>  
Task 2: <short title> - <short description>  
...

Do not include explanations outside of this list.

Here is the Ansible Playbook:
{input_str}
"""

prompt_precise_german_template = """Du bist ein professioneller Entwickler. Unten findest du ein Ansible-Playbook. Deine Aufgabe ist es, das ursprüngliche Prompt zu erraten, das zu diesem Playbook geführt haben könnte.

Gib das Ergebnis in halb-strukturierter Form aus:

- Liste die Aufgaben in der gleichen allgemeinen Reihenfolge, wie sie erscheinen.
- Jede Aufgabe sollte einen kurzen Titel und eine 1-2 Sätze umfassende Beschreibung enthalten, was sie macht.
- Die Formulierungen dürfen leicht umschrieben sein, die Bedeutung soll aber gleich bleiben.

Format:

Aufgabe 1: <kurzer Titel> - <kurze Beschreibung>  
Aufgabe 2: <kurzer Titel> - <kurze Beschreibung>  
...

Füge keine Erklärungen außerhalb dieser Liste hinzu.

Hier ist das Ansible-Playbook:  
{input_str}
"""

prompt_approximate_english_template = """You are a professional developer. I want to generate an Ansible Playbook similar to the one below.  
Please describe in your own words what the playbook should do, as if you were giving me the instructions.  
Summarize the tasks in natural language without strict formatting or technical precision.  

Here is the Ansible Playbook:
{input_str}
"""

prompt_approximate_german_template  = """Du bist ein professioneller Entwickler. Ich möchte ein Ansible-Playbook erstellen, das dem folgenden ähnelt.  
Bitte beschreibe mit deinen eigenen Worten, was das Playbook tun soll, so als würdest du mir die Anweisungen geben.  
Fasse die Aufgaben in natürlicher Sprache zusammen, ohne strenge Formatierung oder technische Präzision.  

Hier ist das Ansible-Playbook:  
{input_str}
"""


benchmark_exact_english_first_yamllint_template = """You are a professional developer. Your task is to generate an Ansible Playbook that strictly adheres to the given instructions.  
The playbook must:  
- Be a valid YAML file, conforming to yamllint and ansible-lint standards.  
- Be structured so it can be directly included in an Ansible Role.  
- Contain the tasks exactly as described, with the precise names and order provided.  

{input_str}

Important:  
- Use the exact task names and module calls as specified.  
- Do not add, omit, or modify tasks.  
- The output must consist only of the complete YAML playbook, without explanations, comments, or formatting outside of YAML.  
"""

benchmark_precise_english_first_yamllint_template = """You are a professional developer. Your task is to generate an Ansible Playbook based on the task descriptions provided below.  
The playbook must:  
- Be valid YAML, lint-compliant with yamllint and ansible-lint.  
- Be suitable for inclusion in an Ansible Role.  
- Implement the tasks in the same general order as described.  

Guidelines:  
- You may slightly adjust task names or descriptions if it improves readability or aligns with Ansible conventions, but the functional intent must remain unchanged.  
- Each task should be clearly defined, using appropriate Ansible modules.  

{input_str}

Output only the final YAML playbook. Do not include explanations or comments.  
"""

benchmark_approximate_english_first_yamllint_template = """You are a professional developer. I want you to generate an Ansible Playbook that captures the overall intent of the following instructions.  
The playbook should:  
- Be valid YAML, conforming to yamllint and ansible-lint standards.  
- Be usable within an Ansible Role.  

The description of the tasks is intentionally approximate. Please interpret the intent and create a coherent, functional set of Ansible tasks that fulfill the described outcome.  
You may choose appropriate module names, handlers, and variables as necessary.  

Instruction:  
{input_str}

Provide only the YAML playbook as output.  
"""
# further templates for the generation of Ansible YAML