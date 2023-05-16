clear; clc;

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Schaefer400';
Emotions= {'Anger','Anxiety','Contempt','Disgust','Fear','Happiness','Love','Satisfaction','Sad','Shame','Surprise'};

cd(bPath)
relFiles = dir('Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_*.nii');

for i = 1:length(relFiles)
    rfiles{i,1} = fullfile(bPath,relFiles(i).name);
end

cd(imgBetaPath)
sFolders = dir('sub-S*');

parfor i = 1:length(sFolders)
    thisFolder = fullfile(imgBetaPath, sFolders(i).name);
    cd(thisFolder)
    sModels = dir('FullModel__*_Ortho');
    s = 0;
    for s = 1:length(sModels)
        thisModelP = fullfile(thisFolder, sModels(s).name);
        cd(thisModelP)
        thisFile = fullfile(thisModelP,'SPM.mat');
        st = sModels(s).name;
        dirName = extractBetween(st, 'FullModel__', '_Ortho');
        dirName = dirName{1};
        if ~exist(dirName, 'dir')
            mkdir(dirName)
        end
        opDir = fullfile(thisModelP, dirName);
        atlasHome =  '/home/loued/spm12/atlas';
%         cd (atlasHome)
%         mask= spm_atlas('mask', 'HCPex_2mm.nii', 'HCPex_2mm.xml');
%         mask.fname = 'HCPexmask.nii';
%         mask = spm_write_vol(mask,mask.dat);

        %   end
        cd(opDir)
        for em = 1:length(Emotions)
           % clear matlabbatch;
            spm('Defaults','fMRI');
            spm_jobman('initcfg');
            r = 0;
          
            
            parfor r = 1:length(rfiles)

            maskFF = rfiles{r};
            %%ListOfInputs
            %SPMMatFile
            %relFiles
            %em
            %MaskFF

% List of open inputs
% Volume of Interest: Select SPM.mat - cfg_files
% Volume of Interest: Name of VOI - cfg_entry
% Volume of Interest: Contrast - cfg_entry
% Save Variables: Output Filename - cfg_entry
% Save Variables: Output Directory - cfg_files
nrun = X; % enter the number of runs here
jobfile = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/Scripts/Template_VOISeriesExtract_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(6, nrun);
for crun = 1:nrun
    inputs{1, crun} = cellstr(thisFile); % Volume of Interest: Select SPM.mat - cfg_files
    inputs{2, crun} = relFiles(r).name(1:end-4); % Volume of Interest: Name of VOI - cfg_entry
    inputs{3, crun} = em; % Volume of Interest: Contrast - cfg_entry
    inputs{4, crun} = {maskFF};% Volume of Interest: Image file - cfg_files
    inputs{5, crun} = ['TS_',dirName,'_', relFiles(r).name(1:end-4),'_', Emotions{em}, '.mat']; % Save Variables: Output Filename - cfg_entry
    inputs{6, crun} = {opDir}; % Save Variables: Output Directory - cfg_files
end
    % 
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});


%             matlabbatch{1}.spm.util.voi.spmmat  = cellstr(thisFile);
%             matlabbatch{1}.spm.util.voi.adjust  = 0;                
%             matlabbatch{1}.spm.util.voi.session = 1;                    % Session index
%             matlabbatch{1}.spm.util.voi.name    = relFiles(r).name(1:end-4);               % VOI name
%             %
%             % % Define thresholded SPM for finding the subject's local peak response
%             matlabbatch{1}.spm.util.voi.roi{1}.spm.spmmat      = cellstr(thisFile);
%             matlabbatch{1}.spm.util.voi.roi{1}.spm.contrast = em;
%             matlabbatch{1}.spm.util.voi.roi{1}.spm.conjunction = 1;
%             matlabbatch{1}.spm.util.voi.roi{1}.spm.threshdesc = 'none';
%             matlabbatch{1}.spm.util.voi.roi{1}.spm.thresh = 0.5;
%             matlabbatch{1}.spm.util.voi.roi{1}.spm.extent = 0;
%             matlabbatch{1}.spm.util.voi.roi{1}.spm.mask = struct('contrast', {}, 'thresh', {}, 'mtype', {});
% 
%             matlabbatch{1}.spm.util.voi.roi{2}.mask.image = {maskFF};
%             matlabbatch{1}.spm.util.voi.roi{2}.mask.threshold = 0.5;
%             matlabbatch{1}.spm.util.voi.expression = 'i1 & i2';
%     
%             matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.name = ['TS_',dirName,'_', relFiles(r).name(1:end-4),'_', Emotions{em}, '.mat'] ;
%             matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.outdir = {opDir};
%             matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vname = 'TS';
%             matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vcont(1) = cfg_dep('Volume of Interest:  VOI mat File', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','voimat'));
%             matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.saveasstruct = true;
% 
%             % Run the batch
%             spm_jobman('run',matlabbatch);
        end
    end
    end
end