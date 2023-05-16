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


Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
#subj = ['sub-S01', 'sub-S02','sub-S03','sub-S04']

os.chdir(dmdPath)
dmdFiles = glob.glob('DMD_*_20230325.csv')
testOsc = pd.read_csv('FirstComplexEmoModes20230417.csv')
for em in Emotions:
    emIdx =  [idx for idx, s in enumerate(dmdFiles) if em in s][0]
    dmdV = pd.read_csv(dmdFiles[emIdx])
    fvIdx = testOsc.index[(testOsc.Emotion=='Contempt')][0]
    filename1 = 'Brain_FirstMode_' + em +'.nii'
    filename2 = 'Brain_FirstConj_r_Mode' +str(fvIdx)+ '_' + em +'.nii'
    filename3 = 'Brain_FirstConj_i_Mode' +str(fvIdx)+ '_' + em +'.nii'
    valFirst = dmdV.intensity.iloc[0]
    val1 = dmdV.intensity.iloc[fvIdx]
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
#def fill_and_export_atlas(val, atfile, filename):
        atfile = '/home/loued/Schaefer/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii'
        atlas, _, img = nio.load_nifti_get_mask(atfile, is_mask=True, ndim=3)
        os.chdir(savePath)
        out = nifti.unfold_atlas(val1, atlas)
        nio.export_nifti(out, img, filename1)
        out = nifti.unfold_atlas(valr, atlas)
        nio.export_nifti(out, img, filename2)
        out = nifti.unfold_atlas(vali, atlas)
        nio.export_nifti(out, img, filename3)

#out = atlas.copy()
#
#labels = np.unique(atlas)
#labels = labels[labels > 0]
#
##for n, l in enumerate(labels):
##    out[atlas == l] = valr[n]
##
##io.export_nifti(out, img, filename1)
##    return
#
#for n, l in enumerate(labels):
#    out[atlas == l] = vali[n]
        from nilearn import plotting
        plotting.view_img('Brain_FirstConj_i_Mode' +fvIdx+ '_' + em +'.nii')
        plotting.plot_stat_map
        os.chdir(dmdPath)