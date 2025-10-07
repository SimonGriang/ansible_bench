import subprocess

# Liste mit den Befehlen, die nacheinander laufen sollen
commands = [
    "python ansible_generator.py -m gpt-oss:20b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_gemma3:27b_english_exact/benchmark100 > ../../output/gemma_to_gpt-oss_benchmark.log 2>&1",
    "python ansible_generator.py -m qwen2.5:14b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_qwen_benchmark.log 2>&1",
    "python ansible_generator.py -m deepseek-r1:14b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_deepseek_benchmark.log 2>&1",
    "python ansible_generator.py -m gemma3:27b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_gemma_benchmark.log 2>&1",
    "python ansible_generator.py -m granite-code:20b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_granite_benchmark.log 2>&1",
    "python ansible_generator.py -m llama3.1:8b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_llama_benchmark.log 2>&1",
    "python ansible_generator.py -m phi4:14b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_phi_benchmark.log 2>&1",
    "python ansible_generator.py -m codestral:22b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_codestral_benchmark.log 2>&1",
    "python ansible_generator.py -m gpt-oss:20b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/gemma_to_gpt-oss_benchmark.log 2>&1",
]

for cmd in commands:
    print(f"\n>> Führe aus: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Ausgabe direkt anzeigen
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print("FEHLER:", result.stderr.strip())
