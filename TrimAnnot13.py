#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 14:46:12 2022

@author: elliemorgenroth

Script to make annotations per film in fMRI resolution
"""
import glob
import os
import numpy as np
from mat4py import loadmat


from pandas import read_csv
import pandas as pd
import scipy
from scipy import signal
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from statsmodels.formula.api import ols

#path = '/media/miplab-nas2/Data2/Movies_Emo/Ellie/'
path = '/Volumes/Data2/Movies_Emo/Ellie/'

durs = [496, 808, 490, 405, 599, 667, 1008, 722, 805, 1028, 588, 784, 402, 798]
emodurs13 = [round(i/1.3) for i in durs]

df = read_csv(path+'All_Annotations.csv', delimiter = ',')

df = df.drop(df.columns[0], axis=1)


movs = ['AfterTheRain','BetweenViewings','BigBuckBunny','Chatter', \
              'FirstBite','LessonLearned','Payload', \
              'Sintel','Spaceman','Superhero', \
              'TearsOfSteel','TheSecretNumber','ToClaireFromSonny','YouAgain']
    
labels = np.array(df.columns)
np.savetxt(path + 'EmoFiles/labels.csv',labels,delimiter = '\t', fmt='%s')

AfterTheRain = df.iloc[0:durs[0],:].reset_index(drop=True) 
AfterTheRain13 = signal.resample(AfterTheRain,emodurs13[0])
np.savetxt(path + 'EmoFiles/AfterTheRain13.csv',AfterTheRain13, delimiter='\t' )

BetweenViewings = df.iloc[durs[0]+1: sum(durs[0:2])+1,:].reset_index(drop=True) 
BetweenViewings13 = signal.resample(BetweenViewings,emodurs13[1])
np.savetxt(path + 'EmoFiles/BetweenViewings13.csv',BetweenViewings13, delimiter='\t' )

BigBuckBunny = df.iloc[sum(durs[0:2])+1: sum(durs[0:3])+1,:].reset_index(drop=True) 
BigBuckBunny13 = signal.resample(BigBuckBunny,emodurs13[2])
np.savetxt(path + 'EmoFiles/BigBuckBunny13.csv',BigBuckBunny13, delimiter='\t' )

Chatter = df.iloc[sum(durs[0:3]) + 1: sum(durs[0:4])+1,:].reset_index(drop=True) 
Chatter13 = signal.resample(Chatter,emodurs13[3])
np.savetxt(path + 'EmoFiles/Chatter13.csv',Chatter13, delimiter='\t' )

FirstBite = df.iloc[sum(durs[0:4])+ 1: sum(durs[0:5]) +1,:].reset_index(drop=True) 
FirstBite13 = signal.resample(FirstBite,emodurs13[4])
np.savetxt(path + 'EmoFiles/FirstBite13.csv',FirstBite13, delimiter='\t' )

LessonLearned = df.iloc[sum(durs[0:5]) +1: sum(durs[0:6])+1,:].reset_index(drop=True) 
LessonLearned13 = signal.resample(LessonLearned,emodurs13[5])
np.savetxt(path + 'EmoFiles/LessonLearned13.csv',LessonLearned13, delimiter='\t' )

Payload = df.iloc[sum(durs[0:6]) +1: sum(durs[0:7])+1,:].reset_index(drop=True) 
Payload13 = signal.resample(Payload,emodurs13[6])
np.savetxt(path + 'EmoFiles/Payload13.csv',Payload13, delimiter='\t' )

Sintel = df.iloc[sum(durs[0:7]) +1: sum(durs[0:8])+1,:].reset_index(drop=True) 
Sintel13 = signal.resample(Sintel,emodurs13[7])
np.savetxt(path + 'EmoFiles/Sintel13.csv',Sintel13, delimiter='\t' )

Spaceman = df.iloc[sum(durs[0:8]) +1: sum(durs[0:9])+1,:].reset_index(drop=True) 
Spaceman13 = signal.resample(Spaceman,emodurs13[8])
np.savetxt(path + 'EmoFiles/Spaceman13.csv',Spaceman13, delimiter='\t' )

Superhero = df.iloc[sum(durs[0:9]) +1: sum(durs[0:10])+1,:].reset_index(drop=True) 
Superhero13 = signal.resample(Superhero,emodurs13[9])
np.savetxt(path + 'EmoFiles/Superhero13.csv',Superhero13, delimiter='\t' )

TearsOfSteel = df.iloc[sum(durs[0:10]) +1: sum(durs[0:11])+1,:].reset_index(drop=True) 
TearsOfSteel13 = signal.resample(TearsOfSteel,emodurs13[10])
np.savetxt(path + 'EmoFiles/TearsOfSteel13.csv',TearsOfSteel13, delimiter='\t' )

TheSecretNumber = df.iloc[sum(durs[0:11]) +1: sum(durs[0:12])+1,:].reset_index(drop=True) 
TheSecretNumber13 = signal.resample(TheSecretNumber,emodurs13[11])
np.savetxt(path + 'EmoFiles/TheSecretNumber13.csv',TheSecretNumber13, delimiter='\t' )

ToClaireFromSonny = df.iloc[sum(durs[0:12]) +1: sum(durs[0:13])+1,:].reset_index(drop=True) 
ToClaireFromSonny13 = signal.resample(ToClaireFromSonny,emodurs13[12])
np.savetxt(path + 'EmoFiles/ToClaireFromSonny13.csv',ToClaireFromSonny13, delimiter='\t' )

YouAgain = df.iloc[sum(durs[0:13]) +1: sum(durs[0:])+1,:].reset_index(drop=True) 
YouAgain13 = signal.resample(YouAgain,emodurs13[13])
np.savetxt(path + 'EmoFiles/YouAgain13.csv',YouAgain13, delimiter='\t' )