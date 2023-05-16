#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:26:39 2022

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

dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/TS_MeanScaledImputed'
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise']

os.chdir(dataPath)

TSFiles = glob.glob('Mean_An*')

for file in TSFiles:
    #try out ARIMA 
    thisFile = pd.read_csv(file)
    thisTs = thisFile.MuRatingZ
    start = 'An_'
    end = '.csv'
    string = file
    MovieEmo = (string.split(start))[1].split(end)[0]
    startM = '_'
    thisMovie = (MovieEmo.split(startM))[0]
    thisEmo = (MovieEmo.split(startM))[1]
    

    
    plot_acf(thisTs)
    chkTSST = adfuller(thisTs)
    if chkTSST[1] > 0.05:
        dorder = 1
        chkTSST = adfuller(thisTs.diff().dropna())
        newTS = thisTs.diff().dropna()
        if chkTSST[1] > 0.05:
            dorder = 2
            chkTSST = adfuller(thisTs.diff().diff().dropna())
            newTS = thisTs.diff().diff().dropna()
            if chkTSST[1] > 0.05:
                dorder = 3
                chkTSST = adfuller(thisTs.diff().diff().diff().dropna())
                newTS = thisTs.diff().diff().diff().dropna()
                if chkTSST[1] > 0.05:
                    dorder = 4
                    chkTSST = adfuller(thisTs.diff().diff().diff().diff().dropna())
                    newTS = thisTs.diff().diff().diff().diff().dropna()
                    if chkTSST[1] > 0.05:
                        dorder = 5
                        chkTSST = adfuller(thisTs.diff().diff().diff().diff().diff().dropna())
                        newTS = thisTs.diff().diff().diff().diff().diff().dropna()
                
                
                
                
                
    f = plt.figure()
    ax1 = f.add_subplot(121)
    ax1 .plot(newTS)
    
    ax2 = f.add_subplot(122)
    plot_acf(newTS.dropna(), ax =ax2)
    plt.show()
    
    
    
    
    
    
    arima_model = ARIMA(newTS, order =(1,dorder,2))
    model = arima_model.fit()
    print(model.summary())
   
    model.plot_predict(dynamic = False)
    plt.show()