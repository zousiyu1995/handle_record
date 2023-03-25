import json

# covert idiom from chinese xinhua
with open("./idiom_chinese_xinhua_full.json", "r",
          encoding="utf-8") as json_file:
    idioms = [item['word'] for item in json.load(json_file)]

with open("./idiom_chinese_xinhua_simple.json", mode="w+",
          encoding="utf-8") as file:
    file.write(json.dumps(idioms, ensure_ascii=False, indent=4))

# convert idiom from THUOCL
with open("./idiom_THUOCL_chengyu.txt", "r", encoding="utf-8") as file:
    idioms = [line.split()[0] for line in file]

with open("./idiom_THUOCL_chengyu.json", "w+", encoding="utf-8") as file:
    file.write(json.dumps(idioms, ensure_ascii=False, indent=4))

# convert idiom from handle
with open("./idiom_Handle.txt", "r", encoding="utf-8") as file:
    idioms = [line.split()[0] for line in file]

with open("./idiom_Handle.json", "w+", encoding="utf-8") as file:
    file.write(json.dumps(idioms, ensure_ascii=False, indent=4))


# merge three list
def load_json(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


# 合并三个成语字典，造一个“成语大词典”
big_idioms = list(
    set(
        load_json("./idiom_THUOCL_chengyu.json") +
        load_json("./idiom_chinese_xinhua_simple.json") +
        load_json("./idiom_handle.json")))

with open("./idiom_big_dictionary.json", "w+", encoding="utf-8") as f:
    f.write(json.dumps(big_idioms, ensure_ascii=False, indent=4))
