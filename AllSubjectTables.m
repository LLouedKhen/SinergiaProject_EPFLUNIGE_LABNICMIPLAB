clear; clc;


homeDataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/';
cd(homeDataPath)

load 'emoCheck.mat'

SubjFolders = dir('sub*');

allTables = table();
allEmoTables = table();


for i =1:length(SubjFolders)
    fullSF = fullfile(homeDataPath, SubjFolders(i).name);
    cd (fullSF)
    thisTable = dir('*_Table.mat');
    load (thisTable.name)
    allTables = [allTables; resTable];
end

file1 = 'AllTables_Table.mat';
file2 = 'AllTables_Table.csv';


cd(homeDataPath)
save(file1, 'allTables')
save(file2, 'allTables')

emo = unique(allTables.ItemName);

cd /home/loued
emoTable = readtable('CoreGridDictMF.csv', 'Delimiter',',');

allTables.Component = cell(height(allTables),1);
allTables.BMF = cell(height(allTables),1);
allTables.BMFComponent = cell(height(allTables),1);

for i = 1:height(allTables)
    a = find(ismember(emoTable.Emotion, allTables.ItemName(i)));
    allTables.Component(i) = emoTable.Component(a);
    allTables.BMF(i) = emoTable.BMF(a);
    allTables.BMFComponent(i) = emoTable.BMFComponent(a);
end

cd(homeDataPath)
file1 = 'AllTables_Table.mat';
writetable(allTables, 'AllTables_Table.csv','Delimiter',',','QuoteStrings',true);

% file2 = 'AllEmoTables_Table.mat';
% writetable(allEmoTables, 'AllTables_EmoTable.csv','Delimiter',',','QuoteStrings',true);

save(file1, 'allTables')

% emoByCompT = allTables(strcmp(allTables.Component(:), 'Emotion'), :);

whichRows = [];
for i = 1:height(allTables)
s = allTables.SubjectNum{i} ;   

whichRows(i) =  any(strcmp(s, emoX.emoY2));
end

