#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:36:05 2023

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
import re

#def huevalueplot(cmplxarray):
#    # Creating the black cover layer
#
#    black = np.full((*cmplxarray.shape, 4), 0.)
#    black[:,:,-1] = np.abs(cmplxarray) / np.abs(cmplxarray).max()
#    black[:,:,-1] = 1 - black[:,:,-1]
#
#    # Actual plot
#
#    fig, ax = plt.subplots()
#    # Plotting phases using 'hsv' colormap (the 'hue' part)
#    ax.imshow(np.angle(cmplxarray), cmap='hsv')
#    # Plotting the modulus array as the 'value' part
#    ax.imshow(black)
#    ax.set_axis_off()


nidMDPath = '/home/loued/.local/lib/python3.7/site-packages/nidmd'
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD'
munkResPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD/CorrEmoWise/MunkResOutEmo'
outPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD/CorrEmoWise/MunkResOutEmo/rDMDs'
#dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise'

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32']

os.chdir(munkResPath)
mResFiles = sorted(glob.glob('MunkRes_*toSurprise.csv'))


os.chdir(dmdPath)
files = glob.glob('truncDMD_*GrandMeanSortedDT.csv')
files = sorted(files)
for fn in range(len(files)):
    shFile = files[fn]
    m = re.search('truncDMD_(.+?)GrandMeanSortedDT.csv', shFile)
    em = m.group(1)
    thisEm = em.split('_')[0]
    files[fn] = os.path.join(dmdPath,files[fn])
    thisFile = files[fn] 
    data = pd.read_csv(thisFile)
    if em == 'Surprise':
        continue
    else:
        mFile1 = [i for i in mResFiles if thisEm in i]
        mFile = os.path.join(munkResPath,mFile1[0])
        thisMres = pd.read_csv(mFile) 
        assIdx = thisMres.iloc[:,:-1]
        a = np.array(assIdx)
        b = a -1 
        rdata = data.reindex(b[0])
        rdata = rdata.set_index(np.arange(len(rdata)))
        rdata = rdata.sort_values(by = 'damping_time', ascending=False, ignore_index = True)
        os.chdir(outPath)
        rdata.to_csv('rDMD_TruncData_' + thisEm + '_GroupEmo.csv')
#    os.chdir(dmdPath)     
#    os.chdir(em)
            
        
        
  