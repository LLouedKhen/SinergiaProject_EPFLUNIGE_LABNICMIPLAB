clear; clc;

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/HCPex_v1.0/HCPex_v1.0/ROIs';

cd(bPath)
relFiles = dir('HCPex_2mm_*_roi.mat');

for i = 1:length(relFiles)
files{i,1} = fullfile(bPath,relFiles(i).name);
end

rois = {};
for i =1:length(files)
    rois{i}= maroi(files{i,1});
    thisRoi = rois{i};
    name = relFiles(i).name(1:end-8);
    save_as_image(thisRoi, fullfile(bPath, [name, '.nii']));
end



    