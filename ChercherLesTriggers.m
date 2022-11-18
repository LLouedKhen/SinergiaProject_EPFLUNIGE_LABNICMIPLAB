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
Flags = [];
for i =1:length(SubjFolders)
    fullSF = fullfile(rootDataPath, SubjFolders(i).name);
    subj = SubjFolders(i).name;
    subjStruct.Subj = subj;

    subjTable = table();
    subjRes = {};

    cd (fullSF)
    theseDataFiles = dir('*_psy.mat');
    theseDataFilesSub = [];
    if isempty(theseDataFiles)
        warnMe = sprintf('Subject %s has no files at this level', subj);
        display(warnMe)
        sess = dir('ses*');
        for k = 1:length(sess)

            thisSubjSess = fullfile(fullSF, sess(k).name);
            cd (thisSubjSess)
            theseDataFilesSub = dir('*_psy.mat');

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


                        load(theseDataFilesSub(j).name);
                        trigger =Local_Experiment_time(1,7);
                        MStart = Trigger_times(2,1);
                        toAdd = MStart - trigger;


                        clear Local_Experiment_time Trigger_times VAS_score

                        cd (homeDataPath)

                        cd(subj)
                        file1 = ['PrefilmScanTime_', subj, justMName,'.mat']
                        save(file1, 'toAdd')
                        file2 = ['PrefilmScanTime_', subj, justMName, '.csv']
                        save(file2, 'toAdd')
                        cd(thisSubjSess)
                        Flags = +1;
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
                %%%%%%%%
                load(theseDataFilesSub(j).name);
                trigger =Local_Experiment_time(7,1);
                MStart = Trigger_times(2,1);
                toAdd = MStart - trigger;


                clear Local_Experiment_time Trigger_times VAS_score
                cd (homeDataPath)

                cd(subj)
                file1 = ['PrefilmScanTime_', subj, justMName,'.mat']
                save(file1, 'toAdd')
                file2 = ['PrefilmScanTime_', subj, justMName, '.csv']
                save(file2, 'toAdd')
                Flags = +1;
                movDataFill(i,f).Variables = 1;
                cd(thisSubjSess)
            end
        end
    end
    dataCheck = length(theseDataFiles) + length(theseDataFilesSub);
    warnMe2 = sprintf('Subject has %d files.', dataCheck);
    display(warnMe2)

    %flagBadData

end

