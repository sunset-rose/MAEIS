import os
# 这里很重要
# 设置用户名和密码（不需要修改）（相关功能不稳定，与gradio版本和网络都相关，如果本地使用不建议加这个）
# [("username", "password"), ("username2", "password2"), ...]
AUTHENTICATION = []

# 代码高亮
CODE_HIGHLIGHT = True


# 窗口布局
LAYOUT = "LEFT-RIGHT"   # "LEFT-RIGHT"（左右布局） # "TOP-DOWN"（上下布局）

# 对话窗的高度 （仅在LAYOUT="TOP-DOWN"时生效）
CHATBOT_HEIGHT = 1115

# 加一个live2d装饰
ADD_WAIFU = False

# 发送请求到OpenAI后，等待多久判定为超时
TIMEOUT_SECONDS = 30

# 如果OpenAI不响应（网络卡顿、代理失败、KEY失效），重试的次数限制
MAX_RETRY = 2


# 极少数情况下，openai的官方KEY需要伴随组织编码（格式如org-xxxxxxxxxxxxxxxxxxxxxxxx）使用
API_ORG = ""

API_KEY = os.environ.get("OPENAI_API_KEY", "")
# 智能体对话默认仍走原项目的兼容网关。换网关时设置环境变量 OPENAI_BASE_URL，不要把密钥写回这个文件。
_OPENAI_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.xiaoai.plus/v1").rstrip("/")
API_URL_REDIRECT = {"https://api.openai.com/v1/chat/completions": _OPENAI_BASE + "/chat/completions"}

# 没有本地代理时保持 None。需要代理时再写成 {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}。
proxies = None

# 默认的系统提示词（system prompt）
INIT_SYS_PROMPT = "Serve me as a sentiment analysis assistant."

# 网页的端口, -1代表随机端口
WEB_PORT = -1

# 当前模型
LLM_MODEL = "gpt-3.5-turbo-16k"
# 其他可用模型，这里要改
AVAIL_LLM_MODELS = ["gpt-4-1106-preview", "gpt-4-turbo-preview", "gpt-4-vision-preview",
                    "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k", "gpt-3.5-turbo",
                    "gpt-4", "gpt-4-32k",
                    ]

# 设置gradio的并行线程数（不需要修改）
CONCURRENT_COUNT = 100

# 是否在提交时自动清空输入框
AUTO_CLEAR_TXT = True

# 阿里云实时语音识别 配置难度较高,后期再加
# 参考 https://github.com/binary-husky/gpt_academic/blob/master/docs/use_audio.md
ENABLE_AUDIO = True
ALIYUN_TOKEN = os.environ.get("ALIYUN_TOKEN", "")
ALIYUN_APPKEY = os.environ.get("ALIYUN_APPKEY", "")
ALIYUN_ACCESSKEY="" # （无需填写）
ALIYUN_SECRET=""    # （无需填写）

# 日志文件夹的位置，请勿修改
PATH_LOGGING = "gpt_log"

# 色彩主题, 可选 ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast"]
# 更多主题, 请查阅Gradio主题商店: https://huggingface.co/spaces/gradio/theme-gallery 可选 ["Gstaff/Xkcd", "NoCrypt/Miku", ...]
THEME = "Chuanhu-Small-and-Beautiful"
AVAIL_THEMES = ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast"]

# 暗色模式 / 亮色模式
DARK_MODE = True

# 自定义按钮的最大数量限制
NUM_CUSTOM_BASIC_BTN = 4

# HTTPS 秘钥和证书（不需要修改）
SSL_KEYFILE = ""
SSL_CERTFILE = ""

# 插件分类默认选项
# DEFAULT_FN_GROUPS = ['对话', '编程', '学术', '智能体']
# DEFAULT_FN_GROUPS = ['Love', 'Frustration', 'Pessimist', 'Optimist', 'Shame', 'Compassion', '语音']
DEFAULT_FN_GROUPS = ['Analysts', 'Diplomats', 'Sentinels', 'Explorers', '自定义']

# 启用插件热加载
PLUGIN_HOT_RELOAD = False

# 临时的上传文件夹位置，请勿修改
PATH_PRIVATE_UPLOAD = "private_upload"