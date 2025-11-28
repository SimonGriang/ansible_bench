# KI gestützte IT-Automatisierung: Optimierung des Konfigurationsmanagements durch LLM basierte Skriptgenerierung
This Repository provides the code and some additional information on the master thesis **"KI gestützte IT-Automatisierung: Optimierung des Konfigurationsmanagements durch LLM basierte Skriptgenerierung"** by **Simon Göttsberger** at the **Technical University of Applied Sciences Rosenheim**. 


# Prompts for using this tool

**Ansible Generator**
```bash
python ansible_generator.py --help

usage: ansible_generator.py [-h] -m MODEL [-e ENGINE] [-tk TOP_K] [-tp TOP_P] [-t TEMPERATURE] [-l LANGUAGE] {prompt,benchmark,generation} ...

Tool for creating benchmarks, executing benchmark runs, and generating Ansible YAML files. The behavior is controlled via the --operation_mode argument; additional
parameters vary depending on the selected mode.

options:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        model to use for code translation.
  -e ENGINE, --engine ENGINE
                        Name of the model engine to use. Valid values: 'llamafile', 'ollama', 'torch'. Note that there is only a basic implementation for using      
                        pytorch and the HuggingFace transformers library. Default: 'llamafile'.
  -tk TOP_K, --top_k TOP_K
                        The number of highest probability vocabulary tokens to keep for top-k-filtering. Only applies for sampling mode, with range from 1 to 100.   
                        Default value is 50.
  -tp TOP_P, --top_p TOP_P
                        Only the most probable tokens with probabilities that add up to top_p or higher are considered during decoding. The valid range is 0.0 to    
                        1.0. 1.0 is equivalent to disabled and is the default. Only applies to sampling mode. Also known as nucleus sampling. Default value is       
                        0.95.
  -t TEMPERATURE, --temperature TEMPERATURE
                        A value used to warp next-token probabilities in sampling mode. Values less than 1.0 sharpen the probability distribution, resulting in      
                        "less random" output. Values greater than 1.0 flatten the probability distribution, resulting in "more random" output. A value of 1.0 has    
                        no effect and is the default. The allowed range is 0.0 to 2.0. Default value is 0.7.
  -l LANGUAGE, --language LANGUAGE
                        Prompt languages available. Possible languages are: english, german

operation_mode:
  Specifies the operation mode of the tool:

  {prompt,benchmark,generation}
    prompt              Generate prompts from Ansible role YAML files. Prompts can be created in three different levels of detail.
    benchmark           Run the benchmark by generating Ansible YAML files and validating them using YAML-Lint, Ansible Playbook syntax check Ansible-Lint and       
                        Molecule.
    generation          Generate Ansible YAML files based on user-provided prompts, followed by an automated quality check using YAML-Lint, Ansible Playbook syntax  
                        check, and Ansible-Lint.
```

**Ansible Generator Prompt Mode**
```bash
python ansible_generator.py -m codestral -e llamafile prompt -h                                    
usage: ansible_generator.py prompt [-h] [-d DATASET] [-tt TEMPLATE_TYPE]

options:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        Dataset to use for prompt generation. Note that possible datasets are the files in the directory /dataset/. The folder should contain        
                        ansible-roles with out of the box working molecule tests!
  -tt TEMPLATE_TYPE, --template_type TEMPLATE_TYPE
                        Type of the prompt template to use for code translation. Possible types are: exact, precise, approximate. Default: exact
```

Prompt for using PROMPT mode:
```bash
python ansible_generator.py -m gpt-oss:20b -e ollama prompt -d benchmark100 -tt exact   
```

