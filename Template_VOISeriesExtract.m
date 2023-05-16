% List of open inputs
% Volume of Interest: Select SPM.mat - cfg_files
% Volume of Interest: Name of VOI - cfg_entry
% Volume of Interest: Contrast - cfg_entry
% Volume of Interest: Image file - cfg_files
% Save Variables: Output Filename - cfg_entry
% Save Variables: Output Directory - cfg_files
nrun = X; % enter the number of runs here
jobfile = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/Scripts/Template_VOISeriesExtract_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(6, nrun);
for crun = 1:nrun
    inputs{1, crun} = MATLAB_CODE_TO_FILL_INPUT; % Volume of Interest: Select SPM.mat - cfg_files
    inputs{2, crun} = MATLAB_CODE_TO_FILL_INPUT; % Volume of Interest: Name of VOI - cfg_entry
    inputs{3, crun} = MATLAB_CODE_TO_FILL_INPUT; % Volume of Interest: Contrast - cfg_entry
    inputs{4, crun} = MATLAB_CODE_TO_FILL_INPUT; % Volume of Interest: Image file - cfg_files
    inputs{5, crun} = MATLAB_CODE_TO_FILL_INPUT; % Save Variables: Output Filename - cfg_entry
    inputs{6, crun} = MATLAB_CODE_TO_FILL_INPUT; % Save Variables: Output Directory - cfg_files
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
