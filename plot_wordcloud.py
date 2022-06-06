"""
author: zousiyu
date: 2022.06.01
plot 'handle' (汉兜) data
"""

import json
from typing import TextIO  # for type hints
from matplotlib import pyplot as plt

# for wordcloud
import numpy as np
from wordcloud import WordCloud
from PIL import Image


def read_data(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


idioms = read_data("./output/idioms.json")

# generate word cloud
wc_fig = plt.figure()
wc_ax = wc_fig.add_axes([0.025, 0.025, 0.95, 0.95])
wc_mask = np.array(Image.open("./wc_mask.png"))
wc_font = r"./qiji-combo.ttf"
wc = WordCloud(prefer_horizontal=1,
               background_color="white",
               font_path=wc_font,
               max_font_size=500,
               relative_scaling=1,
               mask=wc_mask,
               width=2000,
               height=2000 * 0.618)
wc.generate_from_frequencies(idioms)
wc_ax.axis("off")
plt.imshow(wc)
wc_fig.savefig("./wc_idiom.jpg", dpi=1000)

plt.show()
