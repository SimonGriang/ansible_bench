## Unterstützte Modelle

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

**Beispiel:**  
```bash
 --engine ollama --model phi3 
 ```


 ## Llamafile

| model_name                   | Port | Kontext‑Limit (Tokens) |
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

**Beispiel:**  
```bash
 --engine llamafile --model phi3 
 ```