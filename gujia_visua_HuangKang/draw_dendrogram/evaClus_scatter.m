function [rIntra, rInter] = evaClus_scatter(sort_label, sort_distMat, n_clus, label_order, i_clus)


sort_label = flipud(sort_label);

n_genColor = 10;
cclr = (cbrewer2('Paired', n_genColor));
[X, Y] = meshgrid([1:3], [1:n_clus]);
if n_clus > n_genColor
    clr = interp2(X(round(linspace(1, n_clus, n_genColor)), :), Y(round(linspace(1, n_clus, n_genColor)), :), cclr, X, Y);
else
    clr = cclr;
    
end


hold on
idx = label_order(i_clus);
tem_clr = clr(idx, :);
intra_idx = sort_label == idx;
inter_idx = sort_label ~= idx;

tem_nIntra = sum(intra_idx);
tem_nInter = sum(inter_idx);

sub_distMatIntra = sort_distMat(intra_idx, :);
sub_distMatInter = sort_distMat(inter_idx, :);

idxIntraA = zeros(1, tem_nIntra);
randA_idxIntra = randperm(tem_nIntra, round(tem_nIntra/2));
idxIntraA(randA_idxIntra) = 1;
idxIntraB = ~idxIntraA;
idxInterB = randperm(tem_nInter, sum(idxIntraB));

sub_distMatIntraA = sub_distMatIntra(find(idxIntraA), :);
sub_distMatIntraB = sub_distMatIntra(find(idxIntraB), :);
sub_distMatInterB = sub_distMatInter(find(idxInterB), :);

dataIntraA = []; dataIntraB = []; dataInterB = [];
for n = 1:size(sub_distMatIntraA, 1)
    for m = 1:size(sub_distMatIntraB, 1)
        temIntraA = sub_distMatIntraA(n, :);
        temIntraB = sub_distMatIntraB(m, :);
        temInterB = sub_distMatInterB(m, :);
        rand_plot = randperm(length(sort_label), 3);
        dataIntraA = [dataIntraA, temIntraA(rand_plot)];
        dataIntraB = [dataIntraB, temIntraB(rand_plot)];
        dataInterB = [dataInterB, temInterB(rand_plot)];
    end
end

[rInter, ~, ~] = regression(dataIntraA, dataInterB);
scatter(dataIntraA, dataInterB, 2,...
    'MarkerFaceColor', [.7 .7 .7 ], 'MarkerEdgeColor', 'none', 'LineWidth', 0.1)

[rIntra, m, b] = regression(dataIntraB, dataIntraA);
yReg = m*dataIntraA + b;
scatter(dataIntraA, dataIntraB, 2, ...
    'MarkerFaceColor', tem_clr, 'MarkerEdgeColor', 'none', 'LineWidth', 0.1)
plot(dataIntraA, yReg, 'Color', 'k')

set(gca, 'Color', 'none', 'xlim', [0, 1], 'ylim', [0, 1])
hold off



