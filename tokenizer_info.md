# Downloading Tokenizer Files for Hugging Face Models

For each model used, the original tokenizer files must be located in the directory specified by `hf_modelfiles` in the `llm_chain.py` file.

## 1. Required Files
Depending on the tokenizer type, different files are required:

- **BPE-based models**:
  - `vocab.json`
  - `merges.txt`
  - `tokenizer_config.json`
  - `special_tokens_map.json` (optional)
- **SentencePiece-based models**:
  - `tokenizer.json` or `tokenizer.model`
  - `tokenizer_config.json`
  - `special_tokens_map.json` (optional)

The required files can be identified in the original Hugging Face repository of the model.

---

## 2. Hugging Face Account and Permissions
- A Hugging Face account is required to access gated or restricted repositories.
- For certain models, additional approval from the model owner may be required, typically via a “Request Access” button in the repository.
- Providing an affiliation (e.g., institution, company, or individual) may be necessary during the access request process.

---

## 3. Installing the Hugging Face CLI
```bash
pip install huggingface_hub
```

## 4. Authentication
```bash
hf auth login
```

## 5. Example Download Commands
Single Files:
```bash
hf download <model-repo> tokenizer.json --local-dir ./tokenizer_files
hf download <model-repo> tokenizer_config.json --local-dir ./tokenizer_files
hf download <model-repo> special_tokens_map.json --local-dir ./tokenizer_files
hf download <model-repo> tokenizer.model --local-dir ./tokenizer_files
```
Entire hf Repository:
```bash
hf download <model-repo> --local-dir ./tokenizer_files --repo-type model
```





