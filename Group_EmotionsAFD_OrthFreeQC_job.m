clear; clc
cd '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/QC_Feb2023'
drop = readtable('MovEmoToDrop.csv');

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/';
delete matlabbatch.mat

cd (imgBetaPath)

Emotions= {'Anger','Anxiety','Contempt','Disgust','Fear','Happiness','Love','Satisfaction','Sad','Shame','Surprise'};
for i = 1:length(Emotions')    
    if i < 10
        emNum = ['0',num2str(i)];
        emCN{i,1} = emNum;
    else 
        emNum = num2str(i);
        emCN{i,1} = emNum;
    end    
end 
EmAndNum = [Emotions', emCN];


 for i= 1:height(drop)
     emoDrop = extractBetween(drop.MovEmo{i},', ', ')');
     sDrop = emoDrop{1}(2:end-1);
     relInd = find(strcmp(Emotions,sDrop));
     dropCon = [', ', 'con_00', EmAndNum{relInd,2}];
     drop.MovEmo{i} = insertBefore(drop.MovEmo{i},')',  dropCon);
 end
 

GAnDir = 'SecondLevel_EmotionsAFD_OrthFreeQC/';
    if ~exist(GAnDir, 'dir')
        mkdir(GAnDir);
    end

cd SecondLevel_EmotionsAFD_OrthFreeQC/
for em = 1:length(Emotions) 
    if em < 10
        emNum = ['0',num2str(em)];
    else 
        emNum = num2str(em);
    end
    thisEm = Emotions{em};
    thisInd = find(strcmp(EmAndNum, thisEm));
    thisCon = ['con_00',EmAndNum{thisInd,2}];

    if ~exist(thisEm, 'dir')
        mkdir(thisEm);
    end
    thisDir = fullfile(imgBetaPath,GAnDir, thisEm);

   
    files =  dir(fullfile(imgBetaPath, '**', ['FullModel__','*','_AllPmod_AFD_OrthFree'], ['con_00',emNum,'.nii']));
    
    cFiles = {};
     for f = 1:length(files)
         thisStr = fullfile(files(f).folder,files(f).name);
         thisMov = extractBetween(thisStr,'FullModel__','_AllPmod_AFD_OrthFree');
         thisMov = thisMov{1};
%          thisCon = thisCon{1};
   
         testDrop = cell2mat(regexp(drop.MovEmo(:), regexptranslate('wildcard',[thisMov, '*', thisCon])));
         if ~isempty(testDrop)
         cFiles{f} = []; 
         else
         cFiles{f} = fullfile(files(f).folder, files(f).name);
         end
         end
   
    cFiles =cFiles';
    cFiles = cFiles(~cellfun('isempty',cFiles));
    %                     cFiles = cFiles(~cellfun('isempty',cFiles));
   
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
end