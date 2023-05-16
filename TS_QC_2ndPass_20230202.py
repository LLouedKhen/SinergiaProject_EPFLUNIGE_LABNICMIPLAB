#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu 02.02.2023
Look for concordance across Ss with Var, maybe Dice, and check for all noise no signal TS 

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
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn import linear_model
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import re
import itertools
from scipy.stats import normaltest, kstest, norm, shapiro, anderson
import seaborn as sns
from scipy.stats import pearsonr


outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/QC_Feb2023'
inDataTSPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Raw_annotations/ParticipantTasks/Processed'

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction','Shame', 'Surprise']

os.chdir(inDataTSPath)
eTSFiles = glob.glob('DF_*')
MovEmo = pd.MultiIndex.from_product([Movies, Emotions],names=['Movie', 'Emotions'])
qcDF = pd.DataFrame(columns = ["n","len", "Var", "CV", "ICC", "CorrMean", "CorrP","Normk", "Normp", "KsTests", "KsTestp", "ShpTests", "ShpTestp"], index = MovEmo)

kap = []
fileSC = pd.DataFrame(columns = ["QC", "n"], index = MovEmo)


for file in eTSFiles:
    
    thisFile = pd.read_csv(file)
    data = thisFile.iloc[:,1:]
    corrM = np.zeros((data.shape[1],data.shape[1]))
    start = 'DF_'
    end = '.csv'
    string = file
    MovEm = (string.split(start))[1].split(end)[0]
    mTest = [m in MovEm for m in Movies]
    t1 = [i for i, y in enumerate(mTest) if y]
    emTest = [em in MovEm for em in Emotions]
    t2 = [j for j, z in enumerate(emTest) if z]
    if t1 and t2:

        thisMov = Movies[t1[0]]
        thisEm = Emotions[t2[0]]
        if data.shape[1] > 1:
            fileSC.loc[thisMov, thisEm].QC = '1P'
        else:
            fileSC.loc[thisMov, thisEm].QC= 'POOR'
        thisLen = data.shape[0]
        qcDF.loc[thisMov, thisEm].len = thisLen
        fileSC.loc[thisMov, thisEm].n= data.shape[1]
        qcDF.loc[thisMov, thisEm].n = data.shape[1]
        qcDF.loc[thisMov, thisEm].Var = np.mean(data.var(axis = 1))  
        qcDF.loc[thisMov, thisEm].CV = np.mean(data.std(axis = 1)/data.mean(axis = 1))
        
        thisCorr= data.corr()
        corrM = thisCorr.iloc[0,1:]
        qcDF.loc[thisMov, thisEm].CorrMean = np.mean(corrM)
        
        n=thisLen
        r=thisCorr
        t=r*np.sqrt((n-2)/(1-r*r))
        import scipy.stats   
        thisCorrp = scipy.stats.t.sf(np.abs(t), n-1)*2
        corrP = thisCorrp[0,1:]
        qcDF.loc[thisMov, thisEm].CorrP = np.mean(corrP)
     
        k2, p = normaltest(data.mean(axis = 1))
        qcDF.loc[thisMov, thisEm].Normk = k2
        qcDF.loc[thisMov, thisEm].Normp = p    
        ks, kp = kstest(data.mean(axis = 1), norm.cdf)
        qcDF.loc[thisMov, thisEm].KsTests = ks
        qcDF.loc[thisMov, thisEm].KsTestp = kp  
        shps, shpp = shapiro(data.mean(axis = 1))
        qcDF.loc[thisMov, thisEm].ShpTests = shps
        qcDF.loc[thisMov, thisEm].ShpTestp = shpp
#        ands, andp = anderson(data.mean(axis = 1), dist='norm')
#        qcDF.loc[thisMov, thisEm].AndTests = shps
#        qcDF.loc[thisMov, thisEm].AndTestp = shpp
        # Now ICC
        icc = []
        for s in range(data.shape[1]):
            sVar = np.var(data.iloc[:,s])
            gVar = data.var(axis = 1)
            icc.append(sVar/(sVar + gVar))
        qcDF.loc[thisMov, thisEm].ICC = np.mean(icc) 
            
        continue
    
for c in qcDF.columns:
    qcDF[c] = pd.to_numeric(qcDF[c])
    
chk = qcDF.corr()
dataplot = sns.heatmap(chk)
            
            
MovEmoDrop = []
MovEmoDrop.append(qcDF.index[qcDF.n == 1].to_list())
MovEmoDrop.append(qcDF.index[qcDF.Normp > 0.05].to_list())
MovEmoDrop.append(qcDF.index[qcDF.CorrP > 0.05].to_list())

flatDrop =  [item for sublist in MovEmoDrop for item in sublist]
movEmToDrop = pd.Series(flatDrop)
movEmToDrop = movEmToDrop.rename('MovEmo')
os.chdir(outPath)
movEmToDrop.to_csv('MovEmoToDrop.csv')