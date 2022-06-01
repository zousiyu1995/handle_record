clear
close all
clc

data = loadjson( ...
    './output_idioms.json', ...
    'UseMap', 1, ...
    'Encoding', 'UTF-8');
data = table(data.keys', data.values');
data.Properties.VariableNames = {'idiom', 'count'};
data.count = cell2mat(data.count);

wc_idiom = wordcloud(data, 'idiom', 'count');
wc_idiom.Title = '';