function align_XYZ = body_alignment(data_3d, paras)
%% varible connection--read
cenflag = paras.Cen;
VAflag = paras.VA;
CenIndex = paras.CenIndex;
VAIndex = paras.VAIndex;
SDSize = paras.SDSize;
SDSDimens = paras.SDSDimens;
X = data_3d.X';
Y = data_3d.Y';
Z = data_3d.Z';

%% varible re-assignment
raw_XY = [];
for k = 1:size(X,1)
    raw_XY = [raw_XY;X(k,:);Y(k,:)];	
end

%% body alignment
if cenflag == 1 && VAflag ~=1
    mean_X = mean(raw_XY(1:2:(end-1),:));
    mean_Y = mean(raw_XY(2:2:end,:));
    white_XY = raw_XY;
    white_XY(1:2:(end-1),:) = white_XY(1:2:(end-1),:)-mean_X;
    white_XY(2:2:end,:) = white_XY(2:2:end,:)-mean_Y;
    back_X = white_XY((CenIndex*2-1),:);
    back_Y = white_XY((CenIndex*2),:);
    back_XY = white_XY;
    back_XY(1:2:(end-1),:) = back_XY(1:2:(end-1),:)-back_X;
    back_XY(2:2:end,:) = back_XY(2:2:end,:)-back_Y;
    out_XY = back_XY;
elseif cenflag == 1 && VAflag == 1
    mean_X = mean(raw_XY(1:2:(end-1),:));
    mean_Y = mean(raw_XY(2:2:end,:));
    white_XY = raw_XY;
    white_XY(1:2:(end-1),:) = white_XY(1:2:(end-1),:)-mean_X;
    white_XY(2:2:end,:) = white_XY(2:2:end,:)-mean_Y;
    back_X = white_XY((CenIndex*2-1),:);
    back_Y = white_XY((CenIndex*2),:);
    back_XY = white_XY;
    back_XY(1:2:(end-1),:) = back_XY(1:2:(end-1),:)-back_X;
    back_XY(2:2:end,:) = back_XY(2:2:end,:)-back_Y;
    root_tail_X = back_XY((VAIndex*2-1),:);
    root_tail_Y = back_XY((VAIndex*2),:);
    rot_alpha = -atan2(root_tail_Y,root_tail_X);
    rot_XY = zeros(size(back_XY));
    for m = 1:size(rot_alpha,2)
        rot_mat = [cos(rot_alpha(1,m)),sin(rot_alpha(1,m)),0;...
                    -1*sin(rot_alpha(1,m)),cos(rot_alpha(1,m)),0;...
                    0,0,1];
        temp_rot = ...
            [back_XY(1:2:(end-1),m),back_XY(2:2:end,m),ones(size(rot_XY,1)/2,1)]*rot_mat;
        rot_XY(1:2:(end-1),m) = temp_rot(:,1);
        rot_XY(2:2:end,m) = temp_rot(:,2);
    end
    out_XY = rot_XY;
else
    out_XY = raw_XY;
    newinfo = 'without alignment';
    addMes2log(1, newinfo, 0, 1, 0, 0, 0)
end

mean_Z = mean(Z);
white_Z = Z;
white_Z = white_Z-mean_Z;
out_XYZ = [];
for k = 1:size(Z,1)
    out_XYZ = [out_XYZ;out_XY(k*2-1:k*2,:);white_Z(k,:)];	
end

%% body size correction
temp_XYZ = out_XYZ;
body_size = (temp_XYZ(SDSDimens(1,1),:).^2+temp_XYZ(SDSDimens(1,2),:).^2+temp_XYZ(SDSDimens(1,3),:).^2).^0.5;
median_index = median(body_size);
corr_prop = SDSize./median_index;
% corr_prop = 1;
out_XYZ = temp_XYZ*corr_prop;

%% varible connection--write
% BeA_DecParam.BA = BA;
align_XYZ = out_XYZ;


