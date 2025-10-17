# 📝 ToDo-Liste

## Aktueller Arbeitsschritt
Code:
- [ ] Refactoring bulky functions!
- [ ] Refactoring of post-processing into seperate file/class
- [ ] add max_iterations parameter
- [ ] add LLM-as-a-Judge to Prompt Generation
- [ ] add molecule testing pipeline to ensure all untouched roles have working molecule tests before benchmark runs --> otherwise stop benchmark
- [ ] include check_missing_entries into ansible_generator
- [ ] include Score-Calculation into ansible_generator report creation
- [ ] Check if RAM memory can be reduced

Model Evaluation:
- [ ] Create score, e.g. yamllint_passed --> +1, yamllint_passed_without_iteration --> +2, ... sum up, average score or percentage of max points
- [ ] run all combinations to prove prompt quality
- [ ] figure out best model combination Prompts/Generation and try serveral different changes in
    - [ ] Temperature (higher temperature --> better/worse?, lower temperature --> better/worse?) (2 more runs)
    - [ ] max_iterations (does it improve results to do more iterations? Do I get worse results with less iterations?) (2 more runs)
    - [ ] prompt gerneration precision (does prompt-standard-information change output?) (2 more runs)
    - [ ] ansible-yaml generation precision (does prompt-standard-information change output?) (2 more runs)
    - [ ] run prompt generation with best model once again with llm as a judge in pipeline
        - llmaaj has 3 iterations to check result (1 more run)
        - until llmaaj approves (1 more run)
    --> overall 10 more runs with best combination

Thesis (only changes to be made):
- [ ] Prüfkriterium für die Literatur, begründen!
- [ ] Workflowkapitel: Wie wird vorgegangen und was ist das Ziel (Unterschiede zwischen den verschiedenen CM-Tools aufzeigen und anschließend auf ein Tool festlegen, für welches die Skriptgenerierung betrachtet wird.)
- [ ] Vergleichskriterien klarer darstellen (Auflistung oder Tabelle, wird zwar später ersichtlich aber muss auf ersten Blick in Kapitel 3.1 ersichtlich sein.)
- [ ] ggf. Konfigurationsmanagement noch klarer darstellen in Kapitel 2
- [ ] Forschungsfragen und Unterforschungsfragen zu Beginn eines Jeden Teils stellen
    - [ ] FF1 vor Vergleichskriterien
    - [ ] Unterforschungsfragen
        - [ ] Wo liegen die technischen zwischen den verschiednene CM-Tools
        - [ ] Wie unterscheidet sich die Nutzung der unterschiedlichen CM-Tools, also welche sind mehr oder weniger verbreitet?
        - [ ] Welche Stärken und Schwächen haben die verschiedenen CM-Tools?
    - [ ] Am Ende des ersten Parts nach Tabelle 3.2 beantwortung der Fragen. Oder in Kapitel 3.4
    - [ ] FF2 vor Überblick über den Ansible-Benchmark
        - [ ] Unterforschungsfragen
            - [ ] Wie kann die Semantik von generiertem Code geprüft werden?
            - [ ] Wie kann die Syntaktik von generiertem Code geprüft werden?
    - [ ] evtl. FF3 "Wie gut können leichtgewichtige Sprachmodelle (LLMs) syntaktisch und semantisch korrektes Ansible-YAML auf Basis eines neu entwickelten Benchmarks generieren?"
        - [ ] Subforschungsfragen:
            - [ ] In welchem Maß erreichen leichtgewichtige LLMs syntaktische Korrektheit im Vergleich zu großen Modellen?
            - [ ] In welchem Maß erreichen leichtgewichtige LLMs semantische Korrektheit im Vergleich zu großen Modellen?  
            - [ ] Wie gut schneiden LLMs bei bei Generierung basierend auf deutscher Sprache ab?
    - [ ] evtl. FF4 "Welche Optimierungsmethoden existieren für um die Fähigkeit Ansible-YAML zu verbessern existieren?"
    - [ ] Subforschungsfragen:
        - [ ] Andere Pompts? (Detaillierungsgrad)
        - [ ] Andere Temperature?
        - [ ] Mehr/Weniger Ansiblelint/Yamllint iterationen?
        - [ ] LLM-as-a-Judge bei der Promptgenerierung/YAML-Generierung?
        - [ ] Kein Fine-Tuning/RAG da ja bereits in anderen Arbeiten beleuchtet (Pujar, Lightspeed, DocCGen, Darnell)

## Weiteres
- [ ] Da ich einen Teil von Veras Code verwende sollte ich eine Referenz dazu angeben.
- [ ] Used max_iterations_yamllint = 5 and max_iterations_ansiblelint = 4 in benchmark runs!

## Notes
```bash
 python ansible_generator.py -m gemma3:27b -e ollama prompt -d benchmark100 -tt exact  > ../../dataset/prompts/gemma_prompt.log 2>&1
```
```bash
python ansible_generator.py -m qwen2.5:32b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:32b_english_exact/benchmark100 > ../../output/qwen_to_qwen_benchmark.log 2>&1
```
```bash
hf download google/gemma-3-270m tokenizer.json --local-dir ~/documents/tokenizer/gemma3/
```

