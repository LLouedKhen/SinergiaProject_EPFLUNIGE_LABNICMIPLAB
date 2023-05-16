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
import scipy.stats

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

os.chdir(dmdPath)
files =glob.glob('DMD_*20230325.csv')

#def cohend(d1, d2):
#    # calculate the size of samples
#    n1, n2 = len(d1), len(d2)
#    # calculate the variance of the samples
#    s1, s2 = np.var(d1, ddof=1), np.var(d2, ddof=1)
#    # calculate the pooled standard deviation
#    s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
#    # calculate the means of the samples
#    u1, u2 = np.mean(d1), np.mean(d2)
#    # calculate the effect size
#    return (u1 - u2) / s

EmoMats = []
EmoMatsP = []
EmoMatsDT = []
EmoCorrMatsR = []
EmoCorrMatsI = []
labelE = []
emTags = []


for fn in range(len(files)):
    files[fn] = os.path.join(dmdPath,files[fn])
    for em in Emotions:
        if em in files[fn]:
            file = files[fn]
            refData = pd.read_csv(file)
#    refFile = files[0]
            Modes = []
            periods = []
            dampT = []
            for m in range(30):
                x = refData.intensity[m]
                damp = refData.damping_time[m]
                p = refData.period[m]
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
                Modes.append(z)
                dampT.append(damp)
                periods.append(p)
            ModesDF = pd.DataFrame(Modes)
            PeriodsDF = pd.DataFrame(periods)
            DampDF = pd.DataFrame(dampT)
            ModesDF = ModesDF.T
            EmoMats.append(ModesDF)
            EmoMatsDT.append(DampDF)
            EmoMatsP.append(PeriodsDF)
            labelE.append(em)
        #    refModes = refModes.rename(columns ={0: 'first_intensity'})
            os.chdir(outPath)
coefP = []
coefDT = []
for em in range(len(labelE)-1):
    emR = EmoMats[em]
    emRP = EmoMatsP[em]
    emRDT = EmoMatsDT[em]
    emoRef = labelE[em]
    for t in range(em +1,len(labelE)):
        emoTarg = labelE[t]
        emT = EmoMats[t]
        emTP = EmoMatsP[t]
        emTDT = EmoMatsDT[t]
        coefsr = []
        coefsi = []

        emTags.append(emoRef + '_' +  emoTarg)
        corrP = pd.DataFrame(pd.concat([emRP, emTP], axis =1)).corr()
        corrDT = pd.DataFrame(pd.concat([emRDT, emTDT], axis =1)).corr()
        coefP.append(corrP.iloc[1,0])
        coefDT.append(corrDT.iloc[1,0])
        for m in np.arange(emT.shape[1]):                   
            corrMat= np.c_[emR.iloc[:,m].values, emT.iloc[:,m].values]
            corrThis = np.corrcoef(corrMat)
            corrReal = corrThis.real
            corrImag = corrThis.imag
#        #        sns.heatmap(corrReal)
#        #        sns.heatmap(corrImag)
#        #        huevalueplot(corrDF)
#                #corrMat.append(corrThis)
            corrThisDF = pd.DataFrame(corrThis)
            muCorrR = np.mean(corrReal)
            muCorrI = np.mean(corrImag)
#            corrDT = np.Corr
            coefsr.append(muCorrR)
            coefsi.append(muCorrI)
        EmoCorrMatsR.append(coefsr)
        EmoCorrMatsI.append(coefsi)
        
eDFR = pd.DataFrame(EmoCorrMatsR, index = emTags) 
eDFRt = eDFR.copy(deep = True)
eDFRp = eDFR.copy(deep = True)

for i in range(eDFRt.shape[0]):
    for j in range(eDFRt.shape[1]):
        eDFRt.iloc[i,j] = (eDFR.iloc[i,j] * np.sqrt(398))/np.sqrt(1-(eDFR.iloc[i,j]**2))
        eDFRp.iloc[i,j] = scipy.stats.t.sf(abs(eDFRt.iloc[i,j]), df = 398) *2
for i in range(eDFR.shape[0]):
    for j in range(eDFRt.shape[1]):
        if eDFRp.iloc[i,j] > 0.05 or eDFR.iloc[i,j] < 0.25:
            eDFR.iloc[i,j] = 0
eDFI = pd.DataFrame(EmoCorrMatsI, index = emTags) 


