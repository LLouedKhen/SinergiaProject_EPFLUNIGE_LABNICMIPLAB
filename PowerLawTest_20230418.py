#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 08:00:17 2022

@author: loued
"""

import plotly.io as pio
pio.kaleido.scope.chromium_args = tuple([arg for arg in pio.kaleido.scope.chromium_args if arg != "--disable-dev-shm-usage"])
#pio.renderers.default ="notebook"

import numpy as np 
import pandas as pd
import os
import glob
#from nidmd import Decomposition, TimeSeries, Radar, TimePlot, Brain, Spectre, Atlas, plotting
from datetime import date
import powerlaw


nidMDPath = '/home/loued/.local/lib/python3.7/site-packages/nidmd'
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Criticality'
os.chdir(outPath)
#drop = pd.read_csv('MovEmoToDrop.csv')

bsPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions'
os.chdir(bsPath)

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
#subj = ['sub-S01', 'sub-S02','sub-S03','sub-S04']

files = glob.glob('BetaSeries* _20230325.csv')
files = sorted(files)
#checkTheseTS = []
for em in Emotions:
    for f in range (len(files)):
        thisFile = files[f]              
        if em in thisFile:
            data1 = np.array(pd.read_csv(thisFile))
            data3 = data1[1:-1,:]
            data3 = np.transpose(data3)            
            for i in range(data3.shape[0]):
                dataM = data3[i,:]
                results = powerlaw.Fit(dataM)
                print(results.power_law.alpha)
                print(results.power_law.xmin)
                R, p = results.distribution_compare('power_law', 'lognormal')
