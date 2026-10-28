# AI Agent Skills Repository

Central repository of Agent Skills, user preferences, and hardware-accelerated profiles for **T3 Code, Claude, Antigravity, Gemini, and OpenAI (ChatGPT/Codex)**.

---

## Core Workstation & Governance Skills

| Skill | Description |
| :--- | :--- |
| [**`user-preferences`**](user-preferences/SKILL.md) | Communication profile (Plain English & Dutch mirroring), didactic explanations, hardware specifications, 24-hour time, and metric units. |
| [**`local-model-runner`**](local-model-runner/SKILL.md) | Sizing heuristics and acceleration strategies for local models (Ollama, vLLM, llama.cpp) on the AMD Threadripper 3990X and RTX 3090. |
| [**`git-worktree-flow`**](git-worktree-flow/SKILL.md) | Safe, non-blocking parallel workflows using Git worktrees and Conventional Commits. |
| [**`t3-orchestration-patterns`**](t3-orchestration-patterns/SKILL.md) | Multi-agent execution guidelines in T3 Code (subagents vs. delegates vs. background tasks). |
| [**`skill-maintenance`**](skill-maintenance/SKILL.md) | Automated lifecycle for creating, updating, and pushing skills directly to this GitHub repository. |

---

## Productivity & Tool Skills

| Category | Skills |
| :--- | :--- |
| **Office Documents** | [**`docx`**](docx/SKILL.md), [**`xlsx`**](xlsx/SKILL.md), [**`pptx`**](pptx/SKILL.md), [**`pdf`**](pdf/SKILL.md), [**`docs`**](docs/SKILL.md) |
| **Research & Web** | [**`deep-research`**](deep-research/SKILL.md), [**`chrome-browser`**](chrome-browser/SKILL.md), [**`built-in-browser`**](built-in-browser/SKILL.md) |
| **Agents & Automation** | [**`google-workspace`**](google-workspace/SKILL.md), [**`computer-use`**](computer-use/SKILL.md), [**`artifact-emulator`**](artifact-emulator/SKILL.md), [**`imagegen`**](imagegen/SKILL.md) |
| **Meta Tools** | [**`skill-creator`**](skill-creator/SKILL.md), [**`skill-installer`**](skill-installer/SKILL.md), [**`review-agent`**](review-agent/SKILL.md), [**`import-memory`**](import-memory/SKILL.md), [**`morning`**](morning/SKILL.md) |

---

## Workstation Profile

* **Host**: ASUS ROG Zenith II Extreme Alpha
* **Processor**: AMD Ryzen Threadripper 3990X (64 Cores / 128 Threads)
* **Memory**: 128 GB Quad-Channel DDR4
* **Graphics**: NVIDIA GeForce RTX 3090 (24 GB GDDR6X VRAM)
* **Dedicated AI Storage**: `D:\AI\`

---

## How It Works

This repository is cloned directly to `C:\Users\Preferred Customer\.agents\skills` on Windows 11. All local AI tools (T3 Code, Claude Desktop, Antigravity, Gemini, OpenAI) access these skills in real time via native Windows NTFS junctions with **zero background software**.