fig1, axr =  plt.subplots(6, 2,layout="constrained", figsize=(15, 15))
for r in np.arange(1,7):
    for c in np.arange(1,3):
        if r ==1:
            el = (r * c)  -1
            print(el)
        elif r == 2:
            el = (c) + 1 
            print(el)
        elif r == 3:
           el = (c + r) 
           print(el)
        elif r == 4:
             el = (c + r) + 1
             print(el)
        elif r == 5:
             el = (c + r) + 2
             print(el)
        elif r == 6:
             el = (c + r) + 3
             print(el)
        
        if el == 11:
                continue
        thisData = eDFR.filter(like = Emotions[el], axis = 0)
        labels = thisData.index
        lgd = []
        for l in labels:
            h = l.replace(Emotions[el],'')
            lgd.append(h.replace('_',''))
        axr[r-1, c-1].plot(thisData.transpose(), label=lgd)
        axr[r-1, c-1].legend(lgd, bbox_to_anchor=(0.5, 1.05),
          ncol=2,loc = 'upper left')
        #axs[r, c].legend(Subjects, loc='center right',  bbox_to_anchor=(1, 0.5), shadow=True)
        axr[r-1, c-1].set_title(Emotions[el] + ' Real')

for ax1 in axr.flat:
    ax1.set(xlabel='Mode', ylabel='R Coef')
    handles, labels = ax1.get_legend_handles_labels()
#    fig1.legend(Subjects, ncol=2, loc='center right',  bbox_to_anchor=(2.25, 0.8), shadow=True )
    os.chdir('/home/loued/Figures')
    plt.savefig('CorrPlotModesAcrossEmotionsReal.png', format="png")
#    os.chdir(inPath)

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
        axi[r-1, c-1].plot(eDFI.filter(like = Emotions[el], axis = 0).transpose())
        #axs[r, c].legend(Subjects, loc='center right',  bbox_to_anchor=(1, 0.5), shadow=True)
        axi[r-1, c-1].set_title(Emotions[el] + ' Imag')

for ax2 in axi.flat:
    ax2.set(xlabel='Mode', ylabel='R Coef')
    handles, labels = ax2.get_legend_handles_labels()
#    fig2.delaxes(axi[3][2])
#    fig2.legend(, ncol=2, loc='center right',  bbox_to_anchor=(1.25, 0.8), shadow=True )
    os.chdir('/home/loued/Figures')
    plt.savefig('CorrPlotModesAcrossEmotionsImag.png', format="png")
#    os.chdir(inPath)        
               


#for em in Emotions:
#    data1 = eDFR.filter(like = em, axis = 0)  
#    plt.plot(data1)     
#    data2 = eDFI.filter(like = em, axis = 0)  
#    plt.plot(data2) 
#            
#                corrThisDF.to_csv('CorrMatMode1to_' + em + '_Mode' + str(t+1)  + '.csv')
#            Ur = np.triu(corrReal)
#            Urm = np.mean(Ur)
#            Ui = np.triu(corrImag)
#            Uim = np.mean(Ui)
#                corrRefFr.append(Urm)
#                corrRefFi.append(Uim)
        
#            modeRef = ModesDF.iloc[:,0].values
#            corrDF = pd.DataFrame()
#            corrMat= modeRef
#            for t in np.arange(1,ModesDF.shape[1]):                   
#                corrMat= np.c_[corrMat, ModesDF.iloc[:,t].values]
#                corrThis = np.corrcoef(corrMat)
#                corrReal = corrThis.real
#                corrImag = corrThis.imag
#        #        sns.heatmap(corrReal)
#        #        sns.heatmap(corrImag)
#        #        huevalueplot(corrDF)
#                #corrMat.append(corrThis)
#                corrThisDF = pd.DataFrame(corrThis)
#                corrThisDF.to_csv('CorrMatMode1to_' + em + '_Mode' + str(t+1)  + '.csv')
#                Ur = np.triu(corrReal)
#                Urm = np.mean(Ur)
#                Ui = np.triu(corrImag)
#                Uim = np.mean(Ui)
#                corrRefFr.append(Urm)
#                corrRefFi.append(Uim)
#            for t in np.arange(1,ModesDF.shape[1]-1):                   
#                corrMat2= np.c_[ModesDF.iloc[:,t].values, ModesDF.iloc[:,t+1].values]
#                corrThis2 = np.corrcoef(corrMat2)
#                corrReal2 = corrThis2.real
#                corrImag2 = corrThis2.imag
#        #        sns.heatmap(corrReal)
#        #        sns.heatmap(corrImag)
#        #        huevalueplot(corrDF)
#                #corrMat.append(corrThis)
#                corrThisDF2 = pd.DataFrame(corrThis2)
#                corrThisDF2.to_csv('CorrMatModeNN' + str(t) + 'to_' + em + '_Mode' + str(t+1)  + '.csv')
#                Ur2 = np.triu(corrReal2)
#                Urm2 = np.mean(Ur2)
#                Ui2 = np.triu(corrImag2)
#                Uim2 = np.mean(Ui2)
#                corrNNFr.append(Urm2)
#                corrNNFi.append(Uim2)
#            os.chdir(dmdPath)
#    corrRefValr.append(corrRefFr)
#    corrRefVali.append(corrRefFi)
#    corrNNValr.append(corrNNFr)
#    corrNNVali.append(corrNNFi)
