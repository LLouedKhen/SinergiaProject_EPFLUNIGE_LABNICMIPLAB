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
brainDataTSPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TCFiles/MeanTS_All'
LabelsPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TCFiles/'
GCResPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis' 
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/QC_Feb2023'
os.chdir(outPath)
drop = pd.read_csv('MovEmoToDrop.csv')

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']
os.chdir(LabelsPath)
LabelsC = pd.read_csv('TC_cort400_labels.csv', header=None)
LC = LabelsC.values.tolist()
LabelsSC = pd.read_csv('TC_sub14_labels.csv', header=None)
LSC = LabelsSC.values.tolist()
ROIs = LC + LSC
roiList = [item for mylist in ROIs for item in mylist]
AllVal = ROIs + Emotions
#BigList = pd.DataFrame(columns = AllVal)
BigList = []

os.chdir(emoDataTSPath)
eTSFiles = glob.glob('Mean_An*')
for ef in range (len(eTSFiles)):
    eTSFiles[ef] = os.path.join(emoDataTSPath, eTSFiles[ef])

os.chdir(brainDataTSPath)
bTSFiles = glob.glob('MeanTC*')
for bf in range (len(bTSFiles)):
    bTSFiles[bf] = os.path.join(brainDataTSPath, bTSFiles[bf])

for m in Movies:
    mTSL = []
    mTS = []
    ld = []
    em = []
   
    for bfile in bTSFiles:
        if m in bfile:
            thisBFile = pd.read_csv(bfile,header = None)
            mTS.append(thisBFile.iloc[1:,1:])
#            mTS = pd.concat(mTSL, axis =1)   
#    mTSDF = pd.DataFrame(np.nan, index=np.arange(len(mTS)), columns = AllVal)
#    mTSDF.iloc[:,:414] = mTS         

    for efile in eTSFiles:
        if m in efile:
            thisEFile = pd.read_csv(efile,header = None)
            thisEFile = thisEFile.iloc[1:, 1]
            string = efile
            start1 = 'Mean_An_'
            end = '.csv'
            start2 = '_'
            MovieEmo = (string.split(start1))[1].split(end)[0]
            thisEm= (MovieEmo.split(start2))[1]
            thisMov = m
            em.append(thisEm)
            thisPair = tuple([thisMov] + [thisEm])
            drops = tuple(drop.MovEmo.to_list())
            if str(thisPair) in drops:
                continue
            else:
                thisEFile = pd.DataFrame(thisEFile.rename(thisEm))
                thisEFile = thisEFile.astype(float)
                mTS.append(thisEFile)
#                thisEFile = thisEFile.astype(float)
#                thisEFile = pd.Series(thisEFile)
#                thisEFile = thisEFile.rename(thisEm)               
#                mTSDF[thisEm] =  thisEFile.values.tolist
    for d in range(len(mTS)):
        ld.append(mTS[d].shape[0])
        minLF = np.min(ld)
        mTS[d] = mTS[d].iloc[:minLF,:]   

    mTSDF =pd.concat(mTS, axis =1) 
  
    for em in Emotions:
        if em not in mTSDF.columns:
            x =pd.Series(np.zeros(len(mTSDF)))
            x = pd.DataFrame(x.rename(em))
            mTSDF = pd.concat([mTSDF,x], axis =1)
    bDF = mTSDF.iloc[:,:414]
    bDF.columns = roiList
    eDF = mTSDF.iloc[:,415:]       
    eDF = eDF.sort_index(axis=1)

    mTSDF = pd.concat([bDF,eDF], axis = 1)
    
    BigList.append(mTSDF)
            
#    for d in range(len(mTS)):
#        ld.append(mTS[d].shape[0])
#        minLF = np.min(ld)
#        mTS[d] = mTS[d].iloc[:minLF,:]   
            
movDF = pd.concat(BigList, axis =0, ignore_index = True)  
movDF = movDF.iloc[1:,:]
#print(movDF.shape[1])

movDF = movDF.fillna(0)
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
   
    #print(movDF.shape[0])
                        
altMovDF = altMovDF.dropna()
os.chdir(GCResPath)   
altMovDF.to_csv('MeanBrainTs_EmoAllM.csv')                       
altMDFB = altMovDF.iloc[:,:414]         
altMDFE = altMovDF.iloc[:,414:]                        
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
mBEm.to_csv('GCResults_AllMovies.csv')
        