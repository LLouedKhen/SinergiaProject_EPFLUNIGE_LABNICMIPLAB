% List of open inputs
% fMRI model specification: Directory - cfg_files
% fMRI model specification: Units for design - cfg_menu
% fMRI model specification: Interscan interval - cfg_entry
% fMRI model specification: Data & Design - cfg_repeat
% Model estimation: Select SPM.mat - cfg_files
% Contrast Manager: Select SPM.mat - cfg_files
nrun = X; % enter the number of runs here
jobfile = {'/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/FirstLevel_Template_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(6, nrun);
for crun = 1:nrun
    inputs{1, crun} = MATLAB_CODE_TO_FILL_INPUT; % fMRI model specification: Directory - cfg_files
    inputs{2, crun} = MATLAB_CODE_TO_FILL_INPUT; % fMRI model specification: Units for design - cfg_menu
    inputs{3, crun} = MATLAB_CODE_TO_FILL_INPUT; % fMRI model specification: Interscan interval - cfg_entry
    inputs{4, crun} = MATLAB_CODE_TO_FILL_INPUT; % fMRI model specification: Data & Design - cfg_repeat
    inputs{5, crun} = MATLAB_CODE_TO_FILL_INPUT; % Model estimation: Select SPM.mat - cfg_files
    inputs{6, crun} = MATLAB_CODE_TO_FILL_INPUT; % Contrast Manager: Select SPM.mat - cfg_files
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
