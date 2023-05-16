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

nidMDPath = '/home/loued/.local/lib/python3.7/site-packages/nidmd'
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD/CorrEmoWise'

dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD'

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32']
first10M = np.arange(10)
os.chdir(dmdPath)

maxCorr = []
labelEm = []
ems = []
maxDiagMode = []

os.chdir(dmdPath)     
files = glob.glob('truncDMD_*SortedDT.csv')
files = sorted(files)
for fn in range(len(files)):
    files[fn] = os.path.join(dmdPath,files[fn])
refFile = 'truncDMD_Fear_GrandMeanSortedDT.csv'
refModes = []
refData = pd.read_csv(refFile)
for m in range(30):
    x = refData.intensity[m]
    y = x.split(',')
    y[0] = y[0].replace("[", "")
    y[399] = y[399].replace("]", "")
    z = y
    for j in range(len(y)):
        z[j] = np.complex_(y[j])
    refModes.append(z)
refModes = pd.DataFrame(refModes)
refModes = refModes.T
#    refModes = refModes.rename(columns ={0: 'first_intensity'})
for f in range (1,len(files)):
    thisFile = files[f] 
    if 'Fear' in thisFile:
        continue
    else:
        em0 =thisFile.split('truncDMD_')[1]
        em = em0.split('_GrandMeanSortedDT.csv')[0]
        targModes = []
        data = pd.read_csv(thisFile)
        for m in range(30):
            x =data.intensity[m]
            y = x.split(',')
            y[0] = y[0].replace("[", "")
            y[399] = y[399].replace("]", "")
            z = y
            for j in range(len(y)):
                z[j] = np.complex_(y[j])
            targModes.append(z)
        targModes = pd.DataFrame(targModes)
        targModes = targModes.T
        os.chdir(outPath)
    
        corrMat = np.array([])
        corrDF = pd.DataFrame()
        for c in range(30):
          if c == 0:
           corrMat= np.append(corrMat, refModes.iloc[:,c])
           corrMat= np.c_[corrMat, targModes.iloc[:,c]]
          else:
           corrMat= np.c_[corrMat, refModes.iloc[:,c]]
           corrMat= np.c_[corrMat, targModes.iloc[:,c]]
         
        corrThis = np.corrcoef(corrMat.T)
        corrKeep = corrThis[0:30, 30:]
        corrReal = corrKeep.real
        corrImag = corrKeep.imag
        corrMu = (corrReal + corrImag)/2
        
        maxCorr.append(np.max(corrMu.diagonal()))
        ems.append(em)
        maxDiagMode.append(np.argmax(corrMu.diagonal()) +1)
        plt.plot(corrMu.diagonal())
        plt.show()
        plt.close()
        corrMuD = 1 -corrMu
        corrThisDF = pd.DataFrame(corrMuD)
          
        corrThisDF.to_csv('CorrMatFearto_' + em + '_30ModesMu'  + '.csv')
        os.chdir(dmdPath)


maxCorrDF = pd.DataFrame(maxCorr)
maxCorrDFa = pd.concat([maxCorrDF, pd.DataFrame(ems), pd.DataFrame(maxDiagMode)], axis = 1)
maxCorrDFa.columns = ['Corr', 'Emotion', 'Mode']
os.chdir(dmdPath)
maxCorrDFa.to_csv('MaxCorr30Modes_byEmotoFear.csv')