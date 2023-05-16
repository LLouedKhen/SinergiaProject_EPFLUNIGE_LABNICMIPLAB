#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:16:09 2023

@author: loued
"""

import plotly.io as pio
pio.kaleido.scope.chromium_args = tuple([arg for arg in pio.kaleido.scope.chromium_args if arg != "--disable-dev-shm-usage"])
#pio.renderers.default ="notebook"

import numpy as np 
import pandas as pd
import os
import glob
from datetime import date
from nilearn import datasets

from nilearn.image import math_img
from nilearn import image, plotting
from statsmodels.stats.multitest import fdrcorrection


dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
imgPath  = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis'

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise']


imgTemplate = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=1, data_dir=None, base_url=None, resume=True, verbose=1)      
#atlas = math_img('img * 0', img=imgTemplate) 
labels = imgTemplate.labels.astype('str')
labels = pd.Series(labels[0:-1])

emLs = {em: pd.DataFrame() for em in Emotions}
semLs = {sem: pd.DataFrame() for sem in Emotions}



os.chdir(imgPath)
files = glob.glob('GCResults*.csv')
files = sorted(files)




#coords =pd.read_csv('Coord2d.csv')
#coords = coords.sort_values(by=['.id'])
#labels = coords.label.drop_duplicates()
#labels = labels.dropna()
#labels = labels.reset_index()

for f in files:
    data = pd.read_csv(f)
    for em in Emotions: 
        emLs[em] = pd.concat([emLs[em], data[em]], axis =1)
        semLs[em] = pd.concat([semLs[em], data[em]], axis =1)
        
for em in Emotions: 
    emLs[em].index = labels
    semLs[em].index = labels
    semLs[em].columns = Movies
    emLs[em].columns = Movies
    emLs[em].to_csv('Emotion_' + em + '_SigGC.csv')


crit = 0.05/400
for em in Emotions: 
    df1 = emLs[em]
    for w in range(df1.shape[1]):
        for r in range(df1.shape[0]):
            arr = df1.iloc[r,w]
            if '100' in arr:
                df1.iloc[r,w] = 100
            else:
                start1 = '['
                end = ' '
                p = (arr.split(start1))[1].split(end)[0]
                if len(p) == 0:
                    p = (arr.split(start1))[1].split(end)[1]
                p  = np.float(p)
                df1.iloc[r,w] = p
                if np.float(p) > crit:
                    df1.iloc[r,w] = 100
    df2 = pd.DataFrame()               
    for w in range(df1.shape[1]):           
        df2.loc[:,w] = fdrcorrection(df1.iloc[:,w])

    semLs[em] = df1

    
        
        
        
for em in Emotions:
    
    semLs[em].to_csv('Emotion_' + em + '_FWESigGC.csv')