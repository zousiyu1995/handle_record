import json

from pypinyin import Style, pinyin

from util import Util


class Idiom():
    def __init__(self, idiom: str) -> None:
        # 成语
        self.idiom = idiom.replace("，", "").replace("、", "")
        # 成语长度
        self.length = len(self.idiom)
        # 成语的声母、韵母和声调
        self.initial, self.final, self.tone = self.__get_pinyin(self.idiom)

    def __get_pinyin(self, phrase: list) -> tuple[list, list, list]:
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


def main():
    with open("./idiom/idiom_big_dictionary.json", "r", encoding="utf-8") as f:
        idiom = [Idiom(i) for i in json.load(f)]

        initial = [i.initial for i in idiom]
        final = [i.final for i in idiom]
        tone = [i.tone for i in idiom]

        Util.to_json(Util.list_to_sorted_dict(initial),
                     "./output/initial_all_idiom.json")
        Util.to_json(Util.list_to_sorted_dict(final),
                     "./output/final_all_idiom.json")
        Util.to_json(Util.list_to_sorted_dict(tone),
                     "./output/tone_all_idiom.json")
        print("done!")


if __name__ == "__main__":
    main()
