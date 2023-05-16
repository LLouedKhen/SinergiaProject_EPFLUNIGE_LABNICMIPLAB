clear; clc;

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Schaefer400';
Emotions= {'Anger','Anxiety','Contempt','Disgust','Fear','Happiness','Love','Satisfaction','Sad','Shame','Surprise'};

cd(imgBetaPath)
sFolders = dir('sub-S*');

relSubs= {'sub-S05', 'sub-S07', 'sub-S15', 'sub-S16', 'sub-S17'};
for i = 1: length(sFolders)
keep(i) = ismember(sFolders(i).name, relSubs);
end

sFolders = sFolders(keep);

for i = 1:length(sFolders)
    thisFolder = fullfile(imgBetaPath, sFolders(i).name);
    cd(thisFolder)
    sModels = dir('FullModel__*Ortho');
    s = 0;
    sprintf('Deleting VOI data for subject %s',sFolders(i).name)
    for s = 1:length(sModels)
        dirName1 = fullfile(thisFolder, sModels(s).name, 'Schaefer400_BetaSeries');

      
        if exist(dirName1, 'dir')
            rmdir(dirName1, "s")
        end


    end
end





