"""
author: zousiyu
summarize handle data
"""

import itertools
import json
from collections import Counter
from datetime import timedelta
from typing import Iterable, TextIO

import numpy as np
from matplotlib import pyplot as plt
from pypinyin import Style, pinyin
from wordcloud import WordCloud
from PIL import Image


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


def sec_to_time_str(sec: int) -> str:
    """int second to 'xx分xx秒' """

    return f"{divmod(sec, 60)[0]}分{divmod(sec, 60)[1]}秒"


def get_pinyin(idiom: str) -> tuple:
    """get initial, final and tone of single idiom"""
    initial = pinyin(idiom, style=Style.INITIALS, strict=False)
    final_tone: str = pinyin(idiom, style=Style.FINALS_TONE3)[0][0]
    final = final_tone[0:-1]
    tone = final_tone[-1]

    return initial, final, tone


def read_idioms(idioms_file: TextIO) -> list:
    """return a true idiom list"""
    with open(idioms_file, "r", encoding="utf-8") as file:
        idioms = [line.split()[0] for line in file]
    return idioms


def is_idiom(phrase: str, idioms: list) -> bool:
    """is **true** idiom?"""
    return phrase in idioms


def save_dict_to_json(a_dict: dict, file_name: str) -> None:
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
        is_idiom(idiom, read_idioms("./THUOCL_chengyu.txt"))
        for idiom in phrases_list
    ]
    idioms_list = list(itertools.compress(phrases_list, idioms_filter))

    # update initial, final, and tone of idiom
    for idiom in idioms_list:
        initial, final, tone = get_pinyin(idiom)
        initials_list.append(initial)
        finals_list.append(final)
        tones_list.append(tone)

    # convert list to dict, all infos are true idiom
    idioms_dict = list_to_sorted_dict(idioms_list)
    initials_dict = list_to_sorted_dict(initials_list)
    finals_dict = list_to_sorted_dict(finals_list)
    tones_dict = list_to_sorted_dict(tones_list)
    num_of_tries_dict = Counter(num_of_tries_list)
    # num_of_tries_dict = list_to_sorted_dict(num_of_tries_list)

    save_dict_to_json(idioms_dict, "./output_idioms.json")
    save_dict_to_json(initials_dict, "./output_initials.json")
    save_dict_to_json(finals_dict, "./output_finals.json")
    save_dict_to_json(num_of_tries_dict, "./output_num_of_tries.json")

    # summary
    print(
        f"游戏天数：{len(all_days)}天，获胜天数：{num_of_wins}天，胜率{round(100 * num_of_wins / len(all_days))}%"
    )
    print(f"无提示比率：{np.round(100 * (1 - sum(hint_list) / len(hint_list)))}%")
    print(f"输入四字短语个数：{len(phrases_list)}个")
    print(
        f"其中成语个数：{len(idioms_list)}，成语比例：{np.round(100*len(idioms_list)/len(phrases_list))}%"
    )
    # print(f"最常用的成语top 10：{list(idioms_dict.items())[0:9]}")
    print(f"总尝试次数：{sum(num_of_tries_list)}次")
    print(f"最多尝试次数：{max(num_of_tries_list)}次")
    print(f"最少尝试次数：{min(num_of_tries_list)}次")
    print(f"平均尝试次数：{np.round(np.mean(num_of_tries_list))}次")
    print(
        f"总浪费时间：{sec_to_time_str(sum(time_of_tries_list, timedelta(0, 0)).seconds)}"
    )
    print(f"平均用时：{sec_to_time_str(np.mean(time_of_tries_list).seconds)}")
    print(f"最长用时：{sec_to_time_str(max(time_of_tries_list).seconds)}")
    print(f"最短用时：{sec_to_time_str(min(time_of_tries_list).seconds)}")

    plt.subplots()
    plt.bar(initials_dict.keys(), initials_dict.values())
    plt.xlabel("initial")
    plt.ylabel("frequency")

    plt.subplots()
    plt.bar(finals_dict.keys(), finals_dict.values())
    plt.xlabel("final")
    plt.ylabel("frequency")

    plt.subplots()
    plt.bar(tones_dict.keys(), tones_dict.values())
    plt.xlabel("tone")
    plt.ylabel("frequency")

    plt.subplots()
    plt.bar(num_of_tries_dict.keys(), num_of_tries_dict.values())
    plt.xlabel("number of tries")
    plt.ylabel("frequency")
    plt.xticks(np.arange(0, 12, 1))

    # generate word cloud
    fig_wc, ax_wc = plt.subplots()
    wc_mask = np.array(Image.open("./mask.png"))
    wc_font = r"./qiji-combo.ttf"
    wc_idiom = WordCloud(prefer_horizontal=1,
                         background_color="white",
                         font_path=wc_font,
                         max_font_size=500,
                         mask=wc_mask,
                         width=2000,
                         height=2000 * 0.618)
    wc_idiom.generate_from_frequencies(idioms_dict)
    ax_wc.set_position([0.05, 0.05, 0.9, 0.9])
    plt.imshow(wc_idiom)
    plt.axis("off")
    plt.savefig("./wc_idiom.jpg", dpi=1000)

    plt.show()


if __name__ == "__main__":
    main()
