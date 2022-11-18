clear; clc
%Use annot, pmod separate fd

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
                    Emotions = {'Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Guilt', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise'};
                    for em =1:12    
                    csName = ['FullModel_',char(movName),  '_', Emotions{em}, '_fd_SepPmod'];

                    if ~exist(csName, 'dir')
                        mkdir(csName)
                    end
                    cd(csName)

                    thisD = fullfile(imgBetaPath, sub, csName);
                    cd(thisD)
                    if exist('SPM.mat')
                        continue
                    else
                        spm('Defaults','fMRI');
                        spm_jobman('initcfg');

                        pModN = Emotions{em};
   
                        data = readtable(thisFile);
                        data = data(2:end, :);
                        data = data(:,2:end);

                        if em == 1
                        pModV = data(:,3).Variables;
                        else
                        pModV = data(:,em + 3).Variables;
                        end

                        onsets = [1:height(data)] + toAdd;

                        dur = 0;


                        cd(imgBetaPath)
                        sprintf("Processing Subject %s on %s", sub, movName{1});




                        matlabbatch{1}.spm.stats.fmri_spec.dir = {thisD};
                        matlabbatch{1}.spm.stats.fmri_spec.timing.units = 'secs';
                        matlabbatch{1}.spm.stats.fmri_spec.timing.RT = 1.3;
                        matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t = 16;
                        matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t0 = 8;

                        matlabbatch{1}.spm.stats.fmri_spec.sess.scans = cellstr(spm_select('FPList', movPath, '^filtered_func_data_res_MNI_.*.nii$'));
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.name = 'Onset';
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.onset = onset;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.duration = dur;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.tmod = 0;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod.name = pModN;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod.param = pModV;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod.poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(2).name = 'Anxiety';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(2).param = data.Anxiety_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(2).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(3).name = 'Contempt';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(3).param = data.Contempt_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(3).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(4).name = 'Disgust';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(4).param = data.Disgust_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(4).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(5).name = 'Fear';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(5).param = data.Fear_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(5).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(6).name = 'Happiness';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(6).param = data.Happiness_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(6).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(7).name = 'Love';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(7).param = data.Love_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(7).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(8).name = 'Sad';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(8).param = data.Sad_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(8).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(9).name = 'Satisfaction';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(9).param = data.Satisfaction_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(9).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(10).name= 'Shame';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(10).param = data.Shame_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(10).poly = 1;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(11).name= 'Surprise';
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(11).param= data.Surprise_Mu;
%                         matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(11).poly = 1;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.orth = 1;

                        matlabbatch{1}.spm.stats.fmri_spec.sess.multi =  {''};
                        matlabbatch{1}.spm.stats.fmri_spec.sess.regress =  struct('name', {}, 'val', {});
                        matlabbatch{1}.spm.stats.fmri_spec.sess.multi_reg =  cellstr(mRegFile);
                        matlabbatch{1}.spm.stats.fmri_spec.sess.hpf =  128;
                        matlabbatch{1}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
                        matlabbatch{1}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
                        matlabbatch{1}.spm.stats.fmri_spec.volt = 1;
                        matlabbatch{1}.spm.stats.fmri_spec.global = 'None';
                        matlabbatch{1}.spm.stats.fmri_spec.mthresh = -Inf;
                        matlabbatch{1}.spm.stats.fmri_spec.mask = {''};
                        matlabbatch{1}.spm.stats.fmri_spec.cvi = 'AR(1)';

                        matlabbatch{2}.spm.stats.fmri_est.spmmat = cfg_dep('fMRI model specification: SPM.mat File', substruct('.', 'val', '{}', {1}, '.', 'val', '{}', {1},'.', 'val', '{}', {1}), substruct('.', 'spmmat'));
                        matlabbatch{2}.spm.stats.fmri_est.write_residuals = 0;
                        matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;

                        matlabbatch{3}.spm.stats.con.spmmat = {fullfile(thisD, 'SPM.mat')};
                        matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = pModN;
                        matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = [0 1];
                        matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{2}.tcon.name = 'Anxiety';
%                         matlabbatch{3}.spm.stats.con.consess{2}.tcon.weights = [0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{2}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{3}.tcon.name = 'Contempt';
%                         matlabbatch{3}.spm.stats.con.consess{3}.tcon.weights = [0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{3}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{4}.tcon.name = 'Disgust';
%                         matlabbatch{3}.spm.stats.con.consess{4}.tcon.weights = [0 0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{4}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{5}.tcon.name = 'Fear';
%                         matlabbatch{3}.spm.stats.con.consess{5}.tcon.weights = [0 0 0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{5}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{6}.tcon.name = 'Happiness';
%                         matlabbatch{3}.spm.stats.con.consess{6}.tcon.weights = [0 0 0 0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{6}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{7}.tcon.name = 'Love';
%                         matlabbatch{3}.spm.stats.con.consess{7}.tcon.weights = [0 0 0 0 0 0 0 1];
                        %matlabbatch{3}.spm.stats.con.consess{7}.tcon.sessrep = 'none';
                        %matlabbatch{3}.spm.stats.con.consess{8}.tcon.name = 'Sad';
                        %matlabbatch{3}.spm.stats.con.consess{8}.tcon.weights = [0 0 0 0 0 0 0 0 1];
                        %matlabbatch{3}.spm.stats.con.consess{8}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{9}.tcon.name = 'Satisfaction';
%                         matlabbatch{3}.spm.stats.con.consess{9}.tcon.weights = [0 0 0 0 0 0 0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{9}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{10}.tcon.name = 'Shame';
%                         matlabbatch{3}.spm.stats.con.consess{10}.tcon.weights = [0 0 0 0 0 0 0 0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{10}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{11}.tcon.name = 'Surprise';
%                         matlabbatch{3}.spm.stats.con.consess{11}.tcon.weights = [0 0 0 0 0 0 0 0 0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{11}.tcon.sessrep = 'none';
%                         %                             matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = Surprise;
                        %                             matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = [0 0 0 0 0 0 0 0 0 0 0 0 1];
                        %                             matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'none';


                        matlabbatch{3}.spm.stats.con.delete = 0;

                        save('matlabbatch');
                        spm_jobman('run', matlabbatch)
                        cd(mainPath)
                    end

                    end
                end

            end

        end
    end
end









