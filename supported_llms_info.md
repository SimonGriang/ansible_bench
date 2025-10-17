# Code Setup Information
This file gives information about the code setup, and all currently supported Models.

This Repository, more precise, some of the code in this Repository is based on the Code of Vera Kowalczuk and her Master Thesis on Code Translation. [LLM_Code_Translation](https://github.com/ast-fortiss-tum/llm-code-translation)
Given this code basis, I started to restructure the project and tailoring it to my demands.

## Supported Models
This work focuses on locally executable open-source language models available through Ollama. The tool currently supports a curated selection of models from major AI developers, as listed in the table below. The evaluation and results presented in this study are based on these models. Depending on future requirements, the selection can be extended with additional models provided via Ollama or llamafile.

A key selection criterion was that each model must be executable under the following hardware constraints:

RAM: minimum 32 GB

VRAM: 20 GB

Because large context windows lead to substantial VRAM usage, primarily due to the self-attention mechanism, smaller models must be preferred to ensure stable execution within these limits.

| Company       | Selected Model |  Size | #Parameters | Context Window | Quantization |
| ------------- | -------------- |  ---- | ----------- | -------------- | ------------ |
| **Alibaba**   |[qwen2.5:14b](https://ollama.com/library/qwen2.5:14b) | 9GB | 14b | 32k | Q4_K_M |
| **Deepseek**  |[deepseek-r1:14b](https://ollama.com/library/deepseek-r1:14b) | 9GB | 14b | 128k | Q4_K_M |
| **Google**    |[gemma3:27b](https://ollama.com/library/gemma3:27b) | 17GB | 27b | 128k | Q4_K_M |
| **IBM**    |[granite-code:20b](https://ollama.com/library/granite-code:20b) | 12GB | 20b | 8k | Q4_0 |
| **Meta**      |[llama3.1:8b](https://ollama.com/library/llama3.1:8b) | 4,9GB | 8b | 128k | Q4_K_M |
| **Microsoft** |[phi4:14b](https://ollama.com/library/phi4:14b) | 9,1GB | 14b | 16k | Q4_K_M |
| **Mistral**   |[codestral:22b](https://ollama.com/library/codestral:22b) | 13GB | 22b | 32k | Q4_0 |
| **OpenAI**    |[gpt-oss:20b](https://ollama.com/library/gpt-oss:20b) | 14GB | 20b | 128k | MXFP4 |

From the selected models, 64 possible model constellations arise with respect to prompt generation and Ansible-YAML generation.

| Benchmark → / Prompt ↓ | **qwen2.5:14b** (Alibaba) | **deepseek-r1:14b** (Deepseek) | **gemma3:27b** (Google) | **granite-code:20b** (IBM) | **llama3.1:8b** (Meta) | **phi4:14b** (Microsoft) |  **codestral:22b** (Mistral) | **gpt-oss:20b** (OpenAI) |
|---------------|---------|-----------|----------|--------|------|-----------|---------|--------|
| **qwen2.5:14b** (Alibaba)   |    (✓)\*   |    (✓)\*    |    (✓)\*    |   (✓)\*   |  (✓)\*  |     (✓)\*    |    (✓)\*   |   (✓)\*   |
| **deepseek-r1:14b** (Deepseek) |    (✓)\*    |     (✓)\*    |    (✓)\*    |   (✓)\*   |  (✓)\*  |     (✓)\*    |    (✓)\*   |   (✓)\*   |
| **gemma3:27b** (Google) |    ✓\*    |     ✓\*     |    ✓\*     |   ✓\*    |  ✓\*   |     ✓\*     |    ✓\*    |   ✓\*    |
| **granite-code:20b** (IBM)|    ✓\*    |     ✓\*     |    ✓\*     |   ✓\*    |  ✓\*   |     ✓\*     |    ✓\*    |   ✓\*    |
| **llama3.1:8b** (Meta)|    ✓\*    |     ✓\*     |    ✓\*     |   ✓\*    |  ✓\*   |     ✓\*     |    ✓\*    |   ✓\*    |
| **phi4:14b** (Microsoft)|    ✓\*    |     ✓     |    ✓     |   ✓    |  ✓   |     ✓     |    ✓    |   ✓    |
| **codestral:22b** (Mistral)|    ✓    |     ✓     |    ✓     |   ✓    |  ✓   |     ✓     |    ✓    |   ✓    |
| **gpt-oss:20b** (OpenAI)|    ✓    |     ✓     |    -     |   ✓    |  ✓   |     –     |    –    |   –    |

**✓** = combination run  <br>
**(✓)** = ran but with wrong passed_ansiblelint_at_first_iteration and 8000 tokens for all models  <br>
**✓\*** = run without modified ansible-role-ansible, ansible-role-bootstrap-JonasPammer and ansible-role-docker, ansiblelint was not passable for these yaml files  --> run these roles again for all models (takes only few hours)  <br>
**–** = combination did not run yet  <br>

## Configuration Files

In the original repository this 

> Setup
> Before running the pipeline you need to adjust the config in codetransbenchmark/config/config.yaml and in codetrans/src/codetrans/codetrans_config.py to your system.
> We use llamafile and ollama as runtimes for inference with the LLMs. To use GGUFs of the models, download the models and place them in a directory as specified in codetrans/src/codetrans/codetrans_config.py.

Therefore the interesting config files are codetrans/src/codetrans/codetrans_config.py and codetransbenchmark/config/config.yaml. As I have restructured the project and avoided to use two seperate python projects both of the config files can be found as their pendants as src/ansible_bench_code/config/config.yaml and src/ansible_bench_code/utils/config.py
