#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:37:10 2023

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



nidMDPath = '/home/loued/.local/lib/python3.7/site-packages/nidmd'
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
rDMDPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD/CorrEmoWise/MunkResOutEmo/rDMDs'
dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise'

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32']

os.chdir(rDMDPath)
rDMDFiles = sorted(glob.glob('rDMD_*.csv'))
for r in range(len(rDMDFiles)):
    rDMDFiles[r] = os.path.join(rDMDPath,rDMDFiles[r])
refDMD = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise/TruncDMD/truncDMD_Surprise_GrandMeanSortedDT.csv'
rDMDFiles.append(refDMD)

valDF = pd.DataFrame(columns =Emotions, index = np.arange(30) + 1)
valROIDF = pd.DataFrame(columns =Emotions, index = np.arange(30) + 1)
dtDF = pd.DataFrame(columns =Emotions, index = np.arange(30) + 1)
periodDF = pd.DataFrame(columns =Emotions, index = np.arange(30) + 1)
for em in Emotions:
    emFile = [i for i in rDMDFiles if em in i]
#    bigDF = pd.DataFrame(columns =['mode', 'value', 'intensity', 'damping_time', 'period',
#       'conjugate', 'strength_real', 'strength_imag', 'activity'], index = np.arange(30))
#    bigDF['mode'] = np.arange(30) +1
    bigL = []
#    for fn in range(len(emFiles)):
#        thisFile = emFiles[fn]
    data = pd.read_csv(emFile[0])
    for m in range(30):
        x =data.intensity[m]
        y = x.split(',')
        y[0] = y[0].replace("[", "")
        y[399] = y[399].replace("]", "")
        z = y
        for j in range(len(y)):
#            c1 = z[j] + 'j'
#            c2 = c1.replace(" ", "")
#            c3 = c2.lstrip()
#            c4 = c3.rstrip()
#            c5 = c4.strip('\n')
            z[j] = np.complex(y[j])
        data.intensity.iloc[m] = z
#        for m in range(30):
#            x =data.strength_imag[m]
#            y = x[1:-1]
#            z = [float(i) for i in y.split(',')]
##            z[0] = z[0][1:]
##            for j in range(len(z)):
##                c1 = z[j]
##                c2 = c1.replace(" ", "")
##                c3 = c2.lstrip()
##                c4 = c3.rstrip()
##                c5 = c4.strip('\n')
##                z[j] = float(c5)
#            data.strength_imag[m] = z
#        for m in range(30):
#            x =data.strength_real[m]
#            y = x[1:-1]
#            z = [float(i) for i in y.split(',')]
##            z[0] = z[0][1:]
##            for j in range(len(z)):
##                c1 = z[j]
##                c2 = c1.replace(" ", "")
##                c3 = c2.lstrip()
##                c4 = c3.rstrip()
##                c5 = c4.strip('\n')
##                z[j] = float(c5)
#            data.strength_real[m] = z
##        for m in range(30):
##            x =data.activity[m]
##            y = x[1:-1]
##            z = y.replace('\n', '')
##            z = [float(i) for i in y.split(',')]
###            z[0] = z[0][1:]
###            for j in range(len(z)):
###                c1 = z[j]
###                c2 = c1.replace(" ", "")
###                c3 = c2.lstrip()
###                c4 = c3.rstrip()
###                c5 = c4.strip('\n')
###                z[j] = float(c5)
##            data.activity[m] = z
        bigL.append(data)
        valROIDF[em] = data.intensity.values
        valDF[em] = data.value.values
        dtDF[em] = data.damping_time.values
        periodDF[em] = data.period.values
    
valDFa = valDF.to_numpy().astype(complex)

valStd = np.zeros(30)
dtStd = np.zeros(30)
periodStd = np.zeros(30)

for i in range(30):
    valStd[i] = np.std(valDFa[i,:])
    dtStd[i] = np.std(dtDF.iloc[i,:])
    periodStd[i] = np.std(periodDF.iloc[i,:])

periodStd[periodStd > 15000] = 2000
dmdOutstd = np.transpose(np.vstack((valStd, dtStd, periodStd)))


fig, (ax1, ax2, ax3) = plt.subplots(nrows = 1, ncols = 3, sharex=True, sharey=False, figsize=(12, 6))

stdminVal = valStd.min()
stdminDT = dtStd.min()
stdminPer = periodStd.min()

ax1.set_title('DMD Eigenvalue')
ax1.fill_between(np.arange(30), stdminVal, valStd, alpha=0.7)
ax2.set_title('DMD Damping Time')
ax2.fill_between(np.arange(30), stdminDT, dtStd, color = 'orange', alpha=0.7)
ax3.set_title('DMD Period')
ax3.fill_between(np.arange(30), stdminPer, periodStd, color = 'pink', alpha=0.7)

for ax in ax1, ax2, ax3:
    ax.grid(True)
    ax.label_outer()

ax1.set_ylabel('STD')
ax1.set_xlabel('Modes')

fig.suptitle('Standard Deviation across Emotion DMDs')
os.chdir('/home/loued/Figures')
plt.savefig('FigureDispersion_rDMDGM_AcrossEmo.png', format = 'png')


#        if fn == 0:
#            bigDF['value'] = data.value
#            bigDF['intensity'] = data.intensity
#            bigDF['damping_time'] = data.damping_time
#            bigDF['period'] = data.period
#            bigDF['strength_real'] = data.strength_real
#            bigDF['strength_imag'] = data.strength_imag
#            #bigDF['activity'] = data.activity
#        else:
#            bigDF['value'] = (data.value.astype(complex)+ bigDF['value'].astype(complex)) /2
#            for l in range(len(data)):
#                for w in range(len(data.intensity.iloc[l])):
#                    bigDF['intensity'].iloc[l][w] = (data.intensity.iloc[l][w]  + bigDF['intensity'].iloc[l][w]) /2
##            bigDF['damping_time'] = (data.damping_time + bigDF['damping_time'])  /2
##            bigDF['period'] = (data.period + bigDF['period'] ) /2
#            for l in range(len(data)):
#                for w in range(len(data.strength_real.iloc[l])):
#                    bigDF['strength_real'].iloc[l][w] = (data.strength_real.iloc[l][w] + bigDF['strength_real'].iloc[l][w]) /2
#            for l in range(len(data)):
#                for w in range(len(data.strength_imag.iloc[l])):        
#                    bigDF['strength_imag'].iloc[l][w]= (data.strength_imag.iloc[l][w] + bigDF['strength_imag'].iloc[l][w])  /2
#           
##            bigDF['activity'] = (data.activity + bigDF['activity'])   /2
#    for bl in range(len(bigDF)):
#        if isinstance(bigDF.value.iloc[bl], complex):
#            bigDF.conjugate = True
#        
#    for bl in range(len(bigDF)):
#        bigDF['damping_time'].iloc[bl] = (-1 / np.log(np.abs(bigDF.value.iloc[bl]))) * 1.3
#        bigDF['period'].iloc[bl] =((2 * np.pi) / np.abs(np.angle(bigDF.value.iloc[bl]))) * 1.3 if bigDF.conjugate.iloc[bl] else np.inf
#    
#    bigDF.to_csv('truncDMD_' + em + '_GrandMean.csv')
#    bigDF2 = bigDF.sort_values(by = 'damping_time', ascending=False, ignore_index = True)
#    bigDF2['mode'] = np.arange(30) + 1
#    bigDF2.to_csv('truncDMD_' + em + '_GrandMeanSortedDT.csv')