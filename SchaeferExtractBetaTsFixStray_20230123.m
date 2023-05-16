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
        thisFile = fullfile(thisModelP,'SPM.mat');
        st = sModels(s).name;
        dirName = extractBetween(st, 'FullModel__', 'AllPmod_Ortho');
        dirName = 'Schaefer400_BetaSeries';
        if ~exist(dirName, 'dir')
            mkdir(dirName)
        end
        opDir = fullfile(thisModelP, dirName);

        if length(dir('con*')) > 0
            
            atlasHome =  '/home/loued/spm12/atlas';
            %         cd (atlasHome)
            %         mask= spm_atlas('mask', 'HCPex_2mm.nii', 'HCPex_2mm.xml');
            %         mask.fname = 'HCPexmask.nii';
            %         mask = spm_write_vol(mask,mask.dat);

            %   end


            for em = 1:length(Emotions)
                %             clear matlabbatch;
                cd(opDir) 
                if isfile(['Done',Emotions{em},'.txt'])
                    continue
                else
                    cd (thisModelP)
                    spm('Defaults','fMRI');
                    spm_jobman('initcfg');
                    r = 0;


                    for r = 1:length(rfiles)

                        maskFF = rfiles{r};


                        matlabbatch{1}.spm.util.voi.spmmat  = cellstr(thisFile);
                        matlabbatch{1}.spm.util.voi.adjust  = 0;
                        matlabbatch{1}.spm.util.voi.session = 1;                    % Session index
                        matlabbatch{1}.spm.util.voi.name    = relFiles(r).name(1:end-4);               % VOI name
                        %
                        % % Define thresholded SPM for finding the subject's local peak response
                        matlabbatch{1}.spm.util.voi.roi{1}.spm.spmmat      = cellstr(thisFile);
                        matlabbatch{1}.spm.util.voi.roi{1}.spm.contrast = em;
                        matlabbatch{1}.spm.util.voi.roi{1}.spm.conjunction = 1;
                        matlabbatch{1}.spm.util.voi.roi{1}.spm.threshdesc = 'none';
                        matlabbatch{1}.spm.util.voi.roi{1}.spm.thresh = 0.5;
                        matlabbatch{1}.spm.util.voi.roi{1}.spm.extent = 0;
                        matlabbatch{1}.spm.util.voi.roi{1}.spm.mask = struct('contrast', {}, 'thresh', {}, 'mtype', {});

                        matlabbatch{1}.spm.util.voi.roi{2}.mask.image = {maskFF};
                        matlabbatch{1}.spm.util.voi.roi{2}.mask.threshold = 0.5;
                        matlabbatch{1}.spm.util.voi.expression = 'i1 & i2';

%                         matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.name = ['TS_',dirName,'_', relFiles(r).name(1:end-4),'_', Emotions{em}, '.mat'] ;
%                         matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.outdir = {opDir};
%                         matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vname = 'TS';
%                         matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vcont(1) = cfg_dep('Volume of Interest:  VOI mat File', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','voimat'));
%                         matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.saveasstruct = true;

                        % Run the batch
                        batch{r} = matlabbatch;

                    end
                    parfor r = 1:length(rfiles)
                        spm_jobman('run',batch{r});
                    end
                    cd(opDir)
                    fileID = fopen(['Done',Emotions{em},'.txt'],'w');
                    fclose(fileID);

                    thisEm = Emotions{em};
                    if ~exist(thisEm, 'dir')
                        mkdir(thisEm)
                    end
                    emff = fullfile(opDir, thisEm);
                    cd (thisModelP)
                    resVOI = dir('VOI*');
                    if length(resVOI) > 1
                        movefile ('VOI*', emff)
                    else
                        continue
                    end

                end
            end
        else
            continue
        end
    end
end