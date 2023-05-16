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
#Emotions = ['Anger']

os.chdir(dmdPath)
dmdFiles = glob.glob('DMD_*_20230325.csv')
testOsc = pd.read_csv('FirstComplexEmoModes20230417.csv')
allEm = []

for em in Emotions:
    bFile1 = os.path.join(glm1Path, em, em + '_MU_FWE.nii')
#    a = plotting.plot_stat_map(bFile1)
#    coordComp.MaxCoord.iloc[0] = np.round(a.cut_coords, 2)
    create_output(bFile1, cluster_extent=5, atlas=['aal'], outdir = savePath)

    bFile2 = os.path.join(glm2Path, em, em + '_FD_FWE.nii')    
#    b = plotting.plot_stat_map(bFile2)  
#    coordComp.MaxCoord.iloc[1] = np.round(b.cut_coords, 2)
    create_output(bFile2, cluster_extent=5, atlas=['aal'], outdir = savePath)
#    create_output(bFile2, cluster_extent=5, atlas=['destrieux'], voxel_thresh=0.001
    
          
#    c = plotting.plot_stat_map(filename3)
#    coordComp.MaxCoord.iloc[2] = np.round(plotting.find_xyz_cut_coords(filename3, activation_threshold = 0.001))
##    coordComp.MaxCoord.iloc[2] = np.round(c.cut_coords, 2)
#    create_output(filename3, cluster_extent=100, atlas=['aal'], voxel_thresh=0.0001)
#    
#        
#    d = plotting.plot_stat_map(filename1)
#    #coordComp.MaxCoord.iloc[3] = np.round(d.cut_coords, 2)
#    coordComp.MaxCoord.iloc[3] = np.round(plotting.find_xyz_cut_coords(filename1, activation_threshold = 0.001))
#    create_output(filename1, cluster_extent=100, atlas=['aal'], voxel_thresh=0.001)
#       
#    e = plotting.plot_stat_map(filename2)
#    #coordComp.MaxCoord.iloc[4] = np.round(e.cut_coords, 2)
#    coordComp.MaxCoord.iloc[4] = np.round(plotting.find_xyz_cut_coords(filename2, activation_threshold = 0.001))
#    create_output(filename2, cluster_extent=100, atlas=['aal'], voxel_thresh=0.001)
#    #create_output(filename2, cluster_extent=100, atlas=['destrieux'], voxel_thresh=0.001)


#allEms = pd.concat(allEm)
#allEms.to_csv('EmGLMtoDMD_MaxComparison.csv')