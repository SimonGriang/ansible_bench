# Code Setup Information
This Repository, more precise, some of the code in this Repository is based on the Code of Vera Kowalczuk and her Master Thesis on Code Translation. [LLM_Code_Translation](https://github.com/ast-fortiss-tum/llm-code-translation))
Given this code basis, I started to restructure the project and tailoring it to my demands. Therefore I state her some basic information on the original unmodified code. 

## Supported Models
This section shows all supported models in the original code and their context-window-size

### Ollama

| model_name       | Kontext‑Limit (Tokens) |
|------------------|-----------------------:|
| `mistral`        | 8192                   |
| `mixtral:8x7b`   | 8192                   |
| `codellama:70b`  | 100000                 |
| `dolphin-mistral`| 16000                  |
| `dolphin-mixtral`| 16000                  |
| `llama3`         | 8000                   |
| `phi3`           | 4000                   |
| `codestral`      | 32000                  |
| `gemma-3`        | 131000                 |

**Example:**  
```bash
 --engine ollama --model phi3 
 ```


 ## Llamafile

| model_name                   | Port | Context‑Limit (Tokens) |
|------------------------------|-----:|-----------------------:|
| `mistral`                    |  8090 |                   8192 |
| `mixtral`                    |  8091 |                   8192 |
| `codellama`                  |  8092 |                 100000 |
| `dolphin-2.6-mistral`        |  8093 |                  16000 |
| `dolphin-2.7-mixtral`        |  8094 |                  16000 |
| `dolphincoder-starcoder2-15b`|  8095 |                   4000 |
| `dolphin-2.6-phi-2`          |  8096 |                   2048 |
| `llama3`                     |  8097 |                   8000 |
| `phi3`                       |  8098 |                   4000 |
| `codestral`                  |  8099 |                  32000 |

**Example:**  
```bash
 --engine llamafile --model phi3 
 ```

## Configuration Files

In the original repository this 

> Setup
> Before running the pipeline you need to adjust the config in codetransbenchmark/config/config.yaml and in codetrans/src/codetrans/codetrans_config.py to your system.
> We use llamafile and ollama as runtimes for inference with the LLMs. To use GGUFs of the models, download the models and place them in a directory as specified in codetrans/src/codetrans/codetrans_config.py.

Therefore the interesting config files are codetrans/src/codetrans/codetrans_config.py and codetransbenchmark/config/config.yaml. As I have restructured the project and avoided to use two seperate python projects both of the config files can be found as their pendants as src/ansible_bench_code/config/config.yaml and src/ansible_bench_code/utils/config.py
