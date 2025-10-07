import re


def transform(path: str) -> str:
    # Extrahiere Teil zwischen "ollama_" und dem Sprach/Genauigkeits-Block
    m = re.search(r"ollama_(.*?)_[^_/]+_[^_/]+", path)
    if not m:
        return path  # kein Match -> Original zurück
    
    core = m.group(1)  # z.B. "qwen2.5:14b", "gpt-oss:20b", "deepseek-r1.3:14b", "phi4:14b"

    return f"prompts_{core}"

if __name__ == "__main__":
    # Teste die Funktion mit einigen Beispielen
    test_paths = [
        "prompts/ollama_qwen2.5:14b_english_exact/benchmark100",
        "prompts/ollama_llama3.1:8b_german_precise/benchmark100",
        "prompts/ollama_gpt-oss:20b_multilingual_approximate/benchmark100",
    ]
    
    for path in test_paths:
        transformed = transform(path)
        print(f"Original: {path} -> Transformed: {transformed}")
