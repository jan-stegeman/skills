---
name: user-preferences
description: Global user preferences for language (simple English & Dutch), didactic explanations, hardware profile, Windows 11 PowerShell rules, and formatting standards
---

# User Preferences & Communication Profile

## Language & Communication
- **Primary Language (Plain, Simple English)**:
  - English is the default language for all interactions, conversations, code, commit messages, and documentation.
  - **Clarity & Simplicity**: Write in clear, straightforward, and easy-to-read English. Avoid dense academic jargon, overly complex sentence structures, or unnecessary fluff.
  - **Executive Summary First**: Start responses with a concise 1–2 sentence high-level summary so the user immediately understands what is happening before diving into technical details.
- **Bilingual Flexibility (Nederlands / Dutch)**:
  - The user is bilingual (English and Nederlands).
  - When explicitly addressed in Dutch, seamlessly mirror and reply in natural, clear Dutch.
  - When explaining complex architectural or technical trade-offs, feel free to provide Dutch translations or summaries if requested.

## Code & Explanation Style
- **Didactic & Step-by-Step**:
  - Break complex problems down into logical, easy-to-follow steps.
  - Explain the *why* behind architectural patterns and non-obvious choices before presenting code.
  - Provide self-contained, working walkthroughs rather than dumping uncontextualized code blocks.
- **Code Quality**:
  - Emphasize type safety, clean separation of concerns, and robust error handling.

## Hardware & Local Compute Profile
- **Workstation**: ASUS ROG Zenith II Extreme Alpha
- **CPU**: AMD Ryzen Threadripper 3990X (64 Cores / 128 Logical Processors)
- **RAM**: 128 GB Quad-Channel DDR4
- **GPU**: NVIDIA GeForce RTX 3090 (24 GB GDDR6X VRAM, Ampere, Compute Capability 8.6, CUDA 12+)
- **Compute Context**:
  - Full local GPU acceleration available (CUDA, PyTorch, Ollama, llama.cpp, vLLM).
  - Can host local models up to 32B fully in VRAM, or 70B+ with split offloading to system RAM.
  - Highly parallel execution capacity (scale compilation and batch workloads to 64 threads where appropriate).

## Storage Invariant
- **Drive C: Invariant**: Reserved strictly for the Windows OS, installed applications, and source checkouts. Never download weights, checkpoints, or datasets onto `C:`.
- **Dedicated AI Root (`D:\AI`)**:
  - Hugging Face cache: `D:\AI\huggingface`
  - Ollama models: `D:\AI\ollama\models`
  - PyTorch / Inductor cache: `D:\AI\cache\torch`
  - Model weights (GGUF, Safetensors): `D:\AI\models`
  - Datasets: `D:\AI\datasets`

## Operating System & Terminal (Windows 11 / PowerShell)
- **PowerShell Native**: The primary environment is Windows 11 using PowerShell.
- Provide commands formatted for PowerShell:
  - Avoid Bash-only constructs (`export`, `source`, Bash variable substitution `${VAR}`, `grep`/`sed`/`awk`).
  - Always quote file paths defensively to handle spaces in usernames (`C:\Users\Preferred Customer`).
  - Prefer concise, robust PowerShell commands (`Get-ChildItem`, `Test-Path`, `Join-Path`, `Start-Process`).

## Git & Workflow Conventions
- **Commit Messages**: Strictly follow Conventional Commits (`feat: ...`, `fix: ...`, `refactor: ...`, `docs: ...`, `chore: ...`).
- **Safety First**: Do not force-push or push directly to `main` without explicit confirmation.

## Units & Formatting Standards
- Adhere to European / Metric standards:
  - **Time Format**: 24-hour notation (e.g. `14:30`, `21:15` instead of AM/PM).
  - **Temperature**: Degrees Celsius (°C).
  - **Measurement Units**: Metric system (meters, kilograms, liters).
  - **Number Formatting**: Standard decimal points in code, formulas, and configurations.

## Style & Tone
- Maintain a helpful, calm, actionable, and structured tone. Keep explanations accessible and easy to digest.
