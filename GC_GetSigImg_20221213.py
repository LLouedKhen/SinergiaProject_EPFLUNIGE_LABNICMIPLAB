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
roiPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/ROIs/Schaefer400'

os.chdir(roiPath)
rois = glob.glob('Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm*.nii')

st1 = 'Schaefer2018_400Parcels_17Networks_order_FSLMNI152_1mm_'
end1 = '.nii '
rnum = []
for r in range(len(rois)):
    str1 = (rois[r].split(st1))[1].split(end1)[0] 
    rn = int(str1[:-4])
    rnum.append(rn)

rois =pd.DataFrame(rois)
rnum =pd.DataFrame(rnum)
regions = pd.concat([rois, rnum], axis = 1)   
regions.columns = ['roi', 'num']
regions = regions.sort_values(by =['num'])
roiList = regions.roi.values.tolist()

for r in range(len(roiList)):
    roiList[r] = os.path.join(roiPath, roiList[r])

imgTemplate = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=1, data_dir=None, base_url=None, resume=True, verbose=1)      
#atlas = math_img('img * 0', img=imgTemplate) 
labels = imgTemplate.labels

testMovPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis'

os.chdir(testMovPath)

today = date.today().strftime("%Y%m%d")

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction','Surprise'];
Coord2d =pd.read_csv('/media/miplab-nas2/Data2/Movies_Emo/Leyla/GC_Analysis/Coord2d.csv')
dataF = pd.DataFrame(columns = Emotions)

sanityCheck = np.zeros([33, 13])
files = glob.glob('GCResults_*.csv')
crit = 0.05/400
sig = 0
sigFile = []

for m in range(len(Movies)):
    dataF = pd.DataFrame()
    for f in range (len(files)):
        thisFile = files[f]        
        if Movies[m] in thisFile:
            mov = Movies[m]
            data3 = pd.read_csv(thisFile)
            data3 = data3.iloc[:,1:]
            
        else:
            continue
      
        for em in range(len(Emotions)):
            emo = Emotions[em]
            for j in range (data3.shape[0]):
                x = data3.iloc[j, em]
                if '100 ' in x:
                    st = ' '
                    end = ' '
                    xx = (x.split(st))[0].split(end)[0]
                    br = '['
                    xxx = (xx.split(br))[1]
                    dataF.loc[j, em] = float(xxx)
                elif x.startswith('['):
                    st = '['
                    end = ' '
                    xx = x.replace('[', '')
                    if xx[0].isdigit():
                        xxx = (xx.split(end)[0])
                        dataF.loc[j, em] = float(xxx)
                    else:
                        xxx = (xx.split(end)[1])
                    dataF.loc[j, em] = float(xxx)
                
                if dataF.iloc[j, em] == 100:
                    dataF.iloc[j, em] = 1
                elif dataF.iloc[j, em] > crit and dataF.iloc[j, em] < 100:
                    dataF.iloc[j, em] = 1
                elif dataF.iloc[j, em] <= crit:
                    print(emo, 'for ', mov , ' is significant')
                    sig +=1
                    lab = str(labels[j])[1:]
                    sigFile.append(mov + '_' + emo + '_' + lab)
                    dataF.iloc[j, em] =  np.abs(np.log(dataF.iloc[j, em])) 
                
                val = dataF.iloc[j, em]
                thisROI = image.math_img('img == %s' % j, img = imgTemplate.maps)
                thisROIGC = image.math_img('thisImg * %f' % val, thisImg = thisROI)
                if j == 0:
                    bigROI = thisROIGC
                elif j > 0:
                    bigROI =image.math_img('i1 + i2', i1 = bigROI, i2 = thisROIGC)
            
            
            #plotting.plot_stat_map(bigROI, threshold = 1.1, cmap = 'gist_rainbow')
            bigROI.to_filename('SigGC_'+ mov + '_' + emo + '.nii')

sigFilePD = pd.DataFrame(sigFile)
sigFilePD.to_csv('ListOfSignificant_MovieEmotionRegions.csv')
                    
                    
#            dataF.columns = Emotions    
            
