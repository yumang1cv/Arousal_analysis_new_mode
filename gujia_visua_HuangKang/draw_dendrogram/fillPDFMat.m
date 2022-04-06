function bodyCloudMat = fillPDFMat(bodyCloudMat, bodySubCloudMat, weight)

[nBodyRow, ~] = size(bodyCloudMat.PPDF);
[nRow, nCol] = size(bodySubCloudMat.PPDF);
subPPDF = bodySubCloudMat.PPDF;
bodyXX = bodyCloudMat.X;
bodyYY = bodyCloudMat.Y;


for ic = 1:nCol
    subRowData = subPPDF(:, ic);
    subXX = bodySubCloudMat.X(nRow*(ic-1)+1 : ic*nRow);
    subYY = bodySubCloudMat.Y(nRow*(ic-1)+1 : ic*nRow);
    rowLocIdx = find(bodyXX == subXX(1));
    rowLocIdx = ceil(rowLocIdx(1)/nBodyRow);
    colLocIdx = mod(find(bodyYY(1:nBodyRow) == subYY(1)), nBodyRow);
    orgclusCloudPPDF = bodyCloudMat.PPDF(colLocIdx:colLocIdx+nRow-1, rowLocIdx);
    bodyCloudMat.PPDF(colLocIdx:colLocIdx+nRow-1, rowLocIdx) = subRowData*weight + orgclusCloudPPDF;

end


