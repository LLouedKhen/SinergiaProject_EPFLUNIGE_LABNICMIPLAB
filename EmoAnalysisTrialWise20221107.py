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

mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
groupPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/GroupData'

os.chdir(groupPath)

emData = pd.read_csv('emByTrial_Table.csv',  encoding = "utf-8")
SubNum = pd.Series(name = 'SubNum')
for i in range(len(emData)):
    thisSub = emData.Subject[i]
    subNum = int(thisSub[5:])
    SubNum.loc[i] = subNum
    
    
emData = pd.concat([emData, SubNum], axis =1)

Emos = pd.DataFrame([pd.unique(emData.Emotion1Name).tolist() + pd.unique(emData.Emotion2Name).tolist()+ pd.unique(emData.Emotion3Name).tolist()]).transpose()
EmoU = pd.DataFrame(pd.unique(Emos.loc[:,0]).tolist())
EmoU = EmoU.dropna()

AnxData = pd.DataFrame()
AngerData = pd.DataFrame()
ContemptData = pd.DataFrame()
DisgustData = pd.DataFrame()
FearData = pd.DataFrame()
GuiltData = pd.DataFrame()
HappinessData = pd.DataFrame()
LoveData = pd.DataFrame()
SadData = pd.DataFrame()
SatisfactionData = pd.DataFrame()
ShameData = pd.DataFrame()
SurpriseData = pd.DataFrame()
WarmHeartData = pd.DataFrame()

EmoU =EmoU.iloc[:,0].values.tolist()
EmoU.sort()
emoCat = ['Emotion1Name','Emotion2Name', 'Emotion3Name','Emotion4Name']
for j in range(len(EmoU)):
    for emNum in range(len(emoCat)):
        AngerData= AngerData.append(emData.loc[emData[emoCat[emNum]] == EmoU[0]])
        AnxData = AnxData.append(emData.loc[emData[emoCat[emNum]] == EmoU[1]])
        ContemptData = ContemptData.append(emData.loc[emData[emoCat[emNum]] == EmoU[2]])
        DisgustData = DisgustData.append(emData.loc[emData[emoCat[emNum]] == EmoU[3]])
        FearData =FearData.append(emData.loc[emData[emoCat[emNum]] == EmoU[4]])
        GuiltData = GuiltData.append(emData.loc[emData[emoCat[emNum]] == EmoU[5]])
        HappinessData = HappinessData.append(emData.loc[emData[emoCat[emNum]] == EmoU[6]])
        LoveData = LoveData.append(emData.loc[emData[emoCat[emNum]] == EmoU[7]])
        SadData = SadData.append(emData.loc[emData[emoCat[emNum]] == EmoU[8]])
        SatisfactionData = SatisfactionData.append(emData.loc[emData[emoCat[emNum]] == EmoU[9]])
        ShameData = ShameData.append(emData.loc[emData[emoCat[emNum]] == EmoU[10]])
        SurpriseData = SurpriseData.append(emData.loc[emData[emoCat[emNum]] == EmoU[11]])
        WarmHeartData = WarmHeartData.append(emData.loc[emData[emoCat[emNum]] == EmoU[12]])

Subjects = pd.Series(pd.unique(emData.Subject))
Emotions = pd.Series(['Emotion1Name', 'Emotion1Score','Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'])
Components = pd.Series(['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'])

