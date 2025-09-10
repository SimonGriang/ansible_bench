# Ollama User Guide (Linux)

## 1. Installation
curl -fsSL https://ollama.com/install.sh | sh


Check the installation:
```bash
ollama --version
 ```



Optional: Start Ollama automatically at system boot

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```


## 2. Downloading and Running Models

Download and run model:

```bash
ollama run deepseek-r1:14b
```

This opens an interactive console (Prompt >).

Other models in the same family (e.g. DeepSeek-R1-Distill-Qwen-14B) are available as alternatives for different hardware/VRAM setups.

## 3. Interaction
Interaktive Session

Type directly at the prompt:

> Erkläre Quantencomputing in einfachen Worten.


End the Sesssion:

CTRL+D → ends the active Chat-Session.

Alternativ: exit oder quit works as well.

One-time query without interactive session
```bash
ollama query deepseek-r1:14b "Erkläre die Relativitätstheorie in einfachen Worten."
```

Query from a file
```bash
ollama query deepseek-r1:14b "$(cat prompt.txt)"
```
