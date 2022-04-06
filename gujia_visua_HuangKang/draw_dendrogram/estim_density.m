function PDF = estim_density(points, Border, Sigma, stepSize)

% estemating density map of points
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
D = [X, Y];
N = length(X);

Xrange = [floor(min(X))-Border ceil(max(X))+Border];
Yrange = [floor(min(Y))-Border ceil(max(Y))+Border];


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
        for d = 1:N
            PPDF(r,c) = PPDF(r,c) + ...
                pf1([XX(1,c) YY(r,1)],[D(d,1) D(d,2)]);
        end
        XXX = [XXX, XX(1,c)];
        YYY = [YYY, YY(r,1)];
    end
end

%Normalize data
m1 = max(PPDF(:));
PPDF = PPDF / m1;

PDF.PPDF = PPDF;
PDF.X = XXX;
PDF.Y = YYY;