for emoSS in range(len(EmoU)):
    emP = str(emoSS)
    emP2 = emP.zfill(2)
    if emoSS == 0:
        thisData = AngerData
    elif emoSS == 1:
        thisData = AnxData
    elif emoSS == 2:
        thisData = ContemptData
    elif emoSS == 3:
        thisData = DisgustData
    elif emoSS == 4:
        thisData = FearData
    elif emoSS == 5:
        thisData = GuiltData
    elif emoSS == 6:
        thisData = HappinessData
    elif emoSS == 7:
        thisData = LoveData
    elif emoSS == 8:
        thisData = SadData
    elif emoSS == 9:
        thisData = SatisfactionData
    elif emoSS == 10:
        thisData = ShameData
    elif emoSS == 11:
        thisData = SurpriseData
    elif emoSS == 12:
        thisData = WarmHeartData
        
        
        
    thisDataLoc = thisData.columns[thisData.isin([EmoU[emoSS]]).any()]
    Ems = []
    ENum = []
    theseSub = pd.unique(thisData.SubNum)   
    allEmoSub = pd.DataFrame(columns = ['Emotion','Predictors', 'tValues', 'pValues', 'Type', 'Subject'])
    theseSub = pd.unique(thisData.SubNum)    
    for frqSub in range(len(theseSub)):
        sb = theseSub[frqSub]
        subjData = thisData.loc[thisData['SubNum'] == sb]
        subjData = subjData.loc[:, ~subjData.columns.str.endswith('Type')]
        subjData = subjData.dropna(axis = 1)
       # justScores = pd.concat([subjData.C1S, subjData.C2S, subjData.C3S, subjData.C4S, subjData.ES], axis =1)
        compCol = [col for col in subjData.columns if 'Component' in col]
        compNum = int(len(compCol)/2)
        emNum = 5 - compNum
        for comp in range(1, compNum+1):
            print (comp)
            nStr = 'C' + str(comp)
            if comp == 1:
                subjData = subjData.rename(columns ={compCol[comp-1]: nStr+ 'N', compCol[comp]: nStr+ 'S'})
            elif comp == 2:
                subjData = subjData.rename(columns ={compCol[comp]: nStr+ 'N', compCol[comp +1]: nStr+ 'S'})
            elif comp == 3:
                subjData = subjData.rename(columns ={compCol[comp +1]: nStr+ 'N', compCol[comp +2]: nStr+ 'S'})
            elif comp == 4:
                subjData = subjData.rename(columns ={compCol[comp +2]: nStr+ 'N', compCol[comp +3]: nStr+ 'S'})
        len(compCol)
        #subjData = subjData.drop(columns = CompLoc, axis = 1, inplace = True)
        emCol = [col for col in subjData.columns if 'Emotion' in col]
        emNum = len(emCol)/2
        thisEm = subjData.columns[subjData.isin([EmoU[emoSS]]).any()]
        nameEmN = thisEm.values[0]
        nameEmS = nameEmN[:-4] + 'Score'
        wNum = int(nameEmN[7])
        eStr = 'E'
        subjData = subjData.rename(columns= {nameEmN : eStr + 'N', nameEmS:eStr + 'S'})
        emCol.remove(nameEmN)
        emCol.remove(nameEmS)
        emNum = int(len(emCol)/2)
#        if len(emCol) > 0:
        for eC in range(emNum):
            print (eC)

            if emNum == 1:
                intEm = emCol[eC][7]
                nInt = 4
                nStr = 'C' + str(nInt)
                subjData = subjData.rename(columns ={emCol[eC]: nStr+ 'N', emCol[eC +1]: nStr+ 'S'})
            elif emNum == 2:
                intEm = eC 
                nStr = 'C' + str(intEm + 3)     
                if eC == 0:
                    subjData = subjData.rename(columns ={emCol[eC]: nStr+ 'N',emCol[eC + 1]: nStr+ 'S'})
                elif eC == 1:
                    subjData = subjData.rename(columns ={emCol[eC + 1]: nStr+ 'N',emCol[eC + 2]: nStr+ 'S'})
 
            elif emNum == 3:
                intEm = eC
           
                nStr = 'C' + str(intEm + 2)
                if eC == 0:
                    subjData = subjData.rename(columns ={emCol[eC]: nStr+ 'N',emCol[eC + 1]: nStr+ 'S'})
                elif eC == 1:
                    subjData = subjData.rename(columns ={emCol[eC + 1]: nStr+ 'N',emCol[eC + 2]: nStr+ 'S'})
                elif eC == 2:
                    subjData = subjData.rename(columns ={emCol[eC + 2]: nStr+ 'N',emCol[eC + 3]: nStr+ 'S'})
 
         
        
        thisSub = subjData.Subject.iloc[1]
        thisPath = os.path.join(mainPath, thisSub)
        os.chdir(thisPath)
        regs = glob.glob('Regressors*')
