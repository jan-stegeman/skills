# Windows AI Setup

Read this guide only when setting up an AI tool or checking its storage.
It is a guide, not an instruction to change settings on every task.
All commands use PowerShell 5.1 or 7. Run them in the same session unless stated otherwise.

## 1. Check before changing anything

Check space on both drives. Values below are in bytes:

```powershell
Get-PSDrive -Name 'C', 'D' | Select-Object Name, Used, Free
```

Allow room for the download, extracted files, conversion output, and saved results.
Do not move existing projects, models, Docker data, or WSL disks without approval.
Check the current and saved values before replacing any settings:

```powershell
$aiSettingNames = @(
    'HF_HOME', 'OLLAMA_MODELS', 'TORCH_HOME', 'PIP_CACHE_DIR',
    'UV_CACHE_DIR', 'TEMP', 'TMP', 'TMPDIR'
)
foreach ($settingName in $aiSettingNames) {
    [pscustomobject]@{
        Name = $settingName
        CurrentSession = [Environment]::GetEnvironmentVariable($settingName, 'Process')
        SavedForUser = [Environment]::GetEnvironmentVariable($settingName, 'User')
    }
}
```

A value being present does not prove it points to the right folder.

## 2. Set paths for the current AI job

Use these settings only as part of an approved AI setup or job.
They affect this PowerShell session and programs it starts, not all Windows apps.
This block creates the folders if needed. It does not move or delete files.

```powershell
if (-not (Test-Path -LiteralPath 'D:\')) {
    throw 'Drive D: is not available. Stop and check the storage.'
}

$aiPaths = [ordered]@{
    HF_HOME = 'D:\AI\huggingface'
    OLLAMA_MODELS = 'D:\AI\ollama\models'
    TORCH_HOME = 'D:\AI\cache\torch'
    PIP_CACHE_DIR = 'D:\AI\cache\pip'
    UV_CACHE_DIR = 'D:\AI\cache\uv'
    TEMP = 'D:\AI\temp'
    TMP = 'D:\AI\temp'
    TMPDIR = 'D:\AI\temp'
}

foreach ($setting in $aiPaths.GetEnumerator()) {
    New-Item -ItemType Directory -Path $setting.Value -Force -ErrorAction Stop | Out-Null
    Set-Item -Path ('Env:\' + $setting.Key) -Value $setting.Value -ErrorAction Stop
}

foreach ($folder in @('D:\AI\models', 'D:\AI\datasets', 'D:\AI\envs')) {
    New-Item -ItemType Directory -Path $folder -Force -ErrorAction Stop | Out-Null
}
```

Start the AI program from this session. An app already running will not gain these values.
For Python, set temp paths before starting Python; it can remember its temp choice.

## 3. Save cache paths only with approval

This is a permanent change to user environment settings and falls under rule 8.
Get approval for saving these paths before running the block.
Use the values from section 2. Leave Windows-wide temp settings alone.

```powershell
$cacheSettingNames = @(
    'HF_HOME', 'OLLAMA_MODELS', 'TORCH_HOME', 'PIP_CACHE_DIR', 'UV_CACHE_DIR'
)
foreach ($settingName in $cacheSettingNames) {
    $expectedPath = $aiPaths[$settingName]
    if ([string]::IsNullOrWhiteSpace($expectedPath)) {
        throw 'Run the approved session setup in section 2 first.'
    }
    [Environment]::SetEnvironmentVariable($settingName, $expectedPath, 'User')
}
```

Keep TEMP, TMP, and TMPDIR limited to the AI job's session.
After saving cache paths, fully restart the affected app and its terminal host.
For example, an old terminal inside an editor may still use old values.
Quit and reopen the Ollama tray app if its model path changed.
Check all values again inside the process that starts the job.
Do not assume a restart worked.

## 4. Check the project Python and GPU

Use the actual project's environment path. This example uses an environment named my-project.
Activation is optional. No execution policy change is needed for this direct call.

```powershell
$projectPython = 'D:\AI\envs\my-project\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    throw 'Choose the existing project environment Python path first.'
}

& $projectPython -c "import sys, tempfile; print(sys.executable); print(tempfile.gettempdir())"
if ($LASTEXITCODE -ne 0) {
    throw 'The Python path or temp check failed.'
}

nvidia-smi
if ($LASTEXITCODE -ne 0) {
    throw 'The NVIDIA check failed. Stop before GPU work.'
}
```

The Python path must be the chosen environment. Its temp path should be D:\AI\temp.
For a project using PyTorch on the GPU, also run:

```powershell
& $projectPython -c "import torch; available = torch.cuda.is_available(); print(available); print(torch.version.cuda); raise SystemExit(0 if available else 1)"
if ($LASTEXITCODE -ne 0) {
    throw 'The PyTorch GPU check failed.'
}
```

GPU availability must print True for that PyTorch GPU job.
Use the official PyTorch installer selector for a compatible Windows build.
A successful import alone does not prove GPU support.

Before a large job, run a small save or download test to check write access.
Then run a short model trial with the intended chat length and workload.
Check actual GPU memory and saved file paths. Stop if files go to the wrong drive.
Record the Python and package versions using that environment's Python.
A package list helps rebuild the setup but is not proof every package works.

## Official sources

Check current requirements when installing or changing software:

- [Windows processor groups](https://learn.microsoft.com/en-us/troubleshoot/windows-server/setup-upgrade-and-drivers/number-of-processors-environment-variable-show-incorrect-values)
- [PowerShell environment settings](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables)
- [Windows temp paths](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-gettemppathw)
- [Python temp paths](https://docs.python.org/3/library/tempfile.html)
- [Python environments](https://docs.python.org/3/library/venv.html#how-venvs-work)
- [NVIDIA driver and CUDA support](https://docs.nvidia.com/datacenter/tesla/drivers/latest/cuda-toolkit-driver-and-architecture-matrix.html)
- [vLLM platform requirements](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/)
- [Ollama chat length and memory](https://docs.ollama.com/context-length)
- [PyTorch install selector](https://pytorch.org/get-started/locally/)
