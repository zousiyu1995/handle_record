import json
from datetime import timedelta

from numpy import mean

from handlerecord import HandleRecord


def save_to_json(data, file_name: str) -> None:
    """save to json"""
    with open(file_name, mode='w+', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

    return None


def main() -> None:
    # get records
    with open("summary.json", "r", encoding="utf-8") as json_file:
        record = [HandleRecord(i) for i in json.load(json_file)]

        win = [i.win for i in record]
        time = [i.time for i in record]
        hint = [i.hint for i in record]
        phrase = list(HandleRecord.flatten([i.phrase for i in record]))
        idiom = list(HandleRecord.flatten([i.idiom for i in record]))
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
    print(f"去重后成语个数：{len(HandleRecord.list_to_sorted_dict(idiom))}个")

    print(f"总尝试：{sum(attempt)}次")
    print(f"最多尝试：{max(attempt)}次")
    print(f"最少尝试：{min(attempt)}次")
    print(f"平均尝试：{round(mean(attempt))}次")

    print(f"总用时：{HandleRecord.print_time(sum(time, timedelta(0, 0)))}")
    print(f"平均用时：{HandleRecord.print_time(mean(time))}")
    print(f"最长用时：{HandleRecord.print_time(max(time))}")
    print(f"最短用时：{HandleRecord.print_time(min(time))}")

    print(f"开局词最高分：{max(opening_phrase_score)}")
    print(f"开局词最低分：{min(opening_phrase_score)}")
    print(f"开局词平均分：{round(mean(opening_phrase_score))}")

    save_to_json(list(map(str, time)), "./output/time.json")
    save_to_json(HandleRecord.list_to_sorted_dict(idiom),
                 "./output/idiom.json")
    save_to_json(HandleRecord.list_to_sorted_dict(opening_idiom),
                 "./output/opening_idiom.json")
    save_to_json(HandleRecord.list_to_sorted_dict(opening_phrase_score),
                 "./output/opening_phrase_score.json")
    save_to_json(HandleRecord.list_to_sorted_dict(attempt),
                 "./output/attempt.json")
    save_to_json(HandleRecord.list_to_sorted_dict(initial),
                 "./output/initial.json")
    save_to_json(HandleRecord.list_to_sorted_dict(final),
                 "./output/final.json")
    save_to_json(HandleRecord.list_to_sorted_dict(tone), "./output/tone.json")

    return None


if __name__ == "__main__":
    main()
