mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/';
imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
bPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/';
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
             movF = fullfile(sessFolder, mF(m).name);
            if ~contains(mF(m).name,'Rest')
               
                cd(movF)
                normF = dir('*MNI.nii.gz');
               
%                 if ~isempty(normF) && length(normFuz) < 3 && ~exist('Done.txt')
                if ~isempty(normF) && ~exist('Done.txt')
             
                gunzip(normF.name)
                normFuz = dir('*MNI.nii');
                normFuzV = spm_select('List', '*MNI.nii');
                spm_file_split(normFuzV)
                d = 'Done';
                fId = fopen('Done.txt','w');
                nB = fprintf(fId,'%s',d);

                end
%                 imFiles = dir('filtered_func_data_res_MNI_*.nii');
%                 mReg = dir('Regressors.txt');
%                 mRegFile =[mRegFile; fullfile(movF, mReg.name)];
%                 movPath= [movPath; fullfile(movF)];

                %movPath(find(strcmp(movPath, 'Rest'))) = [];
%                 regsCheck = importdata(mRegFile);
%                 useRegs = regsCheck(:,3:end);
            else 
                continue
            end
        end
    end



    

end