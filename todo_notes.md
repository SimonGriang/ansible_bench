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
- [ X ] Create score, e.g. yamllint_passed --> +1, yamllint_passed_without_iteration --> +2, ... sum up, average score or percentage of max points
- [ X ] run all combinations to prove prompt quality
- [ ] EDA for 
    - [ ] file sizes (Korrelation, size-score (yaml, ansible, bench))
    - [ ] references in yamlfils (yes/no) (Korrelation, refs-score (yaml, ansible, bench))
    - [ ] Ggf. durchschnittliche Generierungsfähigkeit über alle Prompt-Modelle hinweg
    - [ ] Datensatz-Dateien in 
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


## EDA

Sehr gut – das ist ein solider Datensatz, mit dem man eine Menge machen kann.
Ich fasse zuerst strukturiert zusammen, welche Arten von Analysen und Visualisierungen hier sinnvoll sind und welche nicht, basierend auf den Abhängigkeiten, die du genannt hast (z. B. BenchmarkScore hängt teilweise von YamllintScore und AnsiblelintScore ab).

### 1. Sinnvolle Analyse-Ebenen
#### A. Modell-Kombinationsanalyse (Prompt-Modell × Benchmark-Modell)

Hier geht’s um die 64 Kombinationen.
Ziel: herausfinden, welche Modelle in welcher Rolle (Promptgenerator vs. Ausführungsmodell) am besten harmonieren.

Aussagen / Grafiken:

Heatmap des Benchmark100 Scores → sofort erkennbar, welche Kombinationen stark/schwach sind.

Durchschnittlicher Score pro Prompt-Modell → welches Modell generiert die besten Prompts?

Durchschnittlicher Score pro Benchmark-Modell → welches Modell reagiert am besten auf Prompts?

Varianz pro Modell → Stabilität der Leistung (manche Modelle liefern gleichmäßig gut, andere stark schwankend).

Korrelationsanalyse zwischen Laufzeit und Score → ist bessere Qualität teurer (zeitintensiver)?

Achtung: keine Korrelation mit Yamllint/Ansiblelint, da Bestandteil der Benchmarks.

#### B. Performance-Zeit-Beziehung

Du hast für jede Kombination auch Run Duration.
Fragen, die man beantworten kann:

Gibt es ein Modell, das signifikant länger braucht, aber nicht besser abschneidet → Effizienzvergleich.

Scatterplot: BenchmarkScore vs. Laufzeit → Trendanalyse (z. B. lohnt sich längere Laufzeit?).

Heatmap der durchschnittlichen Laufzeit pro Modell-Kombination.

#### C. YAML/Ansiblelint Scores separat

Auch wenn sie nicht direkt in den Benchmark-Vergleich einfließen sollen, kann man sie für Qualitäts-Konsistenz prüfen:

Wie konsistent sind Modelle im Linting (Varianz der Scores)?

Korrelationsmatrix zwischen YamllintScore und AnsiblelintScore → ob Lint-Qualität generell zusammenhängt.

Histogramme pro Modell: wie „streng“ oder „fehleranfällig“ ist das Modell im Linting?

#### D. YAML-Datei-Analyse (Detaildaten)

Das ist dein „Error Landscape“.
Was du daraus ziehen kannst:

Häufigkeit von Fehlern je Datei-Typ oder Datei-Größe → Komplexität vs. Fehlerrate.

Korrelation zwischen Dateigröße (chars) und Molecule failed/passed.

Dateien, die konsistent versagen → Kandidaten für Benchmark-Bias oder strukturelle Schwächen im YAML.

Anteil „Molecule passed“ pro Datei → Erfolgsquote.

Heatmap: (Fehlertyp vs. Anzahl) – zeigt, wo typischerweise Probleme liegen (Lint vs. Molecule).

#### E. Cross-Dimensionale Insights

Ein paar gezielte Hypothesen, die man prüfen kann:

„Starke Promptgeneratoren = stärkere Benchmarkmodelle?“
→ Korrelation zwischen Durchschnittsleistung als Promptgenerator und als Benchmarkmodell.

„Laufzeit-Preis für Qualität?“
→ Modelle mit hoher Benchmarkleistung, aber sehr langen Laufzeiten, sind ineffizient.

„Einfluss der Modellgröße“
→ Vergleich kleiner vs. großer Modelle (8B, 14B, 27B, 20B …).

### 2. Konkrete Visualisierungen (empfohlen)
| Art | Ziel | Empfehlung |
|------|------|-------------|
| **Heatmap (BenchmarkScore)** | Welche Kombinationen sind stark/schwach? | 8×8 Matrix |
| **Bar Chart – Durchschnittlicher Score pro Prompt-Modell** | Promptqualität | Sortiert nach Mittelwert |
| **Bar Chart – Durchschnittlicher Score pro Benchmark-Modell** | YAML-Verarbeitungsqualität | Sortiert nach Mittelwert |
| **Scatterplot – BenchmarkScore vs. Run Duration** | Effizienz | Marker pro Kombination |
| **Boxplot – Lint-Scores je Modell** | Streuung der Lint-Qualität | Yamllint / Ansiblelint getrennt |
| **Histogramm – Molecule Passed pro Datei** | Erfolgsquote im Detail | ggf. nach Dateigröße gruppieren |
| **Heatmap – Molecule Failed / Lint Failed vs. File Size** | Komplexitätseinfluss | visuell sehr aufschlussreich |
| **Korrelationsmatrix (ohne BenchmarkScore)** | Unabhängige Beziehungen prüfen | zwischen RunTime, Yamllint, Ansiblelint |

