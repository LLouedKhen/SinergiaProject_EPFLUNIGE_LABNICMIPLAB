%-----------------------------------------------------------------------
% Job saved on 22-Nov-2022 14:56:50 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.spm.util.voi.spmmat = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/sub-S01/FullModel__AfterTheRain_AllPmod_Ortho/SPM.mat'};
matlabbatch{1}.spm.util.voi.adjust = 0;
matlabbatch{1}.spm.util.voi.session = 1;
matlabbatch{1}.spm.util.voi.name = 'HCPex_2mm_10';
matlabbatch{1}.spm.util.voi.roi{1}.spm.spmmat = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/sub-S01/FullModel__AfterTheRain_AllPmod_Ortho/SPM.mat'};
matlabbatch{1}.spm.util.voi.roi{1}.spm.contrast = 1;
matlabbatch{1}.spm.util.voi.roi{1}.spm.conjunction = 1;
matlabbatch{1}.spm.util.voi.roi{1}.spm.threshdesc = 'none';
matlabbatch{1}.spm.util.voi.roi{1}.spm.thresh = 0.5;
matlabbatch{1}.spm.util.voi.roi{1}.spm.extent = 0;
matlabbatch{1}.spm.util.voi.roi{1}.spm.mask = struct('contrast', {}, 'thresh', {}, 'mtype', {});
matlabbatch{1}.spm.util.voi.roi{2}.mask.image = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/HCPex_v1.0/HCPex_v1.0/ROIs/HCPex_2mm_1.nii,1'};
matlabbatch{1}.spm.util.voi.roi{2}.mask.threshold = 0.5;
matlabbatch{1}.spm.util.voi.expression = 'i2';
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.name = 'TS_AfterTheRain_AllPmod_HCPex_2mm_1.mat';
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.outdir = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/sub-S01/FullModel__AfterTheRain_AllPmod_Ortho/AfterTheRain_AllPmod'};
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vname = 'TS';
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vcont(1) = cfg_dep('Volume of Interest:  VOI mat File', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','voimat'));
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.saveasstruct = true;
