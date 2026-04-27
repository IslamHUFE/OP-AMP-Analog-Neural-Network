filename = 'C:\Users\tarek m eid\Desktop\freelancer\AANN\ltspice\Draft2.txt';
fid = fopen(filename, 'r');

all_data = {};
current_data = [];

while true
    line = fgetl(fid);
    if ~ischar(line)
        break
    end

    % اذا كانت السطر من نوع Step Information → نبدأ sweep جديد
    if contains(line, 'Step Information')
        if ~isempty(current_data)
            all_data{end+1} = current_data;
            current_data = [];
        end
        continue
    end

    % نحاول قراءة سطرين: time و value
    nums = sscanf(line, '%f %f');
    if length(nums) == 2
        current_data = [current_data; nums'];
    end
end

% أضف آخر sweep
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

% ========== إعدادات تجعل MATLAB يقص الشكل تمامًا ==========
set(fig, 'PaperPositionMode', 'auto');   % اجعل حجم الطباعة مطابق لحجم النافذة
set(fig, 'InvertHardcopy', 'off');       % احتفظ بالألوان الأصلية

% اضبط الـ LooseInset ليكون صغير جداً
set(gca, 'LooseInset', max(get(gca,'TightInset'), 0.001)*[1 1 1 1]);

% الآن اطبع الشكل PDF مقصوص تماماً
print(fig, 'cropped_plot', '-dpdf', '-r300'); 
