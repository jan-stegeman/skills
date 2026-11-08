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

## Third-Party Skills (checked before install)

Copied as they are, with their own license file in the folder, unless the table says *changed*. Checked with NVIDIA SkillSpector 2.12.0 (`--no-llm`, `D:\AI\envs\skillspector`) and read by hand before install. `obsidian-bases` (1,776 words) and `diagram-design` (4,231 words) are above the 1,500-word limit of these rules: deliberate exceptions, so that they stay the same as their source and easy to update.

| Skill | Description | Source and check |
| :--- | :--- | :--- |
| [**`obsidian-bases`**](obsidian-bases/SKILL.md) | Obsidian Bases (`.base` files): views, filters, formulas, summaries. | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) `3ccff53`, MIT (Steph Ango). SkillSpector: CAUTION only because its parser could not resolve the function list in `references/FUNCTIONS_REFERENCE.md`; read by hand: a list of Bases formula functions, nothing that runs. |
| [**`obsidian-markdown`**](obsidian-markdown/SKILL.md) | Obsidian Flavored Markdown: wikilinks, embeds, callouts, properties. | Same source and commit. SkillSpector: SAFE, no findings. |
| [**`json-canvas`**](json-canvas/SKILL.md) | JSON Canvas (`.canvas` files): nodes, edges, groups. | Same source and commit. SkillSpector: SAFE, no findings. |
| [**`context7-mcp`**](context7-mcp/SKILL.md) | When to fetch current library documentation through the Context7 MCP server. | [upstash/context7](https://github.com/upstash/context7) `078c0c7`, MIT (Upstash). SkillSpector: SAFE, no findings. Needs the MCP server: in Claude added as the remote `https://mcp.context7.com/mcp` (user scope, no API key, nothing runs locally); only a library name and the question go online. |
| [**`simple-english`**](simple-english/SKILL.md) | Plain, ASD-STE100-style English for documents: short sentences, active voice, one word one meaning. | [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) `a6fcb4f`, MIT (AminBlg). **Changed:** its rules for every chat reply (prose only, no lists, headings, bold or tables) are removed, so it shapes documents only; a note in the file says so. SkillSpector: SAFE, no findings, before and after the change. |
| [**`diagram-design`**](diagram-design/SKILL.md) | Diagrams of many kinds as self-contained HTML/SVG (PNG with Playwright), with draw.io, Mermaid and Excalidraw import. | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) `e57eda6`, MIT (Cathryn Lavery). SkillSpector: 100/100 only from false alarms (HTML comments and diagram text in the examples), read by hand; its scripts use the Python standard library only. Diagrams load Google Fonts by default; profiles go to `~/.diagram-design`; PNG export needs Playwright, not installed here. |

Not taken from kepano/obsidian-skills: `knap` and `defuddle` (they install global npm tools and fetch web pages) and `obsidian-cli` (runs JavaScript inside Obsidian and copies to the clipboard). Not taken from upstash/context7: `find-docs` and `context7-cli` (they run the unpinned npm tool `npx ctx7`).

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
