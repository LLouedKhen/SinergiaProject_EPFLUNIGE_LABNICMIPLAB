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
from nidmd import Decomposition, TimeSeries, Radar, TimePlot, Brain, Spectre, Atlas, plotting
from datetime import date



nidMDPath = '/home/loued/.local/lib/python3.7/site-packages/nidmd'
dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis'
dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data'
os.chdir(testMovPath)

today = date.today().strftime("%Y%m%d")

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = {'Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise'};
Coord2d =pd.read_csv('/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis/Coord2d.csv')
dataF = pd.DataFrame(columns = Emotions)

sanityCheck = np.zeros([33, 13])
files = glob.glob('GCResults_*.csv')
crit = 0.05/200
for m in range(len(Movies)):
    dataF = pd.DataFrame()
    for f in range (len(files)):
        thisFile = files[f]        
        if Movies[m] in thisFile:
            data3 = pd.read_csv(thisFile)
            data3 = data3.iloc[:,1:]
            
        else:
            continue
      
        for em in range(len(Emotions)):
            dataS = pd.DataFrame()
            for j in range (data3.shape[0]):
                x = data3.iloc[j, em]
                if '100 ' in x:
                    st = ' '
                    end = ' '
                    xx = (x.split(st))[0].split(end)[0]
                    br = '['
                    xxx = (xx.split(br))[1]
                    dataF.loc[j, em] = float(xxx)
                elif x.startswith('['):
                    st = '['
                    end = ' '
                    xx = x.replace('[', '')
                    if xx[0].isdigit():
                        xxx = (xx.split(end)[0])
#                    br = '['
#                    xxx = (xx.split(br))[1]
                        dataF.loc[j, em] = float(xxx)
                    else:
                        xxx = (xx.split(end)[1])
#                    br = '['
#                    xxx = (xx.split(br))[1]
                    dataF.loc[j, em] = float(xxx)
                
                if dataF.iloc[j, em] == 100:
                    dataF.iloc[j, em] = 1
                elif dataF.iloc[j, em] > crit and dataF.iloc[j, em] < 100:
                    dataF.iloc[j, em] = 1
                elif dataF.iloc[j, em] <= crit:
                    dataF.iloc[j, em] =  np.abs(np.log(dataF.iloc[j, em])) 
#            dataF.columns = Emotions    
            
            dataS['intensity'] = dataF.iloc[:,em]
            dataS['conjugate'] = False
    
    
                  
#    dcp = Decomposition(dataS, filenames ='/home/loued/.local/lib/python3.7/site-packages/nidmd/tests/data/schaefer_test.mat' )
#    #dcp = Decomposition(data3)
##    ts = TimeSeries(data = data3, sampling_time = 1.3)
##    
##    dmd = ts.dmd()
##    
#    #dmd.keys(), dmd['values'][:5]
#    
#    where = dcp.atlas.coords_2d
#    dcp.eig_val[:5]
#    
#    
#    dfI =dcp.df.head()
#    
    
        fig2a = Brain(dataS, 1, Coord2d).figure(colormap = 'Spectral')
        fig2a.show(renderer="png")
#    fig2a.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2a.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) + 'Mode1.png')
    
