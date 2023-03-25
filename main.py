import json
from datetime import timedelta

from numpy import mean

from handlerecord import HandleRecord
from util import Util


def main() -> None:
    # get records
    with open("./handlerecord.json", "r", encoding="utf-8") as f:
        record = [HandleRecord(i) for i in json.load(f)]
        # record = HandleRecord(json.load(json_file)[-1])

        win = [i.win for i in record]
        time = [i.time for i in record]
        hint = [i.hint for i in record]
        phrase = list(Util.flatten([i.phrase for i in record]))
        idiom = list(Util.flatten([i.idiom for i in record]))
        score = [i.score for i in record]
        opening_idiom = [
            i.opening_idiom for i in record if i.opening_idiom != None
        ]
        opening_phrase_score = [i.opening_phrase_score for i in record]
        attempt = [i.attempt for i in record]
        initial = [i.initial for i in record]
        final = [i.final for i in record]
        tone = [i.tone for i in record]

    # summary
    print(
        f"游戏天数：{len(record)}天，获胜天数：{sum(win)}天，胜率：{round(100 * sum(win) / len(record))}%"
    )
    print(
        f"无提示游戏天数：{len(record)-sum(hint)}天，无提示游戏比率：{round(100 * (1 - sum(hint) / len(hint)))}%"
    )

    print(f"输入四字短语总个数：{len(phrase)}个")
    print(f"其中成语个数：{len(idiom)}个")
    print(f"其中成语占比：{round(100*len(idiom)/len(phrase))}%")
    print(f"去重后成语个数：{len(Util.list_to_sorted_dict(idiom))}个")

    print(f"总尝试：{sum(attempt)}次")
    print(f"最多尝试：{max(attempt)}次")
    print(f"最少尝试：{min(attempt)}次")
    print(f"平均尝试：{round(mean(attempt))}次")

    print(f"总用时：{Util.print_time(sum(time, timedelta(0, 0)))}")
    print(f"平均用时：{Util.print_time(mean(time))}")
    print(f"最长用时：{Util.print_time(max(time))}")
    print(f"最短用时：{Util.print_time(min(time))}")

    print(f"开局词最高分：{max(opening_phrase_score)}")
    print(f"开局词最低分：{min(opening_phrase_score)}")
    print(f"开局词平均分：{round(mean(opening_phrase_score))}")

    # save summary
    Util.to_json(list(map(str, time)), "./output/time.json")
    Util.to_json(Util.list_to_sorted_dict(idiom), "./output/idiom.json")
    Util.to_json(score, "./output/score.json")
    Util.to_json(Util.list_to_sorted_dict(opening_idiom),
                 "./output/opening_idiom.json")
    Util.to_json(Util.list_to_sorted_dict(opening_phrase_score),
                 "./output/opening_phrase_score.json")
    Util.to_json(Util.list_to_sorted_dict(attempt), "./output/attempt.json")
    Util.to_json(Util.list_to_sorted_dict(initial), "./output/initial.json")
    Util.to_json(Util.list_to_sorted_dict(final), "./output/final.json")
    Util.to_json(Util.list_to_sorted_dict(tone), "./output/tone.json")

    return None


if __name__ == "__main__":
    main()
