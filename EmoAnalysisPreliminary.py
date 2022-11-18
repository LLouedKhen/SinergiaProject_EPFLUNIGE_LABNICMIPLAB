#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:33:33 2022

@author: loued
"""
import time
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
import seaborn as sn


mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla'

os.chdir(mainPath)

allData = pd.read_csv('AllTables_Table.csv',  encoding = "utf-8")

muByEmotion = allData.groupby(['ItemName'])['ItemScore'].mean()
varByEmotion = allData.groupby(['ItemName'])['ItemScore'].var()

muByComponent = allData.groupby(['Component'])['ItemScore'].mean()
varByComponent = allData.groupby(['Component'])['ItemScore'].var()

muByEmotionByMovie = allData.groupby(['ItemName', 'MovieName'])['ItemScore'].mean()
varByEmotionByMovie = allData.groupby(['ItemName', 'MovieName'])['ItemScore'].var()

muByComponentByMovie = allData.groupby(['Component', 'MovieName'])['ItemScore'].mean()
varByComponentByMovie = allData.groupby(['Component', 'MovieName'])['ItemScore'].var()

redData = allData.loc[allData['Component'] == 'Emotion']

muByEByMMainEmo = pd.DataFrame(redData.groupby(['MovieName', 'ItemName'])['ItemScore'].mean())
varByEByMMainEmo  = pd.DataFrame(redData.groupby(['MovieName', 'ItemName'])['ItemScore'].var())

muByEByMMainEmo = muByEByMMainEmo.reset_index()
varByEByMMainEmo = varByEByMMainEmo.reset_index()

muByEByMMainEmoMax = pd.DataFrame(columns=['MovieName','ItemName','ItemScore'])
varByEByMMainEmoMax = pd.DataFrame(columns=['MovieName','ItemName','ItemScore'])


for i in range(1, len(muByEByMMainEmo), 13):
    a = muByEByMMainEmo.loc[i:i +12,:]
    m = a.ItemScore.idxmax()
    muByEByMMainEmoMax.loc[i, 'MovieName'] = muByEByMMainEmo.loc[i,'MovieName']
    muByEByMMainEmoMax.loc[i, 'ItemName'] = a.loc[m,'ItemName'] 
    muByEByMMainEmoMax.loc[i, 'ItemScore'] = a.loc[m,'ItemScore'] 
    b = varByEByMMainEmo.loc[i:i +12,:]
    n = b.ItemScore.idxmax()
    varByEByMMainEmoMax.loc[i, 'MovieName'] = varByEByMMainEmo.loc[i,'MovieName']
    varByEByMMainEmoMax.loc[i, 'ItemName'] = b.loc[n,'ItemName'] 
    varByEByMMainEmoMax.loc[i, 'ItemScore'] = b.loc[n,'ItemScore'] 
    
f1 = sn.relplot(
data=muByEByMMainEmoMax,
x="MovieName", y="ItemScore", 
hue="ItemName", style="ItemName")
plt.xticks(plt.xticks()[0], muByEByMMainEmoMax.MovieName, rotation=90)
plt.tight_layout()
plt.show()
plt.savefig('/media/miplab-nas2/Data2/Movies_Emo/Leyla/Figures/muMaxByMovie.png')


f2 = sn.relplot(
data=varByEByMMainEmoMax,
x="MovieName", y="ItemScore", 
hue="ItemName", style="ItemName")

plt.xticks(plt.xticks()[0], varByEByMMainEmoMax.MovieName, rotation=90)
plt.tight_layout()
plt.show()
plt.savefig('/media/miplab-nas2/Data2/Movies_Emo/Leyla/Figures/varMaxByMovie.png')


scaledData = allData
scaledData.ItemScore = preprocessing.scale(scaledData.ItemScore, with_mean=True)
scaledData.TimeDur= preprocessing.scale(scaledData.TimeDur, with_mean=True)


md = smf.mixedlm("ItemScore ~ TimeDur + C(Component) + SessionNum + ClipNum + C(MovieName)", allData, groups=allData["SubjectNum"])
mdf =md.fit()
print(mdf.summary())

md2 = smf.mixedlm("ItemScore ~ TimeDur  +  SessionNum +ClipNum +C(ItemName) + C(MovieName)", allData, groups=allData["SubjectNum"])
mdf2 =md2.fit()
print(mdf2.summary())

md3 = smf.mixedlm("ItemScore ~ TimeDur + C(Component) + SessionNum + ClipNum + C(MovieName)", scaledData, groups=scaledData["SubjectNum"])
mdf3 =md3.fit()
print(mdf3.summary())

md4 = smf.mixedlm("ItemScore ~ TimeDur  +  SessionNum +ClipNum +C(ItemName) + C(MovieName)", scaledData, groups=scaledData["SubjectNum"])
mdf4 =md4.fit()
print(mdf4.summary())

M = pd.Series(allData['MovieName'].unique())
E = pd.Series(redData['ItemName'].unique())

C = np.zeros((14, 1))
M1 = redData.loc[redData['MovieName'] == M[0]]
C[0] = max(M1.ClipNum)
M2 = redData.loc[redData['MovieName'] == M[1]]
C[1] = max(M2.ClipNum)
M3 = redData.loc[redData['MovieName'] == M[2]]
C[2] = max(M3.ClipNum)
M4 = redData.loc[redData['MovieName'] == M[3]]
C[3] = max(M4.ClipNum)
M5 = redData.loc[redData['MovieName'] == M[4]]
C[4] = max(M5.ClipNum)
M6 = redData.loc[redData['MovieName'] == M[5]]
C[5] = max(M6.ClipNum)
M7 = redData.loc[redData['MovieName'] == M[6]]
C[6] = max(M7.ClipNum)
M8 = redData.loc[redData['MovieName'] == M[7]]
C[7] = max(M8.ClipNum)
M9 = redData.loc[redData['MovieName'] == M[8]]
C[8] = max(M9.ClipNum)
M10 = redData.loc[redData['MovieName'] == M[9]]
C[9] = max(M10.ClipNum)
M11 = redData.loc[redData['MovieName'] == M[10]]
C[10] = max(M11.ClipNum)
M12 = redData.loc[redData['MovieName'] == M[11]]
C[11] = max(M12.ClipNum)
M13 = redData.loc[redData['MovieName'] == M[12]]
C[12] = max(M13.ClipNum)
M14 = redData.loc[redData['MovieName'] == M[13]]
C[13] = max(M14.ClipNum)

howManyClips = np.sum(C)

cols = {'MovieName', 'ClipNum','C1n', 'C1v','C2n', 'C2v', 'C3n', 'C3v', 'muMax', 'varMax'}
pcaMainMovieDF = pd.DataFrame(columns = {'MovieName', 'ClipNum','C1n', 'C1v','C2n', 'C2v', 'C3n', 'C3v', 'muMax', 'varMax'})
from sklearn.decomposition import PCA

for i in range(0,len(M)):
    print(i)
    a = redData.loc[redData['MovieName'] == M.loc[i]].reset_index()
    n = np.max(a.ClipNum)
    pcaMainMovieDF.MovieName.append =  M.loc[i]
    for j in range(1,n):
        b = a.loc[a['ClipNum'] == j].reset_index();
        pcaMainMovieDF.ClipNum.append =  j
        grpMu = pd.DataFrame(b.groupby(['ItemName'])['ItemScore'].mean().reset_index())
        em = grpMu.ItemScore.idxmax()
        muMaxEm =grpMu.ItemName.loc[em]
        grpVar =pd.DataFrame(b.groupby(['ItemName'])['ItemScore'].var().reset_index())
        ev = grpVar.ItemScore.idxmax()
        varMaxEm =grpVar.ItemName.loc[ev]
        
        #varMaxEm = float('NaN')
        c = b.pivot(index = None, columns= "ItemName", values = ["ItemScore"])
        c = c.droplevel(0, axis = 1)
        d = c
        for k in range(0, 13):
            d.iloc[:,k] = np.sort(np.array(c.iloc[:,k]), axis = None)
        c = d.dropna()
        print('The length of Clip ' + repr(j) + ' in ' + repr(M.loc[i]) + ' data set is ' + repr(len(c)) + ' .')
        cPCA = PCA()
        cPCA.fit(c)
        if np.count_nonzero(cPCA.components_) >1:
            TopComponents = np.abs(cPCA.components_[1]).argsort()[::-1]
            print('The top 3 components are ' + repr(c.columns[TopComponents[0]]) + ' , ' + repr(c.columns[TopComponents[1]]) + ' , ' + repr(c.columns[TopComponents[2]]) + ' . ')
            C1n= c.columns[TopComponents[0]]
            C2n= c.columns[TopComponents[1]]
            C3n =c.columns[TopComponents[2]]
            
            cPCA_Var = cPCA.explained_variance_ratio_
            cPCA_Varp = cPCA.explained_variance_ratio_*100
            C1v = cPCA_Varp[0]
            
            if cPCA_Varp[1] > 1:
                C2v = cPCA_Varp[1]
            else:
                C2v =float("NaN")
            if len(cPCA_Varp) > 2:
                C3v = cPCA_Varp[2]
            else:
                C3v = float("NaN")
                
                
            pcaMainMovieDF = pcaMainMovieDF.append({'MovieName': M.loc[i], 'ClipNum':j, 'C1n': C1n,'C1v': C1v,'C2n': C2n, 'C2v': C2v, 'C3n': C3n, 'C3v': C3v, 'varMax': varMaxEm, 'muMax': muMaxEm}, ignore_index=True)       
            pcaMainMovieDF.columns = cols
            cPCA_var = cPCA.explained_variance_ratio_.cumsum()

            plt.ylabel('%Variance explained.')
            plt.xlabel('# of features')
            plt.title('PCA Analysis for Emotions Indices')
            #plt.ylim(30,100.5)
            plt.plot(cPCA_Var)

            
        else:
            print("Flag problem in " + repr(M.loc[i]))
            time.sleep(5)
            continue
        
#let's plot 
NewDF = pd.concat([pcaMainMovieDF.MovieName, pcaMainMovieDF.ClipNum, pcaMainMovieDF.C1n, pcaMainMovieDF.C1v], axis = 1)
NewDF1 = pd.concat([pcaMainMovieDF.MovieName, pcaMainMovieDF.ClipNum, pcaMainMovieDF.muMax], axis = 1)
NewDF2 = pd.concat([pcaMainMovieDF.MovieName, pcaMainMovieDF.ClipNum, pcaMainMovieDF.varMax], axis = 1)

NewDF = NewDF.reset_index()
f3 = sn.relplot(data=NewDF, x = 'index', y="C1v", hue='C1n')
f3.add_legend()
plt.tight_layout()
plt.show()
plt.savefig('/media/miplab-nas2/Data2/Movies_Emo/Leyla/Figures/pcaEmobClipBzMovie.png')