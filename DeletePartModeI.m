clear; clc;

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Schaefer400';
Emotions= {'Anger','Anxiety','Contempt','Disgust','Fear','Happiness','Love','Satisfaction','Sad','Shame','Surprise'};

cd(imgBetaPath)
sFolders = dir('sub-S*');

for i = 1:length(sFolders)
    thisFolder = fullfile(imgBetaPath, sFolders(i).name);
    cd(thisFolder)
    sModels = dir('PartModel*');
    s = 0;
    sprintf('Deleting VOI data for subject %d',i)
    for s = 1:length(sModels)
        thisModelP = fullfile(thisFolder, sModels(s).name, 'Schaefer    ');

        dirName1 = sModels(s).name;
        if exist(dirName1, 'dir')
            rmdir(dirName1, "s")
        end


    end
end





