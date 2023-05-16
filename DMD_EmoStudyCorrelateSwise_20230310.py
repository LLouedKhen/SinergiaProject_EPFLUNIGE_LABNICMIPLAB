#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 13:56:56 2023

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
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/CorrMat_First10Modes'

dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise'

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30']
first10M = np.arange(10)
os.chdir(dmdPath)


for em in Emotions:
    os.chdir(dmdPath)     
    os.chdir(em)
    files = glob.glob('DMD*')
    files = sorted(files)
    for fn in range(len(files)):
        files[fn] = os.path.join(dmdPath,em,files[fn])
    refFile = files[0]
    refModes = []
    refData = pd.read_csv(refFile)
    for m in range(10):
        refModes.append(refData.intensity[m])
    refModes = pd.DataFrame(refModes)
    refModes = refModes.rename(columns ={0: 'intensity'})
    for f in range (1,len(files)):
        sub = Subjects[f]
        thisFile = files[f] 
        data = pd.read_csv(thisFile)
        for c in range(10):
            corrThis = np.correlate(refModes.intensity[c], data.intensity[c], 'full')
            corrThisDF = pd.DataFrame(corrThis)
            os.chdir(outPath)
            corrThisDF.to_csv('CorrMat_' + sub + '_Mode' + str(c) + '_' + em +  '.csv')
    os.chdir(dmdPath)
    os.chdir(em)