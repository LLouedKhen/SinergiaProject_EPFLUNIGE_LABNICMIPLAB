#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 09:32:41 2023

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
import seaborn as sns
import matplotlib.pyplot as plt
from kneed import DataGenerator, KneeLocator


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
files = sorted(glob.glob('DMD_*20230325.csv'))

#custom_palette = sns.color_palette("viridis", 11)

ifPt = []
emS = []
for fn in range(len(files)):
    files[fn] = os.path.join(dmdPath,files[fn])
    for em in Emotions:
        if em in files[fn]:
            file = files[fn]
            data = pd.read_csv(file)
            y = data.damping_time
            x = np.arange(len(y))
            kneedle = KneeLocator(x, y, S=1.0, curve="convex", direction="decreasing")
            ifPt.append(kneedle.elbow)
            emS.append(em)
            kneedle.plot_knee()
emSdf= pd.DataFrame(emS)
ifPtdf = pd.DataFrame(ifPt)
elbowPts = pd.concat([ifPtdf, emSdf], axis = 1)
elbowPts.columns = ['elbow', 'Emotion']

elbowPts.to_csv('ModesPerEmotion_toInflectionPoint.csv')
