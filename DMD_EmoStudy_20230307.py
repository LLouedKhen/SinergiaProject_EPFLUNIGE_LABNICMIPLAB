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
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/QC_Feb2023'
os.chdir(outPath)
drop = pd.read_csv('MovEmoToDrop.csv')
subsPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/SubjectWise'
dmdPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/DMD_Data/MovieEmotions/'
os.chdir(dmdPath)

today = date.today().strftime("%Y%m%d")
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Subjects = ['sub-S01', 'sub-S02', 'sub-S03', 'sub-S04', 'sub-S05', 'sub-S06', 'sub-S07', 'sub-S08', 'sub-S09', 'sub-S10', 'sub-S11', 'sub-S13', 'sub-S14', 'sub-S15', 'sub-S16', 'sub-S17', 'sub-S19', 'sub-S20', 'sub-S21', 'sub-S22', 'sub-S23', 'sub-S24', 'sub-S25', 'sub-S26', 'sub-S27', 'sub-S28', 'sub-S29', 'sub-S30', 'sub-S31', 'sub-S32']

checkTheseTS = []
for em in Emotions:
    
    os.chdir(dmdPath)
    os.chdir(em)
    for s in range(len(Subjects)):
        sub = Subjects[s]
        files = glob.glob('BetaSeries*'+sub+'*')
        files = sorted(files)
        for fn in range(len(files)):
            files[fn] = os.path.join(dmdPath,em,files[fn])
        data3 = np.array([])
        for f in range (len(files)):
            thisFile = files[f] 
            start = 'BetaSeries_'
            end = '.csv'
            string = thisFile
            str1 = (string.split(start))[1].split(end)[0]
            start2 = '_'
            thisMov = (str1.split(start2))[1]
            thisEm = em
            thisPair = tuple([thisMov] + [thisEm])
            drops = tuple(drop.MovEmo.to_list())
            if thisPair in drops:
                print('Skipping ' + str(thisPair))
                continue
            else:
                data1 = np.array(pd.read_csv(thisFile))
                data2 = data1[1:-1,:]
                data2 = np.transpose(data1)
                diff = 400 - data2.shape[0]
                if diff > 0:
                    rel = em + '_' +  thisMov + '_' + sub + '_' + str(diff)
                    checkTheseTS.append(rel)
                    for d in range(diff):
                        data2[-1, :] = np.zeros(data2.shape[1])
                if len(data3) == 0:
                    data3 = data2
                else:
                    data3 = np.hstack([data3, data2])
        thisSub_CortParc400 = pd.DataFrame(data3)
        os.chdir(subsPath)
        if os.path.isdir(em):
            continue
        else:
            os.mkdir(em)
        savePath = os.path.join(subsPath, em)
        os.chdir(savePath)
#        dfAll.to_csv('DMD_' + sub + '_' + em +  '_' + str(today) + '.csv')
        thisSub_CortParc400.to_csv('BetaSeriesSubjectWise_' + sub + '_' + em +  '.csv')
    os.chdir(dmdPath)
    
    os.chdir(em)
os.chdir(dmdPath)
sanCheck = pd.DataFrame(checkTheseTS)
sanCheck.to_csv('CheckSize.csv')
    
        
        
#        dcp = Decomposition(data3, filenames ='/home/loued/.local/lib/python3.7/site-packages/nidmd/tests/data/glasser.csv' )
#    #dcp = Decomposition(data3)
#        ts = TimeSeries(data = data3, sampling_time = 1.3)
#        dmd = ts.dmd()
#        where = dcp.atlas.coords_2d
#        dcp.eig_val[:5]
#        dfI =dcp.df.head()
#        dfAll =dcp.df
#
#    fullEmPath = os.path.join(dmdPath,em)
#        os.chdir(fullEmPath)
      
#    os.chdir('/home/loued/Figures')
#    fig1 = Radar(dcp.df, dcp.atlas).figure(imag = True, amount = 6)
#    fig1.show(renderer="png")
#    fig1.update_layout(title = 'Radar_' + em + '  _AllMovies' )
#    fig1.write_image('Radar_' + em + '  _AllMovies'  + str(today) + '.png')
#    
#    fig2a = Brain(dcp.df, 1, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2a.show(renderer="png")
##    fig2a.add_annotation(text = 'T =' + str(dfAll.period[2]) + '; Δ = ' + str(dfAll.damping_time[2]), align='right', valign='top')
###    fig2a.update_annotations(valign='top')
##    fig2a.update_annotations(align='right')
#    #fig2a.update_annotations(yshift=<VALUE>)
#    fig2a.update_layout(title = 'BrainSchaefer_' + em + '_AllMovies     T =' + str(round(dfAll.period[1],3)) + '; Δ = ' + str(round(dfAll.damping_time[1],3)))
#    fig2a.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) + 'Mode1.png')
#    
#    fig2b = Brain(dcp.df, 2, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
#    fig2b.show(renderer="png")
##    fig2b.add_annotation(text = 'T =' + str(dfAll.period[2]) + '; Δ = ' + str(dfAll.damping_time[2]), align='right', valign='top')
###    fig2b.update_annotations(valign='top')
###    fig2b.update_annotations(align='right')
#    fig2b.update_layout(title = 'BrainSchaefer_' + em + '_AllMovies      T =' + str(round(dfAll.period[2],3)) + '; Δ = ' + str(round(dfAll.damping_time[2],3)))
#    fig2b.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode2.png')
#    
##    fig2c = Brain(dcp.df, 3, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2c.show(renderer="png")
##    fig2c.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2c.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode3.png')
##    
##    fig2d = Brain(dcp.df, 4, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2d.show(renderer="png")
##    fig2d.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2d.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode4.png')
##    
##    fig2d = Brain(dcp.df, 5, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2d.show(renderer="png")
##    fig2d.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2d.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode5.png')
##    
##    fig2e = Brain(dcp.df, 6, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2e.show(renderer="png")
##    fig2e.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2e.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode6.png')
##    
##    fig2f = Brain(dcp.df, 7, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2f.show(renderer="png")
##    fig2f.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2f.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode7.png')
##    
##    fig2g = Brain(dcp.df, 8, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2g.show(renderer="png")
##    fig2g.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2g.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode8.png')
##    
##    fig2h = Brain(dcp.df, 9, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2h.show(renderer="png")
##    fig2h.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2h.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) +  'Mode9.png')
##    
##    fig2i = Brain(dcp.df, 10, dcp.atlas.coords_2d).figure(colormap = 'Spectral')
##    fig2i.show(renderer="png")
##    fig2i.update_layout(title = 'BrainGlasser_' + em + '  _AllMovies' )
##    fig2i.write_image('BrainGlasser_' + em + '  _AllMovies' + str(today) + 'Mode10.png')
##    
#    fig3 = Spectre(dcp.df, ['Group 1']).figure()
#    fig3.show(renderer="png")
#    fig3.update_layout(title = 'Spectre_' + em + '  _AllMovies' )
#    fig3.write_image('Spectre_' + em + '  _AllMovies' + str(today) + '.png')
#    
#    fig4 = TimePlot(dcp.df).figure(amount = 3)
#    fig4.update_layout(title = 'Timeseries_' + em + '  _AllMovies' )
#    fig4.show(renderer="png")
#    fig4.write_image('TimePlot_' + em + '  _AllMovies'  + str(today) + '.png')
#    os.chdir(dmdPath)