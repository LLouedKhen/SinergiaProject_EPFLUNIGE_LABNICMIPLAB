clear; clc;

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Schaefer400';
Emotions= {'Anger','Anxiety','Contempt','Disgust','Fear','Happiness','Love','Satisfaction','Sad','Shame','Surprise'};

cd(bPath)
relFiles = dir('Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_*.nii');

for i = 1:length(relFiles)
    rfiles{i,1} = fullfile(bPath,relFiles(i).name);
end

cd(imgBetaPath)
sFolders = dir('sub-S*');

for i = 27:length(sFolders)
    thisFolder = fullfile(imgBetaPath, sFolders(i).name);
    cd(thisFolder)
    sModels = dir('FullModel__*_Ortho');
    s = 0;
    sprintf('Deleting VOI data for subject %d',i)
    for s = 1:length(sModels)
        thisModelP = fullfile(thisFolder, sModels(s).name);
        cd(thisModelP)
        delete VOI_Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm*
        %thisFile = fullfile(thisModelP,'SPM.mat');
        st = sModels(s).name;
        mName = extractBetween(st, 'FullModel__', 'AllPmod_Ortho');
        dirName1 = [mName{1}, '_Schaefer400_BetaSeries'];
        if exist(dirName1, 'dir')
            rmdir(dirName1, "s")
        end
        dirName2 = 'Schaefer400_BetaSeries';
        if exist(dirName2, 'dir')
            cd (dirName2)
            if exist('Anger', 'dir')
            cd Anger    
            foldercontent = dir();
            if numel(foldercontent) > 2
                cd (thisModelP)
            else
                cd ../../
                rmdir(dirName2, 's')
            end
            else 
                cd ../../
                rmdir(dirName2, 's')
            
            end
        end
    end
end




