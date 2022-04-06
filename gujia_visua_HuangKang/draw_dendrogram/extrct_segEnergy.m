function [ClusSeg_eneH, ClusSeg_eneZ, group] = ...
    extrct_segEnergy(reMap, vel_XY, labels, label_order, selection)

nfeatures = 16;
n_clus = length(unique(labels));

ClusSeg_eneH = [];
ClusSeg_eneZ = [];
ClusSeg_eneMeanH = zeros(1, n_clus);
ClusSeg_eneMeanZ = zeros(1, n_clus);
ClusSeg_eneStderrH = zeros(1, n_clus);
ClusSeg_eneStderrZ = zeros(1, n_clus);
group = [];

for i_clus = 1:n_clus
    ilabel = label_order(i_clus);
    tem_idx = find(labels == ilabel);
    
    temSeg_eneH = zeros(1, length(tem_idx));
    temSeg_eneZ = zeros(1, length(tem_idx));
    for i_seg = 1:length(tem_idx)
        selectedIdx = reMap(tem_idx(i_seg)) : reMap(tem_idx(i_seg)+1)-1;
        temAliVel = (vel_XY(:, selectedIdx));
        temSegEne = power(reshape(temAliVel, 3, nfeatures, size(temAliVel, 2)), 2);
        
        energy_temX = reshape(temSegEne(1, selection, :), length(selection), size(temSegEne, 3));
        energy_temY = reshape(temSegEne(2, selection, :), length(selection), size(temSegEne, 3));
        energy_temZ = reshape(temSegEne(3, selection, :), length(selection), size(temSegEne, 3));
        energy_temH = energy_temX + energy_temY;
        
        temSeg_eneH(i_seg) = mean(mean(energy_temH, 2));
        temSeg_eneZ(i_seg) = mean(mean(energy_temZ, 2));

    end
    
    ClusSeg_eneH = [ClusSeg_eneH, temSeg_eneH];
    ClusSeg_eneZ = [ClusSeg_eneZ, temSeg_eneZ];
    group = [group, i_clus*ones(1, length(tem_idx))];
    ClusSeg_eneMeanH(i_clus) = mean(temSeg_eneH);
    ClusSeg_eneMeanZ(i_clus) = mean(temSeg_eneZ);
    ClusSeg_eneStderrH(i_clus) = std(temSeg_eneH, 0, 2) / sqrt(size(temSeg_eneH, 2));
    ClusSeg_eneStderrZ(i_clus) = std(temSeg_eneZ, 0, 2) / sqrt(size(temSeg_eneZ, 2));
    
end

maxEneH = max(ClusSeg_eneMeanH+ClusSeg_eneStderrH); minEneH = min(ClusSeg_eneMeanH-ClusSeg_eneStderrH);
maxEneZ = max(ClusSeg_eneMeanZ+ClusSeg_eneStderrH); minEneZ = min(ClusSeg_eneMeanZ-ClusSeg_eneStderrZ);

ClusSeg_eneH = (ClusSeg_eneH - minEneH)/(maxEneH - minEneH);
ClusSeg_eneZ = (ClusSeg_eneZ - minEneZ)/(maxEneZ - minEneZ);








