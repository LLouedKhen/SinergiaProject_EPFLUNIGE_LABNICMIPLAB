clear; clc
%HC FD, 6 variables, excluded shame, guilt and warmheartednes 
mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/';
imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
delete matlabbatch.mat
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/HCluster_Data';
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
                    regsS = dir('HC_*');
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

                    csName = ['PartModel_', '_',char(movName),'_6HCPmod_AFD_Ortho'];

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

s
                        data = readtable(thisFile);
%                         data = data(2:end,:);
                        dData = data.Variables;
                        idData = abs(diff(dData));
                        idData = [repmat(nan,[1, size(idData,2)]); idData];
                        data.Variables = idData;
                        data = data(2:end,:);


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
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.onset = onsets;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.duration = dur;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.tmod = 0;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(1).name = 'HC1';
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(1).param = data.HC1;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(1).poly = 1;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(2).name = 'HC2';
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(2).param = data.HC2;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(2).poly = 1;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(3).name = 'HC3';
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(3).param = data.HC3;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(3).poly = 1;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(4).name = 'HC4';
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(4).param = data.HC4;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(4).poly = 1;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(5).name = 'HC5';
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(5).param = data.HC5;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(5).poly = 1;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(6).name = 'HC6';
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(6).param = data.HC6;
                        matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod(6).poly = 1;
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
                        matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = 'HC1 > HC2';
                        matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = [1 -1];
                        matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{2}.tcon.name = 'HC1 < HC2';
                        matlabbatch{3}.spm.stats.con.consess{2}.tcon.weights = [-1 1];
                        matlabbatch{3}.spm.stats.con.consess{2}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{3}.tcon.name = 'HC1 > HC3';
                        matlabbatch{3}.spm.stats.con.consess{3}.tcon.weights = [1 0 -1];
                        matlabbatch{3}.spm.stats.con.consess{3}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{4}.tcon.name = 'HC1 < HC3';
                        matlabbatch{3}.spm.stats.con.consess{4}.tcon.weights = [-1 0 1 0 0];
                        matlabbatch{3}.spm.stats.con.consess{4}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{5}.tcon.name = 'HC1 > HC4';
                        matlabbatch{3}.spm.stats.con.consess{5}.tcon.weights = [1 0 0 -1 0 0];
                        matlabbatch{3}.spm.stats.con.consess{5}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{6}.tcon.name = 'HC1 < HC4';
                        matlabbatch{3}.spm.stats.con.consess{6}.tcon.weights = [-1 0 0 1 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{6}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{7}.tcon.name = 'HC1 > HC5';
                        matlabbatch{3}.spm.stats.con.consess{7}.tcon.weights = [1 0 0 0 -1 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{7}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{8}.tcon.name = 'HC1 < HC5';
                        matlabbatch{3}.spm.stats.con.consess{8}.tcon.weights = [-1 0 0 0 1 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{8}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{9}.tcon.name = 'HC1 > HC6';
                        matlabbatch{3}.spm.stats.con.consess{9}.tcon.weights = [1 0 0 0 0 -1 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{9}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{10}.tcon.name = 'HC1 < HC6';
                        matlabbatch{3}.spm.stats.con.consess{10}.tcon.weights = [-1 0 0 0 0 1 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{10}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{11}.tcon.name = 'HC2 > HC3';
                        matlabbatch{3}.spm.stats.con.consess{11}.tcon.weights = [0 1 -1 0 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{11}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{12}.tcon.name = 'HC2 < HC3';
                        matlabbatch{3}.spm.stats.con.consess{12}.tcon.weights = [0 -1 1 0 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{12}.tcon.sessrep = 'none';
                        
                        matlabbatch{3}.spm.stats.con.consess{13}.tcon.name = 'HC2 > HC4';
                        matlabbatch{3}.spm.stats.con.consess{13}.tcon.weights = [0 1 0 -1 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{13}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{14}.tcon.name = 'HC2 < HC4';
                        matlabbatch{3}.spm.stats.con.consess{14}.tcon.weights = [0 -1 0 1 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{14}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{15}.tcon.name = 'HC2 > HC5';
                        matlabbatch{3}.spm.stats.con.consess{15}.tcon.weights = [0 1 0 0 -1 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{15}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{16}.tcon.name = 'HC2 < HC5';
                        matlabbatch{3}.spm.stats.con.consess{16}.tcon.weights = [0 -1 0 0 1 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{16}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{17}.tcon.name = 'HC2 > HC6';
                        matlabbatch{3}.spm.stats.con.consess{17}.tcon.weights = [0 1 0 0 0 -1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{17}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{18}.tcon.name = 'HC2 < HC6';
                        matlabbatch{3}.spm.stats.con.consess{18}.tcon.weights = [0 -1 0 0 0 1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{18}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{19}.tcon.name = 'HC3 > HC4';
                        matlabbatch{3}.spm.stats.con.consess{19}.tcon.weights = [0 0 1 -1 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{19}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{20}.tcon.name = 'HC3 < HC4';
                        matlabbatch{3}.spm.stats.con.consess{20}.tcon.weights = [0 -1 0 1 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{20}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{21}.tcon.name = 'HC3 > HC5';
                        matlabbatch{3}.spm.stats.con.consess{21}.tcon.weights = [0 0 1 0 -1 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{21}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{22}.tcon.name = 'HC3 < HC5';
                        matlabbatch{3}.spm.stats.con.consess{22}.tcon.weights = [0 0 -1 0 1 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{22}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{23}.tcon.name = 'HC3 > HC6';
                        matlabbatch{3}.spm.stats.con.consess{23}.tcon.weights = [0 0 1 0 0 -1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{23}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{24}.tcon.name = 'HC3 < HC6';
                        matlabbatch{3}.spm.stats.con.consess{24}.tcon.weights = [0 0 -1 0 0 1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{24}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{25}.tcon.name = 'HC4 > HC5';
                        matlabbatch{3}.spm.stats.con.consess{25}.tcon.weights = [0 0 0 1 -1 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{25}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{26}.tcon.name = 'HC4 < HC5';
                        matlabbatch{3}.spm.stats.con.consess{26}.tcon.weights = [0 0 0 -1 1 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{26}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{27}.tcon.name = 'HC4 > HC6';
                        matlabbatch{3}.spm.stats.con.consess{27}.tcon.weights = [0 0 0 1 0 -1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{27}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{28}.tcon.name = 'HC4 < HC6';
                        matlabbatch{3}.spm.stats.con.consess{28}.tcon.weights = [0 0 0 -1 0 1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{28}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{29}.tcon.name = 'HC5 > HC6';
                        matlabbatch{3}.spm.stats.con.consess{29}.tcon.weights = [0 0 0 0 1 -1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{29}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{30}.tcon.name = 'HC5 < HC6';
                        matlabbatch{3}.spm.stats.con.consess{30}.tcon.weights = [0 0 0 0 -1 1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{30}.tcon.sessrep = 'none';
                        
                        matlabbatch{3}.spm.stats.con.consess{31}.tcon.name = 'HC1';
                        matlabbatch{3}.spm.stats.con.consess{31}.tcon.weights = [1 0 0 0 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{31}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{32}.tcon.name = 'HC2';
                        matlabbatch{3}.spm.stats.con.consess{32}.tcon.weights = [0 1 0 0 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{32}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{33}.tcon.name = 'HC3';
                        matlabbatch{3}.spm.stats.con.consess{33}.tcon.weights = [0 0 1 0 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{33}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{34}.tcon.name = 'HC4';
                        matlabbatch{3}.spm.stats.con.consess{34}.tcon.weights = [0 0 0 1 0 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{34}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{35}.tcon.name = 'HC5';
                        matlabbatch{3}.spm.stats.con.consess{35}.tcon.weights = [0 0 0 0 1 0 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{35}.tcon.sessrep = 'none';
                        matlabbatch{3}.spm.stats.con.consess{36}.tcon.name = 'HC6';
                        matlabbatch{3}.spm.stats.con.consess{36}.tcon.weights = [0 0 0 0 0 1 0 0 0 0 0 0];
                        matlabbatch{3}.spm.stats.con.consess{36}.tcon.sessrep = 'none';
%                         matlabbatch{3}.spm.stats.con.consess{37}.ess.name = 'HC ANOVA';
%                         matlabbatch{3}.spm.stats.con.consess{37}.ess.weights = [1 0 0 0 0 0; 0 1 0 0 0 0; 0 0 1 0 0 0; 0 0 0 1 0 0; 0 0 0 0 1 0; 0 0 0 0 0 1];
%                         matlabbatch{3}.spm.stats.con.consess{37}.ess.sessrep = 'none';
%         

                        matlabbatch{3}.spm.stats.con.delete = 0;
% 
                        save('matlabbatch');
                        spm_jobman('run', matlabbatch)
                        cd(mainPath)


                    batch{m} = matlabbatch;

                    end
%                     parfor m = 1:length(mF)
%                         spm_jobman('run',batch{m});
%                     end
                end

            end
    
        end
    end
end









