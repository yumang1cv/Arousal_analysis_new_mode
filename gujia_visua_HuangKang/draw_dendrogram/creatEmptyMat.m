function eMat = creatEmptyMat(points, Border, Sigma, stepSize)

% creating an empty matrix for density estimating
%
% Input
%   - points      -  2-D points 
%   - Border      -  add border around the density map
%   - Sigma       -  
%   - stepSize    -  
%
% Output
%   Estimated probability density 
%
% History
%   create  -  Kang Huang  (kang.huang@siat.ac.cn), 03-02-2020


% n_clus = max(tem_seg);

X = points(:,1);
Y = points(:,2);
N = length(X);

Xrange = [floor(min(X))-Border ceil(max(X))+Border];
Yrange = [floor(min(Y))-Border ceil(max(Y))+Border];

% stepSize = max([Xrange(2)-Xrange(1), Yrange(2)-Yrange(1)])/stepNum;

%Setup coordinate grid
[XX, YY] = meshgrid(Xrange(1):stepSize:Xrange(2), Yrange(1):stepSize:Yrange(2));
YY = flipud(YY);

%Parzen parameters and function handle
pf1 = @(C1,C2) (1/N)*(1/((2*pi)*Sigma^2)).*...
    exp(-( (C1(1)-C2(1))^2+ (C1(2)-C2(2))^2)/(2*Sigma^2));

PPDF = zeros(size(XX));

%Populate coordinate surface
[R, C] = size(PPDF);

XXX = [];
YYY = [];
for c = 1:C
    for r = 1:R
        XXX = [XXX, XX(1,c)];
        YYY = [YYY, YY(r,1)];
    end
end


eMat.PPDF = PPDF;
eMat.X = XXX;
eMat.Y = YYY;



