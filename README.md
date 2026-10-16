English | [中文](README.zh-CN.md)

# 心迹漫游: Multi-Agent Emotional Dialogue System

A local Gradio 3 web app. The main panel is a chat window labeled **Agentbot**. From the side panel you can invite any of 16 MBTI personality agents, or build one custom agent. Voice input and the face camera sit near the input box. They are optional add-ons, not required for text chat.

After startup the terminal prints a local URL. The port is random by default because `WEB_PORT = -1` in `config.py`.

Most on-screen labels are still Chinese. This guide gives the English meaning next to each label you need to click.

This repository is a cleaned public copy:

- API keys are not stored in source. They are read from environment variables.
- No local proxy is used unless you set `proxies` in `config.py`.
- Point agent calls at your own OpenAI-compatible gateway with `OPENAI_BASE_URL`. If you leave it unset, the app still uses the original project gateway, `https://api.xiaoai.plus/v1`.

The install steps below follow the import chain that `main.py` actually loads. They have not been re-checked on a brand-new machine. If `pip` or startup reports a missing module, install the package named in the error.

## Requirements

- OS: Windows, macOS, or Linux. The first command block is Windows PowerShell. A bash block follows.
- Python: 3.9 or a newer 3.x. The comment in `main.py` says the same.
- Network access to the chat gateway you configure. The original gateway is a third-party compatible endpoint used by the 2024 project. It may no longer be available.

## Install

Open a terminal in this directory (the directory that contains `main.py`).

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```

bash:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

`requirements.txt` pins Gradio 3. The UI uses Gradio 3 APIs: `gr.Chatbot.postprocess`, `.queue(concurrency_count=...)`, and `.style()`. Do not install Gradio 4 or 5.

The text-chat path uses `gradio`, `openai`, `pyautogen`, `requests`, `numpy`, `scipy`, `matplotlib`, `tiktoken`, `markdown`, `pymdown-extensions`, and `latex2mathml`.

## Configure keys

Copy the example file and fill it in. Do not commit a filled-in `.env`:

```powershell
Copy-Item .env.example .env
```

```bash
cp .env.example .env
```

`.env.example` contains:

```text
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.xiaoai.plus/v1
ALIYUN_TOKEN=
ALIYUN_APPKEY=
```

This program does not load `.env` by itself. Export the variables in the same terminal before you start it.

PowerShell:

```powershell
$env:OPENAI_API_KEY = "replace-with-your-key"
# Change the next line only if that gateway is down. Stop at /v1. Do not append /chat/completions.
$env:OPENAI_BASE_URL = "https://api.xiaoai.plus/v1"
python main.py
```

Command Prompt:

```bat
set OPENAI_API_KEY=replace-with-your-key
set OPENAI_BASE_URL=https://api.xiaoai.plus/v1
python main.py
```

bash:

```bash
export OPENAI_API_KEY="replace-with-your-key"
export OPENAI_BASE_URL="https://api.xiaoai.plus/v1"
python main.py
```

| Variable | Used by | If empty |
| --- | --- | --- |
| `OPENAI_API_KEY` | Normal chat, the 16 MBTI agents, the custom agent, and the emotion assistant | The page still opens. The first message or agent click fails because the key is empty. |
| `OPENAI_BASE_URL` | Same callers. OpenAI-compatible API root. | Defaults to `https://api.xiaoai.plus/v1`. |
| `ALIYUN_TOKEN` | Aliyun real-time speech, `crazy_functions/live_audio/aliyunASR.py` | Affects voice only. Text chat does not need it. |
| `ALIYUN_APPKEY` | Same as above | Affects voice only. |

Keep keys in environment variables or a local `.env`. Do not write them back into `config.py` or into files under `crazy_functions/personality_agents/`.

Two related settings in `config.py`:

