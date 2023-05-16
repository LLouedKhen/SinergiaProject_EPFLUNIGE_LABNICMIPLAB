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
brainDataTSPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TCFiles'
outPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TCFiles/MeanTS_All'

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise']

os.chdir(emoDataTSPath)
eTSFiles = glob.glob('Mean_An*')

os.chdir(brainDataTSPath)
bTSFiles = glob.glob('TC_400_sub*')

regions = pd.read_csv('TC_cort400_labels.csv')
for m in Movies:
    movBFiles = []
    ld = []
    for file in bTSFiles:
        #try out ARIMA 
        thisFile = pd.read_csv(file,header = None)
        start = 'ses-'
        end = '.csv'
        string = file
        Mov1 = (string.split(start))[1].split(end)[0]
        Mov2 = (Mov1.split('_'))[1]
        if Mov2 in m:
            movBFiles.append(thisFile)
            for d in range(len(movBFiles)):
                ld.append(movBFiles[d].shape[0])
                minLF = np.min(ld)
            for d in range(len(movBFiles)):
                movBFiles[d] = movBFiles[d].iloc[:minLF,:]
            movBFilesA = np.array(movBFiles)
            os.chdir(outPath)
            thisMMean = pd.DataFrame(np.mean(movBFilesA, axis = 0))
            thisMMean.to_csv('MeanTCC_' + m + '_Schaefer.csv')
            os.chdir(brainDataTSPath)
            
bTSFiles = glob.glob('TC_14_sub*')

regions = pd.read_csv('TC_sub14_labels.csv')
for m in Movies:
    movBFiles = []
    ld = []
    for file in bTSFiles:
        #try out ARIMA 
        thisFile = pd.read_csv(file,header = None)
        start = 'ses-'
        end = '.csv'
        string = file
        Mov1 = (string.split(start))[1].split(end)[0]
        Mov2 = (Mov1.split('_'))[1]
        if Mov2 in m:
            movBFiles.append(thisFile)
            for d in range(len(movBFiles)):
                ld.append(movBFiles[d].shape[0])
                minLF = np.min(ld)
            for d in range(len(movBFiles)):
                movBFiles[d] = movBFiles[d].iloc[:minLF,:]
            movBFilesA = np.array(movBFiles)
            os.chdir(outPath)
            thisMMean = pd.DataFrame(np.mean(movBFilesA, axis = 0))
            thisMMean.to_csv('MeanTCSC_' + m + '_Schaefer.csv')
            os.chdir(brainDataTSPath)

            
            
            
            

