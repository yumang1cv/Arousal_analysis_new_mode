%%
genPath = genpath('C:/Users/12517/Desktop/PostAnalysis222(1)');
addpath(genPath)

working_path = 'D:/3D_behavior/Arousal_behavior/Arousal_result_all';

nfeatures = 16;
selection = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14];
% selection = [1, 3];

BA.Cen = 1;
BA.VA = 1;
BA.CenIndex = 13;
BA.VAIndex = 14;
BA.SDSize = 25;
BA.SDSDimens = [40,41,42];

save_path = [working_path, '/body_scatter_class'];
if ~exist(save_path, 'dir')
    mkdir(save_path)
end

%% data, correction_3D
% dataname_list = {'rec-1-Moedl-20210902154720','rec-1-sham-20210902142949','rec-2-Moedl-20210902155917',...
%                  'rec-2-sham-20210902144146','rec-3-Moedl-20210902161217','rec-3-sham-20210902145419'};
dataname_struct = dir([working_path,'/3Dskeleton/Calibrated_3DSkeleton/','*_Cali_Data3d.csv']);
dataname_list = cell(length(dataname_struct), 1);
for i_name = 1:length(dataname_struct)
    dataname_cell = {dataname_struct.name}';
    name_split = strsplit(dataname_cell{i_name}, '_');
    dataname_list{i_name} = name_split{1};
end

method = 'median filtering';
WinWD = 1000;
fs = 30;
ali_XY = []; raw_XY = []; vel_XY = []; labels = []; reMap = [];
single_frame = 1;
for i_num = 1:length(dataname_list)
    data3d = importdata([working_path,'/3Dskeleton/Calibrated_3DSkeleton/',dataname_list{i_num},'_Cali_Data3d.csv']);
    tempdata = fillmissing(data3d.data, 'linear');
    RawData.X = tempdata(:,1:3:nfeatures*3);
    RawData.Y = tempdata(:,2:3:nfeatures*3);
    RawData.Z = tempdata(:,3:3:nfeatures*3);
    
    raw = zeros(nfeatures*3, size(RawData.X,1));
    PreproData = correction_3D(RawData, method, WinWD, fs);
    raw(1:3:end, :) = PreproData.X';
    raw(2:3:end, :) = PreproData.Y';
    raw(3:3:end, :) = PreproData.Z';
    raw_XY = [raw_XY, raw];
    
    vel = diff(raw')';
    vel = [vel, vel(:, end)];
    vel_XY = [vel_XY, vel];
    
    BeA_DecData_XYZ = body_alignment(PreproData, BA);
    ali_XY = [ali_XY, BeA_DecData_XYZ];
    
    feature_space_csv = importdata([working_path,'/BeAMapping/',dataname_list{i_num},'_Feature_Space.csv']).data;
    labels = [labels; feature_space_csv(:,1)];
    single_boundary = feature_space_csv(:,2)';
    boundary = [0, single_boundary(1:end-1)] + single_frame;
    reMap = [reMap, boundary];
    single_frame = single_frame + size(RawData.X,1);

    disp(['Read data: ', num2str(i_num), ' -> ', num2str(length(dataname_list))]);
end
reMap = [reMap, single_frame];
n_clus = max(unique(labels));


%% 画图1
n_genColor = 12;
cclr = (cbrewer2('Dark2', n_genColor));
[X, Y] = meshgrid([1:3], [1:n_clus]);
if n_clus > n_genColor
    clr = interp2(X(round(linspace(1, n_clus, n_genColor)), :), Y(round(linspace(1, n_clus, n_genColor)), :), cclr, X, Y);
else
    clr = cclr(1:n_clus, :);
end



% label_order = [1];
% label_order = [1, 3];
label_order = 1:40;
n_clus1 = length(label_order);
[avg_coord, avg_skeleton, clus_energy, limXY, limZ] = extrct_AvgMouse(reMap,...
            ali_XY, vel_XY, labels, label_order, nfeatures, n_clus1, selection);



for i = 1:n_clus1
    ilabel = label_order(i);
    tem_idx = find(labels == ilabel);
    
    temClus_aliXYZ = [];
    temClus_velXYZ = [];
    for iseg = 1:length(tem_idx)
        selectedIdx = reMap(tem_idx(iseg)) : reMap(tem_idx(iseg)+1)-1;
        temAliXYZ = (ali_XY(:, selectedIdx));
        temAliVel = (vel_XY(:, selectedIdx));
        temClus_aliXYZ = cat(3, temClus_aliXYZ, reshape(temAliXYZ, 3, nfeatures, size(temAliXYZ, 2)));
        temClus_velXYZ = cat(3, temClus_velXYZ, reshape(temAliVel, 3, nfeatures, size(temAliVel, 2)));
    end
    
    tem_avg_coord = avg_coord{1, i};
    tem_avg_skeleton = avg_skeleton{1, i};
    tem_clus_energy = clus_energy{1, i};
    
    figure(131)
%     subplot(1, 2, 1); 
    hold on;
    mouse_CloudXY(avg_skeleton, avg_coord, clus_energy, selection, temClus_aliXYZ, limXY, limZ, i)
    view([90, 90])
    print(gcf, '-djpeg', [save_path, '/', num2str(i), '_XY.jpg'], '-r300');
    savefig([save_path, '/', num2str(i), '_XY.fig']);
    close 131

    figure(132)
%     subplot(1, 2, 2); 
    hold on;
    mouse_CloudXZ(avg_skeleton, avg_coord, clus_energy, selection, temClus_aliXYZ, limXY, limZ, i)
    view([90, 90])
    print(gcf, '-djpeg', [save_path, '/', num2str(i), '_XZ.jpg'], '-r300');
    savefig([save_path, '/', num2str(i), '_XZ.fig']);
    close 132
    
    figure(133)
%     subplot(1, 2, 2);
    hold on;
    mouse_CloudXZ(avg_skeleton, avg_coord, clus_energy, selection, temClus_aliXYZ, limXY, limZ, i)
    view([90, 90])
    print(gcf, '-djpeg', [save_path, '/', num2str(i), '_XZ.jpg'], '-r300');
    savefig([save_path, '/', num2str(i), '_XZ.fig']);
    close 132

%     drawnow
    disp(['Plot figure: ', num2str(i), ' -> ', num2str(n_clus1)]);
end



