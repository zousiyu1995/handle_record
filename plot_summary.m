clear
close all
clc

idiom = load_data('./output/idiom.json', 'idioms');
initial = load_data('./output/initial.json', 'initials');
final = load_data('./output/final.json', 'finals');
tone = load_data('./output/tone.json', 'tones');
attempt = load_data('./output/attempt.json', 'num_of_tries');
time = duration(loadjson('./output/time.json')); % histogram

fig = figure;
adjust_fig(fig);

ax_initials = axes('Position', [0.1, 0.83, 0.85, 0.15]);
b_initials = bar(ax_initials, ...
    reordercats(categorical(initial.initials), initial.initials), ...
    initial.counts);
text(ax_initials, b_initials.XEndPoints, b_initials.YEndPoints, string(b_initials.YData), ...
    'FontSize', 8, ...
    'HorizontalAlignment', 'center', ...
    'VerticalAlignment', 'bottom');
adjust_ax(ax_initials, "Initials", "Frequency")
ax_initials.YLim = [0, 350];

ax_finals = axes('Position', [0.1, 0.6, 0.85, 0.15]);
b_finals = bar(ax_finals, ...
    reordercats(categorical(final.finals), final.finals), ...
    final.counts);
text(ax_finals, b_finals.XEndPoints, b_finals.YEndPoints, string(b_finals.YData), ...
    'FontSize', 7, ...
    'HorizontalAlignment', 'center', ...
    'VerticalAlignment', 'bottom');
adjust_ax(ax_finals, "Finals", "Frequency")
ax_finals.YLim = [0, 600];

ax_tones = axes('Position', [0.1, 0.34, 0.38, 0.15]);
b_tones = bar(ax_tones, ...
    reordercats(categorical(tone.tones), {'1', '2', '3', '4'}), ...
    tone.counts);
text(ax_tones, b_tones.XEndPoints, b_tones.YEndPoints, string(b_tones.YData), ...
    'FontSize', 8, ...
    'HorizontalAlignment', 'center', ...
    'VerticalAlignment', 'bottom');
adjust_ax(ax_tones, "Tones", "Frequency")
ax_tones.YLim = [0, 1200];
ax_tones.YLabel.Position(1) = -0.14;

ax_num_of_tries = axes('Position', [0.57, 0.34, 0.38, 0.15]);
b_num_of_tries = bar(ax_num_of_tries, ...
    reordercats( ...
    categorical(attempt.num_of_tries), ...
    {'2', '3', '4', '5', '6', '7', '8', '9', '10', '11'} ...
    ), ...
    attempt.counts);
text(ax_num_of_tries, b_num_of_tries.XEndPoints, b_num_of_tries.YEndPoints, string(b_num_of_tries.YData), ...
    'FontSize', 8, ...
    'HorizontalAlignment', 'center', ...
    'VerticalAlignment', 'bottom');
adjust_ax(ax_num_of_tries, "Number of Tries", "Frequency")
ax_num_of_tries.YLim = [0, 35];
ax_num_of_tries.YLabel.Position(1) = -0.13;

ax_time_of_tries = axes('Position', [0.1, 0.1, 0.85, 0.15]);
h = histogram(time);
h.NumBins = 20;
h.FaceAlpha = 1;
h.BinWidth = duration('00:01:00');
text(ax_time_of_tries, h.BinEdges(2:end)-h.BinWidth/2, h.BinCounts, string(h.BinCounts), ...
    'HorizontalAlignment', 'center', ...
    'VerticalAlignment', 'bottom');
adjust_ax(ax_time_of_tries, "Time of Tries (minute)", "Frequency");
ax_time_of_tries.XLim = [duration('-00:01:00'), duration('00:26:00')];
ax_time_of_tries.XTick = duration(0, 0:1:25, 0);
ax_time_of_tries.XTickLabel = 0:1:25;
ax_time_of_tries.YLim = [0, 25];

print(fig, './summary.jpg', '-djpeg', '-painters', '-r600');

% fig_wc = figure;
% ax_wc = axes(fig_wc);
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
fig.Position(1:2) = [10, 5];
fig.Position(3:4) = [20, 18];
fig.Color = [1.0, 1.0, 1.0];
fig.Renderer = "painters";
end

function adjust_ax(ax, xlabel_string, ylabel_string)
ax.FontSize = 10;
ax.XLabel.String = xlabel_string;
ax.YLabel.String = ylabel_string;
ax.TickLength(1) = 0.005;
ax.YLabel.Units = 'normalized';
ax.YLabel.Position(1) = -0.06;
end
