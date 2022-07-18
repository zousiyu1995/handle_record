import itertools
import json
from collections import Counter
from typing import Iterable

from pypinyin import Style, pinyin


def flatten(items: Iterable) -> Iterable:
    """flatten nested iterable object"""
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            for sub_item in flatten(item):
                yield sub_item
        else:
            yield item


def save_to_json(data, file_name: str) -> None:
    """save to json"""
    with open(file_name, mode='w+', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

    return None


def list_to_sorted_dict(input_list: list) -> dict:
    """element->key, count of element->value, sort by value"""

    return dict(
        sorted(Counter(list(flatten(input_list))).items(),
               key=lambda item: item[1],
               reverse=True))


def int_seconds_to_time_str(seconds: int) -> str:
    """int second to 'xx分xx秒' or 'xx时xx分xx秒' """

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    if h == 0:
        return f"{m}分{s}秒"
    else:
        return f"{h}时{m}分{s}秒"


def get_pinyin(idiom: str) -> tuple:
    """
    Get initial, final and tone of single idiom.

    Args:
        idiom: An idiom string.

        For example: 纸上谈兵

    Returns:
        A tuple containing the initials, finals and tones of an idiom.

        For example: get_pinyin("纸上谈兵")
            initials: ['zh', 'sh', 't', 'b']
            finals:   ['i', 'ang', 'an', 'ing']
            tones:    ['3', '4', '2', '1']
    """
    initials = []
    finals = []
    tones = []
    for char in idiom:
        initial = list(
            flatten(pinyin(char, style=Style.INITIALS, strict=False)))[0]
        if initial == '':
            initial = '_'
        initials.append(initial)

        # TODO: 如何更好地分离字符串中的数字
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


def compare_list(l1: list, l2: list):
    """
    输入两个相同长度的数组，检查list l1中的元素在list l2中的分布情况

    Args:
        l1: A list with length n
        l2: A list with length n

    Returns:
        A weight list

        For example:
            a = [1, 2, 3]
            b = [1, 3, 4]
            compare_list(a, b)
            weight: [1, 0, 0.5]
    """
    # 位置相同，元素相同，得1权重
    same_position = [1 if i == j else 0 for i, j in zip(l1, l2)]
    # 位置不同，元素相同，得0.5权重
    different_position = [
        0.5 if i in l2 and i != j else 0 for i, j in zip(l1, l2)
    ]
    return [i + j for i, j in zip(same_position, different_position)]


def get_score(opening_idiom: str, ans: str):
    """
    评估开局词的分数
    """

    # 四个位置，对于每一个位置，字25分，声母10分，韵母10分，声调5分
    idiom_weight = 25
    initial_weight = 10
    final_weight = 10
    tone_weight = 5
    # 如果开局词和答案之间存在相同的字，每个字得25分，
    idiom_score = sum(compare_list(opening_idiom, ans)) * idiom_weight
    # 把相同的字移除，仅留下不同的字。因为字相同代表声母、韵母和声调都相同，没必要继续比较这个字的声母、韵母和声调了。
    new_opening_idiom = list(
        itertools.compress(opening_idiom,
                           [not i for i in compare_list(opening_idiom, ans)]))
    new_ans = list(
        itertools.compress(ans,
                           [not i for i in compare_list(opening_idiom, ans)]))
    # 获取开局词和答案之间不同的字声母、韵母和声调
    opening_idiom_initials, opening_idiom_finals, opening_idiom_tones = get_pinyin(
        new_opening_idiom)
    ans_initials, ans_finals, ans_tones = get_pinyin(new_ans)
    # 打分
    initial_score = sum(compare_list(opening_idiom_initials,
                                     ans_initials)) * initial_weight
    final_score = sum(compare_list(opening_idiom_finals,
                                   ans_finals)) * final_weight
    tone_score = sum(compare_list(opening_idiom_tones,
                                  ans_tones)) * tone_weight
    return idiom_score + initial_score + final_score + tone_score