**Ansible Generator Benchmark Mode**
```bash
python ansible_generator.py -m codestral -e llamafile benchmark -h                                 
usage: ansible_generator.py benchmark [-h] [-d DATASET] [-tt TEMPLATE_TYPE] -p PROMPTS

options:
  -h, --help            show this help message and exit
  -d DATASET, --dataset DATASET
                        Dataset to use for benchmark creation (same as for prompt generation). Note that possible datasets are the files in the directory
                        /dataset/. The folder should contain ansible-roles.
  -tt TEMPLATE_TYPE, --template_type TEMPLATE_TYPE
                        Type of the prompt template to use for code translation. Possible types are: exact, precise, approximate. Default: exact
  -p PROMPTS, --prompts PROMPTS
                        Path to generated prompts generated with this tool. Path relative to /dataset/ folder. Path construction:
                        /dataset/prompts/<engine>_<model>_<language>_<template_type>
```

Example for using BENCHMARK mode:
```bash
python ansible_generator.py -m gpt-oss:20b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_gpt-oss:20b_english_exact/benchmark100
```

**Ansible Generator Generation Mode**
```bash
usage: ansible_generator.py generation [-h] [-y MAX_YAMLLINT_ITERATIONS] [-a MAX_ANSIBLELINT_ITERATIONS] [-s MAX_SYNTAXCHECK_ITERATIONS]
                                       [-o OUTPUT_PATH] [-tt TEMPLATE_TYPE] [-i INVENTORY]

options:
  -h, --help            show this help message and exit
  -y MAX_YAMLLINT_ITERATIONS, --max_yamllint_iterations MAX_YAMLLINT_ITERATIONS
                        Number of maximum iterations for yamllint quality assurance loop. If the generated YAML file does not pass the
                        yamllint check the last generated file will be returned. If no value is provided, yamllint quality assurance
                        will continued until, either a file passes or the process is manually stopped.
  -a MAX_ANSIBLELINT_ITERATIONS, --max_ansiblelint_iterations MAX_ANSIBLELINT_ITERATIONS
                        Number of maximum iterations for ansiblelint quality assurance loop. If the generated YAML file does not pass
                        the ansiblelint check the last generated file will be returned. If no value is provided, ansiblelint quality
                        assurance will continued until, either a file passes or the process is manually stopped.
  -s MAX_SYNTAXCHECK_ITERATIONS, --max_syntaxcheck_iterations MAX_SYNTAXCHECK_ITERATIONS
                        Number of maximum iterations for ansible-playbook --syntax-check quality assurance loop. If the generated YAML
                        file does not pass the syntax check the last generated file will be returned. If no value is provided, syntax
                        check quality assurance will continued until, either a file passes or the process is manually stopped. Note that
                        syntax check is only effective for template_type playbook.
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to output directory where generated files will be saved. Full path from root directory. Default
  -tt TEMPLATE_TYPE, --template_type TEMPLATE_TYPE
                        Type of the prompt to use for Ansible-YAML generation. Template type defines if the generated YAML files are
                        task files or playbooks. Possible types are: task_file, playbook. Default: task_file
  -i INVENTORY, --inventory INVENTORY
                        file path to the Ansible inventory file. If not provided, it will be assumed the only inventories in the ansible
                        src/ file will be used. Specification highly recoomended.
```

Example for using GENERATION mode:
```bash
python ansible_generator.py -m gpt-oss:20b -e ollama generation -tt playbook -i /home/user/documents/ansible_bench/src/inventory/inventory.ini -y 5 -s 5 -a 5
```

# 1. Extending the Repository with New Models

This repository is designed to benchmark the ability of various local LLMs to reconstruct and generate Ansible automation code. To support a broad and evolving ecosystem of models, the system was built to be modular. Adding new models is straightforward, provided that the tokenizer and model directory structure follow the expected conventions.

The project supports three execution backends:

- **Ollama** (preferred and primary runtime)
- **llamafile** (binary-distributable LLM runtime)
- **PyTorch/HuggingFace** (mainly for experimentation)

Local execution avoids cloud dependencies and enables reproducible, controlled experiments.

## 1.1 Tokenizer Setup

