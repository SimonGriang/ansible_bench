from langchain.schema import AIMessage
import re

def clean_text_prompt(self, raw_output: str) -> str:
    """
    Cleans text:
    - removes everything in front of the first quotation mark
    - removes everthing following the last quotation mark
    - removes stamp </s>.
    """
    if isinstance(raw_output, AIMessage):
        raw_output = raw_output.content
    if self.model_name == "deepseek-r1:14b":
        raw_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
    if '"' in raw_output:
        raw_output = raw_output.split('"', 1)[1]  
    raw_output = raw_output.lstrip()
    if '"' in raw_output:
        raw_output = raw_output.rsplit('"', 1)[0]
    raw_output = re.sub(r'</s>', '', raw_output, flags=re.IGNORECASE)

    return raw_output.strip()


def clean_text_yaml(self, raw_output: str) -> str:
    """
    Cleans text while preserving line content and line breaks:
    - removes everything in front of '---'
    - removes everything following '```'
    - removes stamp </s>
    - removes everything after two consecutive empty lines
    - removes everything after a single empty line if the next line
    does not contain ':' and is not indented
    - checks output is not empty
    """
    
    if isinstance(raw_output, AIMessage):
        raw_output = raw_output.content
   
    backup_input = raw_output
    
    if self.model_name == "deepseek-r1:14b":
        raw_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
    if '---' in raw_output:
        raw_output = '---' + raw_output.split('---', 1)[1]

    if '```' in raw_output:
        raw_output = raw_output.split('```', 1)[0]

    if '...' in raw_output:
        raw_output = raw_output.split('...', 1)[0]

    raw_output = raw_output.replace("</s>", "")
    lines = raw_output.splitlines(keepends=True)
    cleaned_lines = []
    empty_count = 0
    for i, line in enumerate(lines):
        is_empty = line.strip() == ''
        if is_empty:
            empty_count += 1
            if empty_count == 1 and i + 1 < len(lines):
                next_line = lines[i + 1]
                stripped_next = next_line.lstrip()
                if ':' not in next_line and len(next_line) == len(stripped_next):
                    break

            if empty_count >= 2:
                if cleaned_lines and cleaned_lines[-1].strip() == '':
                    cleaned_lines.pop()
                break
        else:
            empty_count = 0
            cleaned_lines.append(line)

        if is_empty:
            cleaned_lines.append(line)

    if not cleaned_lines:
        return backup_input.strip() + "\n"

    if self.model_name in {"gpt-oss:20b",
                            "granite-code:20b",}:
        return ''.join(cleaned_lines) + "\n"
    return ''.join(cleaned_lines)
