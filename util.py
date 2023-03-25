import json
from collections import Counter
from datetime import timedelta
from typing import Iterable


class Util():
    @staticmethod
    def flatten(items: Iterable) -> Iterable:
        """
        flatten nested iterable object
        """
        for item in items:
            if isinstance(item,
                          Iterable) and not isinstance(item, (str, bytes)):
                for sub_item in Util.flatten(item):
                    yield sub_item
            else:
                yield item

    @staticmethod
    def list_to_sorted_dict(input_list: list) -> dict:
        """
        element->key, count of element->value, sort by value
        """

        return dict(
            sorted(Counter(list(Util.flatten(input_list))).items(),
                   key=lambda item: item[1],
                   reverse=True))

    @staticmethod
    def to_json(data, file_name: str) -> None:
        """save to json"""
        with open(file_name, mode='w+', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))

        return None

    @staticmethod
    def print_time(time: timedelta) -> str:
        """
        second(int) to 'xx天xx时xx分xx秒'(str)
        """

        if time.days:
            d = time.days
            m, s = divmod(time.seconds, 60)
            h, m = divmod(m, 60)
        else:
            d = 0
            m, s = divmod(time.seconds, 60)
            h, m = divmod(m, 60)

        return f"{d:02}天{h:02}时{m:02}分{s:02}秒"

        # if h == 0:
        #     return f"{m:02}分{s:02}秒"
        # else:
        #     return f"{h:02}时{m:02}分{s:02}秒"
