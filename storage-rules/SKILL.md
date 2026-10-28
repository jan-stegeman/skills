---
name: storage-rules
description: Rules for disk locations, model caches, large datasets, and AI storage paths on Windows 11
---

# Storage & AI Cache Rules

## Drive Conventions
- **Primary OS Drive (`C:`)**: Reserved for system files, applications, and source code checkouts. Never download large AI model weights, checkpoints, or bulk datasets to `C:`.
- **Dedicated AI Data Root**: Use `D:\AI` (on the DATA drive) for all large AI workloads, weights, caches, and datasets.

## Standard Directory Structure
When generating scripts, configuration files, or docker mounts for AI workloads, adhere to this structure:
- **Hugging Face Cache**: `D:\AI\huggingface` (`HF_HOME=D:\AI\huggingface`)
- **Ollama Models**: `D:\AI\ollama\models` (`OLLAMA_MODELS=D:\AI\ollama\models`)
- **PyTorch / TorchInductor Cache**: `D:\AI\cache\torch`
- **Model Checkpoints & Weights (GGUF, Safetensors)**: `D:\AI\models`
- **Datasets**: `D:\AI\datasets`

## Environment & Script Guidelines
- When writing Python or PowerShell scripts that download weights or datasets:
  - Explicitly set `cache_dir="D:/AI/huggingface"` or configure the `HF_HOME` environment variable.
  - Do not use default `~/.cache` paths on Windows without pointing them to `D:\AI`.
