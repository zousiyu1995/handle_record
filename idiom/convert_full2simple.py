import json

with open("idiom_from_chinese_xinhua_full.json", "r",
          encoding="utf-8") as json_file:
    idiom = [item['word'] for item in json.load(json_file)]

with open("idiom_from_chinese_xinhua_simple.json", mode="w+",
          encoding="utf-8") as file:
    file.write(json.dumps(idiom, ensure_ascii=False, indent=4))
