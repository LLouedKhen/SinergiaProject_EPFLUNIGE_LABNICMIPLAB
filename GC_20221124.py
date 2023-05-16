#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 10:53:59 2022

@author: loued
"""

import os
import numpy as np 
import pandas as pd
import statsmodels.api as sm 
import statsmodels.formula.api as smf
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn import preprocessing
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
import matplotlib.pyplot as plt
import glob
import shutil

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf, grangercausalitytests
from statsmodels.nonparametric.smoothers_lowess import lowess
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA


from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn import linear_model
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
import seaborn as sns
from dtw import *
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import re

emoDataTSPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/TS_MeanScaledImputed'
brainDataTSPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TCFiles/MeanTS_Cort'
GCResPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis' 

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise']

os.chdir(emoDataTSPath)
eTSFiles = glob.glob('Mean_An*')
for ef in range (len(eTSFiles)):
    eTSFiles[ef] = os.path.join(emoDataTSPath, eTSFiles[ef])

os.chdir(brainDataTSPath)
bTSFiles = glob.glob('MeanTC*')
for bf in range (len(bTSFiles)):
    bTSFiles[bf] = os.path.join(brainDataTSPath, bTSFiles[bf])

for m in Movies:
    mTS = []
    ld = []
    em = []
    for bfile in bTSFiles:
        if m in bfile:
            thisBFile = pd.read_csv(bfile,header = None)
            mTS.append(thisBFile.iloc[1:,1:])
    for efile in eTSFiles:
        if m in efile:
            thisEFile = pd.read_csv(efile,header = None)
            thisEFile = thisEFile.iloc[1:, 1]
            string = efile
            start1 = 'Mean_An_'
            end = '.csv'
            start2 = '_'
            MovieEmo = (string.split(start1))[1].split(end)[0]
            thisEmo = (MovieEmo.split(start2))[1]
            em.append(thisEmo)
            thisEFile = pd.DataFrame(thisEFile.rename(thisEmo))
            thisEFile = thisEFile.astype(float)
            mTS.append(thisEFile)
            
    for d in range(len(mTS)):
        ld.append(mTS[d].shape[0])
        minLF = np.min(ld)
        mTS[d] = mTS[d].iloc[:minLF,:]   
            
    movDF = pd.concat(mTS, axis = 1)
    movDF = movDF.dropna()
    print(movDF.shape[1])
    
    altMovDF = movDF   
    
    for i in range(movDF.shape[1]):
        thisTs = movDF.iloc[:,i]
        plot_acf(thisTs)
        chkTSST = adfuller(thisTs)
        if chkTSST[1] > 0.05:
            dorder = 1
            chkTSST = adfuller(thisTs.diff().dropna())
            newTS = thisTs.diff().dropna()
            altMovDF.loc[:,i] = newTS
            if chkTSST[1] > 0.05:
                dorder = 2
                chkTSST = adfuller(thisTs.diff().diff().dropna())
                newTS = thisTs.diff().diff().dropna()
                altMovDF.loc[:,i] = newTS
                if chkTSST[1] > 0.05:
                    dorder = 3
                    chkTSST = adfuller(thisTs.diff().diff().diff().dropna())
                    newTS = thisTs.diff().diff().diff().dropna()
                    altMovDF.loc[:,i] = newTS
                    if chkTSST[1] > 0.05:
                        dorder = 4
                        chkTSST = adfuller(thisTs.diff().diff().diff().diff().dropna())
                        newTS = thisTs.diff().diff().diff().diff().dropna()
                        altMovDF.loc[:,i] = newTS
                        if chkTSST[1] > 0.05:
                            dorder = 5
                            chkTSST = adfuller(thisTs.diff().diff().diff().diff().diff().dropna())
                            newTS = thisTs.diff().diff().diff().diff().diff().dropna()
                            altMovDF.loc[:,i] = newTS
    print(movDF.shape[1])
                        
    altMovDF = altMovDF.dropna()
    os.chdir(GCResPath)   
    altMovDF.to_csv('MeanBrainTs_Emo_' + m + '.csv')                       
    altMDFB = altMovDF.iloc[:,:399]         
    altMDFE = altMovDF.iloc[:,400:410]                        
    mBEm = pd.DataFrame(columns = Emotions)                            
    for b in range(len(altMDFB.columns)):
        for e in altMDFE.columns:
            br = np.array(altMDFB.iloc[:,b])
            emo = np.array(altMDFE[e])
            compTs = np.transpose(np.vstack([br, emo]))
            BEmGC = grangercausalitytests(compTs, 15)
            stest = []
            for l in range(1,15):
                resp = list(BEmGC[l][0].values())[3][1]
                resf = list(BEmGC[l][0].values())[3][0]
                if resp < 0.05:
                    thisLag = (resp, resf, l)
                    stest.append(thisLag)
                else:
                    thisLag = (100, 0, 20)
                    stest.append(thisLag)            
            nstest= np.array(stest)
            windex = np.argmin(nstest[:,0])
            win = nstest[windex,:]
            mBEm.at[b, e] = win
    mBEm.to_csv('GCResults_' + m + '.csv')
            
            
                        
            
            
    
        
        
               
     
                
                
                
                
    
        
    #    thisTs = thisFile.MuRatingZ
    
    
    
    
    #for file in TSFiles:
    #    #try out ARIMA 
    #    thisFile = pd.read_csv(file)
    #    thisTs = thisFile.MuRatingZ
    #    start = 'An_'
    #    end = '.csv'
    #    string = file
    #    MovieEmo = (string.split(start))[1].split(end)[0]
    #    startM = '_'
    #    thisMovie = (MovieEmo.split(startM))[0]
#    thisEmo = (MovieEmo.split(startM))[1]
#    
    
    
#    from statsmodels.tsa.arima_model import ARIMA
#    from statsmodels.graphics.tsaplots import plot_acf
#    from statsmodels.tsa.stattools import adfuller
#    
#    plot_acf(thisTs)
#    chkTSST = adfuller(thisTs)
#    if chkTSST[1] > 0.05:
#        dorder = 1
#        chkTSST = adfuller(thisTs.diff().dropna())
#        newTS = thisTs.diff().dropna()
#        if chkTSST[1] > 0.05:
#            dorder = 2
#            chkTSST = adfuller(thisTs.diff().diff().dropna())
#            newTS = thisTs.diff().diff().dropna()
#            if chkTSST[1] > 0.05:
#                dorder = 3
#                chkTSST = adfuller(thisTs.diff().diff().diff().dropna())
#                newTS = thisTs.diff().diff().diff().dropna()
#                if chkTSST[1] > 0.05:
#                    dorder = 4
#                    chkTSST = adfuller(thisTs.diff().diff().diff().diff().dropna())
#                    newTS = thisTs.diff().diff().diff().diff().dropna()
#                    if chkTSST[1] > 0.05:
#                        dorder = 5
#                        chkTSST = adfuller(thisTs.diff().diff().diff().diff().diff().dropna())
#                        newTS = thisTs.diff().diff().diff().diff().diff().dropna()
#                
#                
#                
