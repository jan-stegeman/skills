---
name: ai-workstation
description: "Hardware, storage and Python rules for AI work on this Windows 11 PC (Threadripper 3990X, 128 GB RAM, RTX 3090 24 GB): where models, caches, environments and temp files go (D:\\AI), checks before big jobs, and uv environments. Load before GPU or model work, downloads, big jobs, installing Python packages, or making an environment. Rules 14, 15 and 17 of user-preferences until 2026-11-15."
metadata:
  version: "2026-11-15.1"
---

# AI Workstation

These were rules 14, 15 and 17 of `user-preferences` until 2026-11-15, moved word for word to keep that file under
1,500 words. All rules of `user-preferences` still hold, such as rule 8 (approval for permanent settings).

## 1. Computer and Compute
- CPU: AMD Ryzen Threadripper 3990X (64 cores, 128 threads; measure, do not assume all threads is best). RAM: 128 GB DDR4. GPU: NVIDIA RTX 3090, 24 GB VRAM.
- Use FP16 or BF16 when the tool supports it. Do not suggest FP8 settings.
- A 32B Q4 model may fit for inference; larger models may need slower RAM offload.
- Before big work, check free RAM, disk space and VRAM (`nvidia-smi`); leave room for Windows. Start with a small trial; no two big GPU jobs together. Bind local AI servers to `127.0.0.1`. Save long run outputs to `D:\AI\logs`. Warn if Windows sleep could stop a long job.
- The CUDA number in `nvidia-smi` is driver support, not proof of an installed toolkit.
- Official vLLM needs Linux (WSL). Prefer native Windows tools; get approval before adding WSL.

## 2. Storage Rule
- C: is for Windows, apps, and their required settings. Put new source projects on D:. Do not move existing projects without approval.
- Keep AI data under `D:\AI`:
  - `HF_HOME`: `D:\AI\huggingface`
  - `OLLAMA_MODELS`: `D:\AI\ollama\models`
  - `TORCH_HOME`: `D:\AI\cache\torch`
  - `PIP_CACHE_DIR`: `D:\AI\cache\pip`
  - `UV_CACHE_DIR`: `D:\AI\cache\uv`; `UV_PYTHON_INSTALL_DIR`: `D:\AI\uv\python`
  - Models: `D:\AI\models`; datasets: `D:\AI\datasets`
  - Environments: `D:\AI\envs\<project-name>`; temp: `D:\AI\temp`
- Before big jobs, check folders exist, are writable, and have room.
- Set `TEMP`, `TMP`, and `TMPDIR` to `D:\AI\temp` in the session starting the job.
- Keep Docker and WSL data on D: if used.
- Read [Windows AI setup](references/windows-ai-setup.md) for setup commands.

## 3. Python and AI Tools
- Use one environment per project under `D:\AI\envs`. Never install AI packages into the main Python.
- Always use `uv`, pointed at the project environment: `uv pip install --python "D:\AI\envs\<project>\Scripts\python.exe" ...` (or `$env:UV_PROJECT_ENVIRONMENT` for `uv run`). Call that `python.exe` directly, without activation.
- Use `if __name__ == "__main__":` for multi-worker Python scripts on Windows.
- Install CUDA PyTorch with `uv pip` from the official PyTorch wheel index; check `torch.cuda.is_available()` there.
- Save package versions with `uv pip freeze` so the setup can be rebuilt.
