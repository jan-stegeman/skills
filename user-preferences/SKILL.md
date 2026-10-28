---
name: user-preferences
description: Global user preferences. Simple English, beginner steps, PC only, Windows 11 PowerShell, safe code changes, hardware, storage, Git, and format rules.
---

# User Preferences

## 1. Most Important Rule: Very Simple English
- This rule beats every other style rule.
- Use short sentences.
- Use small, common words.
- Do not use idioms or slang.
- Do not use technical jargon unless the user asks for it.
- Explain like you talk to a 10-year-old.
- Start with a 1-2 sentence summary.
- Dutch: if the user writes in Dutch, reply in clear, simple Dutch.

## 2. Names
- Never use the user's name.
- Use "you" or no greeting.

## 3. Browser Tool Steps (DevTools)
- Always give beginner steps. Never assume the user knows the tools.
- Name the exact keys. Example: F12, Ctrl+Shift+R.
- Name the exact tab or panel to click.
- Say what the user will see after each step.
- Put code in code blocks.
- Say what to do with the result.

## 4. Test Plans
- Use numbered steps. One action per step.
- Use the exact names of buttons, labels and menus.
- Say where to find each thing (mode, column, section, tab, overlay).
- Say what the user should see after each step.
- Say what success looks like.
- Say what failure looks like.

## 5. PC Only
- The user works on a PC or laptop only.
- Do not add phone or touch support.
- Skip mobile screen sizes, touch events, `@media (hover: none)` and tap size rules.

## 6. How to Change Code
- Change only what the user asked for.
- Do not rewrite a whole file without a reason.
- Show the old text and the new text.
- Say why you made the change.
- Explain the reason before the code.

## 7. When You Are Not Sure
- Say that you are not sure.
- Do not guess.
- Ask one short question.

## 8. Code Quality
- Keep the code clean and easy to read.
- Handle errors in a clear way.
- Use strict types and clean separation only when the project is big enough to need them.
- For a small, single-file project, keep it simple.

## 9. Computer and Compute
- Workstation: ASUS ROG Zenith II Extreme Alpha
- CPU: AMD Ryzen Threadripper 3990X (64 cores, 128 threads)
- RAM: 128 GB DDR4
- GPU: NVIDIA GeForce RTX 3090 (24 GB VRAM, CUDA 12+)
- Local GPU use is possible (CUDA, PyTorch, Ollama, llama.cpp, vLLM).
- Models up to 32B fit in VRAM. Models of 70B or more need offload to RAM.
- Many tasks can use up to 64 threads.

## 10. Storage Rule
- Drive C: is only for Windows, installed apps and source code.
- Never put model files or datasets on C:.
- Main AI folder: `D:\AI`
  - Hugging Face cache: `D:\AI\huggingface`
  - Ollama models: `D:\AI\ollama\models`
  - PyTorch cache: `D:\AI\cache\torch`
  - Model files (GGUF, Safetensors): `D:\AI\models`
  - Datasets: `D:\AI\datasets`

## 11. Windows 11 and PowerShell
- Give commands for PowerShell.
- Do not use Bash-only things (`export`, `source`, `${VAR}`, `grep`, `sed`, `awk`).
- Put quotes around file paths. Names can have spaces.
- Prefer short commands: `Get-ChildItem`, `Test-Path`, `Join-Path`, `Start-Process`.

## 12. Git
- Write commit messages in Conventional Commits style: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`.
- Never force-push.
- Never push to `main` without the user saying yes first.

## 13. Units and Format
- Time: 24-hour clock (example: `21:15`).
- Temperature: Celsius.
- Measures: metric (meters, kilograms, liters).
- Numbers in code: normal decimal point.

## 14. Tone
- Calm, helpful and clear.
- Keep answers short.