emoData = allTables(logical(whichRows'), :);

szT = [height(emoData)/5,25];
dTypes = {'string', 'string',  'string','double','double','string', 'double', 'string', 'double','string', 'double','string', 'double', 'string', 'string', 'double', 'string', 'string', 'double', 'string', 'string', 'double', 'string', 'string', 'double', 'double'};
tVarNames = {'Subject','Clip', 'Movie', 'Start', 'Dur', 'Emotion1Name', 'Emotion1Score', 'Emotion2Name', 'Emotion2Score','Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score', ...
     'Component1Name', 'Component1Type', 'Component1Score',  'Component2Name', 'Component2Type', 'Component2Score',  'Component3Name', 'Component3Type', 'Component3Score',  'Component4Name', 'Component4Type', 'Component4Score','Session'};

allEM = table();
 %emLMT.Properties.VariableNames = {'Sub','Clip', 'Movie', 'Start', 'Dur', 'Emotion1Name', 'Emotion1Score', 'Emotion2Name', 'Emotion2Score','Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score', ...
     %'Component1Name', 'Component1Type', 'Component1Score',  'Component2Name', 'Component2Type', 'Component2Score',  'Component3Name', 'Component3Type', 'Component3Score',  'Component4Name', 'Component4Type', 'Component4Score'}
% kSub = unique(emoData.SubjectNum(:));
% vSub =  1:length(kSub);
% kMove = sort(unique(emoData.MovieName(:)));
% vMove = 1:length(kMove);
% kEmoN = unique(emoData.)

s = unique(emoData.SubjectNum);

m = unique(emoData.MovieName);
for su = 1:length(s)  
    sub = s(su);
    emLMT = table();
 
    emf = emoX.emoY1(find(strcmp(sub{1}, emoX.emoY2(:))));
    miniTable1 = emoData(find(ismember(emoData.SubjectNum(:),sub)),:);
    
    for em = 1:length(m)
        mov = m{em};

        miniTable2 =  miniTable1(find(ismember(miniTable1.MovieName(:),mov)),:);
       for clip = 1:max(miniTable2.ClipNum)

        cl = emoData.ClipNum(em);
        miniTable3 =  miniTable2(find(ismember(miniTable2.ClipNum(:), clip)),:);
        clT = 1: height(miniTable2)/5;

        stT = [1, 26];
        thisTable =table('Size', stT, 'VariableTypes', dTypes, 'VariableNames',tVarNames);
        emidx = find(strcmp(miniTable3.Component(:), 'Emotion'));
        if isempty(emidx)
            continue
        else
        r = [1:5]';
        emnidx = find(sum(r == emidx',2) ==0);
        
        sprintf('Processing subject %s watching movie %s clip %d',char(sub),char(mov), clip)

    tic

    thisTable.Subject(clip) = miniTable3.SubjectNum(emidx(1));
    thisTable.Clip(clip) = miniTable3.ClipNum(emidx(1));
    thisTable.Movie(clip) =  miniTable3.MovieName(emidx(1));
    thisTable.Start(clip) =miniTable3.TimeStart(emidx(1));
    thisTable.Dur(clip) =  miniTable3.TimeDur(emidx(1));
    thisTable.Session(clip) =  miniTable3.SessionNum(emidx(1));
    
    toc
    tic
    if emf ==1

    thisTable.Emotion1Name(clip) = miniTable3.ItemName(emidx(1));
    thisTable.Emotion1Score (clip) =  miniTable3.ItemScore(emidx(1));
    thisTable.Emotion2Name (clip) = nan;
    thisTable.Emotion2Score (clip) = nan;
    thisTable.Emotion3Name(clip) = nan;
    thisTable.Emotion3Score(clip) = nan;
    thisTable.Emotion4Name(clip) = nan;
    thisTable.Emotion4Score(clip) = nan;


    thisTable.Component1Name(clip) =  miniTable3.ItemName(emnidx(1));
    thisTable.Component1Type(clip) = miniTable3.Component(emnidx(1));
    thisTable.Component1Score(clip) =  miniTable3.ItemScore(emnidx(1));
    thisTable.Component2Name(clip) =  miniTable3.ItemName(emnidx(2));
    thisTable.Component2Type(clip) =  miniTable3.Component(emnidx(2));
    thisTable.Component2Score (clip) =  miniTable3.ItemScore(emnidx(2));
    thisTable.Component3Name(clip) = miniTable3.ItemName(emnidx(3));
    thisTable.Component3Type(clip) =  miniTable3.Component(emnidx(3));
    thisTable.Component3Score(clip) = miniTable3.ItemScore(emnidx(3));
    thisTable.Component4Name(clip) = miniTable3.ItemName(emnidx(4));
    thisTable.Component4Type(clip) = miniTable3.Component(emnidx(4));
    thisTable.Component4Score(clip) =  miniTable3.ItemScore(emnidx(4));



    elseif emf ==2

    thisTable.Emotion1Name(clip) = miniTable3.ItemName(emidx(1));
    thisTable.Emotion1Score (clip) = miniTable3.ItemScore(emidx(1));
    thisTable.Emotion2Name(clip) =  miniTable3.ItemName(emidx(2));
    thisTable.Emotion2Score(clip) = miniTable3.ItemScore(emidx(2));
    thisTable.Emotion3Name(clip) = nan;
    thisTable.Emotion3Score(clip) = nan;
    thisTable.Emotion4Name(clip) = nan;
    thisTable.Emotion4Score(clip) = nan;


    thisTable.Component1Name(clip) =miniTable3.ItemName(emnidx(1));
    thisTable.Component1Type(clip) = miniTable3.Component(emnidx(1));
    thisTable.Component1Score(clip) = miniTable3.ItemScore(emnidx(1));
    thisTable.Component2Name(clip) =  miniTable3.ItemName(emnidx(2));
    thisTable.Component2Type(clip) =miniTable3.Component(emnidx(2));
    thisTable.Component2Score(clip) = miniTable3.ItemScore(emnidx(2));
    thisTable.Component3Name(clip) =  miniTable3.ItemName(emnidx(3));
    thisTable.Component3Type(clip) = miniTable3.Component(emnidx(3));
    thisTable.Component3Score(clip) = miniTable3.ItemScore(emnidx(3));
    thisTable.Component4Name(clip) = nan;
    thisTable.Component4Type(clip) = nan;
    thisTable.Component4Score(clip) =  nan;

    elseif emf ==3

    thisTable.Emotion1Name(clip) = miniTable3.ItemName(emidx(1));
    thisTable.Emotion1Score(clip) =  miniTable3.ItemScore(emidx(1));
    thisTable.Emotion2Name(clip) =  miniTable3.ItemName(emidx(2));
    thisTable.Emotion2Score(clip) =  miniTable3.ItemScore(emidx(2));
    thisTable.Emotion3Name(clip) = miniTable3.ItemName(emidx(3));
    thisTable.Emotion3Score(clip) =  miniTable3.ItemScore(emidx(3));
    thisTable.Emotion4Name(clip) = nan;
    thisTable.Emotion4Score(clip) = nan;
    


    thisTable.Component1Name(clip) =  miniTable3.ItemName(emnidx(1));
    thisTable.Component1Type(clip) = miniTable3.Component(emnidx(1));
    thisTable.Component1Score(clip) =  miniTable3.ItemScore(emnidx(1));
    thisTable.Component2Name(clip) =  miniTable3.ItemName(emnidx(2));
    thisTable.Component2Type(clip) =  miniTable3.Component(emnidx(2));
    thisTable.Component2Score(clip) =  miniTable3.ItemScore(emnidx(2));
    thisTable.Component3Name(clip) = nan;
    thisTable.Component3Type(clip) = nan;
    thisTable.Component3Score(clip) =  nan;
    thisTable.Component4Name(clip) = nan;
    thisTable.Component4Type(clip) = nan;
    thisTable.Component4Score(clip) =  nan;

    

    elseif emf == 4

    thisTable.Emotion1Name(clip) = miniTable3.ItemName(emidx(1));
    thisTable.Emotion1Score(clip) =  miniTable3.ItemScore(emidx(1));
    thisTable.Emotion2Name(clip) =  miniTable3.ItemName(emidx(2));
    thisTable.Emotion2Score(clip) = miniTable3.ItemScore(emidx(2));
    thisTable.Emotion3Name(clip) =  miniTable3.ItemName(emidx(3));
    thisTable.Emotion3Score(clip) = miniTable3.ItemScore(emidx(3));
    thisTable.Emotion4Name(clip) =  miniTable3.ItemName(emidx(4));
    thisTable.Emotion4Score(clip) =  miniTable3.ItemScore(emidx(4));


    thisTable.Component1Name(clip) =  miniTable3.ItemName(emnidx(1));
    thisTable.Component1Type(clip) =  miniTable3.Component(emnidx(1));
    thisTable.Component1Score(clip) =  miniTable3.ItemScore(emnidx(1));
    thisTable.Component2Name(clip) = nan;
    thisTable.Component2Type(clip) = nan;
    thisTable.Component2Score(clip) =  nan;
    thisTable.Component3Name(clip) = nan;
    thisTable.Component3Type(clip) = nan;
    thisTable.Component3Score(clip) =  nan;
    thisTable.Component4Name(clip) = nan;
    thisTable.Component4Type(clip) = nan;
    thisTable.Component4Score(clip) =  nan;
    end
    toc
    tic
%   
%    fTable1 =ismissing(thisTable.Subject);
%    thisTable =  thisTable(~fTable1, :);
   emLMT = [emLMT; thisTable];
   toc
        end
       end
       tic
%         fTable2 =ismissing(emLMT.Subject);
%         emLMT = emLMT(~fTable2, :);
        emLMTc = [emLMT;emLMT];
    toc
    end

        cd(homeDataPath)
        if ~isempty(emLMT)
        fTable3 =ismissing(emLMT.Subject);
        emLMTd = emLMTc(~fTable3, :);
        fullSF = fullfile(homeDataPath, char(sub));
        fullSF
        cd (fullSF)
        char(sub)
        writetable(emLMTd, [char(sub), 'emByTrial_Table.csv'],'Delimiter',',','QuoteStrings',true);
        allEM = [allEM; emLMTd];
        else 
            continue
  
        end
        
end
% 
% fTable3 =ismissing(emLMT.Subject);
% emLMTc = emLMT(~fTable3, :);


cd(homeDataPath)
 
writetable(allEM, 'emByTrial_Table.csv','Delimiter',',','QuoteStrings',true);