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
import seaborn as sns
import matplotlib.pyplot as plt

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
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/EmoWiseMunkRes'

dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/'

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32']
first10M = np.arange(10)
os.chdir(dmdPath)


for em in Emotions:
    os.chdir(dmdPath)     
    for fn in range(len(files)):
        files[fn] = os.path.join(dmdPath,files[fn])
    refFile = files[0]
    refModes = []
    refData = pd.read_csv(refFile)
    for m in range(30):
        x = refData.intensity[m]
        y = x.split('j')
        z = y[:-1]
        z[0] = z[0][1:]
        for j in range(len(z)):
            c1 = z[j] + 'j'
            c2 = c1.replace(" ", "")
            c3 = c2.lstrip()
            c4 = c3.rstrip()
            c5 = c4.strip('\n')
            z[j] = np.complex_(c5)
        refModes.append(z)
    refModes = pd.DataFrame(refModes)
    refModes = refModes.T
#    refModes = refModes.rename(columns ={0: 'first_intensity'})
    os.chdir(outPath)
    modeRef = refModes.iloc[:,0].values
    corrDF = pd.DataFrame()
    corrMat= modeRef
    for t in np.arange(1,refModes.shape[1]):                   
        corrMat= np.c_[corrMat, refModes.iloc[:,t].values]
        corrThis = np.corrcoef(corrMat)
        corrReal = corrThis.real
        corrImag = corrThis.imag
#        sns.heatmap(corrReal)
#        sns.heatmap(corrImag)
#        huevalueplot(corrDF)
        #corrMat.append(corrThis)
        corrThisDF = pd.DataFrame(corrThis)
        corrThisDF.to_csv('CorrMatMode1to_' + em + '_Mode' + str(t+1)  + '.csv')
    os.chdir(dmdPath)
