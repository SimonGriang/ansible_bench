from datetime import datetime
from multiprocessing import process
import os
import subprocess
import re
import time

# List of commands to run
commands = [
    "python ansible_generator.py -m gpt-oss:20b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_qwen2.5:14b_english_exact/benchmark100 > ../../output/ollama_gpt-oss:20b_english_exact/benchmark100/qwen_to_gpt-oss_benchmark.log 2>&1",
    #"python ansible_generator.py -m qwen2.5:14b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_qwen2.5:14b_english_exact/benchmark100/deepseek_to_qwen_benchmark.log 2>&1",
    "python ansible_generator.py -m deepseek-r1:14b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_deepseek-r1:14b_english_exact/benchmark100/deepseek_to_deepseek_benchmark.log 2>&1",
    "python ansible_generator.py -m gemma3:27b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_gemma3:27b_english_exact/benchmark100/deepseek_to_gemma_benchmark.log 2>&1",
    "python ansible_generator.py -m granite-code:20b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_granite-code:20b_english_exact/benchmark100/deepseek_to_granite_benchmark.log 2>&1",
    "python ansible_generator.py -m llama3.1:8b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_llama3.1:8b_english_exact/benchmark100/deepseek_to_llama_benchmark.log 2>&1",
    "python ansible_generator.py -m phi4:14b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_phi4:14b_english_exact/benchmark100/deepseek_to_phi_benchmark.log 2>&1",
    "python ansible_generator.py -m codestral:22b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_codestral:22b_english_exact/benchmark100/deepseek_to_codestral_benchmark.log 2>&1",
    "python ansible_generator.py -m gpt-oss:20b -e ollama benchmark -d benchmark100 -tt exact -p prompts/ollama_deepseek-r1:14b_english_exact/benchmark100 > ../../output/ollama_gpt-oss:20b_english_exact/benchmark100/deepseek_to_gpt-oss_benchmark.log 2>&1",
]

for cmd in commands:
    match = re.search(r'>\s*(.*?)\s*2>&1', cmd)
    if match:
        log_path = match.group(1).strip()
        output_dir = os.path.dirname(log_path) + '/'
    else:
        print("Kein Redirect gefunden")
    print("Output-Verzeichnis erstellt:", output_dir)
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n>> [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Führe aus: {cmd}")
    #result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    process = subprocess.Popen(cmd, shell=True)

    # every 60 seconds, print a status message while the process is running
    while process.poll() is None:
        print(f">> [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Läuft: {cmd}", flush=True)
        time.sleep(60)

    # when process is done, check the exit code
    return_code = process.wait()
    if return_code == 0:
        print(f">> Fertig: {cmd}")
    else:
        print(f">> FEHLER ({return_code}): {cmd}")