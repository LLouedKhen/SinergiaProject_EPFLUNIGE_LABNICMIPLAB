clear; clc;
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/MunkResOut';
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/CorrMat_FirstLast10Modes';
dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise';
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise'];
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain'];
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32'];

cd(dataPath)
CorrMats = dir('CorrMatS1*Mode*');
for c = 5992:length(CorrMats)
startP = 'CorrMatS1to_';
endP = '_Mode';
file = CorrMats(c).name;
thisSubEm = extractBetween(file, startP, endP);
thisSubEm = thisSubEm{1};
thisSub = thisSubEm(1:7);
thisEm = thisSubEm(8:end);
thisMode = extractBetween(file, [thisEm,'_'], '.csv');
thisFile = fullfile(CorrMats(c).folder, CorrMats(c).name);
data = readtable(thisFile);
mData = data(2:end,2:end);
dataMat = table2array(mData);
dataNMat = cellfun(@str2num, dataMat);
% % dataNMat = dataMat;
% for i = 1:length(dataMat)
%     for j = 1:length(dataMat)
%     x = cell2mat(dataMat(i,j));
%     dataNMat(i,j) = str2num(x);
%     end
% end
[ass, cost] = munkres(dataNMat);
mRes.ass = ass;
mRes.cost = cost;
saveRes = struct2table(mRes);
cd(outPath)
fileN = strcat('MunkRes_', thisSub, '_', thisEm, '_', thisMode, '.csv');
writetable(saveRes, fileN{1})
end