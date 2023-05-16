clear; clc
%remove results since they include artifact annotations

mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/';
imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
delete matlabbatch.mat
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Raw_annotations/ParticipantTasks/Means2';
rPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/';

cd (mainPath)
subjFolders = dir('sub-*');
for i = 1:length(subjFolders)
    sub = subjFolders(i).name(1:7);
    folderN = fullfile(mainPath, subjFolders(i).name);
    cd(folderN)
    sessF = dir('ses*');
    mRegFile = {};
    movPath = {};
    for s = 1:length(sessF)
        sessFolder = fullfile(folderN, sessF(s).name);
        cd(sessFolder)
        mF = dir('pp_*');
        for m = 1:length(mF)
            if ~contains(mF(m).name,'Rest')
                movF = fullfile(sessFolder, mF(m).name);
                cd(movF)

                mReg = dir('Regressors.txt');

                mRegFile = fullfile(movF, mReg.name);
                movPath= fullfile(movF);

                movNamesRegs = {};
                sessStr =['ses-' num2str(s)];

                if contains(mRegFile, sessStr)
                    movName1 = extractBetween(mRegFile, 'ses-', '.feat');
                    movName2 = extractAfter(movName1, sub);
                    movName = extractAfter(movName2, [sessStr,'_']);
                    movNamesRegs = [movNamesRegs, movName];
                end

                %                 movNamesRegs = movNamesRegs';

                bf = fullfile(rPath, sub);
                cd(bf)

                scanTimes = dir('PrefilmScanTime_*.mat');
                for triT = 1:length(scanTimes)
                    tTimes{triT} = scanTimes(triT).name;
                end

                scIdx = find(contains(tTimes, movName));
                if isempty(scIdx)
                    continue
                else
                    load(scanTimes(scIdx).name)
                    clear tTimes


                    cd (bPath)
                    regsS = dir('DF_*');
                    theseRegFile = {};
                    emReg = [];
                    for mN = 1:length(regsS)

                        regFile = regsS(mN).name;
                        if  contains(regFile, movName)
                            thisFile =fullfile(bPath,regsS(mN).name);
                            %                         theseRegFile(mN) = cellstr(regsS(mN).name);


                            %                         if contains(tTimes, movName)
                            %                         keep = 1;
                            %                         scIdx = find(contains(tTimes, movName));
                            %                         load(scanTimes(scIdx).name)
                            %                         end
                        end
                    end
                    %                 theseRegFile = theseRegFile(~cellfun('isempty',theseRegFile));


                    cd(imgBetaPath)
                    if ~exist(sub, 'dir')
                        mkdir(sub)
                    end
                    cd(sub)

                    csName = ['FullModel_', '_',char(movName),'_AllPmod_AFD_OrthOn'];

                    if ~exist(csName, 'dir')
                        mkdir(csName)
                    end
                    rmdir(csName, 's')
                end
            end
        end
    end
end

