import itertools
import json
from datetime import timedelta

from pypinyin import Style, pinyin

from util import Util


class HandleRecord():
    IDIOM_DICT_PATH = "./idiom/idiom_big_dictionary.json"

    def __init__(self, record: dict) -> None:
        # 日期
        self.date: str = record['date']
        # 猜测时间
        self.time: timedelta = self.__get_time(record['time'])
        # 是否提示
        self.hint: bool = record['hint']
        # 输入的四字短语
        self.phrase: list[str] = record['idiom']
        # 输入的四字短语中真正的成语
        self.idiom: list[str] = self.__get_idiom(self.phrase)
        # 开局词
        self.opening_phrase: str = record['idiom'][0]
        # 开局词中的成语
        self.opening_idiom: str = self.__get_opening_idiom(self.opening_phrase)
        # 答案
        self.ans: str = record['idiom'][-1]
        # 开局词的分数
        self.opening_phrase_score: float = self.__get_phrase_score(
            self.opening_phrase, self.ans)
        # 全部词的分数
        self.score: list[float] = [
            self.__get_phrase_score(i, self.ans) for i in self.phrase
        ]
        # 尝试次数
        self.attempt: int = len(self.phrase)
        # 是否胜利
        self.win: bool = self.attempt <= 10
        # 声母、韵母和声调
        self.initial, self.final, self.tone = self.__get_pinyin(self.phrase)

    @staticmethod
    def compare_list(l1: list, l2: list) -> list:
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
        same_position = [1.0 if i == j else 0 for i, j in zip(l1, l2)]
        # 位置不同，元素相同，得0.5权重
        different_position = [
            0.5 if i in l2 and i != j else 0 for i, j in zip(l1, l2)
        ]

        return [i + j for i, j in zip(same_position, different_position)]

    def __get_time(self, time: str) -> timedelta:
        """
        输入时间字符串，形如"00:01:10"，返回timedelta类型
        """
        splited_time_str = list(map(int, time.split(":")))

        return timedelta(hours=splited_time_str[0],
                         minutes=splited_time_str[1],
                         seconds=splited_time_str[2])

    def __get_idiom(self, phrase: list) -> list:
        with open(HandleRecord.IDIOM_DICT_PATH, "r", encoding="utf-8") as f:
            idiom_dict = json.load(f)

        idiom_filter = [True if i in idiom_dict else False for i in phrase]
        idiom = list(itertools.compress(phrase, idiom_filter))

        return idiom

    def __get_pinyin(self, phrase: list) -> tuple:
        """
        phrase is list or string
        """
        initial = [
            '_' if i == '' else i for i in Util.flatten(
                pinyin(phrase, style=Style.INITIALS, strict=False))
        ]
        # 如果字符串的最后一位是数字，添加从开始到最后一位为韵母；否则，添加整个字符串为韵母
        fianl = [
            i[0:-1] if i[-1].isdigit() else i for i in Util.flatten(
                pinyin(phrase, style=Style.FINALS_TONE3, strict=False))
        ]
        # 如果字符串的最后一位是数字，添加最后一位为声调；否则，声调设置为'_'
        tone = [
            i[-1] if i[-1].isdigit() else '_' for i in Util.flatten(
                pinyin(phrase, style=Style.FINALS_TONE3, strict=False))
        ]

        return initial, fianl, tone

    def __get_opening_idiom(self, opening_phrase: str) -> str:
        with open(HandleRecord.IDIOM_DICT_PATH, "r", encoding="utf-8") as f:
            idiom_dict = json.load(f)

        if opening_phrase in idiom_dict:
            return opening_phrase

    def __get_phrase_score(self, opening_phrase: str, ans: str) -> float:
        """
        评估开局词的分数
        """
        # TODO: 打分算法有问题
        # 四个位置，对于每一个位置，字25分，声母10分，韵母10分，声调5分
        idiom_weight = 25
        initial_weight = 12.5
        final_weight = 10
        tone_weight = 2.5
        # 如果开局词和答案之间存在相同的字，每个字得25分，
        idiom_score = sum(HandleRecord.compare_list(opening_phrase,
                                                    ans)) * idiom_weight
        # 把相同的字移除，仅留下不同的字。因为字相同代表声母、韵母和声调都相同，没必要继续比较这个字的声母、韵母和声调了。
        new_opening_phrase = list(
            itertools.compress(opening_phrase, [
                not i for i in HandleRecord.compare_list(opening_phrase, ans)
            ]))
        new_ans = list(
            itertools.compress(ans, [
                not i for i in HandleRecord.compare_list(opening_phrase, ans)
            ]))
        # 获取开局词和答案之间不同的字声母、韵母和声调
        opening_idiom_initials, opening_idiom_finals, opening_idiom_tones = self.__get_pinyin(
            new_opening_phrase)
        ans_initials, ans_finals, ans_tones = self.__get_pinyin(new_ans)
        # 打分
        initial_score = sum(
            HandleRecord.compare_list(opening_idiom_initials,
                                      ans_initials)) * initial_weight
        final_score = sum(
            HandleRecord.compare_list(opening_idiom_finals,
                                      ans_finals)) * final_weight
        tone_score = sum(
            HandleRecord.compare_list(opening_idiom_tones,
                                      ans_tones)) * tone_weight

        return idiom_score + initial_score + final_score + tone_score
