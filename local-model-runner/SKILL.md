---
name: local-model-runner
description: Execution rules, sizing heuristics, and acceleration strategies for running local AI models (Ollama, vLLM, llama.cpp, PyTorch) on the Threadripper 3990X and RTX 3090 workstation
---

# Local AI Model Runner & Acceleration Profile

## Hardware and Storage
- Load the skill `ai-workstation` first: it has the CPU, RAM and GPU, the checks before big jobs, the storage folders
  under `D:\AI` (models, `HF_HOME`, `OLLAMA_MODELS`, `TORCH_HOME`; never models or datasets on `C:`), and the Python
  environment rules.
- Extra details for model work: board ASUS ROG Zenith II Extreme Alpha; RAM is quad-channel; the RTX 3090 has
  GDDR6X memory and Compute Capability 8.6.

## Model Sizing & Placement Heuristics

1. **Fully GPU-Resident (Up to 32B Parameters)**:
   - **Target**: Models up to 32B in 4-bit quantization (e.g., 7B, 14B, 27B, 32B Q4_K_M or AWQ). A full-size 32B FP16 model exceeds 24 GB VRAM and will not fit.
   - **Engine**: Ollama or llama.cpp (--n-gpu-layers 99) natively on Windows; vLLM requires Linux/WSL.
   - **Constraint**: Maintain at least 1.5 GB free VRAM for context window KV caches.
   - **Context Window**: Leverage FlashAttention-2 where supported.

2. **Split Offloading & High-Capacity Inference (70B+ Parameters)**:
   - **Target**: 70B, 72B, or MoE models (e.g., Mixtral 8x7B, Llama-3-70B, Qwen-2.5-72B).
   - **Quantization**: Standardize on GGUF `Q4_K_M` or `Q5_K_M`.
   - **Offloading**: Offload ~20–30 layers to the RTX 3090 (fill ~20 GB VRAM) and offload the remaining layers to the 128 GB system RAM.
   - **CPU Threading**: Test thread scaling (typically 32 to 64 threads) in llama.cpp to utilize Threadripper compute without causing cache thrashing.

## Multi-Threaded Local Compute Conventions
- When writing Python or C++ scripts for data processing or inference batching, explicitly configure thread pool scaling:
  ```python
  import os
  import torch

  # Utilize Threadripper cores effectively
  torch.set_num_threads(32)  # Start at 32; test 32 to 64 and keep the fastest
  torch.set_num_interop_threads(16)
  ```
- Use native Windows CUDA device indexing (`CUDA_VISIBLE_DEVICES="0"`).
