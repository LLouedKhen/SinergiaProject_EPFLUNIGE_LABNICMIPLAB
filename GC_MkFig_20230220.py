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
from datetime import date
from nilearn import datasets

from nilearn.image import math_img
from nilearn import image, plotting


dataPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
#testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Preprocessed_data/sub-S01/ses-1/pp_sub-S01_ses-1_FirstBite.feat'
imgPath  = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis'

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise']

os.chdir(imgPath)
files = glob.glob('SigGC__*.nii')

import time

for f in range(len(files)):
            thisImg= files[f]
            string = thisImg
            start1 = 'SigGC__'
            end = '.nii'

            thisEmo = (string.split(start1))[1]
           
            x = plotting.plot_glass_brain(thisImg, title= thisEmo, threshold =1.1 )
            plotting.show()
            x.savefig('GCFig_' + thisEmo + ".png")
            x.close()
            

                    
#            dataF.columns = Emotions    
            
