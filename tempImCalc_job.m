%-----------------------------------------------------------------------
% Job saved on 28-Nov-2022 12:15:15 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.spm.util.imcalc.input = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/HCPex_v1.0/HCPex_v1.0/ROIs/HCPex_2mm_1.nii,1'};
matlabbatch{1}.spm.util.imcalc.output = 'Test';
matlabbatch{1}.spm.util.imcalc.outdir = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis/GC_MovEmImgSchaefer'};
matlabbatch{1}.spm.util.imcalc.expression = 'i1 * rand(1,1)';
matlabbatch{1}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{1}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{1}.spm.util.imcalc.options.mask = 0;
matlabbatch{1}.spm.util.imcalc.options.interp = 1;
matlabbatch{1}.spm.util.imcalc.options.dtype = 4;
