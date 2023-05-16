#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 10:45:58 2023

@author: loued
"""
import numpy as np 
import pandas as pd
import os
import glob
from datetime import date
from matplotlib import pyplot as plt
#from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.cluster.hierarchy as shc

ratingMeansPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Raw_annotations/ParticipantTasks/Means2'
HCdataPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/HCluster_Data'
FigPath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla/Figures'

Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise']
#Dropped shame

os.chdir(ratingMeansPath)

df = {}
for em in Emotions:
    df[em] = pd.Series()

dataEMMu = sorted(glob.glob('DF_*_Means2.csv'))
allData = pd.DataFrame(columns = Emotions)
mData = []

for em in Emotions:
    A= df.get(em)
    for m in range(len(Movies)):
        thisData = pd.read_csv(dataEMMu[m])
        if m == 0:
            A = thisData[em + '_Mu']
            mData.append(len(A))
        else:
            B = thisData[em + '_Mu']
            A = A.append(B, ignore_index=True)
            mData.append(len(B))
    allData[em] = A


#different distance measures used here, best c won         
Z = shc.linkage(allData, metric='chebyshev')   

from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

c, coph_dists = cophenet(Z, pdist(allData))
c

#plt.figure(figsize=(10, 7))
#plt.title("Z Dendrogram")
#
#shc.dendrogram(Z=Z)
#plt.show()





#plt.figure(figsize=(10, 7))
#plt.title("Dendogram with line")
#clusters = shc.linkage(allData, 
#            metric="chebyshev")
#shc.dendrogram(clusters)
#plt.axhline(y = 0.5, color = 'r', linestyle = '-')



#Now try scikit learn feature agglomeration

from sklearn.cluster import FeatureAgglomeration
import seaborn as sns

sns.pairplot(allData)

from sklearn.decomposition import PCA

pca = PCA(n_components=10)
pca.fit_transform(allData)
emVars = pca.explained_variance_ratio_.cumsum()

cluster = FeatureAgglomeration(n_clusters=6, affinity='chebyshev', linkage='single')  
cluster.fit(allData)
cluster.labels_
data_labels = cluster.labels_



allData_reduced = cluster.transform(allData)
X_restored = cluster.inverse_transform(allData_reduced)

data_labels = cluster.labels_

plt.figure(figsize=(10, 7))
sns.scatterplot(data=allData_reduced, 
                hue=data_labels)
plt.show()

emotionLabels = pd.concat([pd.Series(Emotions), pd.Series(data_labels)], axis = 1) 
HCData = pd.DataFrame(allData_reduced)
HCData = HCData.rename(columns = {0:'HC1',1:'HC2',2:'HC3', 3:'HC4', 4:'HC5', 5:'HC6'})

os.chdir(HCdataPath)
emotionLabels.to_csv('EmotionLabelsHC6.csv')
for m in range(len(Movies)):
    if m == 0:
        C = HCData.iloc[0:mData[m],:]
        C.to_csv('HC_' + Movies[m] +'.csv')
    else:
        C = HCData.iloc[mData[m-1]:mData[m-1] + mData[m],:]
        C.to_csv('HC_' + Movies[m] +'.csv')
            