Many models—especially those executed via HuggingFace—require a tokenizer that is not included by default.  
Because this repository performs strict prompt-length validation before inference, the tokenizer must be available locally and must match the model's internal naming.

Instructions for downloading and placing tokenizers are described here:

➡️ **[tokenizer_info.md](./tokenizer_info.md)**

After obtaining a tokenizer:

1. Put the tokenizer folder into the directory defined in  
   `ansible_generator_config.py` → `TOKENIZER_MODELS_PATH`.

2. The tokenizer directory name must match exactly the identifier returned by  
   `llm_chain.py` → `hf_modelfiles_path_for()`.

This ensures that prompt size estimation uses the correct tokenization scheme.  
Since context windows often appear large on paper (32k, 64k, 128k), but real-world VRAM limitations reduce the feasible limit drastically, exact token counting is mandatory for stable execution.

---

# 2. Supported Models

The repository includes a curated set of open-source language models well-suited for local execution on hardware with:

- **≥ 32 GB system RAM**
- **≈ 20 GB VRAM**

These constraints significantly reduce the number of models that can be evaluated in practice.  
Large context windows cause rapid VRAM growth due to the quadratic cost of attention mechanisms.  
Therefore, this repository focuses on models that are:

- available via Ollama,  
- quantized efficiently (Q4 or MXFP4), and  
- small enough to run inference reliably.

The following table lists all supported models currently integrated into the benchmark:

