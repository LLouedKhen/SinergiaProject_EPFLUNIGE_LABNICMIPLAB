#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:01:03 2023

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
#subj = ['sub-S01', 'sub-S02','sub-S03','sub-S04']

sanityCheck = pd.DataFrame(columns = {"Len", "Mov", "Em", "Sub"})
for em in Emotions:
    os.chdir(em)
    files = glob.glob('BetaSeries*')
    files = sorted(files)

    data3 = np.array([])
    for f in range (len(files)):
        
        
            thisFile = files[f] 
            start = 'BetaSeries_'
            end = '.csv'
            string = thisFile
            str1 = (string.split(start))[1].split(end)[0]
            start2 = '_'
        
            thisMov = (str1.split(start2))[1]
            thisSub = (str1.split(start2))[0].split(end)[0]
            thisEm = ((string.split(thisMov))[1].split(end)[0])[1:]
            thisPair = tuple([thisMov] + [thisEm])
            drops = tuple(drop.MovEmo.to_list())
            if str(thisPair) in drops:
                continue
            else:
            
#                if any(s in thisFile for s in subj):
                
                if em in thisFile:
                    data1 = np.array(pd.read_csv(thisFile))
                    data2 = np.transpose(data1)
                    if data2.shape[0] < 400:
                        new_row = {'Len':data2.shape[0], 'Mov':thisMov, 'Em':thisEm, 'Sub':thisSub}
                        sanityCheck = sanityCheck.append(new_row, ignore_index=True)
#                        sanityCheck.Len = sanityCheck.Len.append(data2.shape[0]) 
#                        sanityCheck.Mov = sanityCheck.Mov.append(thisMov)
#                        sanityCheck.Em = sanityCheck.Em.append(thisEm)
#                        sanityCheck.Sub = sanityCheck.Sub.append(thisSub)
    os.chdir(dmdPath)
    sanityCheck.to_csv('SanityCheckLen.csv')