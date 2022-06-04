import json

# covert idiom from chinese xinhua
with open("idioms_from_chinese_xinhua_full.json", "r",
          encoding="utf-8") as json_file:
    idioms = [item['word'] for item in json.load(json_file)]

with open("idioms_from_chinese_xinhua_simple.json",
          mode="w+",
          encoding="utf-8") as file:
    file.write(json.dumps(idioms, ensure_ascii=False, indent=4))

# convert idiom from THUOCL
with open("./idioms_from_THUOCL_chengyu.txt", "r", encoding="utf-8") as file:
    idioms = [line.split()[0] for line in file]

with open("./idioms_from_THUOCL_chengyu.json", "w+", encoding="utf-8") as file:
    file.write(json.dumps(idioms, ensure_ascii=False, indent=4))

# convert idiom from handle
with open("./idioms_from_handle.txt", "r", encoding="utf-8") as file:
    idioms = [line.split()[0] for line in file]

with open("./idioms_from_handle.json", "w+", encoding="utf-8") as file:
    file.write(json.dumps(idioms, ensure_ascii=False, indent=4))


# merge three list
def load_json(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


big_idioms = list(
    set(
        load_json("./idioms_from_THUOCL_chengyu.json") +
        load_json("./idioms_from_chinese_xinhua_simple.json") +
        load_json("./idioms_from_handle.json")))

with open("./big_idioms.json", "w+", encoding="utf-8") as f:
    f.write(json.dumps(big_idioms, ensure_ascii=False, indent=4))
