# 心迹漫游：多智能体情感对话系统

这是一个基于 Gradio 3 的本地网页程序。主界面是一个名为 Agentbot 的对话窗。侧边可以按 MBTI 分组邀请 16 个性格智能体，也可以生成一个专属智能体。语音输入和面部画面入口在输入区附近，属于附加功能。

程序启动后会在终端打印本机地址。默认端口是随机的，因为 `config.py` 里 `WEB_PORT = -1`。

本仓库是整理过的公开副本：

- 模型密钥不再写在源码里，只从环境变量读取。
- 默认不走本机代理。需要代理时再在 `config.py` 里设置 `proxies`。
- 智能体的接口地址可以用 `OPENAI_BASE_URL` 换成你自己的 OpenAI 兼容网关。不设置时仍使用原项目的 `https://api.xiaoai.plus/v1`。

下面的安装步骤是按源码的启动导入链整理的。这次整理没有在一台全新环境里把界面跑通，所以如果 `pip` 或启动报缺包，按报错里的模块名补装即可。

## 环境

- 操作系统：Windows、macOS、Linux 都可以。下面的命令按 Windows PowerShell 来写。
- Python：3.9 或更新的 3.x。`main.py` 里的注释也是这个建议。
- 能访问你配置的对话网关。原网关是 2024 年项目用的第三方兼容地址，现在不一定还能用。

## 安装

在本目录（含有 `main.py` 的目录）打开终端：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
```

`requirements.txt` 锁在 Gradio 3，因为界面用了 Gradio 3 的写法：`gr.Chatbot.postprocess`、`.queue(concurrency_count=...)`、`.style()`。不要装 Gradio 4 或 5。

对话主路径会用到这些包：`gradio`、`openai`、`pyautogen`、`requests`、`numpy`、`scipy`、`matplotlib`、`tiktoken`、`markdown`、`pymdown-extensions`、`latex2mathml`。

## 配置密钥

复制示例文件再填写，不要把填好的 `.env` 提交到仓库：

```powershell
Copy-Item .env.example .env
```

`.env.example` 的内容是：

```text
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.xiaoai.plus/v1
ALIYUN_TOKEN=
ALIYUN_APPKEY=
```

这个程序不会自动读取 `.env`。启动前要在当前终端里设环境变量。PowerShell：

```powershell
$env:OPENAI_API_KEY = "这里换成你的密钥"
# 网关不可用时再改下一行。只写到 /v1，不要再加 /chat/completions
$env:OPENAI_BASE_URL = "https://api.xiaoai.plus/v1"
python main.py
```

命令提示符：

```bat
set OPENAI_API_KEY=这里换成你的密钥
set OPENAI_BASE_URL=https://api.xiaoai.plus/v1
python main.py
```

变量说明：

| 变量 | 谁在用 | 不填会怎样 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 普通对话，以及 16 个 MBTI 智能体、专属智能体、情绪识别助理 | 能打开网页，一发消息或一点智能体就会因空密钥失败 |
| `OPENAI_BASE_URL` | 同上，OpenAI 兼容根地址 | 默认 `https://api.xiaoai.plus/v1` |
| `ALIYUN_TOKEN` | 阿里云实时语音，`crazy_functions/live_audio/aliyunASR.py` | 只影响语音。文字对话不需要 |
| `ALIYUN_APPKEY` | 同上 | 只影响语音 |

密钥只放在环境变量或本机 `.env` 里。不要写回 `config.py`，也不要写进 `crazy_functions/personality_agents/` 下的文件。

`config.py` 里这两处和密钥相关：

- `API_KEY` 读取 `OPENAI_API_KEY`。普通对话经 `request_llms/bridge_all.py` 的 `API_URL_REDIRECT`，把 OpenAI 官方聊天地址改到 `OPENAI_BASE_URL`。
- `proxies = None`。如果你必须走本地代理，再改成字典，例如 `{"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}`。原先写死的 `127.0.0.1:8001` 已去掉，避免没开代理时请求直接失败。

各智能体文件里的模型名没有收成同一个函数，避免改动原来的调用。它们都读 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`。当前文件里生效的模型名是：INFJ、ESTP 为 `gpt-4o`；其余性格文件和 `crazy_functions/auto_gen.py` 为 `gpt-3.5-turbo-16k-0613`；`crazy_functions/self_agent.py` 与面部情绪识别助理为 `gpt-3.5-turbo-16k`。要换模型，改对应文件 `config_list` 里的 `model`，并确认网关提供这个名字。

固定端口可以改 `config.py` 的 `WEB_PORT`。`-1` 表示每次启动找一个空闲端口。

## 启动

仍在含有 `main.py` 的目录：

```powershell
python main.py
```

终端会打印类似下面的地址，并尝试打开浏览器：

```text
如果浏览器没有自动打开，请复制并转到以下URL：
    「暗色主题已启用（支持动态切换主题）」: http://localhost:端口
