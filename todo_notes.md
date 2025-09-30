# 📝 ToDo-Liste

## Aktueller Arbeitsschritt
- [ ] Refactoring bulky functions!
- [ ] add LLM-as-a-Judge to Prompt Generation
- [ ] add molecule testing pipeline to ensure all untouched roles have working molecule tests before benchmark runs --> otherwise stop benchmark
- [ ] Check if RAM memory can be reduced

## Weiteres
- [ ] Da ich einen Teil von Veras Code verwende sollte ich eine Referenz dazu angeben.

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

