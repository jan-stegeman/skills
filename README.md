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
| [**`desktop-ui-check`**](desktop-ui-check/SKILL.md) | Read-only review of a Windows desktop program: wording, measured colour contrast, keyboard use, screen states, and a check per release. |

---

## Productivity & Tool Skills

| Category | Skills |
| :--- | :--- |
| **Office Documents** | [**`docx`**](docx/SKILL.md), [**`xlsx`**](xlsx/SKILL.md), [**`pptx`**](pptx/SKILL.md), [**`pdf`**](pdf/SKILL.md) |
| **Research & Web** | [**`deep-research`**](deep-research/SKILL.md), [**`chrome-browser`**](chrome-browser/SKILL.md), [**`built-in-browser`**](built-in-browser/SKILL.md) |
| **Agents & Automation** | [**`google-workspace`**](google-workspace/SKILL.md), [**`computer-use`**](computer-use/SKILL.md), [**`artifact-emulator`**](artifact-emulator/SKILL.md), [**`imagegen`**](imagegen/SKILL.md) |
| **Meta Tools** | [**`skill-creator`**](skill-creator/SKILL.md), [**`skill-installer`**](skill-installer/SKILL.md), [**`review-agent`**](review-agent/SKILL.md), [**`import-memory`**](import-memory/SKILL.md), [**`morning`**](morning/SKILL.md) |

---

## Third-Party Skills (unchanged copies, checked before install)

Copied as they are, with their own license file in the folder. Checked with NVIDIA SkillSpector 2.12.0 (`--no-llm`, `D:\AI\envs\skillspector`) and read by hand before install. `obsidian-bases` is 1,776 words, above the 1,500-word limit of these rules: a deliberate exception, so that it stays the same as its source and easy to update.

| Skill | Description | Source and check |
| :--- | :--- | :--- |
| [**`obsidian-bases`**](obsidian-bases/SKILL.md) | Obsidian Bases (`.base` files): views, filters, formulas, summaries. | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) `3ccff53`, MIT (Steph Ango). SkillSpector: CAUTION only because its parser could not resolve the function list in `references/FUNCTIONS_REFERENCE.md`; read by hand: a list of Bases formula functions, nothing that runs. |
| [**`obsidian-markdown`**](obsidian-markdown/SKILL.md) | Obsidian Flavored Markdown: wikilinks, embeds, callouts, properties. | Same source and commit. SkillSpector: SAFE, no findings. |
| [**`json-canvas`**](json-canvas/SKILL.md) | JSON Canvas (`.canvas` files): nodes, edges, groups. | Same source and commit. SkillSpector: SAFE, no findings. |

Not taken from the same repository: `knap` and `defuddle` (they install global npm tools and fetch web pages) and `obsidian-cli` (runs JavaScript inside Obsidian and copies to the clipboard).

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
