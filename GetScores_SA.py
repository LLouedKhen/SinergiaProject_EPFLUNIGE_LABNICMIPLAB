#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 13:16:33 2022

@author: loued
"""

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
import re
import time
import seaborn as sns
import sympy as sym


mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla'    
os.chdir(mainPath)
allData = pd.read_csv('AllTables_Table.csv',  encoding = "utf-8")
Movies = sorted(pd.unique(allData.MovieName).tolist())
Emotions = sorted(['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Guilt', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Shame', 'Surprise', 'WarmHeartedness'])
d = {}
Names = {}
for m in Movies:
    for em in Emotions:
        d[m,em] = pd.DataFrame()


AnnotationsPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Raw_annotations/ParticipantTasks'
os.chdir(AnnotationsPath)
subFolders = sorted(glob.glob('SA0*'))
problem = 0
included = 0
allFiles = 0
emoFiles = 0

allEmos =[]
allEmos2=[]
allEmos3=[]

scaleEmos2=[]
scaleEmos3=[]

emoFound = []
subjMeans = np.array([])
subjStd = np.array([])

for i in range(len(subFolders)):
    os.chdir(subFolders[i])
    subj = subFolders[i]
    subjData = np.array([])
    for m in range(len(Movies)):
        thisMovie = Movies[m];
        thisMovieFiles = glob.glob(thisMovie +'*')
        for f in range(len(thisMovieFiles)):
#              if any(x in thisMovieFiles[f] for x in Emotions):
              thisFile = thisMovieFiles[f]  
              if 'CORRUPT'  in thisFile:
                  continue
              elif 'damaged'  in thisFile:
                  continue
              else:
                  allFiles += 1
                  Split1 = thisFile.split('.csv')[0]
                  Split2 = Split1.split('SA0')[1]
                  thisEmo = Split2.split('_')[1]
                  #print(thisEmo)
                  allEmos.append(thisEmo)
                  data = pd.read_csv(thisFile, header = 0)
                  
                  if data.shape[1] == 1:
                      data=  data.iloc[8:, 0].str.split(';', expand = True)
                     
                  thisEmo2 = data.iloc[2,1] 
                  thisEmo3 = data.iloc[1,1] 

                  if thisEmo2 == 'Surprised':
                      thisEmo2 = thisEmo2.replace(thisEmo2, 'Surprise')
                  elif thisEmo2 == 'WarmHearted':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'WarmHeartedness')
                  elif thisEmo2 == 'Fearful':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Fear')    
                  elif thisEmo2 == 'Guilty':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Guilt')       
                  elif thisEmo2 == 'Satisfied':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Satisfaction')   
                  elif 'Anxious' in thisEmo2:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Anxiety')  
                  elif thisEmo2 == 'Disgusted':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Disgust')  
                  elif 'Happy' in thisEmo2:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Happiness')  
                  elif 'Angry' in thisEmo2:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Anger')  
                  elif 'Contempt' in thisEmo3:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Contempt')  
                  elif 'shame' in thisEmo3:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Shame')  
                  
                  if any(x in thisEmo2 for x in Emotions):
                      ratingSpot = np.where(data.values == 'Rating')
                      x = ratingSpot[0][0] + 2
                      y = ratingSpot[1][0]
                      thisData = np.array(data.iloc[x:,y])
                      if 'Shame' in thisEmo2:
                          thisData = (np.array(data.iloc[x:,y]).astype(float) -100) * -1
                      subjData = np.hstack([subjData, thisData])
    subjData = np.array(subjData.tolist()).astype(float)
               
    subjMeans = np.append(subjMeans,[np.nanmean(subjData)])
    subjStd = np.append(subjStd,[np.nanstd(subjData)])
    os.chdir(AnnotationsPath)
                      


for i in range(len(subFolders)):
    os.chdir(subFolders[i])
    subj = subFolders[i]
    for m in range(len(Movies)):
        thisMovie = Movies[m];
        thisMovieFiles = glob.glob(thisMovie +'*')
        for f in range(len(thisMovieFiles)):
#              if any(x in thisMovieFiles[f] for x in Emotions):
              thisFile = thisMovieFiles[f]  
              if 'CORRUPT'  in thisFile:
                  continue
              elif 'damaged'  in thisFile:
                  continue
              else:
                  allFiles += 1
                  Split1 = thisFile.split('.csv')[0]
                  Split2 = Split1.split('SA0')[1]
                  thisEmo = Split2.split('_')[1]
                  #print(thisEmo)
                  allEmos.append(thisEmo)
                  data = pd.read_csv(thisFile, header = 0)
                  
                  if data.shape[1] == 1:
                      data=  data.iloc[8:, 0].str.split(';', expand = True)
                  thisEmo2 = data.iloc[2,1] 
                  thisEmo3 = data.iloc[1,1] 
                  #time.sleep(10)
                  scaleEmos2.append(thisEmo2)
                  scaleEmos3.append(thisEmo3)

                  if thisEmo2 == 'Surprised':
                      thisEmo2 = thisEmo2.replace(thisEmo2, 'Surprise')
                  elif thisEmo2 == 'WarmHearted':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'WarmHeartedness')
                  elif thisEmo2 == 'Fearful':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Fear')    
                  elif thisEmo2 == 'Guilty':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Guilt')       
                  elif thisEmo2 == 'Satisfied':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Satisfaction')   
                  elif 'Anxious' in thisEmo2:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Anxiety')  
                  elif thisEmo2 == 'Disgusted':
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Disgust')  
                  elif 'Happy' in thisEmo2:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Happiness')  
                  elif 'Angry' in thisEmo2:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Anger')  
                  elif 'Contempt' in thisEmo3:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Contempt')  
                  elif 'shame' in thisEmo3:
                      thisEmo2 = thisEmo2.replace(thisEmo2,'Shame')  
                      
                  allEmos2.append(thisEmo2)
                  allEmos3.append(thisEmo3)
                  
                  if thisEmo in data.iloc[2,1]:  
                      included +=1
                  else:
                      #this appeared to happen consistently with anger, anxiety, contempt, happiness, satisfaction
                      #print(data.iloc[2,1])
                      problem +=1
#                      continue 
                  if any(x in thisEmo2 for x in Emotions):
                      print(thisEmo2)
                      emoFiles += 1
                      emoFound.append(thisEmo2)
                      ratingSpot = np.where(data.values == 'Rating')
                      x = ratingSpot[0][0] + 2
                      y = ratingSpot[1][0]
                     
                      thisArr = pd.Series(data.iloc[x:,y])
                      nArr = thisArr.reset_index(drop = True)
                      nArr = (nArr.astype(float)-subjMeans[i])/subjStd[i]
                      cNarrName = nArr.name
                      nArr = nArr.rename(subj+ '_' + thisEmo2)
                      if not d[thisMovie,thisEmo2].empty and len(thisArr) > len(d[thisMovie,thisEmo2]):
                          nArr = nArr.truncate(before = None, after = len(d[thisMovie,thisEmo2]))
                      elif not d[thisMovie,thisEmo2].empty and len(thisArr) < len(d[thisMovie,thisEmo2]):
                          nArr = d[thisMovie,thisEmo2].truncate(before = None, after = len(  nArr))
                       
                      d[thisMovie,thisEmo2] = pd.concat([d[thisMovie,thisEmo2],nArr], axis =1)
                      
#            
                  
#                  if m == 1:
#                      if len(M1[thisEmo]) == 0 or M1[thisEmo].isnull().all():
#                          M1[thisEmo] = data.iloc[8:,1]
#                          
#                      else:
#                          newDF = pd.DataFrame(M1[thisEmo].values, data.iloc[8:,1].values).reset_index()
#                          newDF = newDF.rename(columns ={'index': thisEmo, '0': 'temp'})
#                          M1[thisEmo] =newDF.mean(axis= 1)
    os.chdir(AnnotationsPath)
emo2 = pd.unique(allEmos2).tolist()    
emo = pd.unique(allEmos).tolist() 
emo3 = pd.unique(allEmos3).tolist() 
                             

emosColl = pd.unique(emoFound).tolist() 
fileEmo2 = pd.unique(scaleEmos2).tolist() 
fileEmo3 = pd.unique(scaleEmos3).tolist() 

for key, df in d.items():
    df.to_csv('DF_' + key[0] + key[1] + '.csv')

allD=list(d)
M = {}
chunk = len(allD)/len(Movies)
for l in range(0,len(allD), int(chunk)):
    mName = allD[l][0]
    tempDF =list(d.values())[l:l+13]
    ndf = pd.DataFrame()
    for a in range(len(tempDF)):
        hold = tempDF[a]
        tdf= pd.DataFrame()
        tdf[Emotions[a] +'_' +  'Mu'] = hold.mean(axis =1)
        tdf[Emotions[a] +'_' +  'Std'] = hold.std(axis =1)
        tdf[Emotions[a] +'_' +  'FirstDerivative'] = sym.diff(tdf[Emotions[a] +'_' +  'Mu'])
        ndf = pd.concat([ndf, tdf], axis = 1)
#    colNames = []
#    for em in Emotions:  
#        colNames.append(mName +'_' + em +'_' +  'RatingMu') 
#        colNames.append(mName +'_' +  em +'_' + 'RatingVar') 
#    ndf = ndf.rename(columns = colNames)            
    M[mName] =ndf 
        
for keys, dfM in M.items():
    dfM.to_csv('DF_' + keys + '_Means2.csv')
    
sns.set()
allM = list(M) 
for m in range(len(M)):
    thisData = M[allM[m]]
    Means = thisData.iloc[:,0::3]
    Stds = thisData.iloc[:,1::3]
    fds = thisData.iloc[:,2::3]  
    fig, (ax1, ax2) = plt.subplots(1,2)
  
    ax1.plot(Means, label = Emotions)
    minErr = np.array(Means) -np.array(Stds)
    maxErr =  np.array(Means) +np.array(Stds)
    x = np.array(range(len(Means)))
    for err in range(Means.shape[1]):
        ax1.fill_between(x, minErr[:,err], maxErr[:, err]) 
    #ax1.legend(loc='best')
    ax1.set_title(allM[m] + ' Means')
    ax2.plot(fds, label = Emotions)
    ax2.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
    ax2.set_title(allM[m]+ ' Rate of Change in Emotions')
    
   # plt.plot(Means)
    #plt.fill_between(Means-Std, Means+Stds)               
    
    
    
