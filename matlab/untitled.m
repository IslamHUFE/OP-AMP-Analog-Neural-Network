filename = 'C:\Users\tarek m eid\Desktop\freelancer\AANN\ltspice\Draft2.txt';
fid = fopen(filename, 'r');

all_data = {};
current_data = [];

while true
    line = fgetl(fid);
    if ~ischar(line)
        break
    end

    if contains(line, 'Step Information')
        if ~isempty(current_data)
            all_data{end+1} = current_data;
            current_data = [];
        end
        continue
    end

    nums = sscanf(line, '%f %f');
    if length(nums) == 2
        current_data = [current_data; nums'];
    end
end

if ~isempty(current_data)
    all_data{end+1} = current_data;
end

fclose(fid);

% رسم كل sweeps
figure; hold on; grid on;
for k = 1:length(all_data)
    t = all_data{k}(:,1);
    y = all_data{k}(:,2);
    plot(t, y);
end

% افترض أنك رسمت الجراف الآن
fig = gcf;

set(fig, 'PaperPositionMode', 'auto');
set(fig, 'InvertHardcopy', 'off');

set(gca, 'LooseInset', max(get(gca,'TightInset'), 0.001)*[1 1 1 1]);

print(fig, 'cropped_plot', '-dpdf', '-r300'); 
