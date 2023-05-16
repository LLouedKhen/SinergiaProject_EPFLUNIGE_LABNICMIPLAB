%-----------------------------------------------------------------------
% Job saved on 08-Dec-2022 11:31:26 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.spm.util.voi.spmmat = '<UNDEFINED>';
matlabbatch{1}.spm.util.voi.adjust = 0;
matlabbatch{1}.spm.util.voi.session = 1;
matlabbatch{1}.spm.util.voi.name = '<UNDEFINED>';
matlabbatch{1}.spm.util.voi.roi{1}.spm.spmmat = {''};
matlabbatch{1}.spm.util.voi.roi{1}.spm.contrast = '<UNDEFINED>';
matlabbatch{1}.spm.util.voi.roi{1}.spm.conjunction = 1;
matlabbatch{1}.spm.util.voi.roi{1}.spm.threshdesc = 'none';
matlabbatch{1}.spm.util.voi.roi{1}.spm.thresh = 0.05;
matlabbatch{1}.spm.util.voi.roi{1}.spm.extent = 0;
matlabbatch{1}.spm.util.voi.roi{1}.spm.mask = struct('contrast', {}, 'thresh', {}, 'mtype', {});
matlabbatch{1}.spm.util.voi.roi{2}.mask.image = '<UNDEFINED>';
matlabbatch{1}.spm.util.voi.roi{2}.mask.threshold = 0.5;
matlabbatch{1}.spm.util.voi.expression = 'i1 + i2';
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.name = '<UNDEFINED>';
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.outdir = '<UNDEFINED>';
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vname = 'TS';
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vcont(1) = cfg_dep('Volume of Interest:  VOI mat File', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','voimat'));
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.vars.vcont(2) = cfg_dep('Volume of Interest:  VOI Image File', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','voiimg'));
matlabbatch{2}.cfg_basicio.var_ops.cfg_save_vars.saveasstruct = true;
