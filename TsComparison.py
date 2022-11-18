#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:49:11 2022

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
TsPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/Movies'
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Satisfaction']

os.chdir(TsPath)
for m in Movies:
    for em in Emotions:
        thisPath = os.path.join(TsPath, m, em)
        annotRegs =  glob.glob('DF_*')
        imRegs = glob.glob('ScaledRegressors*')
