clear; clc;
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/MovieEmo_DMDImages';
dataPath1 = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/SecondLevel_EmotionsMU_OrthOnQC';
dataPath2 = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/SecondLevel_EmotionsFD_OrthOnQC';

dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/';
Emotions = {'Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise'};
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain'];
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32'];

cd(dataPath1)
muimgs = dir(fullfile('**/*FWE.nii')); 
for f = 1:length(muimgs)
    mui{f} = fullfile(muimgs(f).folder, muimgs(f).name);
end
cd(dataPath2)
fdimgs = dir(fullfile('**/*FWE.nii')); 
for f = 1:length(fdimgs)
    fdi{f} = fullfile(fdimgs(f).folder, fdimgs(f).name);
end

cd(outPath)
firstMimgs = dir(fullfile('Brain_FirstMode_*.nii')); 
rimgs = dir(fullfile('Brain_FirstConj_r_Mode*.nii')); 
iimgs = dir(fullfile('Brain_FirstConj_i_Mode*.nii'));

dmdImgs = [firstMimgs; rimgs; iimgs];
for f = 1:length(dmdImgs)
    dmdi{f} = fullfile(dmdImgs(f).folder, dmdImgs(f).name);
end


allimgs = [mui, fdi, dmdi]';

for i = 1:length(Emotions)
    thisEm = Emotions{i};
    thisEm = strfind(allimgs, 'Anger');
    keep = find(~cellfun(@isempty,thisEm));
    thisCell = allimgs(keep);
    spm_check_registration(char(thisCell));
end