- `API_KEY` reads `OPENAI_API_KEY`. Normal chat goes through `API_URL_REDIRECT` in `request_llms/bridge_all.py`, which rewrites the official OpenAI chat URL to `OPENAI_BASE_URL`.
- `proxies = None`. If you must use a local proxy, set a dict, for example `{"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}`. The old hardcoded `127.0.0.1:8001` proxy was removed so requests do not fail when no proxy is running.

Model names are still set inside each agent file, so the original call sites stay intact. Every agent file reads `OPENAI_API_KEY` and `OPENAI_BASE_URL`. The names currently in effect:

- INFJ and ESTP: `gpt-4o`
- The other personality files, and `crazy_functions/auto_gen.py`: `gpt-3.5-turbo-16k-0613`
- `crazy_functions/self_agent.py` and the face-emotion assistant: `gpt-3.5-turbo-16k`

To change a model, edit `model` inside that file's `config_list`, and confirm the gateway actually serves that name.

To pin the port, edit `WEB_PORT` in `config.py`. `-1` means pick a free port on every launch.

## Start

From the directory that contains `main.py`:

```powershell
python main.py
```

The terminal prints a URL and tries to open a browser. The message is Chinese and looks like this:

```text
如果浏览器没有自动打开，请复制并转到以下URL：
    「暗色主题已启用（支持动态切换主题）」: http://localhost:<port>
```

Use the URL printed in the terminal. The server listens on `0.0.0.0`, so on the same machine `localhost` is enough. Chat logs are written to `gpt_log/chat_secrets.log`. That directory is listed in `.gitignore`.

`main.py` starts with `matplotlib.use('TkAgg')`. If startup fails on the matplotlib backend, change that line to `matplotlib.use('Agg')` and start again. That change affects matplotlib only.

Stop the program with Ctrl+C in the terminal.

## Using the page

The layout is left-right (`LAYOUT = "LEFT-RIGHT"`). The center chat window is labeled **Agentbot**. The page title is **多智能体情感对话系统**.

1. Pick a group in the plugin dropdown. The default groups come from `DEFAULT_FN_GROUPS` in `config.py`: `Analysts`, `Diplomats`, `Sentinels`, `Explorers`, and `自定义` (Custom).
2. Click a personality button. That agent sends a short introduction and joins the current chat. Personas live in `crazy_functions/personality_agents/agents_profiles.json`.
3. Type in the input box. The placeholder says: Enter to send, Shift+Enter for a new line. You can also click **提交** (Submit).
4. **重置** (Reset) clears the current input-related state. **停止** (Stop) interrupts a reply in progress. **新建会话** (New session) is on the session side.
5. Under the input box are **发送语音** (Send voice) and **面部情绪识别** (Face emotion), plus a microphone widget. See the next section.
6. Open the collapsed **自定义 Agent** (Custom Agent) panel. Four sliders set E/I, S/N, T/F, and J/P. Their labels are `外向(E)-内向(I)`, `感觉(S)-直觉(N)`, `思考(T)-情感(F)`, and `判断(J)-知觉(P)`. Type a name in **名字**, click **专属智能体生成** (Generate custom agent), then click the **专属智能体** button to add that agent to the chat.

Personality groups:

| Group | Buttons |
| --- | --- |
| Diplomats | INFJ, INFP, ENFJ, ENFP |
| Analysts | INTJ, INTP, ENTJ, ENTP |
| Sentinels | ISTJ, ISFJ, ESTJ, ESFJ |
| Explorers | ISTP, ISFP, ESTP, ESFP |
| 自定义 (Custom) | 发送语音 (Send voice), 专属智能体 (Custom agent), 面部情绪识别 (Face emotion) |

The button table is `get_crazy_functions()` in `crazy_functional.py`.

## Voice, face, and text emotion

None of these three is required to open the page. Text chat still works when the weights or system libraries are incomplete.

Voice:

