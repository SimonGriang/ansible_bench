# Templates for the generation of Prompts
prompt_exact_german_template = """Du bist ein professioneller Entwickler. Nachfolgend erhältst du ein vollständiges Ansible Playbook. Dieses Playbook wurde auf Basis eines Prompts generiert. Deine Aufgabe ist es, den ursprünglichen Prompt zu rekonstruieren, der dieses Playbook hätte erzeugen können.

Der rekonstruierte Prompt muss exakt folgendem Format folgen:

"Nachfolgend erhältst du Aufgabenschritte, aus denen du ein Ansible Playbook generieren sollst.  
Das generierte Playbook muss gültig innerhalb einer Ansible Role im Verzeichnis tasks/ sein (z. B. tasks/main.yml).  
Füge keine hosts:, vars: oder andere Playbook-Level-Header hinzu. Gib nur gültige Task-Einträge oder Blocks aus, wie sie in einer Role erwartet werden.  

Nenne dabei die Tasks genau so, wie ich sie dir in diesem Prompt vorgebe:

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

"Below you will receive task descriptions from which you should generate an Ansible Playbook.  
The generated playbook must be valid inside an Ansible Role under the tasks/ directory (e.g., tasks/main.yml).  
Do not include hosts:, vars:, or any playbook-level headers. Only output valid task entries or blocks as expected in a role.  

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

- The generated playbook from the reconstructed prompt must be valid inside an Ansible Role under the tasks/ directory (e.g., tasks/main.yml).
- Do not include hosts:, vars:, or any playbook-level headers. Only output valid task entries or blocks as expected in a role.
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

- Das generierte Playbook aus dem rekonstruierten Prompt muss gültig innerhalb einer Ansible Role im Verzeichnis tasks/ sein (z. B. tasks/main.yml).
- Füge keine hosts:, vars: oder andere Playbook-Level-Header hinzu. Gib nur gültige Task-Einträge oder Blocks aus, wie sie in einer Role erwartet werden.
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
The generated playbook must be valid inside an Ansible Role under the tasks/ directory (e.g., tasks/main.yml).  
Do not include hosts:, vars:, or any playbook-level headers. Only output valid task entries or blocks as expected in a role.  
Summarize the tasks in natural language without strict formatting or technical precision.  

Here is the Ansible Playbook:
{input_str}
"""

prompt_approximate_german_template  = """Du bist ein professioneller Entwickler. Ich möchte ein Ansible-Playbook erstellen, das dem folgenden ähnelt.  
Bitte beschreibe mit deinen eigenen Worten, was das Playbook tun soll, so als würdest du mir die Anweisungen geben.  
Das zu generierende Playbook muss gültig innerhalb einer Ansible Role im Verzeichnis tasks/ sein (z. B. tasks/main.yml).  
Füge keine hosts:, vars: oder andere Playbook-Level-Header hinzu. Gib nur gültige Task-Einträge oder Blocks aus, wie sie in einer Role erwartet werden.  
Fasse die Aufgaben in natürlicher Sprache zusammen, ohne strenge Formatierung oder technische Präzision.  

Hier ist das Ansible-Playbook:  
{input_str}
"""


benchmark_exact_english_first_yamllint_template = """You are a professional developer. Your task is to generate an Ansible Playbook that strictly adheres to the given instructions.  
The playbook must: 
- Begin with '---' on the very first line.  
- Be a valid Ansbile Playbook YAML file, conforming to yamllint and ansible-lint standards.  
- Be structured so it can be directly included in an Ansible Role.  
- Contain the tasks exactly as described, with the precise names and order provided.  

{input_str}

Important:  
- Use the exact task names and module calls as specified.  
- Do not add, omit, or modify tasks.  
- The output must consist only of the complete YAML playbook, without explanations, comments, or formatting outside of YAML.
- The playbook must start with --- and a linebreak
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

benchmark_exact_english_recursive_yamllint_template = """You are a professional developer. The Ansible Playbook generated from the prompt below did not pass yamllint checks.  
Your task is to automatically correct the playbook while adhering strictly to the original instructions.  

Requirements:
- Generate a valid YAML playbook, conforming to yamllint and ansible-lint.
- Follow the original task names and order exactly.
- Only fix issues reported in the error logs; do not alter the functional intent or add/remove tasks.
- Output must consist solely of the corrected YAML playbook.

Inputs:
- Original generation prompt: 
{input_str}

- Last generated (faulty) playbook: 
{recursive_str}

- Error messages from yamllint checks: 
{error_str}

Important:
- Keep all task names, variables, and custom identifiers exactly as in the faulty playbook unless necessary to fix lint errors.
- Do not include explanations, comments, or any text outside the YAML.
"""

benchmark_precise_english_recursive_yamllint_template = """You are a professional developer. The Ansible Playbook generated from the prompt below failed yamllint checks.  
Your task is to correct it while maintaining the same functional intent and structure.  

Requirements:
- Generate a valid YAML playbook, lint-compliant with yamllint and ansible-lint.
- Implement the tasks in the same general order as in the faulty playbook.
- Minor adjustments to task names or descriptions are allowed if required to fix lint errors, but do not change the intent.

Inputs:
- Original generation prompt: 
{input_str}

- Last generated (faulty) playbook: 
{recursive_str}

- Error messages from yamllint checks: 
{error_str}

