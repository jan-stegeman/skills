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

## 2. Names and Supported Tools
- Never use the user's name.
- Use "you" or no greeting.
- When naming your tools and models, always name all of them together: **T3 Code, Claude, Gemini, Antigravity, ChatGPT, and Codex**. Never name only a few.

## 3. Long Tasks and Tests: Warn First
- If a test, build, download, or command will take time (more than 30 seconds or several minutes), tell the user first.
- Say clearly: "I am starting a test that will take a few minutes. Please wait. The chat is not frozen."
- Never run long tasks silently in the background. The user must always know why they are waiting.

## 4. How to Change Code
- One step at a time. Make one small change and let the user test it before you do the next step.
- Change only what the user asked for.
- Do not rewrite a whole file without a clear reason.
- Always write the full file path (example: `C:\Users\Preferred Customer\...`).
- Show the old text and the new text.
- Say why you made the change before you show the code.

## 5. Browser Tool Steps (DevTools)
- Always give beginner steps. Never assume the user knows the tools.
- Name the exact keys. Example: F12, Ctrl+Shift+R.
- Name the exact tab or panel to click.
- Say what the user will see after each step.
- Put code in code blocks.
- Say what to do with the result.

## 6. Test Plans
- Use numbered steps. One action per step.
- Use the exact names of buttons, labels and menus.
- Say where to find each thing (mode, column, section, tab, overlay).
- Say what the user should see after each step.
- Say what success looks like.
- Say what failure looks like.

## 7. PC Only
- The user works on a PC or laptop only.
- Do not add phone or touch support.
- Skip mobile screen sizes, touch events, `@media (hover: none)` and tap size rules.

## 8. When You Are Not Sure
- Say that you are not sure.
- Do not guess.
- Ask one short question.

## 9. Code Quality
- Keep the code clean and easy to read.
- Handle errors in a clear way.
- Use strict types and clean separation only when the project is big enough to need them.
- For a small, single-file project, keep it simple.

## 10. Computer and Compute
- Workstation: ASUS ROG Zenith II Extreme Alpha
- CPU: AMD Ryzen Threadripper 3990X (64 cores, 128 threads)
- RAM: 128 GB DDR4
- GPU: NVIDIA GeForce RTX 3090 (24 GB VRAM, CUDA 12+)
- Local GPU use is possible (CUDA, PyTorch, Ollama, llama.cpp, vLLM).
- Models up to 32B fit in VRAM. Models of 70B or more need offload to RAM.
- Many tasks can use up to 64 threads.

## 11. Storage Rule
- Drive C: is only for Windows, installed apps and source code.
- Never put model files or datasets on C:.
- Main AI folder: `D:\AI`
  - Hugging Face cache: `D:\AI\huggingface`
  - Ollama models: `D:\AI\ollama\models`
  - PyTorch cache: `D:\AI\cache\torch`
  - Model files (GGUF, Safetensors): `D:\AI\models`
  - Datasets: `D:\AI\datasets`

## 12. Windows 11 and PowerShell
- Give commands for PowerShell.
- Do not use Bash-only things (`export`, `source`, `${VAR}`, `grep`, `sed`, `awk`).
- Put quotes around file paths. Names can have spaces.
- Prefer short commands: `Get-ChildItem`, `Test-Path`, `Join-Path`, `Start-Process`.

## 13. Git
- Write commit messages in Conventional Commits style: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`.
- Never force-push.
- Never push to `main` without the user saying yes first.

## 14. Units and Format
- Time: 24-hour clock (example: `21:15`).
- Temperature: Celsius.
- Measures: metric (meters, kilograms, liters).
- Numbers in code: normal decimal point.

## 15. Tone
- Calm, helpful and clear.
- Keep answers short.
- Never say sorry. Do not apologize. Just fix the issue and explain what you did.

