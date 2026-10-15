from autogen import ConversableAgent
import os
config_list = [{"model": "gpt-3.5-turbo-16k",
                "api_key": os.environ.get("OPENAI_API_KEY", ""),
                "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.xiaoai.plus/v1"),
                "temperature": 0.9
                }]

from toolbox import update_ui
from crazy_functions.auto_gen import update_agent_list
# from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive

from crazy_functions.agent_utils import extract_contents

from self_agent_utils import get_set


def 自定义智能体(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):


    self_arg = get_set()

    if self_arg != []:
        # 基本信息
        chatbot.append(["你的专属智能体已加入对话",
                    f'你好，我是{self_arg["nick_name"]}，你的专属智能体。'])
        history.extend(["你的专属智能体已加入对话",
                    f'你好，我是{self_arg["nick_name"]}，你的专属智能体。'])
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面


        # 读取当前对话中已有的智能体和用户历史记录
        # user_contents, agent_text = extract_contents(history, "ENFJ")

        sys_prompt = f"""
            你的名字是{self_arg["nick_name"]},是用户的专属智能体。你的具体资料如下：{self_arg}。
            现在用户邀请你日常聊天。
            首先，结合用户当前和历史的回话，实时分析用户的情绪状态极其得分（包括愤怒、厌恶、恐惧、快乐、悲伤、惊讶和中立），满分为10分。注意，此步骤不出现在聊天过程中。
            接着，根据你的习惯特征和用户的情绪状态进行聊天。
            注意，回复字数控制在5-15左右。
            """

        selg_agent = ConversableAgent(
            f'{self_arg["nick_name"]}',
            system_message= sys_prompt,

            # 你的名字是Love, 你是dory人格的一部分，是代表love的人格。
            # dory的其他人格智能体为Frustration, Pessimist, Optimist, Shame, Compassion。
            # 现在dory邀请你进行一场对话
            # 当前对话中已有的智能体为```{agent_text}```
            # 请在每次回话之前分析dory当前的情绪状态得分，根据其情绪状态和历史对话内容进行回答
            # system_message= f'Your name is Love. You are a part of dory\'s personality, the personality that represents love.' \
            #                f'The rest of dory personality is Frustration, Pessimist, Optimist, Shame, Compassion.' \
            #                f'Now Dory invites you to a conversation.' \
            #                f'The agents that are already in the current dialog are ```{agent_text}```.' \
            #                f'Please analyze Dory\'s current emotional state score before each call-back and answer based on her emotional state and historical conversations.' \
            #                f'dory\'s historical conversations are ```{user_contents}```'\
            #                f'notice dory\'s language, change language based on her language',

            llm_config={"config_list": config_list},
            human_input_mode="NEVER",  # 从不请求人类输入。
        )

        update_agent_list(selg_agent)
    else:
        chatbot.append((["你还未生成你的专属智能体", None]))
        yield from update_ui(chatbot=chatbot, history=history)



