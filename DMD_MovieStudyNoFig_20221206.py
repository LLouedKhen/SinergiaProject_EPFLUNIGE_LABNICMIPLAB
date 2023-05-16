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
testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TCFiles'
dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data'
os.chdir(testMovPath)

today = date.today().strftime("%Y%m%d")

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']

sanityCheck = np.zeros([33, 13])
files = glob.glob('TC_400*')
for m in range(len(Movies)):
    data3 = np.array([])
    for f in range (len(files)):
        thisFile = files[f]        
        if Movies[m] in thisFile:
            sub = int(thisFile[12:14])
            sanityCheck[sub, m] = 1
            data1 = np.array(pd.read_csv(thisFile))
            data2 = np.transpose(data1)
            
            if len(data3) == 0:
                data3 = data2
            else:
                data3 = np.hstack([data3, data2])
#            elif data3.shape and data2.shape[1] > data3.shape[1]:
#                data2 = np.delete(data2, range(data3.shape[1],data2.shape[1]), axis = 1)
#                data3 = np.add(data3, data2)/2
#            elif data3.shape and data2.shape[1] < data3.shape[1]:
#                data3 = np.delete(data3, range(data2.shape[1],data3.shape[1]), axis = 1)
#                data3 = np.add(data3, data2)/2
        else:
            continue
    thisn = np.sum(sanityCheck[:,m])    
    thisMovie_CortParc400 = pd.DataFrame(data3)
    os.chdir(dmdPath)
    thisMovie_CortParc400.to_csv('allS_400C_Schaefer_' + Movies[m] + '_n' + str(int(thisn)) + str(today) + '.csv')
                  
    dcp = Decomposition(data3, filenames ='/home/loued/.local/lib/python3.7/site-packages/nidmd/tests/data/glasser.csv' )
    #dcp = Decomposition(data3)
    ts = TimeSeries(data = data3, sampling_time = 1.3)
    
    dmd = ts.dmd()
    
    #dmd.keys(), dmd['values'][:5]
    
    where = dcp.atlas.coords_2d
    dcp.eig_val[:5]
    
    
    dfI =dcp.df.head()
    
    dfAll =dcp.df
#    os.chdir('/home/loued/Figures')
#    fig1 = Radar(dcp.df, dcp.atlas).figure(imag = True, amount = 6)
#    fig1.show(renderer="png")
#    fig1.update_layout(title = 'Radar_' + Movies[m] + '_n' + str(int(thisn)))
#    fig1.write_image('Radar_' + Movies[m] + '_n' + str(int(thisn)) + str(today) + '.png')
#    
#    fig2a = Brain(dcp.df, 1, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2a.show(renderer="png")
#    fig2a.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2a.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) + 'Mode1.png')
#    
#    fig2b = Brain(dcp.df, 2, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2b.show(renderer="png")
#    fig2b.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2b.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode2.png')
#    
#    fig2c = Brain(dcp.df, 3, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2c.show(renderer="png")
#    fig2c.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2c.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode3.png')
#    
#    fig2d = Brain(dcp.df, 4, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2d.show(renderer="png")
#    fig2d.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2d.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode4.png')
#    
#    fig2d = Brain(dcp.df, 5, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2d.show(renderer="png")
#    fig2d.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2d.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode5.png')
#    
#    fig2e = Brain(dcp.df, 6, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2e.show(renderer="png")
#    fig2e.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2e.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode6.png')
#    
#    fig2f = Brain(dcp.df, 7, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2f.show(renderer="png")
#    fig2f.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2f.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode7.png')
#    
#    fig2g = Brain(dcp.df, 8, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2g.show(renderer="png")
#    fig2g.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2g.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode8.png')
#    
#    fig2h = Brain(dcp.df, 9, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2h.show(renderer="png")
#    fig2h.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2h.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) +  'Mode9.png')
#    
#    fig2i = Brain(dcp.df, 10, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2i.show(renderer="png")
#    fig2i.update_layout(title = 'BrainGlasser_' + Movies[m] + '_n' + str(int(thisn)))
#    fig2i.write_image('BrainGlasser_' + Movies[m] + '_n' + str(int(thisn))+ str(today) + 'Mode10.png')
#    
#    fig3 = Spectre(dcp.df, ['Group 1']).figure()
#    fig3.show(renderer="png")
#    fig3.update_layout(title = 'Spectre_' + Movies[m] + '_n' + str(int(thisn)))
#    fig3.write_image('Spectre_' + Movies[m] + '_n' + str(int(thisn))+ str(today) + '.png')
#    
#    fig4 = TimePlot(dcp.df).figure(amount = 3)
#    fig4.update_layout(title = 'Timeseries_' + Movies[m] + '_n' + str(int(thisn)))
#    fig4.show(renderer="png")
#    fig4.write_image('TimePlot_' + Movies[m] + '_n' + str(int(thisn)) + str(today) + '.png')
    os.chdir(testMovPath)