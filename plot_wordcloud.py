"""
author: zousiyu
date: 2022.06.01
plot 'handle' (汉兜) data
"""

import json

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from wordcloud import WordCloud


def read_data(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


# idioms = read_data("./output/opening_idiom.json")  # 开局词
idioms = read_data("./output/idiom.json")  # 所有输入的成语

# generate word cloud
wc_fig = plt.figure()
wc_ax = wc_fig.add_axes([0.025, 0.025, 0.95, 0.95])
wc_mask = np.array(Image.open("./wc_mask.png"))
wc_font = r"./qiji-combo.ttf"
wc = WordCloud(mask=wc_mask,
               prefer_horizontal=1,
               background_color="white",
               font_path=wc_font,
               max_font_size=300,
               max_words=1300,
               relative_scaling=0.6,
               width=5000,
               height=5000 * 0.618)
wc.generate_from_frequencies(idioms)
wc_ax.axis("off")
plt.imshow(wc)
wc_fig.savefig("./wc_idiom.jpg", dpi=1000)

plt.show()