- The microphone widget appears when `ENABLE_AUDIO = True`.
- Recognition goes through Aliyun and needs `ALIYUN_TOKEN` and `ALIYUN_APPKEY`.
- Entry points: `crazy_functions/语音助手.py` and `crazy_functions/live_audio/aliyunASR.py`.

Face:

- The page includes a webcam widget. A source comment says the video stream still has problems and is only there for testing.
- The model is mini-XCEPTION. Weights are at `crazy_functions/emo_agent/face_agent/models/_mini_XCEPTION.102-0.64.hdf5`.
- The code expects Keras / TensorFlow-style `keras`, plus `opencv-python` (`cv2`) and `imutils`. Those packages are not in `requirements.txt`.

Speech-emotion models:

- Weights are in `crazy_functions/emo_agent/audio_agent/checkpoints/`, with one LSTM for OpenSMILE and one for librosa.
- Feature extraction uses `librosa` and `pandas`, and `SMILExtract.exe` in the same tree (an OpenSMILE executable for Windows).

Text emotion:

- Code is in `crazy_functions/emo_agent/txt_agent/` and depends on PyTorch and fairseq.
- The large weights are not in this repository. Download notes, including Quark Netdisk links, are in that directory's `README.md`. Quark is a Chinese file host, so the links may require a Quark account.

| File | Link |
| --- | --- |
| Text-emotion `best_model.pth` | https://pan.quark.cn/s/30598ca731be |
| Pretrained RoBERTa `checkpoint_best.pt` | https://pan.quark.cn/s/8312fd012876 |
| Pretrained COMET `atomic_pretrained_model.pickle` and related files | https://pan.quark.cn/s/c1199a6656b5 |

Install optional packages only for the feature you actually click, for example:

```powershell
python -m pip install opencv-python imutils librosa pandas torch
```

TensorFlow/Keras and fairseq are tied tightly to the 2024 weights. This guide does not invent version pins that have not been verified.

## Layout

```text
main.py                 Starts Gradio and prints the local URL
config.py               Port, model list, keys, and gateway (environment variables only)
core_functional.py      Basic function buttons
crazy_functional.py     Button table for the 16 personalities plus voice, face, and custom agent
toolbox.py              Config loading, UI refresh, file upload
request_llms/           Normal chat requests. bridge_all.py rewrites the URL; bridge_chatgpt.py sends the request
crazy_functions/
  personality_agents/   One file per MBTI type. Personas are in agents_profiles.json
  self_agent.py         Custom agent
  auto_gen.py           Emotion-recognition assistant used during chat
  语音助手.py            Voice button
  emo_agent/            Local speech, face, and text emotion models
  live_audio/           Microphone buffer and Aliyun recognition
themes/                 UI themes and front-end scripts
shared_utils/           Markdown, uploads, config loading
docs/logo.png           Page icon
```

Directories created at runtime and ignored by git:

- `gpt_log/`: chat logs
- `private_upload/`: uploaded files
- `flagged/`: Gradio flag records
- `.cache/`, `__pycache__/`, `.idea/`

## Troubleshooting

`ModuleNotFoundError` at startup: install the missing module with `python -m pip install` inside the active virtual environment. Packages for the text-chat path are already in `requirements.txt`.

The page opens, but an agent click fails: confirm `OPENAI_API_KEY` is non-empty in this terminal, then confirm `OPENAI_BASE_URL` points at a live compatible gateway that serves the model name in that file's `config_list`.

The browser does not open: use the `http://localhost:<port>` line printed in the terminal. The port can change every launch.

Requests time out: check whether this machine must use a proxy. Timeout and retry live in `config.py` as `TIMEOUT_SECONDS` (30) and `MAX_RETRY` (2).

Voice returns nothing: text chat does not depend on voice. Check the two Aliyun environment variables and the microphone permission.

## Do not commit

`.gitignore` already excludes `.env`, `config_private.py`, `OAI_CONFIG_LIST`, logs, and the upload directory. Before a commit, search the source again and confirm there is no key that starts with `sk-`.