#        for fp in regs:
#            os.remove(fp)
        thisDF= subjData[subjData.Subject == thisSub]
        for movie in range(len(pd.unique(thisDF.Movie))):
          thisMovie = pd.unique(thisDF.Movie)[movie]
          df2 = thisDF[thisDF.Movie == thisMovie]
          thisSession = df2.Session.iloc[0]
          thisfName = 'Regressors_EM' + str(emP2) + '_' + thisMovie  + '_' + df2.EN.iloc[0]   + '_' + thisSub + '_ses-' + str(thisSession) +'.csv'
          df2.to_csv(thisfName)
    
            # elif          # elif emNum == 4:
#                        intEm = emCol[eC][7]
#                        nInt = eC + 4
#                        nStr = 'C' + str(nInt)
#                        subjData = subjData.rename(columns ={emCol[eC +3]: nStr+ 'N', emCol[eC +4]: nStr+ 'S'})
#          emNum == 4:
#                        intEm = emCol[eC][7]
#                        nInt = eC + 4
#                        nStr = 'C' + str(nInt)
#                        subjData = subjData.rename(columns ={emCol[eC +3]: nStr+ 'N', emCol[eC +4]: nStr+ 'S'})
        os.chdir(mainPath) 
        os.chdir('TsComparison')
        normData = subjData
        justScores = pd.concat([normData.C1S, normData.C2S, normData.C3S, normData.C4S, normData.ES])
        subMean = justScores.mean()
        subStd = justScores.std()
        
        for no in range(len(normData)):
            normData.C1S.iloc[no] = (normData.C1S.iloc[no] -subMean)/subStd
            normData.C2S.iloc[no] = (normData.C2S.iloc[no] -subMean)/subStd
            normData.C3S.iloc[no]= (normData.C3S.iloc[no] -subMean)/subStd
            normData.C4S.iloc[no] = (normData.C4S.iloc[no] -subMean)/subStd
            normData.ES.iloc[no]= (normData.ES.iloc[no] -subMean)/subStd
            
        for movie in range(len(pd.unique(thisDF.Movie))):
          thisMovie = pd.unique(normData.Movie)[movie]
          thisDF = normData[normData.Movie == thisMovie]
          thisDFName = 'ScaledRegressors_EM' + str(emP2) + '_' + thisMovie  + '_' + normData.EN.iloc[0]   + '_' + thisSub + '.csv'
          thisDF.to_csv(thisDFName)
        
        os.chdir(mainPath)
        scaledData = subjData
        scaledData.C1S = preprocessing.scale(scaledData.C1S, with_mean=True)
        scaledData.C2S = preprocessing.scale(scaledData.C2S, with_mean=True)
        scaledData.C3S = preprocessing.scale(scaledData.C3S, with_mean=True)
        scaledData.C4S = preprocessing.scale(scaledData.C4S, with_mean=True)
        scaledData.ES = preprocessing.scale(scaledData.ES, with_mean=True)
        scaledData.Dur= preprocessing.scale(scaledData.Dur, with_mean=True)

        os.chdir(mainPath) 
        
        Predictors = ['Intercept','dur','C1S','C2S', 'C3S','C4S', 'Clip']
        Type = ['mean', 's', scaledData.C1N.iloc[0], scaledData.C2N.iloc[0], scaledData.C3N.iloc[0], scaledData.C4N.iloc[0], 'num']
        
        md = smf.glm("ES ~ Dur + C1S + C2S + C3S + C4S + Clip", scaledData)
        mdf =md.fit()
        print(mdf.summary())
        resDataFrame = pd.DataFrame(columns = ['Emotion','Predictors', 'tValues', 'pValues', 'Type', 'Subject'])
        resDataFrame.Predictors= Predictors
        resDataFrame.Type= Type
        resDataFrame.tValues.iloc[0:7] = mdf.tvalues[0:7]
        resDataFrame.pValues.iloc[0:7]  = mdf.pvalues[0:7]
        resDataFrame.Subject = sb
        resDataFrame.Emotion =scaledData.EN.iloc[0]
    
        allEmoSub= pd.concat([allEmoSub, resDataFrame])
        fname = EmoU[emoSS] + '_glms.csv'    
        os.chdir('EmoGlms')
        allEmoSub.to_csv(fname)    
        os.chdir(mainPath)

