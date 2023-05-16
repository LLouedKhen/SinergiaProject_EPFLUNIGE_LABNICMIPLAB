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
DMDoutputFiles = glob.glob('DMD_*.csv')

custom_palette = sns.color_palette("viridis", 11)

for f in range(len(DMDoutputFiles)):
    data = pd.read_csv(DMDoutputFiles[f])
    em = Emotions[f]
    os.chdir('/home/loued/Figures')
    dist = sns.distplot(data.damping_time, color= custom_palette[f])
    ymin,ymax = dist.get_ylim()
#    plt.axvline(ymax)
    plt.title(em + " Damping Time Distribution")
    plt.savefig('DMD_DistDampingTimes_' + em + '.png')
    plt.show()
    plt.close()
    
    plt.plot(data.conjugate[:30])
    plt.title(em + " Real and Complex Damping Times over Modes")
    plt.savefig('DMD_RealComplexOverModes_' + em + '.png')
    plt.show()
    plt.close()
    
    ax = (data.conjugate.value_counts().plot(kind = 'bar'))
    plt.title(em + " Real and Complex Damping Times Summed")
    plt.savefig('DMD_RealComplexOverall_' + em + '.png')
    plt.show()
    plt.close()
    os.chdir(dmdPath)