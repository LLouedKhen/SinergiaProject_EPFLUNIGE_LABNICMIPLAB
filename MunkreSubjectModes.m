clear; clc;
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/MunkResOut30Modes';
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD/CorrEmoWise';
dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/';
Emotions = {'Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise'};
Movies = {'AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain'};
Subjects = {'sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32'};

cd(dataPath)
CorrMats = dir('CorrMatSurpriseto_*_30ModesMu.csv');
for c = 1:length(CorrMats)
%for c = 1
startP = 'CorrMatSurpriseto_';
endP = '_30ModesMu.csv';
file = CorrMats(c).name;
SubEm = extractBetween(file, startP, endP);
SubEms = SubEm{1};
thisSub = SubEms(1:7);
thisEm = SubEms(8:end);
% thisMode = extractBetween(file, strcat(thisEm,'_Mode'), '.csv');
thisFile = fullfile(CorrMats(c).folder, CorrMats(c).name);
data = readtable(thisFile);
mData = data(2:end,2:end);
dataMat = table2array(mData);
% dataNMat = cellfun(@str2num, dataMat);
% % dataNMat = dataMat;
% for i = 1:length(dataMat)
%     for j = 1:length(dataMat)
%     x = cell2mat(dataMat(i,j));
%     dataNMat(i,j) = str2num(x);
%     end
% end
[ass, cost] = munkres(dataMat);
mRes.ass = ass;
mRes.cost = cost;
saveRes = struct2table(mRes);
cd(outPath)
fileN = strcat('MunkRes_', thisEm, '_Subject', thisSub, '_toSubject1.csv');
writetable(saveRes, fileN)
end