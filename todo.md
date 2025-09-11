# 📝 ToDo-Liste

## Aktueller Arbeitsschritt
- [ ] Refactoring bulky functions!
- [ ] add LLM-as-a-Judge to Prompt Generation

 &rarr; Check if RAM memory can be reduced

## Aufgaben

- [X] Args & template umbauen auf template_type + language
- [X] Aufbau statt OperationManager mit PromptCreator, BenchmarkManager und GenerationManager umsetzung prüfen
        Dazu müssen wir zuerst prüfen welche Module auch entsprechend unter Verwendung des selben Interfaces modular aufgebaut werden müssten
    - ansible_generator.py --> JA, Klasse für die setup_files und run Methoden
    - Lösung:

        ```python
        # Subklassen (Template-Method Pattern)

        Die Idee: Gemeinsames Verhalten wandert in eine **Basisklasse**, jede Subklasse überschreibt nur die `run()`-Methode.

        
        class BaseOperationManager:
            def __init__(self, args, config):
                self.args = args
                self.config = config
                self.set_model_name_engine()

            # alle Setup-Methoden hier wie gehabt

            def setup_files(self)
                raise NotImplementedError  # von Subklassen implementiert

            def run(self):
                raise NotImplementedError  # von Subklassen implementiert


        class BenchmarkOperationManager(BaseOperationManager):
            def setup_files(self):
                # bench-spezifische Logik
                ...
            def run(self):
                # bench-spezifische Logik
                ...


        class GenerationOperationManager(BaseOperationManager):
            def setup_files(self):
                # generation-spezifische Logik
                ...
            def run(self):
                # generation-spezifische Logik
                ...


        class PromptOperationManager(BaseOperationManager):
            def setup_files(self):
                # prompt-generation spezifische Logik
                ...
            def run(self):
                # prompt-generation spezifische Logik
                ...


        def main(args: CLIArgumentsTranslation, config: Config):
            if args.operation_mode == "bench":
                operationsManager = BenchOperationManager(args, config)
            elif args.operation_mode == "generation":
                operationsManager = GenerationOperationManager(args, config)
            else:
                operationsManager = PromptOperationManager(args, config)

            operationsManager.setup_files()
            operationsManager.setup_llm()
            operationsManager.run()  # ruft run der Subklasse auf
        ´´´

    - Daraus ergibt sich eine klare Trennung der Modi und es ist sehr OOP-konform
    - Folgende Methoden müssen zusätzlich muss für jeden operation_mode in llm_chain eine neue Methode (create_and_invoke_...) erstellt werden, da sonst die Platzhalter in den Templates nicht übergeben werden können.

- [ ] für die folgenden Punkte noch genau überlegen wie ein Prompt-Template aussehen könnte: Immer mit Anfangsprompt im Kontext oder nicht?
- [X] Implementierung Subklasse PromptOperationManager
    - [X] Implementierung Methoden in llm_chain Subklasse PromptOperationManager
    - [X] Implementierung Prompt-Templates Subklasse PromptOperationManager
    - [ ] dataset/prompts/<engine>_<model>_<language>_<template_type>/prompt_log.txt alle Prompts und generierte prompts abspeichern

- [ ] Implementierung Subklasse BenchmarkOperationManager (in teilen auch wiederverwendbar für Generation)
    - [ ] Implementierung Prompt-Templates Subklasse PromptOperationManager
        - [ ] Template für yamllint. Template variablen: yamllint_response, generated_playbook, etc. 
            - [ ] Exit-Code für Fehlererkennung
            - [X] Ansible Role in output/<engine>_<model>_<language>_<template_type> kopieren
            - [ ] Generierte Rolle in output/<engine>_<model>_<language>_<template_type>/<ansible_role>/tasks Ordner ablegen
            - [ ] yamllint output/<engine>_<model>_<language>_<template_type>/<ansible_role>/tasks/<file.yaml> laufen lassen und Exit-Code auslesen
            - [ ] output/<engine>_<model>_<language>_<template_type>/failed_yamllint.txt abspeichern wenn ein Playbook gescheitert ist.
            - [ ] output/<engine>_<model>_<language>_<template_type>/benchmark_log.txt alle Prompts, generierten YAMLs und yamllint Responses abspeichern
        - [ ] Template für ansible syntaxcheck. Template variablen: syntaxcheck_respone, generated_playbook, etc.
        - [ ] Template für ansiblelint. Template variablen: ansiblelint_response, generated_playbook, etc.
        - [ ] Template für molecule. Template variablen: molecule_response, generated_playbook, etc.
- INFO für die oberen Punkte: Veras Handhabung in den Dateien: codetrans/src/codetrans/llm_chain.py, codetransbenchmark/src/codetransbench/translation/translate_open_source.py und codetrans/src/codetrans/prompt_templates.py
- INFO in llm_chain.fillin_prompt_template ist es kein Problem, wenn Platzhalter fehlen: Die Methode ist bewusst „generisch“, damit sie mit verschiedenen Templates funktioniert. Es werden immer alle möglichen Variablen angeboten, aber nur die tatsächlich im Template vorhandenen werden verwendet. D.h. unabhängig vom Template übergebe ich einfach immer alle möglichen "Platzhalter"


## Rechtliches

- [ ] Da ich einen Teil von Veras Code verwende sollte ich eine Referenz dazu angeben.


 

