%% preparation
% input: looming

%%
clear;
load('looming.mat');
N = size(looming,1);


%% select segments
for i = 1:N
    data = looming{i,7};
    s = looming{i,6};
    j = s+2;
    mark = looming{i,j};
    st = mark;
    ed = mark+1799;
    seg = data(st:ed,1);
    a = tabulate(seg);
        a(14,3) = 0;
        b = a(:,3)/100;
    result_num(i,:) = seg';
    result_percent(i,:) = b(1:13,1)';
end
temp(1:15,:) = result_num(13:27,:);  % male
temp(16:27,:) = result_num(1:12,:);  % female
clear result_num
result_num = temp;
save result_num.mat result_num