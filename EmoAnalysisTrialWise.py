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
import glob


mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla'

os.chdir(mainPath)

emData = pd.read_csv('emByTrial_Table.csv',  encoding = "utf-8")

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


for j in range(5,13,2): 
    print (j)
    AngerData= AngerData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[0], na=False),:]])
    AnxData = AnxData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[1],na=False),:]])
    ContemptData = ContemptData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[2], na=False),:]])
    DisgustData = DisgustData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[3], na=False),:]])
    GuiltData = GuiltData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[4], na=False),:]])
    FearData = FearData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[5], na=False),:]])
    HappinessData = HappinessData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[6], na=False),:]])
    LoveData = LoveData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[7], na=False),:]])
    SadData = SadData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[8], na=False),:]])
    SatisfactionData = SatisfactionData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[9], na=False),:]])
    ShameData = ShameData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[10], na=False),:]])
    SurpriseData = SurpriseData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[11], na=False),:]])
    WarmHeartData = WarmHeartData.append([emData.loc[emData.iloc[:,j].str.contains(EmoU[12], na=False),:]])

Emotions = pd.Series(['Emotion1Name', 'Emotion1Score','Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'])
Components = pd.Series(['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'])


WarmHeartData2 = WarmHeartData
WarmHeartData2Loc = WarmHeartData2.columns[WarmHeartData2.isin(['Warm-heartedness']).any()]
if len(WarmHeartData2Loc) == 1:
        for em in range(len(WarmHeartData2Loc)):
            En = WarmHeartData2Loc[0]
            ENum = int(En[7])
            Es = pd.Series([En, En[:8] + 'Score'])
            ix = []
            for em in range(0,len(Es)):
                ix.append(Emotions.tolist().index(Es[em]))
            dropMe = list(Emotions[list((set(range(8)) - set(ix)))])
            WarmHeartData2.drop(columns=dropMe, axis=1, inplace=True)
