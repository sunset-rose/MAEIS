from autogen import ConversableAgent
import os
config_list = [{"model":"gpt-3.5-turbo-16k-0613",
                "api_key": os.environ.get("OPENAI_API_KEY", ""),
                "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.xiaoai.plus/v1"),
                "temperature": 0.9
                }]

from toolbox import update_ui
from crazy_functions.auto_gen import update_agent_list
# from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive

from crazy_functions.agent_utils import extract_contents


def ISTP智能体(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    import json
    with open('crazy_functions/personality_agents/agents_profiles.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    infj_data = next((item for item in data if item["id"] == 10), None)

    # 基本信息
    chatbot.append(["智能体" + infj_data['personality_type'] + "已加入对话",
                    "你好，我是" + infj_data['nick_name'] + "，一个代表" + infj_data['personality_type'] + "的智能体。"])
    history.extend(["智能体" + infj_data['personality_type'] + "已加入对话",
                    "你好，我是" + infj_data['nick_name'] + "，一个代表" + infj_data['personality_type'] + "的智能体。"])
    yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面

    # 读取当前对话中已有的智能体和用户历史记录
    # user_contents, agent_text = extract_contents(history, "INFJ")

    # 注意，不要太生硬！在符合你个性的基础上，让你的回复更口语化、日常化一些。
    # 不要太啰嗦，字数根据用户的聊天调整。
    exp_list = infj_data['exp_list']
    del infj_data['exp_list']
    sys_prompt = f"""
    你的名字是{infj_data['nick_name']}。
    目标是根据提供的聊天记录无缝地继续对话，在不引起对方任何怀疑的情况下，保持你角色的特质和风格，角色的具体资料如下：{infj_data}。
    要求从{exp_list}学习聊天风格和语调，禁止回复重复的内容。
    要求输出缩短到15个字以内。
    首先，结合用户当前和历史的回话，实时分析用户的情绪状态得分（包括愤怒、厌恶、恐惧、快乐、悲伤、惊讶和中立），满分为10分。注意，此步骤不出现在聊天过程中。
    接着，扮演具体资料中的角色，给出与{exp_list}元素相似的回复。
    """


    infj = ConversableAgent(
        infj_data['nick_name'],
        system_message=sys_prompt,
        llm_config={"config_list": config_list},
        human_input_mode="NEVER",  # 从不请求人类输入。
    )

    update_agent_list(infj)