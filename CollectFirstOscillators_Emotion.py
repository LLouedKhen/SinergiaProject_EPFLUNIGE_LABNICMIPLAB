#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 10:05:00 2023

@author: loued
"""

import plotly.io as pio
pio.kaleido.scope.chromium_args = tuple([arg for arg in pio.kaleido.scope.chromium_args if arg != "--disable-dev-shm-usage"])
#pio.renderers.default ="notebook"

import numpy as np 
import pandas as pd
import os
import glob
from nidmd import Decomposition, TimeSeries, Radar, TimePlot, Brain, Spectre, Atlas, plotting
from datetime import date



nidMDPath = '/home/loued/.local/lib/python3.7/site-packages/nidmd'
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/QC_Feb2023'
os.chdir(outPath)
drop = pd.read_csv('MovEmoToDrop.csv')

dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions'
os.chdir(dmdPath)

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']

dmdFiles = glob.glob('DMD*20230325.csv')
checkModesDF1 = pd.DataFrame(index=range(11), columns=['Emotion', 'FirstConj', 'FirstConjP'])
for em in range(len(Emotions)):
    thisEm = Emotions[em]
    emIdx =  [idx for idx, s in enumerate(dmdFiles) if thisEm in s][0]
    thisFile = pd.read_csv(dmdFiles[emIdx])
    checkModesDF1.Emotion.iloc[em] = thisEm
    firstP = thisFile['conjugate'].idxmax() 
    checkModesDF1.FirstConj.iloc[em] = thisFile['conjugate'].idxmax()
    checkModesDF1.FirstConjP.iloc[em] = thisFile['period'].iloc[firstP]

checkModesDF1.to_csv('FirstComplexEmoModes' + today +'.csv')

dmdFiles = glob.glob('DMD*20230417.csv')
checkModesDF2 = pd.DataFrame(index=range(11), columns=['Emotion', 'FirstConj', 'FirstConjP'])
for em in range(len(Emotions)):
    thisEm = Emotions[em]
    emIdx =  [idx for idx, s in enumerate(dmdFiles) if thisEm in s][0]
    thisFile = pd.read_csv(dmdFiles[emIdx])
    checkModesDF2.Emotion.iloc[em] = thisEm
    firstP = thisFile['conjugate'].idxmax() 
    #check, this might not be sufficient
    
    checkModesDF2.FirstConj.iloc[em] = thisFile['conjugate'].idxmax()
    checkModesDF2.FirstConjP.iloc[em] = thisFile['period'].iloc[firstP]

checkModesDF2.to_csv('FirstComplexEmoModesSansS02' + today +'.csv')