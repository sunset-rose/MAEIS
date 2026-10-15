import re
def extract_contents(texts, agent_name):
    # 正则表达式模式匹配role为user的content内容
    pattern1 = re.compile(r'role:user,content:(.*?)')

    unique_agent = set()
    pattern2 = re.compile(r'智能体(.*?)已加入对话')

    for text in texts:
        matches = pattern2.findall(text)
        for match in matches:
            if match != agent_name:
                unique_agent.add(match)

    # 将集合转换为列表
    agent_list = list(unique_agent)

    # 提取content内容并放入列表
    user_contents = [match.group(1) for text in texts for match in pattern1.finditer(text)]

    agent_text = ", ".join(agent_list)
    user_contents = ", ".join(user_contents)

    return user_contents, agent_text
