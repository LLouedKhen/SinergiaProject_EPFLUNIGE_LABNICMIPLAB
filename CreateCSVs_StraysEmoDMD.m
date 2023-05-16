clear; clc;

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
savePath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Schaefer400';
Emotions= {'Anger','Anxiety','Contempt','Disgust','Fear','Happiness','Love','Satisfaction','Sad','Shame','Surprise'};

cd(bPath)
relFiles = dir('Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_*.nii');

for i = 1:length(relFiles)
    rfiles{i,1} = fullfile(bPath,relFiles(i).name);
end

cd(imgBetaPath)
sFolders = dir('sub-S*');

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
    sModels = dir('FullModel__*_Ortho');
    s = 0;
    for s = 1:length(sModels)
        thisModelP = fullfile(thisFolder, sModels(s).name);
        cd(thisModelP)

        st = sModels(s).name;
        mName = extractBetween(st, 'FullModel__', 'AllPmod_Ortho');
        dirName = 'Schaefer400_BetaSeries';
        if exist(dirName, 'dir')
            cd(dirName)
            vDirName = fullfile(thisModelP, dirName);

            for em = 1:length(Emotions)
                thisEm = Emotions{em};
                thisFolder2 = fullfile(vDirName, thisEm);
                if exist(thisFolder2, 'dir')
                cd(thisFolder2)
                voiF = dir('VOI_*.mat');
                if length(voiF) > 0
                for r = 1:length(voiF)
                    rFile{r,1} = voiF(r).name;
                    thisF = rFile{r};
                    numR = extractBetween(thisF, '1mm_', '_');
                    rnum(r,1) = str2num(numR{1});
                end
                tF = table(rFile, rnum);
                idx = 1:length(rFile);
                stF = tF(idx,:);
                stF.idx = idx';
                srFiles = stF.rFile;
                [nstF,idx] = sortrows(stF,'rnum', 'ascend');
                nstFF = nstF;


                %find potentially missing VOI
%                 errV = diff(nstF.rnum);
% 
%                 mv = find(errV> 1);
%                
%                 sk = errV(mv);
%                 
%                 for g = 1:length(sk)
%                     if sk(g) > 2
%                         allInserts = mv(g):mv(g) + (sk(g) -1);
%                         mv = [mv; allInserts'];
%                     end
%                 end
% 
%                  mv = sort(unique(mv));
%                  k = cell2mat(strfind(nstF.rFile(:),'VOI_Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_400_1.mat'));
%                  if isempty(k) 
%                      mv = [mv; 400];
%                  end
                %how many mistakes
%                 fErr = sk -1;
%                 allErr = sum(fErr);
%                 for er = 1:allErr
%                     if sk(er) > 2
%                         mv = [mv; mv(er) + (sk(er) -1)]
%                     end
%                 end
               
                
                perfect = 1:400;
                real = sort(nstF.rnum);
                disc = setdiff(perfect, real);

                if length(disc) > 0
                    for d = 1:length(disc)
                    nstFF.rnum(end + 1) = disc(d);
                    end
                end
                [nstFFF,idx1] = sortrows(nstFF,'rnum', 'ascend');

                srFiles = nstFFF.rFile;
                srNum = nstFFF.rnum;
                thisSubMovieEm = [];
                for rf = 1:400
                    if rf == nstFFF.rnum(rf) && ~ismember(rf,disc)
                        load(srFiles{rf})
                        thisLen = length(Y);
                        prevLen = length(thisSubMovieEm);
                        if thisLen > prevLen
                            Y = Y(1:prevLen);
                        elseif thisLen < prevLen
                            thisSubMovieEm = thisSubMovieEm(1:thisLen, :);
                        end
                        thisSubMovieEm = [thisSubMovieEm, Y];
                    else
                        Y = zeros(length(thisSubMovieEm),1);
                        thisSubMovieEm = [thisSubMovieEm, Y];
                    end
                end
                cd(savePath)
                if exist(thisEm, 'dir')
                    cd(thisEm)
                else
                    mkdir(thisEm)
                    cd(thisEm)
                end
                writematrix(thisSubMovieEm, ['BetaSeries_',char(sFolders(i).name), '_', mName{1}, thisEm, '.csv'], 'Delimiter', ',', 'QuoteStrings', true);
                sprintf('Collating subject %s for movie %s and emotion %s.' ,char(sFolders(i).name), mName{1}, thisEm)
                cd(vDirName)
                clear voiF stF tf rnum rfiles rFile srFiles srNum nstF nstFF nstFFF mv mvi thisSubMovieEm
            
                else
                    continue
                end
                else
                    continue
                end
                end
        else
            continue
        end
        cd (thisFolder)
    end
end

