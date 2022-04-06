clc;clear;
namelist = dir('D:\3D_behavior\Arousal_behavior\Arousal_result_all\body_scatter_class\*.fig');

% 读取后namelist 的格式为
% name -- filename
% date -- modification date
% bytes -- number of bytes allocated to the file
% isdir -- 1 if name is a directory and 0 if not

len = length(namelist);
for i = 2:2:len
    file_name{i}=namelist(i).name;
    %uiopen('D:\3D_behavior\Arousal_behavior\Arousal_result_all\body_scatter_class\11_XY.fig',1);
%     uiopen(file_name{i},1);
    file=openfig(file_name{i});
    %去除上右边框刻度
    box off  
    %移除坐标轴边框
    set(gca,'Visible','off');
    %设置背景为白色
    set(gcf,'color','w');
%     set(gcf,'color','none');
    %view(180,0);  %XZ旋转角度
    view(180,0);
    fig_name = strcat('fig',num2str(i), '.tiff');
%     imwrite(file.cdata ,fig_name,'Resolution', 600);
%     saveas(file,fig_name,'tiff');
    exportgraphics(file,fig_name,'Resolution',3000);
%     sprint(figname,'completed')
    close
end


% uiopen('D:\3D_behavior\Arousal_behavior\Arousal_result_all\body_scatter_class\11_XY.fig',1);
% %去除上右边框刻度
% box off  
% %移除坐标轴边框
% set(gca,'Visible','off');
% %设置背景为白色
% set(gcf,'color','w');
% % set(gcf,'color','none');
% %view(180,0);  %XZ旋转角度
% view(180,0);
