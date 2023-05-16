clear; clc

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
delete matlabbatch.mat

cd (imgBetaPath)

Emotions= {'HC1 > HC2', 'HC1 < HC2', 'HC1 > HC3', 'HC1 < HC3','HC1 > HC4', 'HC1 < HC4', 'HC1 > HC5', 'HC1 < HC5', 'HC1 > HC6', 'HC1 < HC6',...
    'HC2 > HC3', 'HC2 < HC3','HC2 > HC4', 'HC2 < HC4', 'HC2 > HC5', 'HC2 < HC5', 'HC2 > HC6', 'HC2 < HC6',...
    'HC3 > HC4', 'HC3 < HC4', 'HC3 > HC5', 'HC3 < HC5', 'HC3 > HC6', 'HC3 < HC6',...
    'HC4 > HC5', 'HC4 < HC5', 'HC4 > HC6', 'HC4 < HC6',...
    'HC5 > HC6', 'HC5 < HC6', ...
    'HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6'};

GAnDir = 'SecondLevel_HC6_AllPMODMU';
if ~exist(GAnDir, 'dir')
    mkdir(GAnDir);
end

cd SecondLevel_HC6_AllPMODMU/
% for em = 1:length(Emotions)
for em = 35:36
        if em < 10
            emNum = ['0',num2str(em)];
        else
            emNum = num2str(em);
        end
    thisEm = Emotions{em};

    if ~exist(thisEm, 'dir')
        mkdir(thisEm);
    end
    thisDir = fullfile(imgBetaPath,GAnDir, thisEm);

    files =  dir(fullfile(imgBetaPath, '**', ['PartModel_','*', '6HCPmod_Mu_Ortho'],  ['con_00', emNum,'.nii']));


    cFiles = {};
    for f = 1:length(files)
        cFiles{f} = fullfile(files(f).folder, files(f).name);
    end
    %                     cFiles = cFiles(~cellfun('isempty',cFiles))
    cFiles =cFiles';
    %pause
    spm('Defaults','fMRI');
    spm_jobman('initcfg');
    matlabbatch{1}.spm.stats.factorial_design.dir = {thisDir};
    matlabbatch{1}.spm.stats.factorial_design.des.t1.scans = cFiles;
    matlabbatch{1}.spm.stats.factorial_design.cov = struct('c', {}, 'cname', {}, 'iCFI', {}, 'iCC', {});
    matlabbatch{1}.spm.stats.factorial_design.multi_cov = struct('files', {}, 'iCFI', {}, 'iCC', {});
    matlabbatch{1}.spm.stats.factorial_design.masking.tm.tm_none = 1;
    matlabbatch{1}.spm.stats.factorial_design.masking.im = 1;
    matlabbatch{1}.spm.stats.factorial_design.masking.em = {''};
    matlabbatch{1}.spm.stats.factorial_design.globalc.g_omit = 1;
    matlabbatch{1}.spm.stats.factorial_design.globalm.gmsca.gmsca_no = 1;
    matlabbatch{1}.spm.stats.factorial_design.globalm.glonorm = 1;

    matlabbatch{2}.spm.stats.fmri_est.spmmat = cfg_dep('fMRI model specification: SPM.mat File', substruct('.', 'val', '{}', {1}, '.', 'val', '{}', {1},'.', 'val', '{}', {1}), substruct('.', 'spmmat'));
    matlabbatch{2}.spm.stats.fmri_est.write_residuals = 0;
    matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;

    matlabbatch{3}.spm.stats.con.spmmat(1) = cfg_dep('Model estimation: SPM.mat File', substruct('.', 'val', '{}', {2}, '.', 'val', '{}', {1},'.', 'val', '{}', {1}), substruct('.', 'spmmat'));
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = thisEm;
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = 1;
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'none';
    matlabbatch{3}.spm.stats.con.delete = 0;


        save('matlabbatch');
        spm_jobman('run', matlabbatch)
    %     delete matlabbatch.mat
%     batch{em} = matlabbatch;
end


% 
% parfor em = 1:length(Emotions)
%     spm_jobman('run',batch{em});
% end