elif len(WarmHeartData2Loc) == 2:
    wHeartl1 = WarmHeartData2.index[WarmHeartData2['Emotion1Name'] == 'Warm-heartedness']
    wHeartl2 = WarmHeartData2.index[WarmHeartData2['Emotion2Name'] == 'Warm-heartedness']
    wHeart1 = WarmHeartData2.Emotion1Score.loc[wHeartl1]
    wHeart2 = WarmHeartData2.Emotion2Score.loc[wHeartl2]
    otherEmoS = WarmHeartData2.Emotion1Score.loc[wHeartl2]
    otherEmoN = WarmHeartData2.Emotion1Name.loc[wHeartl2]
    WarmHeartData2.Emotion1Score.loc[wHeartl2] = wHeart2
    WarmHeartData2.Emotion1Name.loc[wHeartl2] = WarmHeartData2.Emotion2Name.loc[wHeartl2]
    WarmHeartData2.Emotion2Score.loc[wHeartl2] = otherEmoS 
    WarmHeartData2.Emotion2Name.loc[wHeartl2] = otherEmoN
    WarmHeartData2.drop(columns=['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    WarmHeartData2.drop(columns=[ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(WarmHeartData2Loc) == 3:
    wHeartl1 = WarmHeartData2.index[WarmHeartData2['Emotion1Name'] == 'Warm-heartedness']
    wHeartl2 = WarmHeartData2.index[WarmHeartData2['Emotion2Name'] == 'Warm-heartedness']
    wHeartl3 = WarmHeartData2.index[WarmHeartData2['Emotion3Name'] == 'Warm-heartedness']
    
    wHeart1 = WarmHeartData2.Emotion1Score.loc[wHeartl1]
    wHeart2 = WarmHeartData2.Emotion2Score.loc[wHeartl2]
    wHeart3 = WarmHeartData2.Emotion3Score.loc[wHeartl3]
    
    otherEmoS1 = WarmHeartData2.Emotion1Score.loc[wHeartl2]
    otherEmoN1 = WarmHeartData2.Emotion1Name.loc[wHeartl2]
    otherEmoS2 = WarmHeartData2.Emotion2Score.loc[wHeartl3]
    otherEmoN2 = WarmHeartData2.Emotion2Name.loc[wHeartl3]
    WarmHeartData2.Emotion1Score.loc[wHeartl3] = wHeart3
    WarmHeartData2.Emotion1Name.loc[wHeartl3] = WarmHeartData2.Emotion3Name.loc[wHeartl3]
    WarmHeartData2.Emotion2Score.loc[wHeartl2] = otherEmoS1 
    WarmHeartData2.Emotion2Name.loc[wHeartl2] = otherEmoN1
    WarmHeartData2.Emotion3Score.loc[wHeartl3] = otherEmoS2 
    WarmHeartData2.Emotion3Name.loc[wHeartl3] = otherEmoN2
    WarmHeartData2.drop(columns=['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    WarmHeartData2.drop(columns=[ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(WarmHeartData2Loc) == 4:
    wHeartl1 = WarmHeartData2.index[WarmHeartData2['Emotion1Name'] == 'Warm-heartedness']
    wHeartl2 = WarmHeartData2.index[WarmHeartData2['Emotion2Name'] == 'Warm-heartedness']
    wHeartl3 = WarmHeartData2.index[WarmHeartData2['Emotion3Name'] == 'Warm-heartedness']
    wHeartl4 = WarmHeartData2.index[WarmHeartData2['Emotion4Name'] == 'Warm-heartedness']
    
    wHeart1 = WarmHeartData2.Emotion1Score.loc[wHeartl1]
    wHeart2 = WarmHeartData2.Emotion2Score.loc[wHeartl2]
    wHeart3 = WarmHeartData2.Emotion3Score.loc[wHeartl3]
    wHeart4 = WarmHeartData2.Emotion4Score.loc[wHeartl4]
    
    otherEmoS1 = WarmHeartData2.Emotion1Score.loc[wHeartl2]
    otherEmoN1 = WarmHeartData2.Emotion1Name.loc[wHeartl2]
    otherEmoS2 = WarmHeartData2.Emotion2Score.loc[wHeartl3]
    otherEmoN2 = WarmHeartData2.Emotion2Name.loc[wHeartl3]
    otherEmoS3 = WarmHeartData2.Emotion3Score.loc[wHeartl4]
    otherEmoN3 = WarmHeartData2.Emotion3Name.loc[wHeartl4]
    
    WarmHeartData2.Emotion1Score.loc[wHeartl3] = wHeart3
    WarmHeartData2.Emotion1Name.loc[wHeartl3] = WarmHeartData2.Emotion3Name.loc[wHeartl3]
    WarmHeartData2.Emotion2Score.loc[wHeartl2] = otherEmoS1 
    WarmHeartData2.Emotion2Name.loc[wHeartl2] = otherEmoN1
    WarmHeartData2.Emotion3Score.loc[wHeartl3] = otherEmoS2 
    WarmHeartData2.Emotion3Name.loc[wHeartl3] = otherEmoN2
    WarmHeartData2.Emotion4Score.loc[wHeartl4] = otherEmoS3 
    WarmHeartData2.Emotion4Name.loc[wHeartl4] = otherEmoN3
    WarmHeartData2.drop(columns=['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)





AngerData2 = AngerData
AngerData2Loc = AngerData2.columns[AngerData2.isin(['Anger']).any()]
if len(AngerData2Loc) == 1:
    AngerData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(AngerData2Loc) == 2:
    Angerl1 = AngerData2.index[AngerData2['Emotion1Name'] == 'Anger']
    Angerl2 = AngerData2.index[AngerData2['Emotion2Name'] == 'Anger']
    Anger1 = AngerData2.Emotion1Score.loc[Angerl1]
    Anger2 = AngerData2.Emotion2Score.loc[Angerl2]
    otherEmoS = AngerData2.Emotion1Score.loc[Angerl2]
    otherEmoN = AngerData2.Emotion1Name.loc[Angerl2]
    AngerData2.Emotion1Score.loc[Angerl2] = Anger2
    AngerData2.Emotion1Name.loc[Angerl2] = AngerData2.Emotion2Name.loc[Angerl2]
    AngerData2.Emotion2Score.loc[Angerl2] = otherEmoS 
    AngerData2.Emotion2Name.loc[Angerl2] = otherEmoN
    AngerData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    AngerData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(AngerData2Loc) == 3:
    Angerl1 = AngerData2.index[AngerData2['Emotion1Name'] == 'Anger']
    Angerl2 = AngerData2.index[AngerData2['Emotion2Name'] == 'Anger']
    Angerl3 = AngerData2.index[AngerData2['Emotion3Name'] == 'Anger']
    
    Anger1 = AngerData2.Emotion1Score.loc[Angerl1]
    Anger2 = AngerData2.Emotion2Score.loc[Angerl2]
    Anger3 = AngerData2.Emotion3Score.loc[Angerl3]
    
    otherEmoS1 = AngerData2.Emotion1Score.loc[Angerl2]
    otherEmoN1 = AngerData2.Emotion1Name.loc[Angerl2]
    otherEmoS2 = AngerData2.Emotion2Score.loc[Angerl3]
    otherEmoN2 = AngerData2.Emotion2Name.loc[Angerl3]
    AngerData2.Emotion1Score.loc[Angerl3] = Anger3
    AngerData2.Emotion1Name.loc[Angerl3] = AngerData2.Emotion3Name.loc[Angerl3]
    AngerData2.Emotion2Score.loc[Angerl2] = otherEmoS1 
    AngerData2.Emotion2Name.loc[Angerl2] = otherEmoN1
    AngerData2.Emotion3Score.loc[Angerl3] = otherEmoS2 
    AngerData2.Emotion3Name.loc[Angerl3] = otherEmoN2
    AngerData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    AngerData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(AngerData2Loc) == 4:
    Angerl1 = AngerData2.index[AngerData2['Emotion1Name'] == 'Anger']
    Angerl2 = AngerData2.index[AngerData2['Emotion2Name'] == 'Anger']
    Angerl3 = AngerData2.index[AngerData2['Emotion3Name'] == 'Anger']
    Angerl4 = AngerData2.index[AngerData2['Emotion4Name'] == 'Anger']
    
    Anger1 = AngerData2.Emotion1Score.loc[Angerl1]
    Anger2 = AngerData2.Emotion2Score.loc[Angerl2]
    Anger3 = AngerData2.Emotion3Score.loc[Angerl3]
    Anger4 = AngerData2.Emotion4Score.loc[Angerl4]
    
    otherEmoS1 = AngerData2.Emotion1Score.loc[Angerl2]
    otherEmoN1 = AngerData2.Emotion1Name.loc[Angerl2]
    otherEmoS2 = AngerData2.Emotion2Score.loc[Angerl3]
    otherEmoN2 = AngerData2.Emotion2Name.loc[Angerl3]
    otherEmoS3 = AngerData2.Emotion3Score.loc[Angerl4]
    otherEmoN3 = AngerData2.Emotion3Name.loc[Angerl4]
    
    AngerData2.Emotion1Score.loc[Angerl3] = Anger3
    AngerData2.Emotion1Name.loc[Angerl3] = AngerData2.Emotion3Name.loc[Angerl3]
    AngerData2.Emotion2Score.loc[Angerl2] = otherEmoS1 
    AngerData2.Emotion2Name.loc[Angerl2] = otherEmoN1
    AngerData2.Emotion3Score.loc[Angerl3] = otherEmoS2 
    AngerData2.Emotion3Name.loc[Angerl3] = otherEmoN2
    AngerData2.Emotion4Score.loc[Angerl4] = otherEmoS3 
    AngerData2.Emotion4Name.loc[Angerl4] = otherEmoN3
    AngerData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



AnxData2 = AnxData
AnxData2Loc = AnxData2.columns[AnxData2.isin(['Anxiety']).any()]
if len(AnxData2Loc) == 1:
    AnxData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(AnxData2Loc) == 2:
    Anxietyl1 = AnxData2.index[AnxData2['Emotion1Name'] == 'Anxiety']
    Anxietyl2 = AnxData2.index[AnxData2['Emotion2Name'] == 'Anxiety']
    Anxiety1 = AnxData2.Emotion1Score.loc[Anxietyl1]
    Anxiety2 = AnxData2.Emotion2Score.loc[Anxietyl2]
    otherEmoS = AnxData2.Emotion1Score.loc[Anxietyl2]
    otherEmoN = AnxData2.Emotion1Name.loc[Anxietyl2]
    AnxData2.Emotion1Score.loc[Anxietyl2] = Anxiety2
    AnxData2.Emotion1Name.loc[Anxietyl2] = AnxData2.Emotion2Name.loc[Anxietyl2]
    AnxData2.Emotion2Score.loc[Anxietyl2] = otherEmoS 
    AnxData2.Emotion2Name.loc[Anxietyl2] = otherEmoN
    AnxData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    AnxData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(AnxData2Loc) == 3:
    Anxietyl1 = AnxData2.index[AnxData2['Emotion1Name'] == 'Anxiety']
    Anxietyl2 = AnxData2.index[AnxData2['Emotion2Name'] == 'Anxiety']
    Anxietyl3 = AnxData2.index[AnxData2['Emotion3Name'] == 'Anxiety']
    
    Anxiety1 = AnxData2.Emotion1Score.loc[Anxietyl1]
    Anxiety2 = AnxData2.Emotion2Score.loc[Anxietyl2]
    Anxiety3 = AnxData2.Emotion3Score.loc[Anxietyl3]
    
    otherEmoS1 = AnxData2.Emotion1Score.loc[Anxietyl2]
    otherEmoN1 = AnxData2.Emotion1Name.loc[Anxietyl2]
    otherEmoS2 = AnxData2.Emotion2Score.loc[Anxietyl3]
    otherEmoN2 = AnxData2.Emotion2Name.loc[Anxietyl3]
    AnxData2.Emotion1Score.loc[Anxietyl3] = Anxiety3
    AnxData2.Emotion1Name.loc[Anxietyl3] = AnxData2.Emotion3Name.loc[Anxietyl3]
    AnxData2.Emotion2Score.loc[Anxietyl2] = otherEmoS1 
    AnxData2.Emotion2Name.loc[Anxietyl2] = otherEmoN1
    AnxData2.Emotion3Score.loc[Anxietyl3] = otherEmoS2 
    AnxData2.Emotion3Name.loc[Anxietyl3] = otherEmoN2
    AnxData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    AnxData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(AnxData2Loc) == 4:
    Anxietyl1 = AnxData2.index[AnxData2['Emotion1Name'] == 'Anxiety']
    Anxietyl2 = AnxData2.index[AnxData2['Emotion2Name'] == 'Anxiety']
    Anxietyl3 = AnxData2.index[AnxData2['Emotion3Name'] == 'Anxiety']
    Anxietyl4 = AnxData2.index[AnxData2['Emotion4Name'] == 'Anxiety']
    
    Anxiety1 = AnxData2.Emotion1Score.loc[Anxietyl1]
    Anxiety2 = AnxData2.Emotion2Score.loc[Anxietyl2]
    Anxiety3 = AnxData2.Emotion3Score.loc[Anxietyl3]
    Anxiety4 = AnxData2.Emotion4Score.loc[Anxietyl4]
    
    otherEmoS1 = AnxData2.Emotion1Score.loc[Anxietyl2]
    otherEmoN1 = AnxData2.Emotion1Name.loc[Anxietyl2]
    otherEmoS2 = AnxData2.Emotion2Score.loc[Anxietyl3]
    otherEmoN2 = AnxData2.Emotion2Name.loc[Anxietyl3]
    otherEmoS3 = AnxData2.Emotion3Score.loc[Anxietyl4]
    otherEmoN3 = AnxData2.Emotion3Name.loc[Anxietyl4]
    
    AnxData2.Emotion1Score.loc[Anxietyl3] = Anxiety3
    AnxData2.Emotion1Name.loc[Anxietyl3] = AnxData2.Emotion3Name.loc[Anxietyl3]
    AnxData2.Emotion2Score.loc[Anxietyl2] = otherEmoS1 
    AnxData2.Emotion2Name.loc[Anxietyl2] = otherEmoN1
    AnxData2.Emotion3Score.loc[Anxietyl3] = otherEmoS2 
    AnxData2.Emotion3Name.loc[Anxietyl3] = otherEmoN2
    AnxData2.Emotion4Score.loc[Anxietyl4] = otherEmoS3 
    AnxData2.Emotion4Name.loc[Anxietyl4] = otherEmoN3
    AnxData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



ContemptData2 = ContemptData
ContemptData2Loc = ContemptData2.columns[ContemptData2.isin(['Contempt']).any()]
if len(ContemptData2Loc) == 1:
    ContemptData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(ContemptData2Loc) == 2:
    Contemptl1 = ContemptData2.index[ContemptData2['Emotion1Name'] == 'Contempt']
    Contemptl2 = ContemptData2.index[ContemptData2['Emotion2Name'] == 'Contempt']
    Contempt1 = ContemptData2.Emotion1Score.loc[Contemptl1]
    Contempt2 = ContemptData2.Emotion2Score.loc[Contemptl2]
    otherEmoS = ContemptData2.Emotion1Score.loc[Contemptl2]
    otherEmoN = ContemptData2.Emotion1Name.loc[Contemptl2]
    ContemptData2.Emotion1Score.loc[Contemptl2] = Contempt2
    ContemptData2.Emotion1Name.loc[Contemptl2] = ContemptData2.Emotion2Name.loc[Contemptl2]
    ContemptData2.Emotion2Score.loc[Contemptl2] = otherEmoS 
    ContemptData2.Emotion2Name.loc[Contemptl2] = otherEmoN
    ContemptData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    ContemptData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(ContemptData2Loc) == 3:
    Contemptl1 = ContemptData2.index[ContemptData2['Emotion1Name'] == 'Contempt']
    Contemptl2 = ContemptData2.index[ContemptData2['Emotion2Name'] == 'Contempt']
    Contemptl3 = ContemptData2.index[ContemptData2['Emotion3Name'] == 'Contempt']
    
    Contempt1 = ContemptData2.Emotion1Score.loc[Contemptl1]
    Contempt2 = ContemptData2.Emotion2Score.loc[Contemptl2]
    Contempt3 = ContemptData2.Emotion3Score.loc[Contemptl3]
    
    otherEmoS1 = ContemptData2.Emotion1Score.loc[Contemptl2]
    otherEmoN1 = ContemptData2.Emotion1Name.loc[Contemptl2]
    otherEmoS2 = ContemptData2.Emotion2Score.loc[Contemptl3]
    otherEmoN2 = ContemptData2.Emotion2Name.loc[Contemptl3]
    ContemptData2.Emotion1Score.loc[Contemptl3] = Contempt3
    ContemptData2.Emotion1Name.loc[Contemptl3] = ContemptData2.Emotion3Name.loc[Contemptl3]
    ContemptData2.Emotion2Score.loc[Contemptl2] = otherEmoS1 
    ContemptData2.Emotion2Name.loc[Contemptl2] = otherEmoN1
    ContemptData2.Emotion3Score.loc[Contemptl3] = otherEmoS2 
    ContemptData2.Emotion3Name.loc[Contemptl3] = otherEmoN2
    ContemptData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    ContemptData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(ContemptData2Loc) == 4:
    Contemptl1 = ContemptData2.index[ContemptData2['Emotion1Name'] == 'Contempt']
    Contemptl2 = ContemptData2.index[ContemptData2['Emotion2Name'] == 'Contempt']
    Contemptl3 = ContemptData2.index[ContemptData2['Emotion3Name'] == 'Contempt']
    Contemptl4 = ContemptData2.index[ContemptData2['Emotion4Name'] == 'Contempt']
    
    Contempt1 = ContemptData2.Emotion1Score.loc[Contemptl1]
    Contempt2 = ContemptData2.Emotion2Score.loc[Contemptl2]
    Contempt3 = ContemptData2.Emotion3Score.loc[Contemptl3]
    Contempt4 = ContemptData2.Emotion4Score.loc[Contemptl4]
    
    otherEmoS1 = ContemptData2.Emotion1Score.loc[Contemptl2]
    otherEmoN1 = ContemptData2.Emotion1Name.loc[Contemptl2]
    otherEmoS2 = ContemptData2.Emotion2Score.loc[Contemptl3]
    otherEmoN2 = ContemptData2.Emotion2Name.loc[Contemptl3]
    otherEmoS3 = ContemptData2.Emotion3Score.loc[Contemptl4]
    otherEmoN3 = ContemptData2.Emotion3Name.loc[Contemptl4]
    
    ContemptData2.Emotion1Score.loc[Contemptl3] = Contempt3
    ContemptData2.Emotion1Name.loc[Contemptl3] = ContemptData2.Emotion3Name.loc[Contemptl3]
    ContemptData2.Emotion2Score.loc[Contemptl2] = otherEmoS1 
    ContemptData2.Emotion2Name.loc[Contemptl2] = otherEmoN1
    ContemptData2.Emotion3Score.loc[Contemptl3] = otherEmoS2 
    ContemptData2.Emotion3Name.loc[Contemptl3] = otherEmoN2
    ContemptData2.Emotion4Score.loc[Contemptl4] = otherEmoS3 
    ContemptData2.Emotion4Name.loc[Contemptl4] = otherEmoN3
    ContemptData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



DisgustData2 = DisgustData
DisgustData2Loc = DisgustData2.columns[DisgustData2.isin(['Disgust']).any()]
if len(DisgustData2Loc) == 1:
    DisgustData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(DisgustData2Loc) == 2:
    Disgustl1 = DisgustData2.index[DisgustData2['Emotion1Name'] == 'Disgust']
    Disgustl2 = DisgustData2.index[DisgustData2['Emotion2Name'] == 'Disgust']
    Disgust1 = DisgustData2.Emotion1Score.loc[Disgustl1]
    Disgust2 = DisgustData2.Emotion2Score.loc[Disgustl2]
    otherEmoS = DisgustData2.Emotion1Score.loc[Disgustl2]
    otherEmoN = DisgustData2.Emotion1Name.loc[Disgustl2]
    DisgustData2.Emotion1Score.loc[Disgustl2] = Disgust2
    DisgustData2.Emotion1Name.loc[Disgustl2] = DisgustData2.Emotion2Name.loc[Disgustl2]
    DisgustData2.Emotion2Score.loc[Disgustl2] = otherEmoS 
    DisgustData2.Emotion2Name.loc[Disgustl2] = otherEmoN
    DisgustData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    DisgustData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(DisgustData2Loc) == 3:
    Disgustl1 = DisgustData2.index[DisgustData2['Emotion1Name'] == 'Disgust']
    Disgustl2 = DisgustData2.index[DisgustData2['Emotion2Name'] == 'Disgust']
    Disgustl3 = DisgustData2.index[DisgustData2['Emotion3Name'] == 'Disgust']
    
    Disgust1 = DisgustData2.Emotion1Score.loc[Disgustl1]
    Disgust2 = DisgustData2.Emotion2Score.loc[Disgustl2]
    Disgust3 = DisgustData2.Emotion3Score.loc[Disgustl3]
    
    otherEmoS1 = DisgustData2.Emotion1Score.loc[Disgustl2]
    otherEmoN1 = DisgustData2.Emotion1Name.loc[Disgustl2]
    otherEmoS2 = DisgustData2.Emotion2Score.loc[Disgustl3]
    otherEmoN2 = DisgustData2.Emotion2Name.loc[Disgustl3]
    DisgustData2.Emotion1Score.loc[Disgustl3] = Disgust3
    DisgustData2.Emotion1Name.loc[Disgustl3] = DisgustData2.Emotion3Name.loc[Disgustl3]
    DisgustData2.Emotion2Score.loc[Disgustl2] = otherEmoS1 
    DisgustData2.Emotion2Name.loc[Disgustl2] = otherEmoN1
    DisgustData2.Emotion3Score.loc[Disgustl3] = otherEmoS2 
    DisgustData2.Emotion3Name.loc[Disgustl3] = otherEmoN2
    DisgustData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    DisgustData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(DisgustData2Loc) == 4:
    Disgustl1 = DisgustData2.index[DisgustData2['Emotion1Name'] == 'Disgust']
    Disgustl2 = DisgustData2.index[DisgustData2['Emotion2Name'] == 'Disgust']
    Disgustl3 = DisgustData2.index[DisgustData2['Emotion3Name'] == 'Disgust']
    Disgustl4 = DisgustData2.index[DisgustData2['Emotion4Name'] == 'Disgust']
    
    Disgust1 = DisgustData2.Emotion1Score.loc[Disgustl1]
    Disgust2 = DisgustData2.Emotion2Score.loc[Disgustl2]
    Disgust3 = DisgustData2.Emotion3Score.loc[Disgustl3]
    Disgust4 = DisgustData2.Emotion4Score.loc[Disgustl4]
    
    otherEmoS1 = DisgustData2.Emotion1Score.loc[Disgustl2]
    otherEmoN1 = DisgustData2.Emotion1Name.loc[Disgustl2]
    otherEmoS2 = DisgustData2.Emotion2Score.loc[Disgustl3]
    otherEmoN2 = DisgustData2.Emotion2Name.loc[Disgustl3]
    otherEmoS3 = DisgustData2.Emotion3Score.loc[Disgustl4]
    otherEmoN3 = DisgustData2.Emotion3Name.loc[Disgustl4]
    
    DisgustData2.Emotion1Score.loc[Disgustl3] = Disgust3
    DisgustData2.Emotion1Name.loc[Disgustl3] = DisgustData2.Emotion3Name.loc[Disgustl3]
    DisgustData2.Emotion2Score.loc[Disgustl2] = otherEmoS1 
    DisgustData2.Emotion2Name.loc[Disgustl2] = otherEmoN1
    DisgustData2.Emotion3Score.loc[Disgustl3] = otherEmoS2 
    DisgustData2.Emotion3Name.loc[Disgustl3] = otherEmoN2
    DisgustData2.Emotion4Score.loc[Disgustl4] = otherEmoS3 
    DisgustData2.Emotion4Name.loc[Disgustl4] = otherEmoN3
    DisgustData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



FearData2 = FearData
FearData2Loc = FearData2.columns[FearData2.isin(['Fear']).any()]
if len(FearData2Loc) == 1:
    FearData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(FearData2Loc) == 2:
    Fearl1 = FearData2.index[FearData2['Emotion1Name'] == 'Fear']
    Fearl2 = FearData2.index[FearData2['Emotion2Name'] == 'Fear']
    Fear1 = FearData2.Emotion1Score.loc[Fearl1]
    Fear2 = FearData2.Emotion2Score.loc[Fearl2]
    otherEmoS = FearData2.Emotion1Score.loc[Fearl2]
    otherEmoN = FearData2.Emotion1Name.loc[Fearl2]
    FearData2.Emotion1Score.loc[Fearl2] = Fear2
    FearData2.Emotion1Name.loc[Fearl2] = FearData2.Emotion2Name.loc[Fearl2]
    FearData2.Emotion2Score.loc[Fearl2] = otherEmoS 
    FearData2.Emotion2Name.loc[Fearl2] = otherEmoN
    FearData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    FearData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(FearData2Loc) == 3:
    Fearl1 = FearData2.index[FearData2['Emotion1Name'] == 'Fear']
    Fearl2 = FearData2.index[FearData2['Emotion2Name'] == 'Fear']
    Fearl3 = FearData2.index[FearData2['Emotion3Name'] == 'Fear']
    
    Fear1 = FearData2.Emotion1Score.loc[Fearl1]
    Fear2 = FearData2.Emotion2Score.loc[Fearl2]
    Fear3 = FearData2.Emotion3Score.loc[Fearl3]
    
    otherEmoS1 = FearData2.Emotion1Score.loc[Fearl2]
    otherEmoN1 = FearData2.Emotion1Name.loc[Fearl2]
    otherEmoS2 = FearData2.Emotion2Score.loc[Fearl3]
    otherEmoN2 = FearData2.Emotion2Name.loc[Fearl3]
    FearData2.Emotion1Score.loc[Fearl3] = Fear3
    FearData2.Emotion1Name.loc[Fearl3] = FearData2.Emotion3Name.loc[Fearl3]
    FearData2.Emotion2Score.loc[Fearl2] = otherEmoS1 
    FearData2.Emotion2Name.loc[Fearl2] = otherEmoN1
    FearData2.Emotion3Score.loc[Fearl3] = otherEmoS2 
    FearData2.Emotion3Name.loc[Fearl3] = otherEmoN2
    FearData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    FearData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(FearData2Loc) == 4:
    Fearl1 = FearData2.index[FearData2['Emotion1Name'] == 'Fear']
    Fearl2 = FearData2.index[FearData2['Emotion2Name'] == 'Fear']
    Fearl3 = FearData2.index[FearData2['Emotion3Name'] == 'Fear']
    Fearl4 = FearData2.index[FearData2['Emotion4Name'] == 'Fear']
    
    Fear1 = FearData2.Emotion1Score.loc[Fearl1]
    Fear2 = FearData2.Emotion2Score.loc[Fearl2]
    Fear3 = FearData2.Emotion3Score.loc[Fearl3]
    Fear4 = FearData2.Emotion4Score.loc[Fearl4]
    
    otherEmoS1 = FearData2.Emotion1Score.loc[Fearl2]
    otherEmoN1 = FearData2.Emotion1Name.loc[Fearl2]
    otherEmoS2 = FearData2.Emotion2Score.loc[Fearl3]
    otherEmoN2 = FearData2.Emotion2Name.loc[Fearl3]
    otherEmoS3 = FearData2.Emotion3Score.loc[Fearl4]
    otherEmoN3 = FearData2.Emotion3Name.loc[Fearl4]
    
    FearData2.Emotion1Score.loc[Fearl3] = Fear3
    FearData2.Emotion1Name.loc[Fearl3] = FearData2.Emotion3Name.loc[Fearl3]
    FearData2.Emotion2Score.loc[Fearl2] = otherEmoS1 
    FearData2.Emotion2Name.loc[Fearl2] = otherEmoN1
    FearData2.Emotion3Score.loc[Fearl3] = otherEmoS2 
    FearData2.Emotion3Name.loc[Fearl3] = otherEmoN2
    FearData2.Emotion4Score.loc[Fearl4] = otherEmoS3 
    FearData2.Emotion4Name.loc[Fearl4] = otherEmoN3
    FearData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



GuiltData2 = GuiltData
GuiltData2Loc = GuiltData2.columns[GuiltData2.isin(['Guilt']).any()]
if len(GuiltData2Loc) == 1:
    GuiltData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(GuiltData2Loc) == 2:
    Guiltl1 = GuiltData2.index[GuiltData2['Emotion1Name'] == 'Guilt']
    Guiltl2 = GuiltData2.index[GuiltData2['Emotion2Name'] == 'Guilt']
    Guilt1 = GuiltData2.Emotion1Score.loc[Guiltl1]
    Guilt2 = GuiltData2.Emotion2Score.loc[Guiltl2]
    otherEmoS = GuiltData2.Emotion1Score.loc[Guiltl2]
    otherEmoN = GuiltData2.Emotion1Name.loc[Guiltl2]
    GuiltData2.Emotion1Score.loc[Guiltl2] = Guilt2
    GuiltData2.Emotion1Name.loc[Guiltl2] = GuiltData2.Emotion2Name.loc[Guiltl2]
    GuiltData2.Emotion2Score.loc[Guiltl2] = otherEmoS 
    GuiltData2.Emotion2Name.loc[Guiltl2] = otherEmoN
    GuiltData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    GuiltData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(GuiltData2Loc) == 3:
    Guiltl1 = GuiltData2.index[GuiltData2['Emotion1Name'] == 'Guilt']
    Guiltl2 = GuiltData2.index[GuiltData2['Emotion2Name'] == 'Guilt']
    Guiltl3 = GuiltData2.index[GuiltData2['Emotion3Name'] == 'Guilt']
    
    Guilt1 = GuiltData2.Emotion1Score.loc[Guiltl1]
    Guilt2 = GuiltData2.Emotion2Score.loc[Guiltl2]
    Guilt3 = GuiltData2.Emotion3Score.loc[Guiltl3]
    
    otherEmoS1 = GuiltData2.Emotion1Score.loc[Guiltl2]
    otherEmoN1 = GuiltData2.Emotion1Name.loc[Guiltl2]
    otherEmoS2 = GuiltData2.Emotion2Score.loc[Guiltl3]
    otherEmoN2 = GuiltData2.Emotion2Name.loc[Guiltl3]
    GuiltData2.Emotion1Score.loc[Guiltl3] = Guilt3
    GuiltData2.Emotion1Name.loc[Guiltl3] = GuiltData2.Emotion3Name.loc[Guiltl3]
    GuiltData2.Emotion2Score.loc[Guiltl2] = otherEmoS1 
    GuiltData2.Emotion2Name.loc[Guiltl2] = otherEmoN1
    GuiltData2.Emotion3Score.loc[Guiltl3] = otherEmoS2 
    GuiltData2.Emotion3Name.loc[Guiltl3] = otherEmoN2
    GuiltData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    GuiltData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(GuiltData2Loc) == 4:
    Guiltl1 = GuiltData2.index[GuiltData2['Emotion1Name'] == 'Guilt']
    Guiltl2 = GuiltData2.index[GuiltData2['Emotion2Name'] == 'Guilt']
    Guiltl3 = GuiltData2.index[GuiltData2['Emotion3Name'] == 'Guilt']
    Guiltl4 = GuiltData2.index[GuiltData2['Emotion4Name'] == 'Guilt']
    
    Guilt1 = GuiltData2.Emotion1Score.loc[Guiltl1]
    Guilt2 = GuiltData2.Emotion2Score.loc[Guiltl2]
    Guilt3 = GuiltData2.Emotion3Score.loc[Guiltl3]
    Guilt4 = GuiltData2.Emotion4Score.loc[Guiltl4]
    
    otherEmoS1 = GuiltData2.Emotion1Score.loc[Guiltl2]
    otherEmoN1 = GuiltData2.Emotion1Name.loc[Guiltl2]
    otherEmoS2 = GuiltData2.Emotion2Score.loc[Guiltl3]
    otherEmoN2 = GuiltData2.Emotion2Name.loc[Guiltl3]
    otherEmoS3 = GuiltData2.Emotion3Score.loc[Guiltl4]
    otherEmoN3 = GuiltData2.Emotion3Name.loc[Guiltl4]
    
    GuiltData2.Emotion1Score.loc[Guiltl3] = Guilt3
    GuiltData2.Emotion1Name.loc[Guiltl3] = GuiltData2.Emotion3Name.loc[Guiltl3]
    GuiltData2.Emotion2Score.loc[Guiltl2] = otherEmoS1 
    GuiltData2.Emotion2Name.loc[Guiltl2] = otherEmoN1
    GuiltData2.Emotion3Score.loc[Guiltl3] = otherEmoS2 
    GuiltData2.Emotion3Name.loc[Guiltl3] = otherEmoN2
    GuiltData2.Emotion4Score.loc[Guiltl4] = otherEmoS3 
    GuiltData2.Emotion4Name.loc[Guiltl4] = otherEmoN3
    GuiltData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



HappinessData2 = HappinessData
HappinessData2Loc = HappinessData2.columns[HappinessData2.isin(['Happiness']).any()]
if len(HappinessData2Loc) == 1:
    HappinessData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(HappinessData2Loc) == 2:
    Happinessl1 = HappinessData2.index[HappinessData2['Emotion1Name'] == 'Happiness']
    Happinessl2 = HappinessData2.index[HappinessData2['Emotion2Name'] == 'Happiness']
    Happiness1 = HappinessData2.Emotion1Score.loc[Happinessl1]
    Happiness2 = HappinessData2.Emotion2Score.loc[Happinessl2]
    otherEmoS = HappinessData2.Emotion1Score.loc[Happinessl2]
    otherEmoN = HappinessData2.Emotion1Name.loc[Happinessl2]
    HappinessData2.Emotion1Score.loc[Happinessl2] = Happiness2
    HappinessData2.Emotion1Name.loc[Happinessl2] = HappinessData2.Emotion2Name.loc[Happinessl2]
    HappinessData2.Emotion2Score.loc[Happinessl2] = otherEmoS 
    HappinessData2.Emotion2Name.loc[Happinessl2] = otherEmoN
    HappinessData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    HappinessData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(HappinessData2Loc) == 3:
    Happinessl1 = HappinessData2.index[HappinessData2['Emotion1Name'] == 'Happiness']
    Happinessl2 = HappinessData2.index[HappinessData2['Emotion2Name'] == 'Happiness']
    Happinessl3 = HappinessData2.index[HappinessData2['Emotion3Name'] == 'Happiness']
    
    Happiness1 = HappinessData2.Emotion1Score.loc[Happinessl1]
    Happiness2 = HappinessData2.Emotion2Score.loc[Happinessl2]
    Happiness3 = HappinessData2.Emotion3Score.loc[Happinessl3]
    
    otherEmoS1 = HappinessData2.Emotion1Score.loc[Happinessl2]
    otherEmoN1 = HappinessData2.Emotion1Name.loc[Happinessl2]
    otherEmoS2 = HappinessData2.Emotion2Score.loc[Happinessl3]
    otherEmoN2 = HappinessData2.Emotion2Name.loc[Happinessl3]
    HappinessData2.Emotion1Score.loc[Happinessl3] = Happiness3
    HappinessData2.Emotion1Name.loc[Happinessl3] = HappinessData2.Emotion3Name.loc[Happinessl3]
    HappinessData2.Emotion2Score.loc[Happinessl2] = otherEmoS1 
    HappinessData2.Emotion2Name.loc[Happinessl2] = otherEmoN1
    HappinessData2.Emotion3Score.loc[Happinessl3] = otherEmoS2 
    HappinessData2.Emotion3Name.loc[Happinessl3] = otherEmoN2
    HappinessData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    HappinessData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(HappinessData2Loc) == 4:
    Happinessl1 = HappinessData2.index[HappinessData2['Emotion1Name'] == 'Happiness']
    Happinessl2 = HappinessData2.index[HappinessData2['Emotion2Name'] == 'Happiness']
    Happinessl3 = HappinessData2.index[HappinessData2['Emotion3Name'] == 'Happiness']
    Happinessl4 = HappinessData2.index[HappinessData2['Emotion4Name'] == 'Happiness']
    
    Happiness1 = HappinessData2.Emotion1Score.loc[Happinessl1]
    Happiness2 = HappinessData2.Emotion2Score.loc[Happinessl2]
    Happiness3 = HappinessData2.Emotion3Score.loc[Happinessl3]
    Happiness4 = HappinessData2.Emotion4Score.loc[Happinessl4]
    
    otherEmoS1 = HappinessData2.Emotion1Score.loc[Happinessl2]
    otherEmoN1 = HappinessData2.Emotion1Name.loc[Happinessl2]
    otherEmoS2 = HappinessData2.Emotion2Score.loc[Happinessl3]
    otherEmoN2 = HappinessData2.Emotion2Name.loc[Happinessl3]
    otherEmoS3 = HappinessData2.Emotion3Score.loc[Happinessl4]
    otherEmoN3 = HappinessData2.Emotion3Name.loc[Happinessl4]
    
    HappinessData2.Emotion1Score.loc[Happinessl3] = Happiness3
    HappinessData2.Emotion1Name.loc[Happinessl3] = HappinessData2.Emotion3Name.loc[Happinessl3]
    HappinessData2.Emotion2Score.loc[Happinessl2] = otherEmoS1 
    HappinessData2.Emotion2Name.loc[Happinessl2] = otherEmoN1
    HappinessData2.Emotion3Score.loc[Happinessl3] = otherEmoS2 
    HappinessData2.Emotion3Name.loc[Happinessl3] = otherEmoN2
    HappinessData2.Emotion4Score.loc[Happinessl4] = otherEmoS3 
    HappinessData2.Emotion4Name.loc[Happinessl4] = otherEmoN3
    HappinessData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



LoveData2 = LoveData
LoveData2Loc = LoveData2.columns[LoveData2.isin(['Love']).any()]
if len(LoveData2Loc) == 1:
    LoveData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(LoveData2Loc) == 2:
    Lovel1 = LoveData2.index[LoveData2['Emotion1Name'] == 'Love']
    Lovel2 = LoveData2.index[LoveData2['Emotion2Name'] == 'Love']
    Love1 = LoveData2.Emotion1Score.loc[Lovel1]
    Love2 = LoveData2.Emotion2Score.loc[Lovel2]
    otherEmoS = LoveData2.Emotion1Score.loc[Lovel2]
    otherEmoN = LoveData2.Emotion1Name.loc[Lovel2]
    LoveData2.Emotion1Score.loc[Lovel2] = Love2
    LoveData2.Emotion1Name.loc[Lovel2] = LoveData2.Emotion2Name.loc[Lovel2]
    LoveData2.Emotion2Score.loc[Lovel2] = otherEmoS 
    LoveData2.Emotion2Name.loc[Lovel2] = otherEmoN
    LoveData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    LoveData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(LoveData2Loc) == 3:
    Lovel1 = LoveData2.index[LoveData2['Emotion1Name'] == 'Love']
    Lovel2 = LoveData2.index[LoveData2['Emotion2Name'] == 'Love']
    Lovel3 = LoveData2.index[LoveData2['Emotion3Name'] == 'Love']
    
    Love1 = LoveData2.Emotion1Score.loc[Lovel1]
    Love2 = LoveData2.Emotion2Score.loc[Lovel2]
    Love3 = LoveData2.Emotion3Score.loc[Lovel3]
    
    otherEmoS1 = LoveData2.Emotion1Score.loc[Lovel2]
    otherEmoN1 = LoveData2.Emotion1Name.loc[Lovel2]
    otherEmoS2 = LoveData2.Emotion2Score.loc[Lovel3]
    otherEmoN2 = LoveData2.Emotion2Name.loc[Lovel3]
    LoveData2.Emotion1Score.loc[Lovel3] = Love3
    LoveData2.Emotion1Name.loc[Lovel3] = LoveData2.Emotion3Name.loc[Lovel3]
    LoveData2.Emotion2Score.loc[Lovel2] = otherEmoS1 
    LoveData2.Emotion2Name.loc[Lovel2] = otherEmoN1
    LoveData2.Emotion3Score.loc[Lovel3] = otherEmoS2 
    LoveData2.Emotion3Name.loc[Lovel3] = otherEmoN2
    LoveData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    LoveData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(LoveData2Loc) == 4:
    Lovel1 = LoveData2.index[LoveData2['Emotion1Name'] == 'Love']
    Lovel2 = LoveData2.index[LoveData2['Emotion2Name'] == 'Love']
    Lovel3 = LoveData2.index[LoveData2['Emotion3Name'] == 'Love']
    Lovel4 = LoveData2.index[LoveData2['Emotion4Name'] == 'Love']
    
    Love1 = LoveData2.Emotion1Score.loc[Lovel1]
    Love2 = LoveData2.Emotion2Score.loc[Lovel2]
    Love3 = LoveData2.Emotion3Score.loc[Lovel3]
    Love4 = LoveData2.Emotion4Score.loc[Lovel4]
    
    otherEmoS1 = LoveData2.Emotion1Score.loc[Lovel2]
    otherEmoN1 = LoveData2.Emotion1Name.loc[Lovel2]
    otherEmoS2 = LoveData2.Emotion2Score.loc[Lovel3]
    otherEmoN2 = LoveData2.Emotion2Name.loc[Lovel3]
    otherEmoS3 = LoveData2.Emotion3Score.loc[Lovel4]
    otherEmoN3 = LoveData2.Emotion3Name.loc[Lovel4]
    
    LoveData2.Emotion1Score.loc[Lovel3] = Love3
    LoveData2.Emotion1Name.loc[Lovel3] = LoveData2.Emotion3Name.loc[Lovel3]
    LoveData2.Emotion2Score.loc[Lovel2] = otherEmoS1 
    LoveData2.Emotion2Name.loc[Lovel2] = otherEmoN1
    LoveData2.Emotion3Score.loc[Lovel3] = otherEmoS2 
    LoveData2.Emotion3Name.loc[Lovel3] = otherEmoN2
    LoveData2.Emotion4Score.loc[Lovel4] = otherEmoS3 
    LoveData2.Emotion4Name.loc[Lovel4] = otherEmoN3
    LoveData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



SadData2 = SadData
SadData2Loc = SadData2.columns[SadData2.isin(['Sad']).any()]
if len(SadData2Loc) == 1:
    SadData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(SadData2Loc) == 2:
    Sadl1 = SadData2.index[SadData2['Emotion1Name'] == 'Sad']
    Sadl2 = SadData2.index[SadData2['Emotion2Name'] == 'Sad']
    Sad1 = SadData2.Emotion1Score.loc[Sadl1]
    Sad2 = SadData2.Emotion2Score.loc[Sadl2]
    otherEmoS = SadData2.Emotion1Score.loc[Sadl2]
    otherEmoN = SadData2.Emotion1Name.loc[Sadl2]
    SadData2.Emotion1Score.loc[Sadl2] = Sad2
    SadData2.Emotion1Name.loc[Sadl2] = SadData2.Emotion2Name.loc[Sadl2]
    SadData2.Emotion2Score.loc[Sadl2] = otherEmoS 
    SadData2.Emotion2Name.loc[Sadl2] = otherEmoN
    SadData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    SadData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(SadData2Loc) == 3:
    Sadl1 = SadData2.index[SadData2['Emotion1Name'] == 'Sad']
    Sadl2 = SadData2.index[SadData2['Emotion2Name'] == 'Sad']
    Sadl3 = SadData2.index[SadData2['Emotion3Name'] == 'Sad']
    
    Sad1 = SadData2.Emotion1Score.loc[Sadl1]
    Sad2 = SadData2.Emotion2Score.loc[Sadl2]
    Sad3 = SadData2.Emotion3Score.loc[Sadl3]
    
    otherEmoS1 = SadData2.Emotion1Score.loc[Sadl2]
    otherEmoN1 = SadData2.Emotion1Name.loc[Sadl2]
    otherEmoS2 = SadData2.Emotion2Score.loc[Sadl3]
    otherEmoN2 = SadData2.Emotion2Name.loc[Sadl3]
    SadData2.Emotion1Score.loc[Sadl3] = Sad3
    SadData2.Emotion1Name.loc[Sadl3] = SadData2.Emotion3Name.loc[Sadl3]
    SadData2.Emotion2Score.loc[Sadl2] = otherEmoS1 
    SadData2.Emotion2Name.loc[Sadl2] = otherEmoN1
    SadData2.Emotion3Score.loc[Sadl3] = otherEmoS2 
    SadData2.Emotion3Name.loc[Sadl3] = otherEmoN2
    SadData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    SadData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(SadData2Loc) == 4:
    Sadl1 = SadData2.index[SadData2['Emotion1Name'] == 'Sad']
    Sadl2 = SadData2.index[SadData2['Emotion2Name'] == 'Sad']
    Sadl3 = SadData2.index[SadData2['Emotion3Name'] == 'Sad']
    Sadl4 = SadData2.index[SadData2['Emotion4Name'] == 'Sad']
    
    Sad1 = SadData2.Emotion1Score.loc[Sadl1]
    Sad2 = SadData2.Emotion2Score.loc[Sadl2]
    Sad3 = SadData2.Emotion3Score.loc[Sadl3]
    Sad4 = SadData2.Emotion4Score.loc[Sadl4]
    
    otherEmoS1 = SadData2.Emotion1Score.loc[Sadl2]
    otherEmoN1 = SadData2.Emotion1Name.loc[Sadl2]
    otherEmoS2 = SadData2.Emotion2Score.loc[Sadl3]
    otherEmoN2 = SadData2.Emotion2Name.loc[Sadl3]
    otherEmoS3 = SadData2.Emotion3Score.loc[Sadl4]
    otherEmoN3 = SadData2.Emotion3Name.loc[Sadl4]
    
    SadData2.Emotion1Score.loc[Sadl3] = Sad3
    SadData2.Emotion1Name.loc[Sadl3] = SadData2.Emotion3Name.loc[Sadl3]
    SadData2.Emotion2Score.loc[Sadl2] = otherEmoS1 
    SadData2.Emotion2Name.loc[Sadl2] = otherEmoN1
    SadData2.Emotion3Score.loc[Sadl3] = otherEmoS2 
    SadData2.Emotion3Name.loc[Sadl3] = otherEmoN2
    SadData2.Emotion4Score.loc[Sadl4] = otherEmoS3 
    SadData2.Emotion4Name.loc[Sadl4] = otherEmoN3
    SadData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



SatisfactionData2 = SatisfactionData
SatisfactionData2Loc = SatisfactionData2.columns[SatisfactionData2.isin(['Satisfaction']).any()]
if len(SatisfactionData2Loc) == 1:
    SatisfactionData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(SatisfactionData2Loc) == 2:
    Satisfactionl1 = SatisfactionData2.index[SatisfactionData2['Emotion1Name'] == 'Satisfaction']
    Satisfactionl2 = SatisfactionData2.index[SatisfactionData2['Emotion2Name'] == 'Satisfaction']
    Satisfaction1 = SatisfactionData2.Emotion1Score.loc[Satisfactionl1]
    Satisfaction2 = SatisfactionData2.Emotion2Score.loc[Satisfactionl2]
    otherEmoS = SatisfactionData2.Emotion1Score.loc[Satisfactionl2]
    otherEmoN = SatisfactionData2.Emotion1Name.loc[Satisfactionl2]
    SatisfactionData2.Emotion1Score.loc[Satisfactionl2] = Satisfaction2
    SatisfactionData2.Emotion1Name.loc[Satisfactionl2] = SatisfactionData2.Emotion2Name.loc[Satisfactionl2]
    SatisfactionData2.Emotion2Score.loc[Satisfactionl2] = otherEmoS 
    SatisfactionData2.Emotion2Name.loc[Satisfactionl2] = otherEmoN
    SatisfactionData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    SatisfactionData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(SatisfactionData2Loc) == 3:
    Satisfactionl1 = SatisfactionData2.index[SatisfactionData2['Emotion1Name'] == 'Satisfaction']
    Satisfactionl2 = SatisfactionData2.index[SatisfactionData2['Emotion2Name'] == 'Satisfaction']
    Satisfactionl3 = SatisfactionData2.index[SatisfactionData2['Emotion3Name'] == 'Satisfaction']
    
    Satisfaction1 = SatisfactionData2.Emotion1Score.loc[Satisfactionl1]
    Satisfaction2 = SatisfactionData2.Emotion2Score.loc[Satisfactionl2]
    Satisfaction3 = SatisfactionData2.Emotion3Score.loc[Satisfactionl3]
    
    otherEmoS1 = SatisfactionData2.Emotion1Score.loc[Satisfactionl2]
    otherEmoN1 = SatisfactionData2.Emotion1Name.loc[Satisfactionl2]
    otherEmoS2 = SatisfactionData2.Emotion2Score.loc[Satisfactionl3]
    otherEmoN2 = SatisfactionData2.Emotion2Name.loc[Satisfactionl3]
    SatisfactionData2.Emotion1Score.loc[Satisfactionl3] = Satisfaction3
    SatisfactionData2.Emotion1Name.loc[Satisfactionl3] = SatisfactionData2.Emotion3Name.loc[Satisfactionl3]
    SatisfactionData2.Emotion2Score.loc[Satisfactionl2] = otherEmoS1 
    SatisfactionData2.Emotion2Name.loc[Satisfactionl2] = otherEmoN1
    SatisfactionData2.Emotion3Score.loc[Satisfactionl3] = otherEmoS2 
    SatisfactionData2.Emotion3Name.loc[Satisfactionl3] = otherEmoN2
    SatisfactionData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    SatisfactionData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(SatisfactionData2Loc) == 4:
    Satisfactionl1 = SatisfactionData2.index[SatisfactionData2['Emotion1Name'] == 'Satisfaction']
    Satisfactionl2 = SatisfactionData2.index[SatisfactionData2['Emotion2Name'] == 'Satisfaction']
    Satisfactionl3 = SatisfactionData2.index[SatisfactionData2['Emotion3Name'] == 'Satisfaction']
    Satisfactionl4 = SatisfactionData2.index[SatisfactionData2['Emotion4Name'] == 'Satisfaction']
    
    Satisfaction1 = SatisfactionData2.Emotion1Score.loc[Satisfactionl1]
    Satisfaction2 = SatisfactionData2.Emotion2Score.loc[Satisfactionl2]
    Satisfaction3 = SatisfactionData2.Emotion3Score.loc[Satisfactionl3]
    Satisfaction4 = SatisfactionData2.Emotion4Score.loc[Satisfactionl4]
    
    otherEmoS1 = SatisfactionData2.Emotion1Score.loc[Satisfactionl2]
    otherEmoN1 = SatisfactionData2.Emotion1Name.loc[Satisfactionl2]
    otherEmoS2 = SatisfactionData2.Emotion2Score.loc[Satisfactionl3]
    otherEmoN2 = SatisfactionData2.Emotion2Name.loc[Satisfactionl3]
    otherEmoS3 = SatisfactionData2.Emotion3Score.loc[Satisfactionl4]
    otherEmoN3 = SatisfactionData2.Emotion3Name.loc[Satisfactionl4]
    
    SatisfactionData2.Emotion1Score.loc[Satisfactionl3] = Satisfaction3
    SatisfactionData2.Emotion1Name.loc[Satisfactionl3] = SatisfactionData2.Emotion3Name.loc[Satisfactionl3]
    SatisfactionData2.Emotion2Score.loc[Satisfactionl2] = otherEmoS1 
    SatisfactionData2.Emotion2Name.loc[Satisfactionl2] = otherEmoN1
    SatisfactionData2.Emotion3Score.loc[Satisfactionl3] = otherEmoS2 
    SatisfactionData2.Emotion3Name.loc[Satisfactionl3] = otherEmoN2
    SatisfactionData2.Emotion4Score.loc[Satisfactionl4] = otherEmoS3 
    SatisfactionData2.Emotion4Name.loc[Satisfactionl4] = otherEmoN3
    SatisfactionData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



ShameData2 = ShameData
ShameData2Loc = ShameData2.columns[ShameData2.isin(['Shame']).any()]
if len(ShameData2Loc) == 1:
    ShameData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(ShameData2Loc) == 2:
    Shamel1 = ShameData2.index[ShameData2['Emotion1Name'] == 'Shame']
    Shamel2 = ShameData2.index[ShameData2['Emotion2Name'] == 'Shame']
    Shame1 = ShameData2.Emotion1Score.loc[Shamel1]
    Shame2 = ShameData2.Emotion2Score.loc[Shamel2]
    otherEmoS = ShameData2.Emotion1Score.loc[Shamel2]
    otherEmoN = ShameData2.Emotion1Name.loc[Shamel2]
    ShameData2.Emotion1Score.loc[Shamel2] = Shame2
    ShameData2.Emotion1Name.loc[Shamel2] = ShameData2.Emotion2Name.loc[Shamel2]
    ShameData2.Emotion2Score.loc[Shamel2] = otherEmoS 
    ShameData2.Emotion2Name.loc[Shamel2] = otherEmoN
    ShameData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    ShameData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(ShameData2Loc) == 3:
    Shamel1 = ShameData2.index[ShameData2['Emotion1Name'] == 'Shame']
    Shamel2 = ShameData2.index[ShameData2['Emotion2Name'] == 'Shame']
    Shamel3 = ShameData2.index[ShameData2['Emotion3Name'] == 'Shame']
    
    Shame1 = ShameData2.Emotion1Score.loc[Shamel1]
    Shame2 = ShameData2.Emotion2Score.loc[Shamel2]
    Shame3 = ShameData2.Emotion3Score.loc[Shamel3]
    
    otherEmoS1 = ShameData2.Emotion1Score.loc[Shamel2]
    otherEmoN1 = ShameData2.Emotion1Name.loc[Shamel2]
    otherEmoS2 = ShameData2.Emotion2Score.loc[Shamel3]
    otherEmoN2 = ShameData2.Emotion2Name.loc[Shamel3]
    ShameData2.Emotion1Score.loc[Shamel3] = Shame3
    ShameData2.Emotion1Name.loc[Shamel3] = ShameData2.Emotion3Name.loc[Shamel3]
    ShameData2.Emotion2Score.loc[Shamel2] = otherEmoS1 
    ShameData2.Emotion2Name.loc[Shamel2] = otherEmoN1
    ShameData2.Emotion3Score.loc[Shamel3] = otherEmoS2 
    ShameData2.Emotion3Name.loc[Shamel3] = otherEmoN2
    ShameData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    ShameData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(ShameData2Loc) == 4:
    Shamel1 = ShameData2.index[ShameData2['Emotion1Name'] == 'Shame']
    Shamel2 = ShameData2.index[ShameData2['Emotion2Name'] == 'Shame']
    Shamel3 = ShameData2.index[ShameData2['Emotion3Name'] == 'Shame']
    Shamel4 = ShameData2.index[ShameData2['Emotion4Name'] == 'Shame']
    
    Shame1 = ShameData2.Emotion1Score.loc[Shamel1]
    Shame2 = ShameData2.Emotion2Score.loc[Shamel2]
    Shame3 = ShameData2.Emotion3Score.loc[Shamel3]
    Shame4 = ShameData2.Emotion4Score.loc[Shamel4]
    
    otherEmoS1 = ShameData2.Emotion1Score.loc[Shamel2]
    otherEmoN1 = ShameData2.Emotion1Name.loc[Shamel2]
    otherEmoS2 = ShameData2.Emotion2Score.loc[Shamel3]
    otherEmoN2 = ShameData2.Emotion2Name.loc[Shamel3]
    otherEmoS3 = ShameData2.Emotion3Score.loc[Shamel4]
    otherEmoN3 = ShameData2.Emotion3Name.loc[Shamel4]
    
    ShameData2.Emotion1Score.loc[Shamel3] = Shame3
    ShameData2.Emotion1Name.loc[Shamel3] = ShameData2.Emotion3Name.loc[Shamel3]
    ShameData2.Emotion2Score.loc[Shamel2] = otherEmoS1 
    ShameData2.Emotion2Name.loc[Shamel2] = otherEmoN1
    ShameData2.Emotion3Score.loc[Shamel3] = otherEmoS2 
    ShameData2.Emotion3Name.loc[Shamel3] = otherEmoN2
    ShameData2.Emotion4Score.loc[Shamel4] = otherEmoS3 
    ShameData2.Emotion4Name.loc[Shamel4] = otherEmoN3
    ShameData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



SurpriseData2 = SurpriseData
SurpriseData2Loc = SurpriseData2.columns[SurpriseData2.isin(['Surprise']).any()]
if len(SurpriseData2Loc) == 1:
    SurpriseData2.drop(columns = ['Emotion2Name', 'Emotion2Score', 'Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
elif len(SurpriseData2Loc) == 2:
    Surprisel1 = SurpriseData2.index[SurpriseData2['Emotion1Name'] == 'Surprise']
    Surprisel2 = SurpriseData2.index[SurpriseData2['Emotion2Name'] == 'Surprise']
    Surprise1 = SurpriseData2.Emotion1Score.loc[Surprisel1]
    Surprise2 = SurpriseData2.Emotion2Score.loc[Surprisel2]
    otherEmoS = SurpriseData2.Emotion1Score.loc[Surprisel2]
    otherEmoN = SurpriseData2.Emotion1Name.loc[Surprisel2]
    SurpriseData2.Emotion1Score.loc[Surprisel2] = Surprise2
    SurpriseData2.Emotion1Name.loc[Surprisel2] = SurpriseData2.Emotion2Name.loc[Surprisel2]
    SurpriseData2.Emotion2Score.loc[Surprisel2] = otherEmoS 
    SurpriseData2.Emotion2Name.loc[Surprisel2] = otherEmoN
    SurpriseData2.drop(columns = ['Emotion3Name', 'Emotion3Score', 'Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    SurpriseData2.drop(columns = [ 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)

elif len(SurpriseData2Loc) == 3:
    Surprisel1 = SurpriseData2.index[SurpriseData2['Emotion1Name'] == 'Surprise']
    Surprisel2 = SurpriseData2.index[SurpriseData2['Emotion2Name'] == 'Surprise']
    Surprisel3 = SurpriseData2.index[SurpriseData2['Emotion3Name'] == 'Surprise']
    
    Surprise1 = SurpriseData2.Emotion1Score.loc[Surprisel1]
    Surprise2 = SurpriseData2.Emotion2Score.loc[Surprisel2]
    Surprise3 = SurpriseData2.Emotion3Score.loc[Surprisel3]
    
    otherEmoS1 = SurpriseData2.Emotion1Score.loc[Surprisel2]
    otherEmoN1 = SurpriseData2.Emotion1Name.loc[Surprisel2]
    otherEmoS2 = SurpriseData2.Emotion2Score.loc[Surprisel3]
    otherEmoN2 = SurpriseData2.Emotion2Name.loc[Surprisel3]
    SurpriseData2.Emotion1Score.loc[Surprisel3] = Surprise3
    SurpriseData2.Emotion1Name.loc[Surprisel3] = SurpriseData2.Emotion3Name.loc[Surprisel3]
    SurpriseData2.Emotion2Score.loc[Surprisel2] = otherEmoS1 
    SurpriseData2.Emotion2Name.loc[Surprisel2] = otherEmoN1
    SurpriseData2.Emotion3Score.loc[Surprisel3] = otherEmoS2 
    SurpriseData2.Emotion3Name.loc[Surprisel3] = otherEmoN2
    SurpriseData2.drop(columns = ['Emotion4Name', 'Emotion4Score'], axis=1, inplace=True)
    SurpriseData2.drop(columns = [ 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)
    
elif len(SurpriseData2Loc) == 4:
    Surprisel1 = SurpriseData2.index[SurpriseData2['Emotion1Name'] == 'Surprise']
    Surprisel2 = SurpriseData2.index[SurpriseData2['Emotion2Name'] == 'Surprise']
    Surprisel3 = SurpriseData2.index[SurpriseData2['Emotion3Name'] == 'Surprise']
    Surprisel4 = SurpriseData2.index[SurpriseData2['Emotion4Name'] == 'Surprise']
    
    Surprise1 = SurpriseData2.Emotion1Score.loc[Surprisel1]
    Surprise2 = SurpriseData2.Emotion2Score.loc[Surprisel2]
    Surprise3 = SurpriseData2.Emotion3Score.loc[Surprisel3]
    Surprise4 = SurpriseData2.Emotion4Score.loc[Surprisel4]
    
    otherEmoS1 = SurpriseData2.Emotion1Score.loc[Surprisel2]
    otherEmoN1 = SurpriseData2.Emotion1Name.loc[Surprisel2]
    otherEmoS2 = SurpriseData2.Emotion2Score.loc[Surprisel3]
    otherEmoN2 = SurpriseData2.Emotion2Name.loc[Surprisel3]
    otherEmoS3 = SurpriseData2.Emotion3Score.loc[Surprisel4]
    otherEmoN3 = SurpriseData2.Emotion3Name.loc[Surprisel4]
    
    SurpriseData2.Emotion1Score.loc[Surprisel3] = Surprise3
    SurpriseData2.Emotion1Name.loc[Surprisel3] = SurpriseData2.Emotion3Name.loc[Surprisel3]
    SurpriseData2.Emotion2Score.loc[Surprisel2] = otherEmoS1 
    SurpriseData2.Emotion2Name.loc[Surprisel2] = otherEmoN1
    SurpriseData2.Emotion3Score.loc[Surprisel3] = otherEmoS2 
    SurpriseData2.Emotion3Name.loc[Surprisel3] = otherEmoN2
    SurpriseData2.Emotion4Score.loc[Surprisel4] = otherEmoS3 
    SurpriseData2.Emotion4Name.loc[Surprisel4] = otherEmoN3
    SurpriseData2.drop(columns = ['Component2Name', 'Component2Type', 'Component2Score', 'Component3Name', 'Component3Type', 'Component3Score', 'Component4Name', 'Component4Score', 'Component4Type'], axis=1, inplace=True)



#md = smf.mixedlm("ItemScore ~ TimeDur  +  SessionNum +ClipNum +C(ItemName) + C(MovieName)", allData, groups=allData["SubjectNum"])
#mdf2 =md2.fit()
#print(mdf2.summary())
#
#muByEmotion = allData.groupby(['ItemName'])['ItemScore'].mean()
#varByEmotion = allData.groupby(['ItemName'])['ItemScore'].var()
#
#muByComponent = allData.groupby(['Component'])['ItemScore'].mean()
#varByComponent = allData.groupby(['Component'])['ItemScore'].var()
#
#muByEmotionByMovie = allData.groupby(['ItemName', 'MovieName'])['ItemScore'].mean()
#varByEmotionByMovie = allData.groupby(['ItemName', 'MovieName'])['ItemScore'].var()
#
#muByComponentByMovie = allData.groupby(['Component', 'MovieName'])['ItemScore'].mean()
#varByComponentByMovie = allData.groupby(['Component', 'MovieName'])['ItemScore'].var()
#
#redData = allData.loc[allData['Component'] == 'Emotion']
#
#muByEByMMainEmo = pd.DataFrame(redData.groupby(['MovieName', 'ItemName'])['ItemScore'].mean())
#varByEByMMainEmo  = pd.DataFrame(redData.groupby(['MovieName', 'ItemName'])['ItemScore'].var())
#
#muByEByMMainEmo = muByEByMMainEmo.reset_index()
#varByEByMMainEmo = varByEByMMainEmo.reset_index()
#
#muByEByMMainEmoMax = pd.DataFrame(columns=['MovieName','ItemName','ItemScore'])
#varByEByMMainEmoMax = pd.DataFrame(columns=['MovieName','ItemName','ItemScore'])
#
#for i in range(1, len(muByEByMMainEmo), 13):
#    a = muByEByMMainEmo.loc[i:i +12,:]
#    m = a.ItemScore.idxmax()
#    muByEByMMainEmoMax.loc[i, 'MovieName'] = muByEByMMainEmo.loc[i,'MovieName']
#    muByEByMMainEmoMax.loc[i, 'ItemName'] = a.loc[m,'ItemName'] 
#    muByEByMMainEmoMax.loc[i, 'ItemScore'] = a.loc[m,'ItemScore'] 
#    b = varByEByMMainEmo.loc[i:i +12,:]
#    n = b.ItemScore.idxmax()
#    varByEByMMainEmoMax.loc[i, 'MovieName'] = varByEByMMainEmo.loc[i,'MovieName']
#    varByEByMMainEmoMax.loc[i, 'ItemName'] = b.loc[n,'ItemName'] 
#    varByEByMMainEmoMax.loc[i, 'ItemScore'] = b.loc[n,'ItemScore'] 
#    
#
#scaledData = allData
#scaledData.ItemScore = preprocessing.scale(scaledData.ItemScore, with_mean=True)
#scaledData.TimeDur= preprocessing.scale(scaledData.TimeDur, with_mean=True)
#
#
#md = smf.mixedlm("ItemScore ~ TimeDur + C(Component) + SessionNum + ClipNum + C(MovieName)", allData, groups=allData["SubjectNum"])
#mdf =md.fit()
#print(mdf.summary())
#
#md2 = smf.mixedlm("ItemScore ~ TimeDur  +  SessionNum +ClipNum +C(ItemName) + C(MovieName)", allData, groups=allData["SubjectNum"])
#mdf2 =md2.fit()
#print(mdf2.summary())
#
#md3 = smf.mixedlm("ItemScore ~ TimeDur + C(Component) + SessionNum + ClipNum + C(MovieName)", scaledData, groups=scaledData["SubjectNum"])
#mdf3 =md3.fit()
#print(mdf3.summary())
#
#md4 = smf.mixedlm("ItemScore ~ TimeDur  +  SessionNum +ClipNum +C(ItemName) + C(MovieName)", scaledData, groups=scaledData["SubjectNum"])
#mdf4 =md4.fit()
#print(mdf4.summary())
#
#M = pd.Series(allData['MovieName'].unique())
#E = pd.Series(redData['ItemName'].unique())
#
#C = np.zeros((14, 1))
#M1 = redData.loc[redData['MovieName'] == M[0]]
#C[0] = max(M1.ClipNum)
#M2 = redData.loc[redData['MovieName'] == M[1]]
#C[1] = max(M2.ClipNum)
#M3 = redData.loc[redData['MovieName'] == M[2]]
#C[2] = max(M3.ClipNum)
#M4 = redData.loc[redData['MovieName'] == M[3]]
#C[3] = max(M4.ClipNum)
#M5 = redData.loc[redData['MovieName'] == M[4]]
#C[4] = max(M5.ClipNum)
#M6 = redData.loc[redData['MovieName'] == M[5]]
#C[5] = max(M6.ClipNum)
#M7 = redData.loc[redData['MovieName'] == M[6]]
#C[6] = max(M7.ClipNum)
#M8 = redData.loc[redData['MovieName'] == M[7]]
#C[7] = max(M8.ClipNum)
#M9 = redData.loc[redData['MovieName'] == M[8]]
#C[8] = max(M9.ClipNum)
#M10 = redData.loc[redData['MovieName'] == M[9]]
#C[9] = max(M10.ClipNum)
#M11 = redData.loc[redData['MovieName'] == M[10]]
#C[10] = max(M11.ClipNum)
#M12 = redData.loc[redData['MovieName'] == M[11]]
#C[11] = max(M12.ClipNum)
#M13 = redData.loc[redData['MovieName'] == M[12]]
#C[12] = max(M13.ClipNum)
#M14 = redData.loc[redData['MovieName'] == M[13]]
#C[13] = max(M14.ClipNum)
#
#howManyClips = np.sum(C)
#
#cols = {'MovieName', 'ClipNum','C1n', 'C1v','C2n', 'C2v', 'C3n', 'C3v', 'muMax', 'varMax'}
#pcaMainMovieDF = pd.DataFrame(columns = {'MovieName', 'ClipNum','C1n', 'C1v','C2n', 'C2v', 'C3n', 'C3v', 'muMax', 'varMax'})
#from sklearn.decomposition import PCA
#
#for i in range(0,len(M)):
#    print(i)
#    a = redData.loc[redData['MovieName'] == M.loc[i]].reset_index()
#    n = np.max(a.ClipNum)
#    pcaMainMovieDF.MovieName.append =  M.loc[i]
#    for j in range(1,n):
#        b = a.loc[a['ClipNum'] == j].reset_index();
#        pcaMainMovieDF.ClipNum.append =  j
#        grpMu = pd.DataFrame(b.groupby(['ItemName'])['ItemScore'].mean().reset_index())
#        em = grpMu.ItemScore.idxmax()
#        muMaxEm =grpMu.ItemName.loc[em]
#        grpVar =pd.DataFrame(b.groupby(['ItemName'])['ItemScore'].var().reset_index())
#        ev = grpVar.ItemScore.idxmax()
#        varMaxEm =grpVar.ItemName.loc[ev]
#        
#        #varMaxEm = float('NaN')
#        c = b.pivot(index = None, columns= "ItemName", values = ["ItemScore"])
#        c = c.droplevel(0, axis = 1)
#        d = c
#        for k in range(0, 13):
#            d.iloc[:,k] = np.sort(np.array(c.iloc[:,k]), axis = None)
#        c = d.dropna()
#        print('The length of Clip ' + repr(j) + ' in ' + repr(M.loc[i]) + ' data set is ' + repr(len(c)) + ' .')
#        cPCA = PCA()
#        cPCA.fit(c)
#        if np.count_nonzero(cPCA.components_) >1:
#            TopComponents = np.abs(cPCA.components_[1]).argsort()[::-1]
#            print('The top 3 components are ' + repr(c.columns[TopComponents[0]]) + ' , ' + repr(c.columns[TopComponents[1]]) + ' , ' + repr(c.columns[TopComponents[2]]) + ' . ')
#            C1n= c.columns[TopComponents[0]]
#            C2n= c.columns[TopComponents[1]]
#            C3n = c.columns[TopComponents[2]]
#            
#            cPCA_Var = cPCA.explained_variance_ratio_
#            cPCA_Varp = cPCA.explained_variance_ratio_*100
#            C1v = cPCA_Varp[0]
#            
#            if cPCA_Varp[1] > 1:
#                C2v = cPCA_Varp[1]
#            else:
#                C2v =float("NaN")
#            if len(cPCA_Varp) > 2:
#                C3v = cPCA_Varp[2]
#            else:
#                C3v = float("NaN")
#                
#                
#            pcaMainMovieDF = pcaMainMovieDF.append({'MovieName': M.loc[i], 'ClipNum':j, 'C1n': C1n,'C1v': C1v,'C2n': C2n, 'C2v': C2v, 'C3n': C3n, 'C3v': C3v, 'varMax': varMaxEm, 'muMax': muMaxEm}, ignore_index=True)       
#            pcaMainMovieDF.columns = cols
#            cPCA_var = cPCA.explained_variance_ratio_.cumsum()
#
#            plt.ylabel('%Variance explained.')
#            plt.xlabel('# of features')
#            plt.title('PCA Analysis for Emotions Indices')
#            #plt.ylim(30,100.5)
#            plt.plot(cPCA_Var)
#
#            
#        else:
#            print("Flag problem in " + repr(M.loc[i]))
#            time.sleep(5)
#            continue
#        
