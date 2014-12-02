# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 18:20:12 2014

@author: margulies
"""

import scipy, h5py
from sklearn import manifold
import numpy as np
import nibabel.gifti.giftiio as gio

f = h5py.File('/scr/murg2/HCP_new/HCP_Q1-Q6_GroupAvg_Related440_Unrelated100_v1/HCP_Q1-Q6_R468_rfMRI_groupAvg_left_corr_smoothed2_toR_nifti.mat', 'r')
dataCorr = f.get('dataCorr')
dataCorr = np.array(dataCorr)

gii = gio.read('/scr/murg2/HCP_new/HCP_Q1-Q6_GroupAvg_Related440_Unrelated100_v1/lh.cortex.gii')
structure = gii.darrays[0].data
cortex = np.where(structure != 1)[0]

d = []
for i in cortex:
    d.append(dataCorr[i,cortex])
data = np.array(d)

K = 1 - ((data + 1) / 2.)
tsne = manifold.TSNE(n_components=3, metric='precomputed')
X_tsne = tsne.fit_transform(K)

results = ([0] * 32492) 
count = 0
for i in cortex:
    results[i] = X_tsne[count] + 1
    count = count + 1

scipy.io.savemat(('/scr/litauen1/hcp.lh.tsne.2.mat'), {'results':results})
scipy.io.savemat(('/scr/litauen1/hcp.lh.tsne.3.mat'), {'results':results})