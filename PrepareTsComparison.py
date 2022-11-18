#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:33:33 2022

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

shutil.copyfile

mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
TsPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison'
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise']

annotPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Raw_annotations/ParticipantTasks/Processed'

os.chdir(annotPath)
annotRegs =  glob.glob('DF_*')

os.chdir(TsPath)
imRegs = glob.glob('ScaledRegressors*')


if not os.path.isdir('Movies'):
    os.mkdir('Movies')

mPath = os.path.join(TsPath,'Movies')
os.chdir(mPath)
for m in Movies:
    if not os.path.isdir(m):
        os.mkdir(m)
        thisPath = os.path.join(TsPath, 'Movies', m)
        os.chdir(m)
        for em in Emotions:
            if not os.path.isdir(em):
                os.mkdir(em)
                os.chdir(em)
                for an in annotRegs:
                    if m in an and em in an:
                        thisFile = os.path.join(annotPath, an)
                        myDir = os.path.join(TsPath, 'Movies', m, em, an)
                        shutil.copyfile(thisFile, myDir)
                for im in imRegs:
                    if m in im and em in im:
                        thisFile = os.path.join(TsPath, im)
                        myDir = os.path.join(TsPath,'Movies', m, em, im)
                        shutil.copyfile(thisFile, myDir)
                os.chdir(thisPath)
        os.chdir(mPath)
                    
                
        
        

