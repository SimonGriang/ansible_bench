# Ollama User Guide (Linux)

## 1. Installation
curl -fsSL https://ollama.com/install.sh | sh


Prüfen:
```bash
ollama --version
 ```



Optional: Ollama automatisch beim Systemstart starten:

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```


## 2. Modelle herunterladen und starten

Modell herunterladen und starten:

```bash
ollama run deepseek-r1:14b
```

Das öffnet eine interaktive Konsole (Prompt >).

Andere Modelle in der gleichen Familie (z. B. DeepSeek-R1-Distill-Qwen-14B) sind Alternativen für unterschiedliche Hardware/VRAM.

## 3. Interaktion
Interaktive Session

Eingabe direkt im Prompt:

> Erkläre Quantencomputing in einfachen Worten.


Session beenden:

CTRL+D → beendet die laufende Chat-Session.

Alternativ: exit oder quit funktioniert ebenfalls.

Einmalige Anfrage ohne interaktive Session
```bash
ollama query deepseek-r1:14b "Erkläre die Relativitätstheorie in einfachen Worten."
```

Anfrage aus Datei
```bash
ollama query deepseek-r1:14b "$(cat prompt.txt)"
```
