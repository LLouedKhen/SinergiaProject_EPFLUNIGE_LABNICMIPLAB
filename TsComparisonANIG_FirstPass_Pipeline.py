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
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn import linear_model
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
import seaborn as sns
from dtw import *
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error


mainPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/'
TsPathR = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison'
TsPath = '/media/miplab-nas2/Data2/Movies_Emo/Leyla/TsComparison/Movies'
Movies = ['AfterTheRain', 'BetweenViewings', 'BigBuckBunny', 'Chatter', 'FirstBite', 'LessonLearned', 'Payload', 'Sintel', 'Spaceman', 'TearsOfSteel', 'TheSecretNumber', 'ToClaireFromSonny', 'YouAgain']
Emotions = ['Anger', 'Anxiety', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Love', 'Sad', 'Satisfaction', 'Surprise']

relCond = [Movies, Emotions]
tests = ['Corr', 'DTW', 'GLM', 'ClassACCRF', 'ClassACCRFW', 'ClassRFR2']
mix = pd.MultiIndex.from_product(relCond)
chkMeth = pd.DataFrame(columns = tests, index = mix)


annotRegs =  glob.glob('DF_*')
imRegs = glob.glob('ScaledRegressors*')

MovieEmotionBestImp = []
MovieEmotionBestDTW = []
os.chdir(TsPath)
allALLGLMs = pd.DataFrame()

for m in Movies:
        thisPath = os.path.join(TsPath,  m)
        os.chdir(m)
        for em in Emotions:
                os.chdir(em)
                thisPath2 = os.path.join(thisPath, em)
                annotRegs =  glob.glob('DF_*')
                imRegs = glob.glob('ScaledRegressors*')
                imEm1 = pd.DataFrame(columns = {'Start', 'Dur', 'Off'})
                imEm2 = pd.DataFrame(columns = { em + '_Mu'})
                cn = em + '_Mu'
                imEm3 = pd.DataFrame()
                for imgF in imRegs:
                    thisR = pd.read_csv(imgF)
                    cl = thisR.Clip
                    maxR = cl.idxmax()
                    keep1 = thisR.iloc[0:maxR, :]
                    imEm1.Start = keep1.Start
                    imEm1.Dur = keep1.Dur
                    imEm1.Off = keep1.Start + keep1.Dur
                    imEm2.loc[:,0] = np.zeros(len(keep1.Dur))
                    keep2 = keep1.ES
                    imEm3 = pd.concat([imEm3, keep2], axis = 1)
                imEm2 = imEm3.mean(axis = 1)
                fEm = pd.concat([imEm1, imEm2], axis = 1)
                n = fEm.columns[3]
                fEm = fEm.rename(columns = {n: cn})
                aReg = pd.read_csv(annotRegs[0])
                aEm = pd.DataFrame()
                aReg = aReg.iloc[:, 1:]
                aEm = aReg.mean(axis = 1)
                
                afEm = pd.DataFrame()
                afEm.loc[:,0] = np.zeros(len(aEm)) 
                afEm.loc[:,0] = np.nan
                idx = fEm.Off
                afEm.iloc[idx,0] = fEm.iloc[:,3]
                
                os.chdir('/home/loued/Figures')
                if em == 'Fear' and m == 'LessonLearned' or em == 'Anxiety' and m == 'LessonLearned' or em == 'Happiness' and m == 'AfterTheRain':
                    fig1 = plt.figure()
                    plt.plot(range(len(afEm)), np.array(afEm), marker = '.')
                    plt.plot(range(len(afEm)), np.array(aEm))
                    plt.title('Ts Comparison, Study 1/Study 2, ' + m + ' ' + em)
                    plt.legend('Study 1', 'Study 2')
                    plt.xlabel('t')
                    plt.ylabel('Rating')                    
                    plt.savefig('RawTs_' + m + '_' + em + '.png')
                    
                os.chdir(thisPath2)
                #Fill in missing data
                #ewm
                test1 = afEm.ewm(span=3, adjust=False).mean()
                
                #spline
                test2 = afEm
                test2a = test2.interpolate(method = 'spline', order = 1)
                test2b = test2.interpolate(method = 'spline', order = 2)
                test2c = test2.interpolate(method = 'spline', order = 3)
                test2d = test2.interpolate(method = 'spline', order = 4)
                test2e = test2.interpolate(method = 'spline', order = 5)                
                
                
                
                #KNN
                # Define scaler to set values between 0 and 1
                test3 = afEm
#                scaler = MinMaxScaler(feature_range=(0, 1))
#                test3= pd.DataFrame(scaler.fit_transform(test3))
                # Define KNN imputer and fill missing values
                knn_imputer = KNNImputer(n_neighbors=3, weights='uniform', metric='nan_euclidean')
                test3= pd.DataFrame(knn_imputer.fit_transform(test3))
                
                #MICE
                test4 = afEm
                mice_imputer = IterativeImputer(estimator=linear_model.BayesianRidge(), n_nearest_features=None, imputation_order='ascending')
                test4 = pd.DataFrame(mice_imputer.fit_transform(test4))
                
                #save ts
                outputSave = os.path.join(TsPathR, 'TS_MeanScaledImputed')
                os.chdir(outputSave)
                
                aEm.name = 'MuRatingZ'
                filen1 = 'Mean_An_' + m + '_' + em + '.csv' 
                aEm.to_csv(filen1)
                
                test1.name = 'MuRatingZEWMA'
                filen2 = 'Mean_Im_EWMA_' + m + '_' + em + '.csv' 
                test1.to_csv(filen2)
                
                os.chdir('/home/loued/Figures')
                if em == 'Fear' and m == 'LessonLearned' or em == 'Anxiety' and m == 'LessonLearned' or em == 'Happiness' and m == 'AfterTheRain':
                    fig2 = plt.figure()
                    plt.plot(range(len(afEm)), np.array(test1), marker = '.')
                    plt.plot(range(len(afEm)), np.array(aEm))
                    plt.title('Ts Comparison, Study 1/Study 2, ' + m + ' ' + em)
                    plt.legend('Study 1', 'Study 2')
                    plt.xlabel('t')
                    plt.ylabel('Rating')
                    plt.savefig('ImputedEWMA_' + m + '_' + em + '.png')
                
                os.chdir(thisPath2)
                             
                #how good is the test data?
                
                #first, simple correlation 
                allVis = pd.concat([test1, test2a, test2b, test2c, test2d, test2e, test3, test4,aEm], axis = 1)
                labels = ['EWMA', 'Spline1', 'Spline2', 'Spline3', 'Spline4', 'Spline5', 'KNN3', 'MICE', 'TruTru']
                ax = plt.plot(allVis, label = labels)
                plt.legend(loc ='center left', bbox_to_anchor=(1, 0.5))
                plt.show()
                
                CorrMat = allVis.corr()
                CorrMat.index = labels
                bestFill = CorrMat.iloc[:-1,8].idxmax()
                print('The best fit for movie ' + m + ' and emotion ' + em + 'is ' + bestFill)
                chkMeth.loc[m, em]['Corr'] = bestFill
                MovieEmotionBestImp.append([m, em, bestFill])
                
                hmp1 = sns.heatmap(allVis, cmap= 'viridis')
                os.chdir('/home/loued/Figures')
                if em == 'Fear' and m == 'LessonLearned' or em == 'Anxiety' and m == 'LessonLearned' or em == 'Happiness' and m == 'AfterTheRain':
#                    fig3 = plt.figure()
                    plt.savefig(em + '_' + m + 'hmap.png')
                os.chdir(thisPath2)    
                fvi= allVis.iloc[:,0:-3].first_valid_index()
                
                
                #Next, dynamic time warping 
                remNan = allVis.iloc[fvi:, :]
                testC = remNan.iloc[:,:-1]
                TT=  remNan.iloc[:,8]
                dtwDist = pd.DataFrame(columns = labels[:-1])
            
                dtwDist.loc[0,:] = np.zeros([len(labels)-1])
                
                
                for i in range(testC.shape[1]):
                    impM = labels[i]
                    test1C = testC.iloc[:,i]
                    alignment = dtw(test1C ,TT)
                   # alignment.plot(type= 'threeway')
                    dtwO = dtw(test1C, TT)
                    dtwDistThis = dtwO.distance
                    dtwDist[impM]= dtwDistThis
                bestFill2 = dtwDist.idxmin(axis = 1).loc[0]
                print('The best fit DTW for movie ' + m + ' and emotion ' + em + ' is ' + bestFill2)
                chkMeth.loc[m, em]['DTW'] = bestFill2
                MovieEmotionBestDTW.append([m, em, bestFill2])
                
                #Next, GLM to get statistics 
                
                testC2 = pd.concat([testC, TT], axis = 1)
                testC2.columns = labels
                glm = smf.glm("TruTru ~ EWMA + Spline1 + Spline2 + Spline3 + Spline4 + Spline5 + KNN3 + MICE", testC2 )
                glm_results = glm.fit()
                print(glm_results.summary())
                z = glm_results.tvalues
                p = glm_results.pvalues
                allV = pd.concat([z, p], axis = 1)
                allV = allV.iloc[1:,:]
                allV.columns = ['z', 'p']
                
                allV = allV[allV.p < 0.05]
                winner = allV.z.idxmax()
                
                allALLGLMs  = pd.concat([allALLGLMs, allV], axis = 1)
                
                print('The best fit based on GLM for movie ' + m + ' and emotion ' + em + ' is ' + winner )
                chkMeth.loc[m, em]['GLM'] = winner
                
                
                                
#                #Now, try with simple ML 
#                deg = 2
#                polyreg = make_pipeline(PolynomialFeatures(deg), LinearRegression(fit_intercept = False))
#                linreg = LinearRegression()
#                
#                ClassDF = pd.DataFrame(columns = ['lin', 'poly'], index = labels[:-1])
#                for i in range(testC.shape[1]):
#                    impM = labels[i]
#                    y = TT
#                    x = np.array(testC.iloc[:,i])
#                    X = x.reshape(-1,1)
#                    score = 'r2'
#                    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle = False)
#                    polyscores = cross_validate(polyreg, X_train, y_train, scoring= score, return_estimator = True)
#                    linscores = cross_validate(linreg, X_train, y_train, scoring= score, return_estimator = True)
#                    
#                    print('The GLM score for movie ' + m + ' and emotion ' + em + ' and method ' + impM +  ' is ' + str(linscores['test_score'].mean()))
#                    ClassDF.lin[impM] = linscores['test_score'].mean()
#                    
#                    print('The poly score for movie ' + m + ' and emotion ' + em + ' and method ' + impM +  ' is ' + str(polyscores['test_score'].mean()))
#                    ClassDF.poly[impM] = polyscores['test_score'].mean()
#                    
#                    print('The score difference for movie ' + m + ' and emotion ' + em + ' and method ' + impM +  ' is ' + str(linscores['test_score'].mean() - polyscores['test_score'].mean()))
#                
#                chkMeth.loc[m, em]['Classification R2 Lin'] = pd.to_numeric(ClassDF['lin']).idxmax()
#                chkMeth.loc[m, em]['Classification R2 Poly (2)'] = pd.to_numeric(ClassDF['poly']).idxmax()
#                
                #what was that? Try random forest classification
                
                from sklearn.ensemble import RandomForestRegressor
                from sklearn.metrics import accuracy_score
                
                regressor = RandomForestRegressor(n_estimators = 200)
                ClassDFRF = pd.DataFrame(columns = ['RFAccuracy', 'RFR2'], index = labels[:-1])
                for i in range(testC.shape[1]):
                    impM = labels[i]
                    x = np.array(TT).reshape(-1, 1)
                    
                    y = np.array(testC.iloc[:,i])
                   
                    Y = y.reshape(-1,1)
                    regressor.fit(x,Y)
                    Y_pred = regressor.predict(Y)
                    scoreR2 = regressor.score(Y, x)
                    err = abs(Y_pred - Y)
                    mape = 100 * (err/Y)
                    accuracy = 100 - np.mean(mape)
                    ClassDFRF.RFAccuracy[impM] = accuracy
                    ClassDFRF.RFR2[impM] = scoreR2
                chkMeth.loc[m, em]['ClassACCRFW'] = pd.to_numeric(ClassDFRF['RFAccuracy']).idxmax()
                chkMeth.loc[m, em]['ClassACCRF'] = pd.to_numeric(ClassDFRF['RFAccuracy']).max()
                chkMeth.loc[m, em]['ClassRFR2'] = pd.to_numeric(ClassDFRF['RFR2']).max()
                    
                
#                chkMeth.loc[m, em]['Classification R2 Lin'] = pd.to_numeric(ClassDF['lin']).idxmax()
#                chkMeth.loc[m, em]['Classification R2 Poly (2)'] = pd.to_numeric(ClassDF['poly']).idxmax()
#                
#                
#                
                    #dtw(test1C, TT, keep_internals = True, step_pattern = rabinerJuangStepPattern(6, 'c')).plot(type = 'twoway', offset = 2)
#                ds = dtw.distance_matrix_fast(np.array(allVis))
#                hmp2 = sns.heatmap(pd.DataFrame(ds), cmap = 'Spectral')
                
                    
                
                os.chdir(thisPath)
        os.chdir(TsPath)
                    
fEWMA =  chkMeth['GLM'].value_counts()['EWMA']
fKNN3 =  chkMeth['GLM'].value_counts()['KNN3']
fSpline1 =  chkMeth['GLM'].value_counts()['Spline1']
fSpline2 =  chkMeth['GLM'].value_counts()['Spline2']
fSpline3  =  chkMeth['GLM'].value_counts()['Spline3']
fSpline4  =  chkMeth['GLM'].value_counts()['Spline4']
fSpline5  =  chkMeth['GLM'].value_counts()['Spline5']
fMICE =  chkMeth['GLM'].value_counts()['MICE']
        


