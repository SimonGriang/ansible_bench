from ansible_generator_config import TOKENIZER_MODELS_PATH
from langchain.prompts import PromptTemplate
#from langchain.chains import LLMChain, SequentialChain
#from langchain.schema import RunnableSequence
from langchain.schema.runnable import RunnableLambda
from langchain_core.language_models.llms import LLM
from pathlib import Path
from transformers import AutoTokenizer

from llm_abstraction import LLAMAFILE_CTX_SIZE, OLLAMA_CTX_SIZE
from prompt_templates import (
    prompt_exact_german_template,
    prompt_exact_english_template,
    prompt_precise_english_template,
    prompt_precise_german_template,
    prompt_approximate_english_template,
    prompt_approximate_german_template,
    benchmark_exact_english_first_yamllint_template,
    benchmark_precise_english_first_yamllint_template,
    benchmark_approximate_english_first_yamllint_template,
)


def  hf_modelfiles_path_for(model_name: str) -> Path:
    model_name = model_name.lower()
    hf_model_paths = {
        "mistral": Path.joinpath(TOKENIZER_MODELS_PATH, "Mistral-7B-Instruct-v0.1"),
        "mixtral": Path.joinpath(TOKENIZER_MODELS_PATH, "Mixtral-8x7B-Instruct-v0.1"),
        "codellama": Path.joinpath(TOKENIZER_MODELS_PATH, "CodeLlama-70b-hf"),
        "dolphin-2.6-mistral": Path.joinpath(
            TOKENIZER_MODELS_PATH, "dolphin-2.6-mistral-7b"
        ),
        "dolphin-2.7-mixtral": Path.joinpath(
            TOKENIZER_MODELS_PATH, "dolphin-2.7-mixtral-8x7b"
        ),
        "dolphincoder-starcoder2-15b": Path.joinpath(
            TOKENIZER_MODELS_PATH, "dolphincoder-starcoder2-15b"
        ),
        "dolphin-2.6-phi-2": Path.joinpath(TOKENIZER_MODELS_PATH, "dolphin-2_6-phi-2"),
        "llama3.2": Path.joinpath(TOKENIZER_MODELS_PATH, "Llama-3.2-1B-Instruct"),
        "phi3": Path.joinpath(TOKENIZER_MODELS_PATH, "Phi-3-mini-4k-instruct"),
        "codestral": Path.joinpath(TOKENIZER_MODELS_PATH, "Codestral-22B-v0.1"),
        "gemma-3": Path.joinpath(TOKENIZER_MODELS_PATH, "gemma-3-27b-it"),
        "gemma-3": Path.joinpath(TOKENIZER_MODELS_PATH, "gemma-3-27b-it"),
    }

    if model_name not in hf_model_paths.keys():
        raise NotImplementedError(
            f"The model you are trying to use is not available in this library. Model: {model_name}. Add it to the hf_model_paths dict in codetrans/llm_chain.py"
        )

    return hf_model_paths[model_name]


def apply_chat_template_to_text(text: str, model_name: str) -> str:
    if "codestral" in model_name:
        # The codestral tokenizer does not define a chat template. Codestral uses the same chat template as Mistral. Use that instead.
        tokenizer = AutoTokenizer.from_pretrained(hf_modelfiles_path_for("codestral"))
    elif "deepseek-r1:14b" in model_name:
        # ollama applies the template automatically
        return text
    else:
        tokenizer = AutoTokenizer.from_pretrained(hf_modelfiles_path_for(model_name))
    if "dolphin" in model_name:
        # has no chat template in tokenizer
        tokenizer.chat_template = "{% if not add_generation_prompt is defined %}{% set add_generation_prompt = false %}{% endif %}{% for message in messages %}{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant\n' }}{% endif %}"
        system_prompt = "You are a skilled developer proficient in ansible specific playbook creation."
        chat = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text.removeprefix(system_prompt + " ")},
        ]

    elif "llama3" in model_name:
        return text
    else:
        chat = [
            {"role": "user", "content": text},
        ]
    return tokenizer.apply_chat_template(chat, tokenize=False)


