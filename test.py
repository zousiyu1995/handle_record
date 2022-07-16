from util import get_pinyin, compare_list, get_score

initials, finals, tones = get_pinyin("纸上谈兵")
print(initials)
print(finals)
print(tones)

a = [1, 2, 3]
b = [1, 3, 4]
print(compare_list(a, b))

idiom1 = "矢志不渝"
idiom2 = "矢中不渝"
get_score(idiom1, idiom2)
