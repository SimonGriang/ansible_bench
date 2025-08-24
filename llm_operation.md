# Overview: Models and Quantization across Hugging Face GGUF, llamafile, and Ollama

## 1. Hugging Face GGUF
- **Format**: Standard binary format for `llama.cpp` and compatible runtimes.  
- **Quantization**: Wide variety (Q2, Q3, Q4_K_M, Q5_K_M, Q6, Q8, FP16).  
- **Compatibility**: Runs on CPU, NVIDIA (CUDA), AMD (ROCm), Apple Silicon (Metal).  
- **Use case**: Maximum flexibility; multiple quantization levels available for almost every model.  

---

## 2. llamafile
- **Format**: Single executable file (binary + GGUF model bundled).  
- **Quantization**: Uses the same GGUF variants as Hugging Face, packaged into a portable binary.  
- **Compatibility**: Cross-platform (Linux, macOS, Windows). Supports CPU and GPU the same way as GGUF.  
- **Use case**: Simplifies distribution and execution; same hardware requirements as GGUF.  

---

## 3. Ollama
- **Format**: Own container format, based on GGUF.  
- **Quantization**: Typically ships with Q4_K_M by default, tuned for broad usability. Fewer variants than Hugging Face.  
- **Compatibility**: Optimized for macOS (Apple Silicon), also runs on NVIDIA and Linux/Windows.  
- **Use case**: Focuses on simplicity; preconfigured models with stable performance out of the box.  

---

## General Rules for Quantization Levels

- **Q2/Q3**: Very low memory requirements, noticeable quality drop; suitable only for minimal setups.  
- **Q4**: Common sweet spot, balances memory and accuracy; works on consumer GPUs with 8–12 GB VRAM.  
- **Q5**: Higher accuracy, ~30–40% more memory than Q4; recommended for GPUs with 12–16 GB VRAM or more.  
- **Q6/Q8**: Near lossless, requires roughly 2× the memory of Q4; realistic only with >20 GB VRAM.  
- **FP16**: Full precision, extremely memory-hungry; requires server-class GPUs (40–80 GB VRAM or more).  

---

## Typical Model Sizes (depending on quantization)

| Model size | Q4 (approx.) | Q5 (approx.) | Q8 (approx.) | FP16 (approx.) | Practical on              |
|------------|--------------|--------------|--------------|----------------|---------------------------|
| **7B**     | 4–5 GB       | 6–7 GB       | 10–11 GB     | 13–14 GB       | Almost all systems        |
| **13B**    | 8–10 GB      | 11–13 GB     | 18–20 GB     | 25–26 GB       | Midrange–high-end GPUs    |
| **30B**    | 20–24 GB     | 28–32 GB     | 45–50 GB     | ~60 GB         | High-end GPUs, multi-GPU  |
| **65/70B** | 40–45 GB     | 55–60 GB     | 85–90 GB     | 120+ GB        | Server GPUs, clusters     |

---

## Key Takeaways
- **Hugging Face GGUF** → maximum flexibility, all quantizations available.  
- **llamafile** → same requirements, distributed as portable executables.  
- **Ollama** → fewer variants (mostly Q4_K_M), tuned for easy and stable usage.  
- **In general** → lower-bit quantization reduces memory at the cost of quality; higher-bit quantization increases quality but requires exponentially more memory.


# THRO VM

As the TH VM provides the following VRAM Specs: 10 GB VRAM A100 NVIDIA GPU
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.133.20             Driver Version: 570.133.20     CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  GRID A100D-10C                 On  |   00000000:02:01.0 Off |                    0 |
| N/A   N/A    P0            N/A  /  N/A  |       0MiB /  10240MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.133.20 Driver Version: 570.133.20 CUDA Version: 12.8 |
|-----------------------------------------+------------------------+----------------------|
| GPU Name Persistence-M | Bus-Id Disp.A | Volatile Uncorr. ECC |
| Fan Temp Perf Pwr:Usage/Cap | Memory-Usage | GPU-Util Compute M. |
| | | MIG M. |
|=========================================+========================+======================|
| 0 GRID A100D-10C On | 00000000:02:01.0 Off | 0 |
| N/A N/A P0 N/A / N/A | 0MiB / 10240MiB | 0% Default |
| | | N/A |
+-----------------------------------------------------------------------------------------+

+-----------------------------------------------------------------------------------------+
| Processes: |
| GPU GI CI PID Type Process name GPU Memory |
| ID ID Usage |
|=========================================================================================|
| No running processes found |
+-----------------------------------------------------------------------------------------+


# Suitable Models for A100D-10 GB VRAM Setup

## System Specification
- **GPU**: NVIDIA A100D-10C with 10 GB VRAM
- This VRAM limit defines the upper boundary for quantized model sizes that can run comfortably without offloading.

---

##  Recommended Quantization Levels (All ~7 B Models)

- **Q4_K_M** (≈ 4–5 GB): Balanced between memory efficiency and quality — ideal fit.  
- **Q5_K_M** (≈ 5–7 GB): Higher fidelity, still fits within the 10 GB limit — excellent choice.  
- **Q8_0** (≈ 10–11 GB): At the edge of the memory limit; may cause OOM, especially with large context windows — use with caution or avoid.

---

## Recommended Models (Quantized in GGUF Format)

| Model Name                                 | Quantization | Size (Approx.)  | Notes                             |
|-------------------------------------------|--------------|------------------|-----------------------------------|
| **Mistral-7B-Instruct v0.2 (TheBloke)**   | Q4_K_M       | ~4.37 GB         | Strong general instruction tuning :contentReference[oaicite:0]{index=0} |
| **OpenHermes-2.5 (Mistral-7B)**            | Q4_K_M / Q5_K_M | ~4.37 GB / ~5.13 GB | Quality-focused variants :contentReference[oaicite:1]{index=1} |
| **NuminaMath-7B-TIR**                      | Q4_K_M / Q5_K_M | ~4.22 GB / ~4.93 GB | Math-optimized; efficient quant variant :contentReference[oaicite:2]{index=2} |
| **LLaMA 2-7B** (TheBloke GGUF)             | Supports Q2–Q8 | Q4 ≈ ? (typically ~4–5 GB) | Flexible quant support :contentReference[oaicite:3]{index=3} |
| **CodeLlama 7B** (Meta, GGUF)              | Supports quant variants | Q4 ≈ 4–5 GB | Code-centric tasks, large context :contentReference[oaicite:4]{index=4} |

---

## Key Takeaways

- **7B models** in **Q4_K_M** or **Q5_K_M** quantization are the most suitable—small enough for 10 GB VRAM and high in quality.
- **13B models** in Q4 (~8–10 GB) are theoretically workable but extremely tight; stability and performance may suffer.
- **Models ≥ 30B** or higher-bit quantizations (Q8_0 beyond 10 GB) exceed VRAM limits and are **not recommended**.
- These recommendations apply broadly across **Hugging Face GGUF**, **llamafile**, or **Ollama**, as all support these quant formats.


