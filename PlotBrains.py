#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 13:32:43 2023

@author: loued
Borrowed from S. Moia
"""
import pandas as pd
import os
import numpy as np
from nigsp import nio, nifti
import glob
from nilearn import plotting
from atlasreader import create_output

#atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=1, data_dir=None, base_url=None, resume=True, verbose=1)

nidMDPath = '/home/loued/.local/lib/python3.7/site-packages/nidmd'
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/QC_Feb2023'
os.chdir(outPath)
drop = pd.read_csv('MovEmoToDrop.csv')

dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions'
os.chdir(dmdPath)
savePath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/MovieEmo_DMDImages'

glm1Path = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/SecondLevel_EmotionsMU_OrthOnQC'
glm2Path = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/SecondLevel_EmotionsFD_OrthOnQC'

Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
#subj = ['sub-S01', 'sub-S02','sub-S03','sub-S04']



dmdFiles = glob.glob('DMD_*_20230325.csv')
testOsc = pd.read_csv('FirstComplexEmoModes20230417.csv')
allEm = []

for em in Emotions:
    coordComp = pd.DataFrame(index = ['GLMMU', 'GLMFD',  'FirstConji', 'FirstMode','FirstConjr'], columns =['MaxCoord', 'Region', 'Emotion'])
    emIdx =  [idx for idx, s in enumerate(dmdFiles) if em in s][0]
    dmdV = pd.read_csv(dmdFiles[emIdx])
    fvIdx = testOsc.index[(testOsc.Emotion==em)][0]
    modeN = testOsc.FirstConj.iloc[fvIdx]
    filename1 = 'Brain_FirstMode_' + em +'.nii'
    filename2 = 'Brain_FirstConj_r_Mode' +str(modeN)+ '_' + em +'.nii'
    filename3 = 'Brain_FirstConj_i_Mode' +str(modeN)+ '_' + em +'.nii'
    valFirst = dmdV.intensity.iloc[0]
    yf = valFirst.split('j')
    zf = yf[:-1]
    zf[0] = zf[0][1:]
    for j in range(len(zf)):
        c1 = zf[j] + 'j'
        c2 = c1.replace(" ", "")
        c3 = c2.lstrip()
        c4 = c3.rstrip()
        c5 = c4.strip('\n')
        zf[j] = np.complex_(c5)

        val = np.array(zf)
        valFirst = val.real
    val1 = dmdV.intensity.iloc[modeN]
    y = val1.split('j')
    z = y[:-1]
    z[0] = z[0][1:]
    for j in range(len(z)):
        c1 = z[j] + 'j'
        c2 = c1.replace(" ", "")
        c3 = c2.lstrip()
        c4 = c3.rstrip()
        c5 = c4.strip('\n')
        z[j] = np.complex_(c5)

    val = np.array(z)
    valr = val.real
    vali = val.imag
#    if em == 'Anger' or em == 'Contempt' or  em == 'Anxiety' or em == 'Disgust':
#        print(vali)
#        input('Press enter if ok')
#def fill_and_export_atlas(val, atfile, filename):
    atfile = '/home/loued/Schaefer/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii'
    atlas, _, img = nio.load_nifti_get_mask(atfile, is_mask=True, ndim=3)
    os.chdir(savePath)
    out = nifti.unfold_atlas(valFirst, atlas)
    nio.export_nifti(out, img, filename1)
    out = nifti.unfold_atlas(valr, atlas)
    nio.export_nifti(out, img, filename2)
    out = nifti.unfold_atlas(vali, atlas)
    nio.export_nifti(out, img, filename3)

    bFile1 = os.path.join(glm1Path, em, em + '_MU_FWE.nii')
    a = plotting.plot_stat_map(bFile1)
    coordComp.MaxCoord.iloc[0] = np.round(a.cut_coords, 2)
    create_output(bFile1, cluster_extent=50, atlas=['aal'], voxel_thresh=1.96)

    bFile2 = os.path.join(glm2Path, em, em + '_FD_FWE.nii')    
    b = plotting.plot_stat_map(bFile2)  
    coordComp.MaxCoord.iloc[1] = np.round(b.cut_coords, 2)
    create_output(bFile2, cluster_extent=50, atlas=['aal'], voxel_thresh=1.96)

#    
          
    c = plotting.plot_stat_map(filename3)
    coordComp.MaxCoord.iloc[2] = np.round(plotting.find_xyz_cut_coords(filename3, activation_threshold = 0.00001))
#    coordComp.MaxCoord.iloc[2] = np.round(c.cut_coords, 2)
    create_output(filename3, cluster_extent=5, atlas=['aal'], voxel_thresh=0.0001)
    
        
    d = plotting.plot_stat_map(filename1)
    #coordComp.MaxCoord.iloc[3] = np.round(d.cut_coords, 2)
    coordComp.MaxCoord.iloc[3] = np.round(plotting.find_xyz_cut_coords(filename1, activation_threshold = 0.00001))
    create_output(filename1, cluster_extent=5, atlas=['aal'], voxel_thresh=0.0001)
       
    e = plotting.plot_stat_map(filename2)
    #coordComp.MaxCoord.iloc[4] = np.round(e.cut_coords, 2)
    coordComp.MaxCoord.iloc[4] = np.round(plotting.find_xyz_cut_coords(filename2, activation_threshold = 0.00001))
    create_output(filename2, cluster_extent=5, atlas=['aal'], voxel_thresh=0.001)
    #create_output(filename2, cluster_extent=100, atlas=['destrieux'], voxel_thresh=0.001)
    
    coordComp.Emotion.iloc[0:] = em
    
    allEm.append(coordComp)
    
    os.chdir(dmdPath)

allEms = pd.concat(allEm)
allEms.to_csv('EmGLMtoDMD_MaxComparison.csv')