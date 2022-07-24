# 汉兜猜词记录

## 成语词典

`idiom`文件夹储存成语字典。

`./idiom/idiom_chinese_xinhua_full.json`是来自[pwxcoo/chinese-xinhua开源项目](https://github.com/pwxcoo/chinese-xinhua)的成语字典，包含3万余条成语。

`./idiom/THUOCL_chengyu.txt`是来自[THUOCL：清华大学开放中文词库](http://thuocl.thunlp.org/)的成语字典，包含8000余条成语。

`./idiom/idiom_Handle.txt`是来自开源项目[汉兜 Handle](https://github.com/antfu/handle)的成语字典，包含2万余条成语，好像缺一些常见成语。

## 程序

`handlerecord.json`储存有每日的猜词记录，含日期、时间、是否提示和猜测所用的成语列表，纯手工打造。

`handlerecord.py`是主类，用于分析每天的猜词记录。

`main.py`是主函数，循环分析并储存所有的猜词记录。

`plot_wordcloud.py`用于绘制词云。

`wc_mask.png`是词云的形状蒙版。

`qiji-combo.tff`是词云的字体，来自开源项目[齊伋體 qiji-font](https://github.com/LingDong-/qiji-font)。

`plot_summary.m`用于生成猜词记录统计图。

## 词云输出效果

![词云输出效果](./wc_idiom.jpg)

## 猜词记录统计

![猜词记录统计](./summary.jpg)
