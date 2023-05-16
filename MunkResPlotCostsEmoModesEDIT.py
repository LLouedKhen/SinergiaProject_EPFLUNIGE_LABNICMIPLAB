#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 08:51:13 2023

@author: loued
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 07:59:49 2023

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
#Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32']
Subjects = ['sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32']

inPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/EmoWiseMunkRes/MunkResOutEmo'


os.chdir(inPath)
files = glob.glob('MunkRes_*')
AllEm = []
for em in Emotions:
#    EMO = 'Anger'
    thisEm = [];   
    filesEm = glob.glob('*'+ em +'*.csv' )
    for m in np.arange(1,30):
        mIdx = filesEm.index('MunkRes_' + em + '_Mode' +str(m+1)+'_toMode1.csv')
        thisData = pd.read_csv(filesEm[mIdx])
        z = thisData.cost[0]
        if isinstance(z, str):
            c1 = z.replace("i", "j")
            c2 = c1.replace(" ", "")
            c3 = c2.lstrip()
            c4 = c3.rstrip()
            z = np.complex_(c4)
            thisCost = z 
        else:
            z = np.complex_(z)
            thisCost = z                
        thisEm.append(thisCost)
    thisEmM = np.stack(thisEm)
    AllEm.append(thisEmM)

fig1, axr =  plt.subplots(4, 3,layout="constrained", figsize=(10, 10))
for r in np.arange(1,5):
    for c in np.arange(1,4):
        if r ==1:
            el = (r * c)  -1
            print(el)
        elif r == 2:
            el = (c + r) 
            print(el)
        elif r == 3:
           el = (c + r) + 2
           print(el)
        elif r == 4:
             el = (c + r) + 4
             print(el)
        if el == 11:
                continue
        axr[r-1, c-1].plot(AllEm[el].real)
        #axs[r, c].legend(Subjects, loc='center right',  bbox_to_anchor=(1, 0.5), shadow=True)
        axr[r-1, c-1].set_title(Emotions[el] + ' Real')

for ax1 in axr.flat:
    ax1.set(xlabel='Mode', ylabel='Cost')
    handles, labels = ax1.get_legend_handles_labels()
#    fig1.legend(Subjects, ncol=2, loc='center right',  bbox_to_anchor=(1.25, 0.8), shadow=True )
    os.chdir('/home/loued/Figures')
    plt.savefig('Real Cost by Emotion to Mode 1 Across Modes', format="pdf")
    os.chdir(inPath)

fig2, axi = plt.subplots(4, 3,layout="constrained", figsize=(10, 10))

for r in np.arange(1,5):
    for c in np.arange(1,4):
        if r ==1:
            el = (r * c)  -1
            print(el)
        elif r == 2:
            el = (c + r) 
            print(el)
        elif r == 3:
           el = (c + r) + 2
           print(el)
        elif r == 4:
             el = (c + r) + 4
             print(el)
        if el == 11:
                continue
        axi[r-1, c-1].plot(AllEm[el].imag)
        #axs[r, c].legend(Subjects, loc='center right',  bbox_to_anchor=(1, 0.5), shadow=True)
        axi[r-1, c-1].set_title(Emotions[el] + ' Imag')

for ax2 in axi.flat:
    ax2.set(xlabel='Mode', ylabel='Cost')
    handles, labels = ax2.get_legend_handles_labels()
#    fig2.delaxes(axi[3][2])
#    fig2.legend(Subjects, ncol=2, loc='center right',  bbox_to_anchor=(1.25, 0.8), shadow=True )
    os.chdir('/home/loued/Figures')
    plt.savefig('Imag Cost by Emotion to Mode 1 across Modes', format="pdf")
    os.chdir(inPath)        
               