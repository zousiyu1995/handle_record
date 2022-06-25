"""
author: zousiyu
date: 2022.05.31
summarize 'handle' (汉兜) data
"""

import itertools
import json
from collections import Counter
from datetime import timedelta
from pyexpat import model
from typing import Iterable, TextIO  # for type hints

import numpy as np
from pypinyin import Style, pinyin


def flatten(items: Iterable) -> Iterable:
    """flatten nested iterable object"""
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            for sub_item in flatten(item):
                yield sub_item
        else:
            yield item


def list_to_sorted_dict(a_list: list) -> dict:
    """element->key, count of element->value, sort by value"""
    a_dict = Counter(list(flatten(a_list)))

    return dict(sorted(a_dict.items(), key=lambda item: item[1], reverse=True))


def seconds_to_time_str(seconds: int) -> str:
    """int second to 'xx时xx分xx秒' """

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if h == 0:
        return f"{m}分{s}秒"
    else:
        return f"{h}时{m}分{s}秒"


def get_pinyin(idiom: str) -> tuple:
    """get initial, final and tone of single idiom"""
    initials = []
    finals = []
    tones = []
    for char in idiom:
        initial: str = list(
            flatten(pinyin(char, style=Style.INITIALS, strict=False)))[0]
        if initial == '':
            initial = '_'
        initials.append(initial)

        # TODO: 如何更优雅地分离字符串中的数字
        # TODO: 如何处理成语中的特殊发音
        final_and_tone: str = list(
            flatten(pinyin(char, style=Style.FINALS_TONE3, strict=False)))[0]
        # 只要字符串的最后一位是数字，有声调和韵母，添加tones和finals
        if final_and_tone[-1].isdigit():
            tones.append(final_and_tone[-1])
            finals.append(final_and_tone[0:-1])
        # 如果字符串的最后一位不是数字，代表没有声调，声调设置成'_'，韵母为整个字符串
        else:
            tones.append('_')
            finals.append(final_and_tone)

    return initials, finals, tones


def read_idioms(idioms_file: TextIO) -> list:
    """return a true idiom list"""
    with open(idioms_file, "r", encoding="utf-8") as file:
        # idioms = [line.split()[0] for line in file] # for text file
        idioms = json.load(file)  # for json file
    return idioms


def is_idiom(phrase: str, idioms: list) -> bool:
    """is **true** idiom?"""
    return phrase in idioms


def save_dict_to_json(a_dict: dict, file_name: str) -> None:
    """save counter dict to json"""
    with open(file_name, mode='w+', encoding='utf-8') as file:
        file.write(json.dumps(a_dict, ensure_ascii=False, indent=4))

    return None


def main():
    """main"""
    phrases_list = []
    initials_list = []
    finals_list = []
    tones_list = []
    num_of_tries_list = []
    time_of_tries_list = []
    hint_list = []
    num_of_wins = 0
    max_num_of_tries = 10

    with open("summary.json", "r", encoding="utf-8") as json_file:
        all_days: list = json.load(json_file)
        for every_day in all_days:
            # update phrase, some phrase isn't idiom
            phrases_list.append(every_day['idiom'])
            # update number of tries, time of tries
            num_of_tries_list.append(len(every_day['idiom']))
            splited_time = list(map(int, every_day['time'].split(":")))
            time_of_tries_list.append(
                timedelta(hours=splited_time[0],
                          minutes=splited_time[1],
                          seconds=splited_time[2]))
            # update if hint
            hint_list.append(every_day['hint'])
            # update number of wins
            if len(every_day['idiom']) <= max_num_of_tries:
                num_of_wins += 1

    # remove false idiom in phrases
    phrases_list = list(flatten(phrases_list))  # flatten nest list
    idioms_filter = [
        is_idiom(idiom,
                 read_idioms("./idiom/idioms_from_chinese_xinhua_simple.json"))
        for idiom in phrases_list
    ]
    idioms_list = list(itertools.compress(phrases_list, idioms_filter))

    # update initial, final, and tone of idiom
    for idiom in idioms_list:
        initials, finals, tones = get_pinyin(idiom)
        initials_list.append(initials)
        finals_list.append(finals)
        tones_list.append(tones)

    # convert list to dict, all infos are true idiom
    idioms_dict = list_to_sorted_dict(idioms_list)
    initials_dict = list_to_sorted_dict(initials_list)
    finals_dict = list_to_sorted_dict(finals_list)
    tones_dict = list_to_sorted_dict(tones_list)
    num_of_tries_dict = Counter(num_of_tries_list)
    # num_of_tries_dict = list_to_sorted_dict(num_of_tries_list)

    # save data
    save_dict_to_json(idioms_dict, "./output/idioms.json")
    save_dict_to_json(initials_dict, "./output/initials.json")
    save_dict_to_json(finals_dict, "./output/finals.json")
    save_dict_to_json(tones_dict, "./output/tones.json")
    save_dict_to_json(num_of_tries_dict, "./output/num_of_tries.json")
    with open("./output/time_of_tries.json", mode="w+", encoding="utf-8") as f:
        f.write(
            json.dumps(list(map(str, time_of_tries_list)),
                       ensure_ascii=False,
                       indent=4))

    # print summary
    print(
        f"游戏天数：{len(all_days)}天，获胜天数：{num_of_wins}天，胜率：{round(100 * num_of_wins / len(all_days))}%"
    )
    print(
        f"无提示游戏天数：{len(all_days)-np.sum(hint_list)}天，无提示游戏比率：{np.round(100 * (1 - sum(hint_list) / len(hint_list)))}%"
    )
    print(f"输入四字短语总个数：{len(phrases_list)}个")
    print(f"其中成语个数：{len(idioms_list)}个")
    print(f"其中成语占比：{np.round(100*len(idioms_list)/len(phrases_list))}%")
    print(f"去重后成语个数：{len(idioms_dict)}个")
    # print(f"最常用的成语top 10：{list(idioms_dict.items())[0:9]}")
    print(f"总尝试：{sum(num_of_tries_list)}次")
    print(f"最多尝试：{max(num_of_tries_list)}次")
    print(f"最少尝试：{min(num_of_tries_list)}次")
    print(f"平均尝试：{np.round(np.mean(num_of_tries_list))}次")
    print(
        f"总用时：{seconds_to_time_str(sum(time_of_tries_list, timedelta(0, 0)).seconds)}"
    )
    print(f"平均用时：{seconds_to_time_str(np.mean(time_of_tries_list).seconds)}")
    print(f"最长用时：{seconds_to_time_str(max(time_of_tries_list).seconds)}")
    print(f"最短用时：{seconds_to_time_str(min(time_of_tries_list).seconds)}")


if __name__ == "__main__":
    main()
