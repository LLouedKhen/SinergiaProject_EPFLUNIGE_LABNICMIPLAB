% List of open inputs
% Factorial design specification: Directory - cfg_files
% Factorial design specification: Scans - cfg_files
% Model estimation: Select SPM.mat - cfg_files
% Contrast Manager: Select SPM.mat - cfg_files
nrun = X; % enter the number of runs here
jobfile = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/Group_Emotions_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(4, nrun);
for crun = 1:nrun
    inputs{1, crun} = MATLAB_CODE_TO_FILL_INPUT; % Factorial design specification: Directory - cfg_files
    inputs{2, crun} = MATLAB_CODE_TO_FILL_INPUT; % Factorial design specification: Scans - cfg_files
    inputs{3, crun} = MATLAB_CODE_TO_FILL_INPUT; % Model estimation: Select SPM.mat - cfg_files
    inputs{4, crun} = MATLAB_CODE_TO_FILL_INPUT; % Contrast Manager: Select SPM.mat - cfg_files
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
