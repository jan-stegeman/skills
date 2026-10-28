---
name: user-preferences
description: Global user preferences for language, units, time formats, coding explanations, hardware specs, and environment rules
---

# User Preferences

## Language & Communication
- **Default Language**: English is the primary and default language for all interactions, conversations, code, commit messages, comments, and documentation.
- **Bilingual Flexibility**: When explicitly addressed in Dutch (Nederlands), mirror and respond in Dutch. If the prompt is ambiguous, purely code, or in English, default to English.

## Code & Explanation Style
- **Didactic & Step-by-Step**: When explaining or writing code, adopt a structured, educational approach:
  - Break problems down into logical steps.
  - Explain the *why* behind architectural choices, patterns, and non-obvious code decisions before or alongside the code.
  - Provide clear, self-contained walkthroughs rather than dumping uncontextualized code blocks.
- **Code Quality**: Emphasize type safety, clean separation of concerns, and robust error handling.

## Hardware & Local Compute Profile
- **Workstation**: ASUS ROG Zenith II Extreme Alpha
- **CPU**: AMD Ryzen Threadripper 3990X (64 Cores / 128 Logical Processors)
- **RAM**: 128 GB
- **GPU**: NVIDIA GeForce RTX 3090 (24 GB VRAM, Ampere, Compute Capability 8.6)
- **Compute Context**:
  - Full local GPU acceleration available (CUDA / PyTorch / Ollama / llama.cpp / vLLM).
  - Can host local models up to 32B fully in VRAM, or 70B+ with CPU/RAM offloading.
  - Highly parallel compilation and job execution (scale workloads to high thread counts where appropriate).

## Operating System & Terminal (Windows 11 / PowerShell)
- **PowerShell Native**: The primary environment is Windows 11 using PowerShell.
- Provide commands formatted for PowerShell:
  - Avoid Bash-only constructs (e.g., `export`, `source`, Bash variable substitution like `${VAR}`, or `grep`/`sed`/`awk`).
  - Use proper Windows path handling (forward slashes or quoted backslashes where needed).
  - Prefer concise, single-line PowerShell commands when running automated steps.

## Git & Workflow Conventions
- **Commit Messages**: Follow the Conventional Commits specification (e.g., `feat: ...`, `fix: ...`, `refactor: ...`, `docs: ...`).
- **Safety First**: Do not force-push or push directly to `main` / `master` without explicit user confirmation.

## Units & Formatting Standards
- Adhere to European / Metric standards:
  - **Time Format**: 24-hour notation (e.g., `14:30` instead of `2:30 PM`).
  - **Temperature**: Degrees Celsius (°C).
  - **Measurement Units**: Metric system (meters, kilometers, grams, kilograms, liters). Avoid imperial units unless explicitly requested.
  - **Number Formatting**: Standard decimal points in code, formulas, and configurations.

## Style & Tone
- Keep explanations structured, actionable, and free of unnecessary fluff or repetitive apologies.
