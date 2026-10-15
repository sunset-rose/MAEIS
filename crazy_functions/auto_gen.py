import os
from autogen import ConversableAgent
import json
import logging

# from crazy_functions.emo_agent.txt_agent.txt_infer import predict_emotion

agent_time_list = []
emo_list = []
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]


def update_emo_list(emo_id):
    emo_list.append(emo_id)
    return emo_list


def update_agent_list(agent):
    if agent not in agent_time_list:
        agent_time_list.append(agent)
    return agent_time_list


config_list = [{
    "model": "gpt-3.5-turbo-16k-0613",
    "api_key": os.environ.get("OPENAI_API_KEY", ""),
    "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.xiaoai.plus/v1"),
    "temperature": 0.9
}]

emo_agent = ConversableAgent(
    "情绪识别助理",
    system_message= f'你是一个情绪识别助理，被用于在聊天过程中识别用户情绪。' \
                    f'你需要结合用户历史聊天记录分析当前用户聊天话语的情绪状态。' \
                    f'情绪状态列表为:EMOTIONS = ["愤怒", "厌恶", "恐惧", "快乐", "悲伤", "惊讶", "中立"]'\
                    f'每个情绪状态对应的EMO_id为EMOTIONS对应情绪的下标值',
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
)


# # 语音模型预载入
# from crazy_functions.emo_agent.audio_agent import utils
# from crazy_functions.emo_agent.audio_agent import models
# from emo_agent.audio_agent.predict import predict
# config = utils.parse_opt()
# model = models.load(config)


import re
def gen_reply(input, history, model_state):
    # 文本
    if model_state == 0:
        # 用户情绪历史记录
        log_file = r'gpt_log/chat_secrets.log'
        log_content = []
        # 过滤log日志里非聊天信息
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if f'INFO' and f'content' and f'role' in line:
                    log_content.append(line.strip())

        # # 调用模型的接口
        # input_list = []
        # input_list.append(input)
        # # 文本模型部署
        # # emo_id = predict_emotion(input)

        # 用GPT代替文本模型
        emo_content = f"""
            The earlier user's chat and emotion data:<data>{log_content}</data>.
            The current user's input is {input}.
            ## Requirements for the output format:
            <id>EMO_id</id>
            """
        emo_message = {"content": emo_content, "role": 'user'}
        emo_gpt = emo_agent.generate_reply(messages=[emo_message])

        emo_extract = re.search(r'<id>(\d+)</id>', emo_gpt)
        emo_tulple = emo_extract.groups(1)
        emo_id = emo_tulple[0]
        emo_id = int(emo_id)
        emo_list.append(emo_id)
        emo = EMOTIONS[emo_id]
        logging.info({"content": '<m>'+ input + '<\m>' + '<emo>' + emo + '<\emo>', "role": 'user'})

        # # 用户情绪历史记录
        # log_file = r'gpt_log/chat_secrets.log'
        # with open(log_file, 'r', encoding='utf-8') as f:
        #     log_content = f.read()

        # chat_history.append({"content": txt, "role": 'user'})
        reply = []
        for ag in agent_time_list:

            message_content = f"""
            The earlier user's chat and emotion data:<data>{log_content}</data>.
            The current user's input and emotion are {input} and {emo}, respectively.
            # output requirement
            - Don't generate similar content with other.
            - Use a casual, colloquial tone.
            - Aim for a natural, human-like, concise.
            - Short your output less than 15 words.
            ## Requirements for the output format:
            Return just the message, no extra words, no quotes.
            """

            user_message = {"content": message_content, "role": 'user'}

            # reply_ag = ag.generate_reply(messages=chat_history)
            reply_ag = ag.generate_reply(messages=[user_message])
            # chat_history.append({"content": reply_ag, "role": 'assistant'})
            logging.info({"content": reply_ag, "role": ag.name})

            # 把每个agent的回复实时更新
            log_content.append({"content": reply_ag, "role": ag.name})

            history.extend([f'role:user,content:```{input}```', f'role:```{ag.name}```,content:```{reply_ag}```'])
            reply.append(ag.name + ":" + reply_ag)
    elif model_state == 1:
        # 语音情况input应该处理wav文件，返回reply, history
        # 语音的情绪标签，注意跟文本的情绪标签不同
        audio_emo = ["angry", "fear", "happy", "neutral", "sad", "surprise"]

        # 语音模型识别
        # predict(config, audio_path, model)

        # 测试
        # 用户情绪历史记录
        log_file = r'gpt_log/chat_secrets.log'
        log_content = []
        # 过滤log日志里非聊天信息
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if f'INFO' and f'content' and f'role' in line:
                    log_content.append(line.strip())

        emo_content = f"""
            The earlier user's chat and emotion data:<data>{log_content}</data>.
            The current user's input is {input}.
            ## Requirements for the output format:
            <id>EMO_id</id>
            """
        emo_message = {"content": emo_content, "role": 'user'}
        emo_gpt = emo_agent.generate_reply(messages=[emo_message])

        emo_extract = re.search(r'<id>(\d+)</id>', emo_gpt)
        emo_tulple = emo_extract.groups(1)
        emo_id = emo_tulple[0]
        emo_id = int(emo_id)
        emo_list.append(emo_id)
        emo = EMOTIONS[emo_id]
        logging.info({"content": '<m>'+ input + '<\m>' + '<emo>' + emo + '<\emo>', "role": 'user'})

        # # 用户情绪历史记录
        # log_file = r'gpt_log/chat_secrets.log'
        # with open(log_file, 'r', encoding='utf-8') as f:
        #     log_content = f.read()

        # chat_history.append({"content": txt, "role": 'user'})
        reply = []
        for ag in agent_time_list:
            message_content = f"""
            The earlier user's chat and emotion data:<data>{log_content}</data>.
            The current user's input and emotion are {input} and {emo}, respectively.
            # output requirement
            - Don't be similar to other.
            - Use a casual, colloquial tone.
            - Aim for a natural, human-like, concise.
            - Short your output less than 15 words.
            ## Requirements for the output format:
            Return just the message, no extra words, no quotes.
            """
            user_message = {"content": message_content, "role": 'user'}


            # reply_ag = ag.generate_reply(messages=chat_history)
            reply_ag = ag.generate_reply(messages=[user_message])
            # chat_history.append({"content": reply_ag, "role": 'assistant'})
            logging.info({"content": reply_ag, "role": ag.name})
            # 把每个agent的回复实时更新
            log_content.append({"content": reply_ag, "role": ag.name})
            history.extend([f'role:user,content:```{input}```', f'role:```{ag.name}```,content:```{reply_ag}```'])
            reply.append(ag.name + ":" + reply_ag)
    return reply, history