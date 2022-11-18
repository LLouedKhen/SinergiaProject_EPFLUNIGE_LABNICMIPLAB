#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 08:40:33 2022

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
import nilearn as ni
from nilearn.input_data import NiftiMasker

atlas = ni.datasets.fetch_atlas_schaefer_2018()
atlas_filename = atlas['maps']
label = atlas.labels


aMask = '/home/loued/Schaefer/Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm.nii'

imgBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/SecondLevel_Emotions';
dmdBetaPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ImagingData/SecondLevel_Emotions/EMODMD';
os.chdir(imgBetaPath)
Emotions= ['Anger','Anxiety','Contempt','Disgust','Fear','Guilt','Happiness','Love','Satisfaction','Sad','Shame','Surprise','Warm-heartedness'];



from nilearn.maskers import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img=atlas_filename, standardize=True,
                           memory='nilearn_cache', verbose=5)
for i in range(len(Emotions)):
    thisPath = os.path.join(imgBetaPath, Emotions[i])
    img = os.path.join(thisPath, 'beta_0001.nii')
    #from nilearn.maskers import NiftiMasker
    #masker = NiftiMasker(mask_img=aMask, standardize=True,
    #                         memory='nilearn_cache', verbose=5)
    ###masker.fit(data.func[0])
    #masker.fit(img)
    
    beta = masker.fit_transform(img)
    thisBeta = np.transpose(beta)
    thisBeta = pd.DataFrame(thisBeta)
    os.chdir(dmdBetaPath)
    thisBeta.to_csv(Emotions[i] + '_Shaefer400_BetaPar.csv')
    os.chdir(imgBetaPath)

#thisBeta.columns = label



