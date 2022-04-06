function [avg_coord, avg_skeleton, clus_energy, limHor, limVert] = ...
    extrct_AvgMouse(reMap, ali_XY, vel_XY, labels, label_order, nfeatures, n_clus, selection)

avg_skeleton = cell(1, n_clus);
avg_coord = cell(1, n_clus);
clus_energy = cell(1, n_clus);

maxEneH = zeros(1, n_clus); minEneH = zeros(1, n_clus);
maxEneZ = zeros(1, n_clus); minEneZ = zeros(1, n_clus);
for i_clus = 1:n_clus
    ilabel = label_order(i_clus);
    tem_idx = find(labels == ilabel);
    
    temClus_aliXY = [];
    temClus_velXY = [];
    for iseg = 1:length(tem_idx)
        selectedIdx = reMap(tem_idx(iseg)) : reMap(tem_idx(iseg)+1)-1;
        temAliXY = (ali_XY(:, selectedIdx));
        temAliVel = (vel_XY(:, selectedIdx));
        temClus_aliXY = cat(3, temClus_aliXY, reshape(temAliXY, 3, nfeatures, size(temAliXY, 2)));
        temClus_velXY = cat(3, temClus_velXY, reshape(temAliVel, 3, nfeatures, size(temAliVel, 2)));
    end
    
    if ~isempty(tem_idx)
        avg_skeleton{1, i_clus} = mean(temClus_aliXY, 3);
        avg_coord{1, i_clus} = reshape(avg_skeleton{1, i_clus}, nfeatures*3, 1);
        clus_energy{1, i_clus} = power(temClus_velXY, 2);
        
        tem_clus_energy = clus_energy{1, i_clus};
        energy_temX = reshape(mean(tem_clus_energy(1, selection, :), 1), length(selection), size(tem_clus_energy, 3));
        energy_temY = reshape(mean(tem_clus_energy(2, selection, :), 1), length(selection), size(tem_clus_energy, 3));
        energy_temZ = reshape(mean(tem_clus_energy(3, selection, :), 1), length(selection), size(tem_clus_energy, 3));
        
        energy_temMeanH = mean(energy_temX + energy_temY, 2);
        energy_temMeanZ = mean(energy_temZ, 2);
        
        stderrH = std(sqrt(energy_temX.^2 + energy_temY.^2), 0, 2) / sqrt(size(sqrt(energy_temX.^2 + energy_temY.^2), 2));
        stderrZ = std(energy_temZ, 0, 2) / sqrt(size(energy_temZ, 2));
        
        maxEneH(i_clus) = max(energy_temMeanH+stderrH); minEneH(i_clus) = min(energy_temMeanH-stderrH);
        maxEneZ(i_clus) = max(energy_temMeanZ+stderrZ); minEneZ(i_clus) = min(energy_temMeanZ-stderrZ);
    end
end
limHor = [floor(min(minEneH)), ceil(max(maxEneH))];
limVert = [floor(min(minEneZ)), ceil(max(maxEneZ))];




