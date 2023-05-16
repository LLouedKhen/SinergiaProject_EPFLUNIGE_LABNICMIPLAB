#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:07:17 2022

@author: loued
"""
import glob
import pandas as pd
from nilearn import datasets

imgTemplate = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=1, data_dir=None, base_url=None, resume=True, verbose=1)
from nilearn.image import math_img

angerImgs = glob.glob('Roi*Anger*.nii')

imgs = angerImgs

new_atlas = math_img('img * 0', img=imgTemplate) # initialize new atlas as image full of 0's

for i, img in enumerate(imgs): 
    new_atlas = math_img('i1 + (%d + 1) * i2' %i , i1=new_atlas, i2=img)
# With this, value (i+1) in new_atlas corresponds to the ones of the ith image.