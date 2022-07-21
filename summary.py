"""
author: zousiyu
summarize 'handle' (汉兜) data
"""

import itertools
import json
from collections import Counter
from datetime import timedelta

import numpy as np

from util import (flatten, get_pinyin, get_score, int_seconds_to_time_str,
                  list_to_sorted_dict, save_to_json)


def main():
    """main"""
    phrases_list = []
    opening_phrases_list = []
    ans_list = []
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
            opening_phrases_list.append(every_day['idiom'][0])
            ans_list.append(every_day['idiom'][-1])
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
    with open("./idiom/idioms_from_chinese_xinhua_simple.json",
              "r",
              encoding="utf-8") as f:
        true_idioms_list = json.load(f)

    phrases_list = list(flatten(phrases_list))  # flatten nest list
    idioms_filter = [
        True if idiom in true_idioms_list else False for idiom in phrases_list
    ]
    idioms_list = list(itertools.compress(phrases_list, idioms_filter))

    # remove false idiom in opening phrases
    opening_idioms_list = list(
        itertools.compress(opening_phrases_list, idioms_filter))
    # 给开局词打分
    opening_phare_scores = [
        get_score(opening_phare, ans)
        for opening_phare, ans in zip(opening_phrases_list, ans_list)
    ]

    # update initial, final, and tone of idiom
    for idiom in idioms_list:
        initials, finals, tones = get_pinyin(idiom)
        initials_list.append(initials)
        finals_list.append(finals)
        tones_list.append(tones)

    # convert list to dict, all infos are true idiom
    idioms_dict = list_to_sorted_dict(idioms_list)
    opening_idioms_dict = list_to_sorted_dict(opening_idioms_list)
    initials_dict = list_to_sorted_dict(initials_list)
    finals_dict = list_to_sorted_dict(finals_list)
    tones_dict = list_to_sorted_dict(tones_list)
    num_of_tries_dict = Counter(num_of_tries_list)
    # num_of_tries_dict = list_to_sorted_dict(num_of_tries_list)

    # save data
    save_to_json(idioms_dict, "./output/idiom.json")
    save_to_json(opening_idioms_dict, "./output/opening_idiom.json")
    save_to_json(initials_dict, "./output/initial.json")
    save_to_json(finals_dict, "./output/final.json")
    save_to_json(tones_dict, "./output/tone.json")
    save_to_json(num_of_tries_dict, "./output/num_of_tries.json")
    save_to_json(list(map(str, time_of_tries_list)),
                 "./output/time_of_tries.json")
    save_to_json(opening_phare_scores, "./output/opening_phare_score.json")

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
        f"总用时：{int_seconds_to_time_str(sum(time_of_tries_list, timedelta(0, 0)).seconds)}"
    )
    print(
        f"平均用时：{int_seconds_to_time_str(np.mean(time_of_tries_list).seconds)}")
    print(f"最长用时：{int_seconds_to_time_str(max(time_of_tries_list).seconds)}")
    print(f"最短用时：{int_seconds_to_time_str(min(time_of_tries_list).seconds)}")

    print(f"开局词最高分：{np.max(opening_phare_scores)}")
    print(f"开局词最低分：{np.min(opening_phare_scores)}")
    print(f"开局词平均分：{np.round(np.mean(opening_phare_scores))}")


if __name__ == "__main__":
    main()
