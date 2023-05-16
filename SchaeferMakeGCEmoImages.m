clear; clc;

imgGCPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Schaefer400';
Movies = {'AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain'};
Emotions = {'Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise'};

cd(bPath)
roiFiles = dir('Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_*.nii');

for i = 1:length(roiFiles)
    rfiles{i,1} = fullfile(bPath,roiFiles(i).name);
end

cd(imgGCPath)
GCFiles = dir('GCResults*');
for i = 1:length(GCFiles)
    fGCFiles{i,1} = fullfile(imgGCPath,GCFiles(i).name);
end
crit = 0.05/400;

anDir= '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis/GC_MovEmImgSchaefer';
cd (anDir)

for i = 1:length(fGCFiles)
    thisMov = extractBetween(fGCFiles{i,1}, 'GCResults_', '.csv');
    if ~ exist(thisMov{1}, 'dir')
        mkdir(thisMov{1})
    end
    mDir = fullfile(anDir, thisMov{1});
    data = readtable(fGCFiles{i});
    cd(mDir)

    if exist('MDone.txt')
        cd(anDir)
        continue
    else




        for j = 2:size(data,2)
            thisEm = Emotions(j-1);
            emGC =data(:,j);
            cd(mDir)
            if ~exist(thisEm{1}, 'dir')
                mkdir(thisEm{1})
            end

            fullDir = fullfile(mDir,thisEm{1});
            cd(fullDir)
            if exist('Done.txt')
                cd(mDir)
                continue
            else
                for r = 1:height(emGC)
                    pull = table2array(emGC(r,1));
                    pull2 = pull{1};
                    rdat = str2num(pull2);
                    if rdat(1)== 100
                        rdat(1) = 1;
                    elseif rdat(1) > crit && rdat(1) < 100
                        rdat(1) = 1;
                    elseif rdat(1) <= crit
                        rdat(1) = abs(log(rdat(1)));
                    end
                    %             data(r,j) = rdat(1);
                    val = rdat(1);


                    spm('Defaults','fMRI');
                    spm_jobman('initcfg');
                    matlabbatch{1}.spm.util.imcalc.input = {fullfile(bPath, ['Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_', num2str(r), '.nii'])};
                    matlabbatch{1}.spm.util.imcalc.output = ['Roi_', num2str(r), '_GC_', thisMov{1}, thisEm{1}, '.nii'];
                    matlabbatch{1}.spm.util.imcalc.outdir = {fullDir};
                    matlabbatch{1}.spm.util.imcalc.expression = ['i1 .*', num2str(val)];
                    matlabbatch{1}.spm.util.imcalc.var = struct('name', {}, 'value', {});
                    matlabbatch{1}.spm.util.imcalc.options.dmtx = 0;
                    matlabbatch{1}.spm.util.imcalc.options.mask = 1;
                    matlabbatch{1}.spm.util.imcalc.options.interp = 1;
                    matlabbatch{1}.spm.util.imcalc.options.dtype = 4;
                    %save('matlabbatch');
                    spm_jobman('run', matlabbatch)



                end
                fid = fopen('Done.txt', 'w');
                fclose(fid)


            end


        end
        cd(mDir)
        fid = fopen('MDone.txt', 'w');
        fclose(fid)
        cd (anDir)
    end
end







 