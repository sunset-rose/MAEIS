import json
with open('crazy_functions/personality_agents/self_agents_profiles.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

arg_list = []
def save_arg(name, first, second, third, forth):
    arg_list.clear()
    arg_list.append(name)
    arg_list.append(first)
    arg_list.append(second)
    arg_list.append(third)
    arg_list.append(forth)
    return name, first, second, third, forth

def get_set():

    if arg_list != []:
        # 这里把arg_list的值写入agent的资料库里
        if arg_list[1] > 50:
            mbti_1 = 'I'
        else:
            mbti_1 = 'E'

        if arg_list[2] > 50:
            mbti_2 = 'N'
        else:
            mbti_2 = 'S'

        if arg_list[3] > 50:
            mbti_3 = 'F'
        else:
            mbti_3 = 'T'

        if arg_list[4] > 50:
            mbti_4 = 'J'
        else:
            mbti_4 = 'P'

        mbti = mbti_1 + mbti_2 + mbti_3 + mbti_4

        if json_data is not None:
            for item in json_data:
                if item["nick_name"] == arg_list[0]:
                    return item

        new_entry = {
            "id": 101,
            "nick_name": arg_list[0],
            # "birthday": "1940-12-12",
            # "sign": "一位富有远见的科学家，有着复杂的历史，对宇宙有着深刻的理解，并渴望找到人类最伟大问题的答案。",
            # "tag": "天体物理学,阅读,科学,环保主义,太空",
            # "location": "北京",
            # "job_title": "天体物理学家",
            # "profession": "科学家",
            # "education_level": "研究生",
            # "constellation": "人马座",
            # "pets": "None",
            # "favorite_food": "传统中餐",
            # "music": "古典乐",
            # "movies": "科幻,纪录片",
            # "travel_city": "None specified",
            # "sports": "None specified",
            # "color": "海军蓝",
            # "social_preferences": "喜欢独处和深刻反思；高度内省，专注于科学追求",
            "personality_type": mbti,
            "mbti_scores": {
                "introversion": arg_list[1],
                "extraversion": 100 - arg_list[1],
                "intuition": arg_list[2],
                "sensing": 100 - arg_list[2],
                "feeling": arg_list[3],
                "thinking": 100 - arg_list[2],
                "judging": arg_list[4],
                "perceiving": 100 - arg_list[4]}
        }

        json_data.append(new_entry)

        with open('crazy_functions/personality_agents/self_agents_profiles.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        return new_entry
    else:
        return arg_list
