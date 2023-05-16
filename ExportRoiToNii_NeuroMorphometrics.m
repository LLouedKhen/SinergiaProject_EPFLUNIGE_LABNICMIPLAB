clear; clc;

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Neuromorphometrics';

cd(bPath)
relFiles = dir('atlas_neuromorphometrics*_roi.mat');

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



    