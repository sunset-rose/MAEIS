from toolbox import HotReload
from crazy_functions.语音助手 import 语音助手
from crazy_functions.self_agent import 自定义智能体
from crazy_functions.personality_agents.面部情绪识别助理 import 面部情绪识别助理
from crazy_functions.personality_agents.ISFJ import ISFJ智能体
from crazy_functions.personality_agents.INFJ import INFJ智能体
from crazy_functions.personality_agents.INFP import INFP智能体
from crazy_functions.personality_agents.INTJ import INTJ智能体
from crazy_functions.personality_agents.ISTJ import ISTJ智能体
from crazy_functions.personality_agents.INTP import INTP智能体
from crazy_functions.personality_agents.ISTP import ISTP智能体
from crazy_functions.personality_agents.ISFP import ISFP智能体
from crazy_functions.personality_agents.ENTJ import ENTJ智能体
from crazy_functions.personality_agents.ESTJ import ESTJ智能体
from crazy_functions.personality_agents.ENFJ import ENFJ智能体
from crazy_functions.personality_agents.ESFJ import ESFJ智能体
from crazy_functions.personality_agents.ENTP import ENTP智能体
from crazy_functions.personality_agents.ESTP import ESTP智能体
from crazy_functions.personality_agents.ENFP import ENFP智能体
from crazy_functions.personality_agents.ESFP import ESFP智能体

# 高级函数插件
def get_crazy_functions():
    function_plugins = {
        "INFJ🌌🔮": {
            "Group": "Diplomats",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents INFJ",
            "Function": HotReload(INFJ智能体),
        },
        "INFP🌈💫": {
            "Group": "Diplomats",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents INFP",
            "Function": HotReload(INFP智能体),
        },
        "ENFJ🌟🎓": {
            "Group": "Diplomats",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents ENFJ",
            "Function": HotReload(ENFJ智能体),
        },
        "ENFP🌟💬": {
            "Group": "Diplomats",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents ENFP",
            "Function": HotReload(ENFP智能体),
        },

        "INTJ🧠📐": {
            "Group": "Analysts",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents INTJ",
            "Function": HotReload(INTJ智能体),
        },
        "INTP🤔💡": {
            "Group": "Analysts",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents INTP",
            "Function": HotReload(INTP智能体),
        },
        "ENTJ🏆📈": {
            "Group": "Analysts",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents ENTJ",
            "Function": HotReload(ENTJ智能体),
        },
        "ENTP🎯🧠": {
            "Group": "Analysts",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents ENTP",
            "Function": HotReload(ENTP智能体),
        },

        "ISTJ📚🔧": {
            "Group": "Sentinels",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents ISTJ",
            "Function": HotReload(ISTJ智能体),
        },
        "ISFJ🛡️🌸": {
            "Group": "Sentinels",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents ISFJ",
            "Function": HotReload(ISFJ智能体),
        },
        "ESTJ📊👔": {
            "Group": "Sentinels",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents ESTJ",
            "Function": HotReload(ESTJ智能体),
        },
        "ESFJ🌞🤝": {
            "Group": "Sentinels",
            "Color": "primary",
            "AsButton": True,
            "Info": "A agent represents ESFJ",
            "Function": HotReload(ESFJ智能体),
        },

        "ISTP🛠️🕶️": {
            "Group": "Explorers",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents ISTP",
            "Function": HotReload(ISTP智能体),
        },
        "ISFP🎨💖": {
            "Group": "Explorers",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents ISFP",
            "Function": HotReload(ISFP智能体),
        },
        "ESTP🚀🌍": {
            "Group": "Explorers",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents ESTP",
            "Function": HotReload(ESTP智能体),
        },
        "ESFP🎉🎭": {
            "Group": "Explorers",
            #"Color": "stop",
            "AsButton": True,
            "Info": "A agent represents ESFP",
            "Function": HotReload(ESFP智能体),
        },

        "发送语音🔊": {
            "Group": "自定义",
            "Color": "stop",
            "AsButton": True,
            "Info": "语音助手",
            "Function": HotReload(语音助手),
        },

        "专属智能体": {
            "Group": "自定义",
            "Color": "primary",
            "AsButton": True,
            "Info": "专属智能体",
            "Function": HotReload(自定义智能体),
        },

        "面部情绪识别📷": {
            "Group": "自定义",
            "Color": "stop",
            "AsButton": True,
            "Info": "面部情绪识别助理",
            "Function": HotReload(面部情绪识别助理),
        },
    }
    return function_plugins
