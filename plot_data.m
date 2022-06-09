clear
close all
clc

idioms = load_data('./output/idioms.json', 'idioms');
initials = load_data('./output/initials.json', 'initials');
finals = load_data('./output/finals.json', 'finals');
tones = load_data('./output/tones.json', 'tones');
num_of_tries = load_data('./output/num_of_tries.json', 'num_of_tries');

time_of_tries = duration(loadjson('./output/time_of_tries.json')); % histogram

fig = figure;
adjust_fig(fig);

ax_initials = axes('Position', [0.1, 0.75, 0.85, 0.2]);
bar(ax_initials, ...
    reordercats(categorical(initials.initials), initials.initials), ...
    initials.counts);
adjust_ax(ax_initials, "Initials", "Frequency")

ax_finals = axes('Position', [0.1, 0.45, 0.85, 0.2]);
bar(ax_finals, ...
    reordercats(categorical(finals.finals), finals.finals), ...
    finals.counts);
adjust_ax(ax_finals, "Finals", "Frequency")

ax_tones = axes('Position', [0.1, 0.1, 0.38, 0.2]);
bar(ax_tones, ...
    reordercats(categorical(tones.tones), {'1', '2', '3', '4', '_'}), ...
    tones.counts);
adjust_ax(ax_tones, "Tones", "Frequency")

ax_num_of_tries = axes('Position', [0.57, 0.1, 0.38, 0.2]);
bar(ax_num_of_tries, ...
    reordercats(categorical(num_of_tries.num_of_tries), {'2', '3', '4', '5', '6', '7', '8', '9', '10', '11'}), ...
    num_of_tries.counts);
adjust_ax(ax_num_of_tries, "Number of Tries", "Frequency")

print(fig, './summary.jpg', '-djpeg', '-painters', '-r600');
% wc_idiom = wordcloud( ...
%     idioms, ...
%     idioms.Properties.VariableNames{1}, idioms.Properties.VariableNames{2});
% wc_idiom.Title = '';

function data = load_data(file_name, type)
data = loadjson( ...
    file_name, ...
    'UseMap', 1, ...
    'Encoding', 'UTF-8');

data = table( ...
    data.keys', cell2mat(data.values'), ...
    'VariableNames', {type, 'counts'} ...
    );
% sort table
data = sortrows(data, 'counts', 'descend');
end

function adjust_fig(fig)
fig.Units = 'centimeters';
fig.Position(1:2) = [10, 10];
fig.Position(3:4) = [20, 14];
fig.Color = [1.0, 1.0, 1.0];
fig.Renderer = "painters";
end

function adjust_ax(ax, xlabel_string, ylabel_string)
ax.FontSize = 10;
ax.XLabel.String = xlabel_string;
ax.YLabel.String = ylabel_string;
end