```

用终端里的那个地址。服务监听 `0.0.0.0`，所以同一台机器用 `localhost` 即可。对话记录会写到 `gpt_log/chat_secrets.log`，这个目录已在 `.gitignore` 里。

`main.py` 开头有 `matplotlib.use('TkAgg')`。如果启动报 matplotlib 后端错误，把这一行改成 `matplotlib.use('Agg')` 后再启动。这只影响 matplotlib，不影响对话。

停止程序用终端里的 Ctrl+C。

## 页面怎么用

布局是左右结构（`LAYOUT = "LEFT-RIGHT"`）。中间对话窗的标签是 Agentbot。

1. 在插件按钮区选择分组。默认分组在 `config.py` 的 `DEFAULT_FN_GROUPS`：`Analysts`、`Diplomats`、`Sentinels`、`Explorers`、`自定义`。
2. 点一个性格按钮，该智能体会先发一条自我介绍，并加入当前对话。人设来自 `crazy_functions/personality_agents/agents_profiles.json`。
3. 在「输入区」写入内容。占位提示是：Enter 发送，Shift+Enter 换行。也可以点「提交」。
4. 「重置」清空当前输入相关状态，「停止」中断正在进行的回复，「新建会话」在会话侧。
5. 输入区下方有「发送语音」和「面部情绪识别」按钮，以及麦克风组件。这两项见下一节。
6. 折叠面板「自定义 Agent」用四根滑条设置 E/I、S/N、T/F、J/P，填写名字后点「专属智能体生成」，再点「专属智能体」按钮把它加入对话。

性格和分组：

| 分组 | 按钮 |
| --- | --- |
| Diplomats | INFJ、INFP、ENFJ、ENFP |
| Analysts | INTJ、INTP、ENTJ、ENTP |
| Sentinels | ISTJ、ISFJ、ESTJ、ESFJ |
| Explorers | ISTP、ISFP、ESTP、ESFP |
| 自定义 | 发送语音、专属智能体、面部情绪识别 |

按钮注册表在 `crazy_functional.py` 的 `get_crazy_functions()`。

## 语音、面部、文本情绪

这三块不是打开网页的前提。权重和系统库不完整时，文字对话仍可单独使用。

语音：

- 界面麦克风在 `ENABLE_AUDIO = True` 时出现。
- 识别走阿里云，需要 `ALIYUN_TOKEN` 和 `ALIYUN_APPKEY`。
- 入口是 `crazy_functions/语音助手.py` 和 `crazy_functions/live_audio/aliyunASR.py`。

面部：

- 页面上有一个摄像头组件。源码注释写明视频流仍有问题，只作测试。
- 模型是 mini-XCEPTION，权重在 `crazy_functions/emo_agent/face_agent/models/_mini_XCEPTION.102-0.64.hdf5`。
- 代码使用 Keras / TensorFlow 风格的 `keras`，以及 `opencv-python`（`cv2`）、`imutils`。这些没有写进 `requirements.txt`。

语音情绪小模型：

- 权重在 `crazy_functions/emo_agent/audio_agent/checkpoints/`，含 OpenSMILE 与 librosa 两套 LSTM。
- 特征提取会用到 `librosa`、`pandas`，以及同目录下的 `SMILExtract.exe`（Windows 上的 OpenSMILE 可执行文件）。

文本情绪：

- 代码在 `crazy_functions/emo_agent/txt_agent/`，依赖 PyTorch 和 fairseq。
- 大权重不在仓库里。下载说明在该目录的 `README.md`（夸克网盘链接）。

可选包可以按你实际要点的功能再装，例如：

```powershell
python -m pip install opencv-python imutils librosa pandas torch
```

TensorFlow/Keras 与 fairseq 的版本和 2024 年的权重绑定得很紧，这里不给出未验证的版本号。

## 目录

```text
main.py                 启动 Gradio，打印本地地址
config.py               端口、模型列表、密钥和网关（只读环境变量）
core_functional.py      基础功能按钮
crazy_functional.py     16 个性格智能体和语音/面部/专属智能体的按钮表
toolbox.py              配置读取、界面刷新、上传文件
request_llms/           普通对话请求。bridge_all.py 做地址改写，bridge_chatgpt.py 发请求
crazy_functions/
  personality_agents/   每个 MBTI 一个文件，人设 JSON 在 agents_profiles.json
  self_agent.py         专属智能体
  auto_gen.py           对话中的情绪识别助理配置
  语音助手.py            语音按钮
  emo_agent/            语音、面部、文本三套本地情绪模型
  live_audio/           麦克风缓冲和阿里云识别
themes/                 界面主题和前端脚本
shared_utils/           Markdown、上传、配置加载
docs/logo.png           网页图标
```

运行后会生成、且默认不提交的目录：

- `gpt_log/`：对话日志
- `private_upload/`：上传文件
- `flagged/`：Gradio 标记记录
- `.cache/`、`__pycache__/`、`.idea/`

## 常见问题

启动就报 `ModuleNotFoundError`：看缺的模块名，用当前虚拟环境的 `python -m pip install` 安装。主路径需要的包都在 `requirements.txt`。

网页能开，一点智能体就失败：先确认当前这个终端里 `OPENAI_API_KEY` 非空，再确认 `OPENAI_BASE_URL` 指向一个还活着的兼容网关，并且该网关有你在 `config_list` 里写的模型名。

浏览器没弹出：用终端打印的 `http://localhost:端口`。端口每次可能不同。

请求一直超时：看本机是否必须走代理。超时和重试在 `config.py` 的 `TIMEOUT_SECONDS`（30）和 `MAX_RETRY`（2）。

语音没结果：文字对话不依赖语音。检查阿里云两项环境变量，以及麦克风权限。

## 不要提交的内容

`.gitignore` 已排除 `.env`、`config_private.py`、`OAI_CONFIG_LIST`、日志和上传目录。提交前再搜一遍源码，确认没有 `sk-` 开头的密钥。
