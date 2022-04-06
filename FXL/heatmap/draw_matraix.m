%% ª≠»»¡¶Õº
clear;
load('result_num.mat');
N = size(result_num,2);
for i  = 1:27
    all = result_num(i,:);
    for j = 1:N
        if all(1,j)== 1    % running
            a(i,j,1) = 169/255;  a(i,j,2) = 204/255;  a(i,j,3) = 224/255;
        elseif all(1,j)== 2  % walking
            a(i,j,1) = 35/255;  a(i,j,2) = 114/255;  a(i,j,3) = 169/255;
        elseif all(1,j)== 3  % Left Turning
            a(i,j,1) = 104/255;  a(i,j,2) = 166/255;  a(i,j,3) = 144/255;
        elseif all(1,j)== 4  % Rearing
            a(i,j,1) = 171/255;  a(i,j,2) = 211/255;  a(i,j,3) = 132/255;
        elseif all(1,j)== 5  % Right Turning
            a(i,j,1) = 53/255;  a(i,j,2) = 155/255;  a(i,j,3) = 58/255;
        elseif all(1,j)== 6  % Immobility
            a(i,j,1) = 240/255;  a(i,j,2) = 148/255;  a(i,j,3) = 148/255;
        elseif all(1,j)== 7  % Up Looking
           a(i,j,1) = 230/255;  a(i,j,2) = 87/255;  a(i,j,3) = 88/255;
        elseif all(1,j)== 8  % Hunching
            a(i,j,1) = 201/255;  a(i,j,2) = 33/255;  a(i,j,3) = 36/255;
        elseif all(1,j)== 9  % Grooming
            a(i,j,1) = 247/255;  a(i,j,2) = 188/255;  a(i,j,3) = 101/255;
        elseif all(1,j)== 10  % Sniffing
            a(i,j,1) = 239/255;  a(i,j,2) = 124/255;  a(i,j,3) = 26/255;
        elseif all(1,j)== 11  % Rising
            a(i,j,1) = 220/255;  a(i,j,2) = 148/255;  a(i,j,3) = 101/255;
        elseif all(1,j)== 12  % Flight
           a(i,j,1) = 200/255;  a(i,j,2) = 174/255;  a(i,j,3) = 207/255;
        elseif all(1,j)== 13  % Freezing
            a(i,j,1) = 101/255;  a(i,j,2) = 64/255;  a(i,j,3) = 144/255;
         else
            a(i,j,1) = 255/255;  a(i,j,2) = 255/255;  a(i,j,3) = 255/255;
        end
    end
end

h = figure();
set(h,'position',[100 100 800 400])
%j = copper;
%j(1,:) = [ 1 1 1 ];
%colormap(j);
%clims = [2 18];
imagesc(a);
m = [0 1800];
n = [15.5 15.5];
line(m,n,'linestyle','--','color','b','linewidth',1.5);
box off
xlabel('Time(s)','FontSize',18,'fontweight','bold');
set(gca, 'XTick',[0,300,600,900,1200,1500,1800]);
set(gca,'XTicklabel',{'0','10','20','30','40','50','60'},'fontsize',14,'fontweight','bold');

ylabel('Group','FontSize',18,'position',[-50,47],'fontweight','bold');
set(gca, 'YTick',[0,8,21.5,28]);
set(gca,'YTicklabel',{'','Male','Female',''},'TickLength',[0.005, 0.005],'fontsize',8,'fontweight','bold');
set(gca,'YTicklabelRotation',90);