| Company       | Selected Model | Size | #Parameters | Context Window | Quantization |
| ------------- | -------------- | ---- | ----------- | -------------- | ------------ |
| **Alibaba**   | [qwen2.5:14b](https://ollama.com/library/qwen2.5:14b) | 9GB | 14b | 32k | Q4_K_M |
| **Deepseek**  | [deepseek-r1:14b](https://ollama.com/library/deepseek-r1:14b) | 9GB | 14b | 128k | Q4_K_M |
| **Google**    | [gemma3:27b](https://ollama.com/library/gemma3:27b) | 17GB | 27b | 128k | Q4_K_M |
| **IBM**       | [granite-code:20b](https://ollama.com/library/granite-code:20b) | 12GB | 20b | 8k | Q4_0 |
| **Meta**      | [llama3.1:8b](https://ollama.com/library/llama3.1:8b) | 4.9GB | 8b | 128k | Q4_K_M |
| **Microsoft** | [phi4:14b](https://ollama.com/library/phi4:14b) | 9.1GB | 14b | 16k | Q4_K_M |
| **Mistral**   | [codestral:22b](https://ollama.com/library/codestral:22b) | 13GB | 22b | 32k | Q4_0 |
| **OpenAI**    | [gpt-oss:20b](https://ollama.com/library/gpt-oss:20b) | 14GB | 20b | 128k | MXFP4 |

Because the benchmark evaluates two model-driven steps (prompt reconstruction + YAML generation), these eight models produce **64 possible model combinations**.

This enables analysis of:

- cross-model robustness,  
- consistency between reconstruction and generation,  
- sensitivity of different architectures to structured input,  
- performance variations caused by quantization schemes,  
- differences in code reliability across vendors.

---

# 3. Configuration System

This repository is the result of merging and restructuring the configuration logic from the original work of:

**Vera Kowalczuk — LLM Code Translation**  
https://github.com/ast-fortiss-tum/llm-code-translation

The original project required maintaining two independent Python projects, each containing their own configuration files:

- `codetransbenchmark/config/config.yaml`
- `codetrans/src/codetrans/codetrans_config.py`

To simplify extension and improve maintainability, this benchmark consolidates both into a single structure:

- `src/ansible_bench_code/config/config.yaml`  
- `src/ansible_bench_code/utils/config.py`

This improves:

- portability,  
- reproducibility,  
- clarity of model/runtime selection,  
- and reduces duplication significantly.

These configuration files define:

- model names  
- prompt styles
- evaluation settings  
- enabled test stages  
- context window limits  
- runtime parameters  
- paths for dataset input and report output  
- toggles for each benchmark phase  

Supported execution engines:

- **ollama** — primary, stable, large model support  
- **llamafile** — lightweight, single-file runtime  

Additional documentation:

➡️ **[ollama_user_guide.md](./ollama_user_guide.md)**  
➡️ **[llamafile_user_guide.md](./llamafile_user_guide.md)**  
➡️ **[llm_operation.md](./llm_operation.md)**

---

# 4. Hardware Constraints, Context Windows & Execution Notes

The effective context window depends heavily on VRAM.  
Even if a model advertises:

- 128k tokens  
- 100k+ context  
- or extended RAG windows

…these values cannot simply be used on a 20-GB GPU.

The reason is straightforward:

- The attention mechanism scales with **O(n²)** in memory.
- Doubling the context can require **4× more VRAM**.
- Quantization reduces model size, but not attention memory footprint.

Therefore, this repository separates:

- **theoretical model maximum**  
- **practical benchmark configuration**

Users can configure a smaller, safe effective window in the config file.

Further explanations behind these runtime constraints can be found in:

➡️ **[llm_operation.md](./llm_operation.md)**

---

# 5. Benchmark Workflow

The benchmark follows a strict two-phase evaluation pipeline.  
This ensures consistent, reproducible measurements for all supported models.

## 5.1 Phase 1 — Prompt Reconstruction

For each role in the `dataset/` directory:

1. The tool locates the role’s `tasks/` directory.  
2. All task YAML files are processed except **`assert.yml`**, since this file does not describe task logic but validation.  
3. Each YAML file is parsed and transformed into a structured prompt.  
   This includes:
   - extracting task semantics  
   - capturing module usage  
   - translating task arguments into prompt instructions  
4. All reconstructed prompts are saved.  
   These prompts form a standardized intermediate representation of each task.

The main idea:  
**Every model should receive identical, controlled prompt input.**  
This avoids noise and ensures that models are evaluated fairly and consistently.

## 5.2 Phase 2 — Benchmark Execution

1. For every reconstructed prompt, the chosen model generates a new Ansible task YAML file.  
2. The generated file replaces the corresponding original task in the role.  
3. The benchmark executes a rigorous validation pipeline:

   - **YAML-Lint**  
     Checks syntactic correctness and structure.
   - **Ansible-Lint**  
     Detects semantic and style errors, especially cross-file issues.
   - **Molecule**  
     Executes functional and semantic integration tests.

4. A detailed report is generated for each model combination.  
   Reports include:
   - stage results  
   - failure reasons  
   - runtime statistics  
   - model metadata  
   - summary tables  

This creates a reproducible mechanism to test how reliably LLMs can regenerate valid, functional Ansible code.

---

# 6. Dataset Creation

The benchmark is intentionally extensible.  
Any additional role placed under:

```
dataset/
```

will be automatically included once it fulfills the minimum requirements.

To ensure meaningful evaluations, new roles must satisfy:

### 1. Molecule Tests Must Be Present
The role must include correct Molecule tests.  
The benchmark relies on Molecule to validate functional correctness, not just syntax.

### 2. Tests Must Execute Without Manual Fixes  
Roles must work **as-is**, without human intervention.

### 3. Semantic Validation Is Required  
Tests must include a `verify.yml` that checks real behaviour, not only syntax.

### 4. No Ansible-Lint Issues Caused by Cross-File Dependencies  
Roles with intrinsic lint issues distort benchmark results.

### 5. Tasks Must Be Valid YAML  
Invalid files cannot be converted into prompts.

### 6. Roles Should Be Representative Automation Use Cases  
Roles should contain actual task logic, not placeholders or minimal stubs.

This approach guarantees a clean dataset where errors during the benchmark are attributable to LLM output—not to flawed source data.

---