Guidelines:
- Preserve variables, handlers, and custom names unless absolutely necessary to fix errors.
- Output only the corrected YAML playbook; do not include explanations or comments.
"""

benchmark_approximate_english_recursive_yamllint_template = """You are a professional developer. The Ansible Playbook generated from the prompt below did not pass yamllint checks.  
Your task is to interpret the intent of the original instructions and the faulty playbook, and generate a corrected, working playbook.

Requirements:
- The playbook must be valid YAML, conforming to yamllint and ansible-lint.
- Maintain the overall intent of the original instructions.
- You may adjust task names, module choices, handlers, and variables as needed to fix errors.

Inputs:
- Original generation prompt: 
{input_str}

- Last generated (faulty) playbook: 
{recursive_str}

- Error messages from yamllint checks: 
{error_str}

Instructions:
- Produce a corrected, fully functional YAML playbook.
- Do not include explanations or any content outside of the YAML.
"""

benchmark_exact_english_recursive_syntax_template = """You are a professional developer. The Ansible Playbook generated from the prompt below did not pass ansible-playbook --syntax-check.  
Your task is to automatically correct the playbook while strictly adhering to the original instructions.

Requirements:
- Generate a valid YAML playbook that passes ansible-playbook --syntax-check.
- Follow the original task names and order exactly.
- Only fix syntax issues reported; do not alter the functional intent or add/remove tasks.
- Output must consist solely of the corrected YAML playbook.

Inputs:
- Original generation prompt:
{input_str}

- Last generated (faulty) playbook:
{recursive_str}

- Error messages from ansible syntax check:
{error_str}

Important:
- Keep all task names, variables, and custom identifiers exactly as in the faulty playbook unless necessary to fix syntax errors.
- Do not include explanations, comments, or any text outside the YAML.
"""

benchmark_precise_english_recursive_syntax_template = """You are a professional developer. The Ansible Playbook generated from the prompt below failed ansible-playbook --syntax-check.  
Your task is to correct it while maintaining the same functional intent and structure.

Requirements:
- Generate a valid YAML playbook that passes syntax checks.
- Implement the tasks in the same general order as in the faulty playbook.
- Minor adjustments to task names or descriptions are allowed if required to fix syntax errors, but do not change the intent.

Inputs:
- Original generation prompt:
{input_str}

- Last generated (faulty) playbook:
{recursive_str}

- Error messages from ansible syntax check:
{error_str}

Guidelines:
- Preserve variables, handlers, and custom names unless absolutely necessary to fix errors.
- Output only the corrected YAML playbook; do not include explanations or comments.
"""

benchmark_approximate_english_recursive_syntax_template = """You are a professional developer. The Ansible Playbook generated from the prompt below did not pass ansible-playbook --syntax-check.  
Your task is to interpret the intent of the original instructions and the faulty playbook, and generate a corrected, working playbook.

Requirements:
- The playbook must be valid YAML and pass ansible-playbook --syntax-check.
- Maintain the overall intent of the original instructions.
- You may adjust task names, module choices, handlers, and variables as needed to fix syntax errors.

Inputs:
- Original generation prompt:
{input_str}

- Last generated (faulty) playbook:
{recursive_str}

- Error messages from ansible syntax check:
{error_str}

Instructions:
- Produce a corrected, fully functional YAML playbook.
- Do not include explanations or any content outside of the YAML.
"""

benchmark_exact_english_recursive_ansiblelint_template = """You are a professional developer. The Ansible Playbook generated from the prompt below did not pass ansible-lint.  
Your task is to automatically correct the playbook while strictly adhering to the original instructions.

Requirements:
- Generate a valid YAML playbook that passes ansible-lint.
- Follow the original task names and order exactly.
- Only fix linting issues reported; do not alter the functional intent or add/remove tasks.
- Output must consist solely of the corrected YAML playbook.

Inputs:
- Original generation prompt:
{input_str}

- Last generated (faulty) playbook:
{recursive_str}

- Error messages from ansible-lint:
{error_str}

Important:
- Keep all task names, variables, and custom identifiers exactly as in the faulty playbook unless necessary to fix lint errors.
- Do not include explanations, comments, or any text outside the YAML.
"""

benchmark_precise_english_recursive_ansiblelint_template = """You are a professional developer. The Ansible Playbook generated from the prompt below failed ansible-lint.  
Your task is to correct it while maintaining the same functional intent and structure.

Requirements:
- Generate a valid YAML playbook that passes ansible-lint.
- Implement the tasks in the same general order as in the faulty playbook.
- Minor adjustments to task names or descriptions are allowed if required to fix lint errors, but do not change the intent.

Inputs:
- Original generation prompt:
{input_str}

- Last generated (faulty) playbook:
{recursive_str}

- Error messages from ansible-lint:
{error_str}

Guidelines:
- Preserve variables, handlers, and custom names unless absolutely necessary to fix errors.
- Output only the corrected YAML playbook; do not include explanations or comments.
"""

benchmark_approximate_english_recursive_ansiblelint_template = """You are a professional developer. The Ansible Playbook generated from the prompt below did not pass ansible-lint.  
Your task is to interpret the intent of the original instructions and the faulty playbook, and generate a corrected, working playbook.

Requirements:
- The playbook must be valid YAML and pass ansible-lint.
- Maintain the overall intent of the original instructions.
- You may adjust task names, module choices, handlers, and variables as needed to fix lint errors.

Inputs:
- Original generation prompt:
{input_str}

- Last generated (faulty) playbook:
{recursive_str}

- Error messages from ansible-lint:
{error_str}

Instructions:
- Produce a corrected, fully functional YAML playbook.
- Do not include explanations or any content outside of the YAML.
"""




