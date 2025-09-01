<<<<<<< HEAD
# KI gestützte IT-Automatisierung: Optimierung des Konfigurationsmanagements durch LLM basierte Skriptgenerierung
This Repository provides the code and some additional information on the master thesis **"KI gestützte IT-Automatisierung: Optimierung des Konfigurationsmanagements durch LLMbasierte Skriptgenerierung"** by **Simon Göttsberger** at the **Technical University of Applied Sciences Rosenheim**. 


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
python ansible_generator.py -m codestral -e llamafile prompt -d example -tt exact   
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
python ansible_generator.py -m codestral -e llamafile benchmark -d example -tt exact -p /dataset/llamafile_codestral_english_exact
```
