#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:22:04 2023

@author: loued
"""
import pandas as pd
import os
import numpy as np
from nigsp import nio, nifti
import glob
from nilearn import plotting

#atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=1, data_dir=None, base_url=None, resume=True, verbose=1)

dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'


dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions'

imgPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/MovieEmo_DMDImages'
os.chdir(imgPath)

Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
#subj = ['sub-S01', 'sub-S02','sub-S03','sub-S04']
#Emotions = ['Anger']
numE = len(Emotions)

clFiles = sorted(glob.glob('*clusters.csv'))
indexDFMu = ['MU'] * 3
indexDFFD = ['FD'] * 3
indexFM = ['FirstM'] * 3
indexFirstCpxr = ['FirstCpxr'] *3
indexFirstCpxi = ['FirstCpxi'] *3
columnsDF = ['cluster_id', 'peak_x', 'peak_y', 'peak_z', 'cluster_mean', 'volume_mm', 'aal', 'Emotion']
allData = []
for f in range(len(clFiles)):
    x = clFiles[f]
    if 'FWE' in x:
        em = x.split('_')[0]
        thisData = x.split('_')[1]
        data = pd.read_csv(x)
        nClust = len(data)
        if nClust > 3:
            nClust = 3
        if 'FD' in x:
            df = data.iloc[:nClust, :]
            df.index = indexDFFD[:nClust]
            df['Emotion'] = [em] * nClust
            allData.append(df)
        elif 'MU' in x:
            df = data.iloc[:nClust, :]
            df.index = indexDFMu[:nClust]
            df['Emotion'] = [em] * nClust
            allData.append(df)
    elif 'FirstConj_i_' in x:
        s1 = x.split('FirstConj_i_')[1].split('_clusters.csv')[0]
        em = s1.split('_')[1]
        df = data.iloc[:nClust, :]
        df.index = indexFirstCpxi[:nClust]
        df['Emotion'] = [em] * nClust
        allData.append(df)
    elif 'FirstConj_r_' in x:
        s1 = x.split('FirstConj_r_')[1].split('_clusters.csv')[0]
        em = s1.split('_')[1]
        df = data.iloc[:nClust, :]
        df.index = indexFirstCpxr[:nClust]
        df['Emotion'] = [em] * nClust
        allData.append(df)
    elif 'FirstMode_' in x:
        em = x.split('FirstMode_')[1].split('_clusters.csv')[0]
        df = data.iloc[:nClust, :]
        df.index = indexFM[:nClust]
        df['Emotion'] = [em] * nClust
        allData.append(df)
    
AllData = pd.concat(allData)
