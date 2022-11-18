clear; clc;

cd /home/loued
emoDict = readtable('CoreGridDictMF.csv', 'Delimiter',',');
M = {'AfterTheRain', 'BetweenViewings','BigBuckBunny','Chatter','FirstBite','LessonLearned'...
,'Payload', 'Sintel', 'Spaceman', 'Superhero', 'TearsOfSteel', 'TheSecretNumber','ToClaireFromSonny','YouAgain'};

sz = [30,14];
dT = cellstr('double');
vT = repmat(dT, 1,14);

movDataFill = table('Size',[30 14],'VariableTypes',vT', 'VariableNames',M);

rootDataPath = '/media/miplab-nas2/Data2/Movies_Emo/Raw_data';
homeDataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla';
cd(rootDataPath)

SubjFolders = dir('sub*');
remThis = 'DROPOUT';
for i = 1:length(SubjFolders)
        dropS(i) = contains(SubjFolders(i).name, remThis);
end

allSubjStruct = struct();
SubjFolders = SubjFolders(~dropS);

load /home/loued/ValItems.mat
Items = ValItems(~cellfun(@isempty, ValItems(:,1)), :);
clear ValItems


Times(2).start = BetweenViewings(:,1);
Times(2).dur = BetweenViewings(:,2) - BetweenViewings(:,1);
Times(2).ClipNum = length(BetweenViewings);
clear BetweenViewings

Times(3).start = BigBuckBunny(:,1);
Times(3).dur = BigBuckBunny(:,2) - BigBuckBunny(:,1);
Times(3).ClipNum = length(BigBuckBunny);
clear BigBuckBunny

Times(4).start = Chatter(:,1);
Times(4).dur = Chatter(:,2) - Chatter(:,1);
Times(4).ClipNum = length(Chatter);
clear Chatter

Times(5).start = FirstBite(:,1);
Times(5).dur = FirstBite(:,2) - FirstBite(:,1);
Times(5).ClipNum = length(FirstBite);
clear FirstBite

Times(6).start = LessonLearned(:,1);
Times(6).dur = LessonLearned(:,2) - LessonLearned(:,1);
Times(6).ClipNum = length(LessonLearned);
clear LessonLearned

Times(7).start = Payload(:,1);
Times(7).dur = Payload(:,2) - Payload(:,1);
Times(7).ClipNum = length(Payload);
clear Payload

Times(8).start = Sintel(:,1);
Times(8).dur = Sintel(:,2) - Sintel(:,1);
Times(8).ClipNum = length(Sintel);
clear Sintel

Times(9).start = Spaceman(:,1);
Times(9).dur = Spaceman(:,2) - Spaceman(:,1);
Times(9).ClipNum = length(Spaceman);
clear Spaceman

Times(10).start = Superhero(:,1);
Times(10).dur = Superhero(:,2) - Superhero(:,1);
Times(10).ClipNum = length(Superhero);
clear Superhero

Times(11).start = TearsOfSteel(:,1);
Times(11).dur = TearsOfSteel(:,2) - TearsOfSteel(:,1);
Times(11).ClipNum = length(TearsOfSteel);
clear TearsOfSteel

Times(12).start = TheSecretNumber(:,1);
Times(12).dur = TheSecretNumber(:,2) - TheSecretNumber(:,1);
Times(12).ClipNum = length(TheSecretNumber);
clear TheSecretNumber

Times(13).start = ToClaireFromSonny(:,1);
Times(13).dur = ToClaireFromSonny(:,2) - ToClaireFromSonny(:,1);
Times(13).ClipNum = length(ToClaireFromSonny);
clear ToClaireFromSonny

Times(14).start = YouAgain(:,1);
Times(14).dur =YouAgain(:,2) - YouAgain(:,1);
Times(14).ClipNum = length(YouAgain);
clear YouAgain






for i =1:length(SubjFolders)
sanCheck(i,1) = i;
subjStruct.Subject = [];
subjStruct.Subject.Session = [];
subjStruct.Subject.Session.Movie.Name = [];
subjStruct.Subject.Session.Movie.Num = [];
subjStruct.Subject.Session.Movie.Name.Name = [];
subjStruct.Subject.Session.Movie.Name.ClipNums = [];
subjStruct.Subject.Session.Movie.Name.ClipStart = [];
subjStruct.Subject.Session.Movie.Name.ClipDur = [];
subjStruct.Subject.Item1.Scores = [];
subjStruct.Subject.Item1.Name = [];
subjStruct.Subject.Item2.Scores = [];
subjStruct.Subject.Item2.Name = [];
subjStruct.Subject.Item3.Scores = [];
subjStruct.Subject.Item3.Name = [];
subjStruct.Subject.Item4.Scores = [];
subjStruct.Subject.Item4.Name = [];
subjStruct.Subject.Item5.Scores = [];
subjStruct.Subject.Item5.Name = [];


fullSF = fullfile(rootDataPath, SubjFolders(i).name);
subj = SubjFolders(i).name;
subjStruct.Subj = subj;


subjTable = table();
subjRes = {};


cd (fullSF)
theseDataFiles = dir('*_val.mat');
sanCheck(i,2) = sanCheck(i,2) + length(theseDataFiles);
theseDataFilesSub = [];
if isempty(theseDataFiles)
    warnMe = sprintf('Subject %s has no files at this level', subj);
    display(warnMe)
        sess = dir('ses*'); 
        emoResp ={};
        emoResp(1,:) = Items(i,:);

        for k = 1:length(sess)
            thisSubjSess = fullfile(fullSF, sess(k).name);
            cd (thisSubjSess)
            theseDataFilesSub = dir('*_val.mat');
            
            
            for j = 1:length(theseDataFilesSub)
                if regexp(theseDataFilesSub(j).name, 'mov\d\d')
                x = char(theseDataFilesSub(j).name);
                subjStruct.Subject.Session(k).Num = str2num(x(13));
                
                mfName = theseDataFilesSub(j).name;
                justMName = mfName(25:end-8);
                flagMe =["-","_"];
                if startsWith(justMName, flagMe)
                    justMName = justMName(2:end);
                   
                else 
                    display('Hand named?')
                    display (subj)
                end

                f = find(strcmp(justMName, M(1,:)));
                if movDataFill(i,f).Variables == 1
                    continue
                else 
                sanCheck(i,3) = sanCheck(i,3) + 1;

                 load(theseDataFilesSub(j).name);

                resp = Merged_Answers;
              
                clear Merged_Answers
                if i == 1 && size(resp, 1) ==1
                    resp = reshape(resp, length(resp)/5, 5);
                end
                  emoResp = [emoResp; num2cell(resp)];  
                
                                
                lenResp = length([resp(:,1); resp(:,2); resp(:,3); resp(:,4); resp(:,5)]);
                
                subjRes(k, j, :,1) = {[resp(:,1); resp(:,2); resp(:,3); resp(:,4); resp(:,5)]};
                subjRes(k, j, :,2) = {[ones(length(resp(:,1)), 1); repmat(2,length(resp(:,2)), 1); repmat(3,length(resp(:,3)), 1); repmat(4,length(resp(:,4)), 1); repmat(5,length(resp(:,5)), 1)]};
                subjRes(k, j, :,3) = {[repmat(Items(i,1),length(resp(:,1)), 1); repmat(Items(i,2),length(resp(:,2)), 1); repmat(Items(i,3),length(resp(:,3)), 1); repmat(Items(i,4),length(resp(:,4)), 1); repmat(Items(i,5),length(resp(:,5)), 1)]};
                subjRes(k, j, :,4) = {repmat((1:Times(f).ClipNum)', 5, 1)};
                subjRes(k, j, :,5) = {repmat(Times(f).start, 5, 1)};
                subjRes(k, j, :,6) = {repmat(Times(f).dur, 5, 1)};
                subjRes{k, j, :,7} = repmat(cellstr(subj), lenResp, 1);
                subjRes(k, j, :,8) = {repmat(str2num(x(13)), lenResp, 1)};
                subjRes{k, j, :,9} = repmat(cellstr(justMName), lenResp, 1);
               
                movDataFill(i,f).Variables = 1;

            
                





                
                
                end
                end
            end
        end
    else
        for j = 1:length(theseDataFiles)
                mfName = theseDataFiles(j).name;
                if regexp(theseDataFiles(j).name, 'mov\d\d')
                justMName = mfName(25:end-8);
                flagMe =["-","_"];
                if startsWith(justMName, flagMe)
                    justMName = justMName(2:end);
                   
                else 
                    display('Hand named?')
                    display (subj)
                 

                end
                f = find(strcmp(justMName, M(1,:)));
                

                load(theseDataFiles(j).name);
       
                x = char(theseDataFiles(j).name);
                

                resp = Merged_Answers;
                
                clear Merged_Answers
                if i == 1 && size(resp, 1) ==1
                    resp = reshape(resp, length(resp)/5, 5);
                end
                emoResp =  [emoResp; num2cell(resp)];
                lenResp = length([resp(:,1); resp(:,2); resp(:,3); resp(:,4); resp(:,5)]);
                
                subjRes(k, j, :,1) = {[resp(:,1); resp(:,2); resp(:,3); resp(:,4); resp(:,5)]};
                subjRes(k, j, :,2) = {[ones(length(resp(:,1)), 1); repmat(2,length(resp(:,2)), 1); repmat(3,length(resp(:,3)), 1); repmat(4,length(resp(:,4)), 1); repmat(5,length(resp(:,5)), 1)]};
                subjRes(k, j, :,3) = {[repmat(Items(i,1),length(resp(:,1)), 1); repmat(Items(i,2),length(resp(:,2)), 1); repmat(Items(i,3),length(resp(:,3)), 1); repmat(Items(i,4),length(resp(:,4)), 1); repmat(Items(i,5),length(resp(:,5)), 1)]};
                subjRes(k, j, :,4) = {repmat((1:Times(f).ClipNum)', 5, 1)};
                subjRes(k, j, :,5) = {repmat(Times(f).start, 5, 1)};
                subjRes(k, j, :,6) = {repmat(Times(f).dur, 5, 1)};
                subjRes{k, j, :,7} = repmat(cellstr(subj), lenResp, 1);
                subjRes(k, j, :,8) = {repmat(str2num(x(13)), lenResp, 1)};
                subjRes{k, j, :,9} = repmat(cellstr(justMName), lenResp, 1);
                
                    

 

        movDataFill(i,f).Variables = 1;
                end
        end
end
dataCheck = length(theseDataFiles) + length(theseDataFilesSub);
warnMe2 = sprintf('Subject has %d files.', dataCheck);
display(warnMe2)

sanCheck(i,4) = sanCheck(i,2) + sanCheck(i,3);
cd (homeDataPath)
    if exist(subj, 'dir') == 0
        mkdir (subj)
        cd(subj)
    else
        cd(subj)
    end

resThis = reshape(subjRes, size(subjRes,1) * size(subjRes,2), 9);
ItemScore = []; ItemNum = []; ItemName = []; ClipNum = []; TimeStart = []; TimeDur = []; SubjectNum = []; SessionNum = []; MovieName = []; 
%flagBadData
badData = [];
for r = 1:size(resThis,1)
    if size(resThis{r,4},1) > size(resThis{r,3},1)
        badData(r,1) = 1;
    else 
        badData(r,1) = 0;
    end
end
resThis = resThis(~badData,:);

for r = 1:length(resThis)
    ItemScore = [ItemScore; resThis{r,1}];
    ItemNum = [ItemNum; resThis{r,2}];
    ItemName = [ItemName; resThis{r,3}];
    ClipNum = [ClipNum; resThis{r,4}];
    TimeStart = [TimeStart; resThis{r,5}];
    TimeDur = [TimeDur; resThis{r,6}];
    SubjectNum = [SubjectNum; resThis{r,7}];
    SessionNum = [SessionNum; resThis{r,8}];
    MovieName = [MovieName; resThis{r,9}];
end

ItemScoreScaled = zscore(ItemScore);

resTable = table(ItemScore, ItemScoreScaled, ItemNum, ItemName, ClipNum, TimeStart, TimeDur, SubjectNum, SessionNum, MovieName);

cd /home/loued
emoTable = readtable('CoreGridDictMF.csv', 'Delimiter',',');



Component = cell(1,5);
for h = 1:size(emoResp,2)
    a = find(ismember(emoTable.Emotion, emoResp{1,h}));
    if a
    Component(1, h) = emoTable.Component(a);
    else 
        continue 
    end
end

if cellfun(@isempty,Component)
emoResp = emoResp(2:end, :);
else
emoResp = [Component; emoResp];
end

if sum(~contains(emoResp(1,:), 'Emotion')) == 5
    emoY{i,1} =0;
    emoY{i,2} = nan;
elseif sum(~contains(emoResp(1,:), 'Emotion')) == 4
    emoY{i,1}=1;
    emoY{i,2} = cellstr(subj);
elseif sum(~contains(emoResp(1,:), 'Emotion')) == 3
    emoY{i,1}=2;
    emoY{i,2} = cellstr(subj);
elseif sum(~contains(emoResp(1,:), 'Emotion')) == 2
    emoY{i,1}=3;
    emoY{i,2} = cellstr(subj);
elseif sum(~contains(emoResp(1,:), 'Emotion')) == 1
    emoY{i,1}=4;
    emoY{i,2} = cellstr(subj);
elseif sum(~contains(emoResp(1,:), 'Emotion')) == 0
    emoY{i,1}=5;
    emoY{i,2} = cellstr(subj);
    
end


mySubjPath = fullfile(homeDataPath, subj);

cd(mySubjPath)
fileName = [char(SubjFolders(i).name), '_Table.mat'];
save (fileName, 'resTable')
fileName2 = [char(SubjFolders(i).name), '_Table.csv'];

save (fileName2, 'resTable')

file3 = [char(SubjFolders(i).name), '_EmoResp.mat'];
save (file3, 'emoResp')

file4 = [char(SubjFolders(i).name), '_EmoResp.csv'];
save (file4, 'emoResp')


delete *struct.mat


cd (rootDataPath)
end

cd (homeDataPath)
file5 = 'SanityCheck.mat';
save(file5,"sanCheck")
bar([10, 11, 13, 14], [2, 1, 4, 23])
gcf
xlabel('Movies Rated')
ylabel('Number of Ss')
saveas(gcf,'MoviesWatchedPers.png')

writetable(movDataFill, 'MoviesRated.csv','Delimiter',',','QuoteStrings',true);

emoX = cell2table(emoY);
file6= 'emoCheck.mat';
save(file6, 'emoX')

bar([0, 1, 2, 3, 4], [sum(emoX.emoY1 == 0), sum(emoX.emoY1 == 1), sum(emoX.emoY1 == 2), sum(emoX.emoY1 == 3), sum(emoX.emoY1 == 4)])

gcf
xlabel('Emotions Rated')
ylabel('Number of Ss')
saveas(gcf,['EmotionsRatedPers.png'])
    

      
      

    

      