def check_context_size(text: str, model_name: str) -> int:
    tokenizer = AutoTokenizer.from_pretrained(hf_modelfiles_path_for(model_name))
    tokens = tokenizer.encode(text)
    # print(tokens)

    total_input_tokens = len(tokens)
    print("Total input tokens:", total_input_tokens)
    if model_name in LLAMAFILE_CTX_SIZE.keys():
        model_max_length = LLAMAFILE_CTX_SIZE[model_name]
    elif model_name in OLLAMA_CTX_SIZE.keys():
        model_max_length = OLLAMA_CTX_SIZE[model_name]
    else:
        raise NotImplementedError(
            f"The model {model_name} has no defined context length. Please add it to the LLAMAFILE_CTX_SIZE or OLLAMA_CTX_SIZE dictionary."
        )
    model_max_length = LLAMAFILE_CTX_SIZE[model_name]
    if total_input_tokens >= model_max_length:
        return model_max_length - total_input_tokens
    max_new_tokens = model_max_length - total_input_tokens
    return max_new_tokens


def apply_chat_template_to_prompt_template(
    template: PromptTemplate, model_name: str
) -> PromptTemplate:
    """Apply a LLMs chat template to the text of a prompt template.

    Args:
        template (PromptTemplate): A `PromptTemplate` object containing the text of the prompt template.
        model_name (str): The name of the LLM that will be applied to the prompt template.

    Returns:
        PromptTemplate: A new `PromptTemplate` object with the updated text resulting from applying the chat template to the original prompt template.
    """
    template.template = apply_chat_template_to_text(template.template, model_name)
    return template

#useful
def create_prompt_template_for_model(
     model_name: str, operation_mode: str, language:str, template_type: str, stage: str
) -> list[PromptTemplate]:
    """
    Create a prompt template for a given template type and model name.

    Args:
        template_type (str): The type of prompt template to create.
        model_name (str): The name of the model for with to apply its chat template.

    Returns:
        list[PromptTemplate]: A list of modified prompt templates that have been embedded with the given chat template.
    """
    prompts = create_prompt_template(operation_mode, language, template_type, stage)
    modified_prompts = [
        apply_chat_template_to_prompt_template(p, model_name) for p in prompts
    ]
    return modified_prompts

#useful
def create_prompt_template(operation_mode: str, language:str, template_type: str, stage: str) -> list[PromptTemplate]:
    """Creates a list of PromptTemplate objects based on the given template type and language.

    Args:
        template_type (str): The template type to use for creating prompts.
        language (str): The desired language of the Prompt

    Returns:
        list[PromptTemplate]: A list of PromptTemplate objects with the corresponding input variables.
    """
    prompts = []

    templates = {
        "prompt": {
            "english": {
                "exact": {
                    "first": prompt_exact_english_template,
                    #"recursive": prompt_exact_english_llmaaj_template,
                },
                "precise": {
                    "first": prompt_precise_english_template,
                    #"recursive": prompt_precise_english_llmaaj_template,
                },
                "approximate": {
                    "first": prompt_approximate_english_template,
                    #"recursive": prompt_approximate_english_llmaaj_template,
                },
            },
            "german": {
                "exact": {
                    "first": prompt_exact_german_template,
                    #"recursive": prompt_exact_german_llmaaj_template,
                },
                "precise": {
                    "first": prompt_precise_german_template,
                    #"recursive": prompt_precise_german_llmaaj_template,
                },
                "approximate": {
                    "first": prompt_approximate_german_template,
                    #"recursive": prompt_approximate_german_llmaaj_template,
                },
            },
        },
        "benchmark": {
            "english": {
                "exact": {
                    "first_yamllint": benchmark_exact_english_first_yamllint_template,
                    #"recursive_yamllint": ,
                    #"first_syntaxcheck": ,
                    #"recursive_syntaxcheck": ,
                    #"first_ansiblelint": ,
                    #"recursive_ansiblelint": ,
                },
                "precise": {
                    "first_yamllint": benchmark_precise_english_first_yamllint_template,
                    #"recursive_yamllint": ,
                    #"first_syntaxcheck": ,
                    #"recursive_syntaxcheck": ,
                    #"first_ansiblelint": ,
                    #"recursive_ansiblelint": ,
                },
                "approximate": {
                    "first_yamllint": benchmark_approximate_english_first_yamllint_template,
                    #"recursive_yamllint": ,
                    #"first_syntaxcheck": ,
                    #"recursive_syntaxcheck": ,
                    #"first_ansiblelint": ,
                    #"recursive_ansiblelint": ,
                },
            },
            "german": {
                "exact": {
                    #"first_yamllint": ,
                    #"recursive_yamllint": ,
                    #"first_syntaxcheck": ,
                    #"recursive_syntaxcheck": ,
                    #"first_ansiblelint": ,
                    #"recursive_ansiblelint": ,
                },
                "precise": {
                    #"first_yamllint": ,
                    #"recursive_yamllint": ,
                    #"first_syntaxcheck": ,
                    #"recursive_syntaxcheck": ,
                    #"first_ansiblelint": ,
                    #"recursive_ansiblelint": ,
                },
                "approximate": {
                    #"first_yamllint": ,
                    #"recursive_yamllint": ,
                    #"first_syntaxcheck": ,
                    #"recursive_syntaxcheck": ,
                    #"first_ansiblelint": ,
                    #"recursive_ansiblelint": ,
                },
            },
        },
        "generation": {
            # TODO: später generation-Templates hier definieren
        },
    }

    input_vars_map = {
        "prompt": {
            "first": ["input_str"], #playbook
            "recursive": ["input_str", "recursive_str", "error_str"], #playbook, generated Prompt, LLM-as-a-Judge Feedback
        },
        "benchmark": {
            "first": ["input_str"], #prompt 
            "recursive": ["input_str", "recursive_str", "error_str"], #prompt, generated YAML, Error Message
        },
        "generation": {
            "first": ["input_str"], #prompt 
            "recursive": ["input_str", "recursive_str", "error_str"], #prompt, generated YAML, Error Message
        },
    }

    if operation_mode not in templates:
        raise ValueError(f"Unbekannter operation_mode: {operation_mode}")
    if language not in templates[operation_mode]:
        raise ValueError(f"Unbekannte Sprache '{language}' für {operation_mode}")
    if template_type not in templates[operation_mode][language]:
        raise ValueError(f"Unbekannter template_type '{template_type}' für {operation_mode}")
    if stage not in templates[operation_mode][language][template_type]:
        raise ValueError(f"Stage '{stage}' nicht definiert für {operation_mode}")

    try:
        template = templates[operation_mode][language][template_type][stage]
        input_var_selection = stage.split('_')[0]
        input_var = input_vars_map[operation_mode][input_var_selection]
    except KeyError:
        raise ValueError(f"No template für operation_mode='{operation_mode}', language='{language}', template_type='{template_type}' and stage='{stage}' found.")


    prompts.insert(0, PromptTemplate(template=template, input_variables=input_var))
    return prompts


def fillin_prompt_template(
    prompt: PromptTemplate,
    input_str: str,
    recursive_str: str = "",
    error_str: str = "",
) -> dict[str, str]:
    """
    Fills the prompt template with the given input values.

    Args:
        prompt (PromptTemplate): A prompt template that will be used to generate the LLM chain.
        reference_playbook (str): The reference Playbook from the dataset.
        playbook_prompt (str): The prompt generated to a specific ansible yaml file.

        #llm_response (str): The current translation of the source code in the target language. #stop
        #stderr (str): The error information of standard error of the latest execution.
        #test_data (dict): The data from the latest test execution (input, expected output, and generated output).

    Returns:
        The filled in prompt template of the chain as a string.
    """
    return prompt.format(
        input_str=input_str,
        recursive_str = recursive_str,
        error_str = error_str,
    )


def create_and_invoke_prompt_chain(
    prompt: PromptTemplate,
    llm: LLM,
    input_str: str,
) -> dict[str, str]:
    """
    Creates an LLMChain using a given prompt template and LLM object.

    Args:
        prompt (PromptTemplate): A prompt template that will be used to generate the LLM chain.
        llm (LLM): An LLM model that will be used in the LLM chain.
        playbook (str): The playbook for which a prompt is needed.

    Returns:
        A dictionary containing the translated source code and its corresponding source code in the specified languages.
    """

    # create prompt template > LLM sequence
    chain = prompt | llm 

    # Invoke the chain (identisch wie vorher)
    return chain.invoke(
        {
            "input_str": input_str,
        }
    )

def create_and_invoke_recursive_chain(
    prompt: PromptTemplate,
    llm: LLM,
    input_str: str,
    recursive
) -> dict[str, str]:
    """
    Creates an LLMChain using a given prompt template and LLM object.

    Args:
        prompt (PromptTemplate): A prompt template that will be used to generate the LLM chain.
        llm (LLM): An LLM model that will be used in the LLM chain.
        playbook (str): The playbook for which a prompt is needed.

    Returns:
        A dictionary containing the translated source code and its corresponding source code in the specified languages.
    """

    # create prompt template > LLM sequence
    chain = prompt | llm 

    # Invoke the chain (identisch wie vorher)
    return chain.invoke(
        {
            "input_str": input_str,
        }
    )

