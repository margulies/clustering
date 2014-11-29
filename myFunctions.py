# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 21:22:00 2014

@author: margulies
"""
import numpy as np
from sklearn.utils.arpack import eigsh  
from sklearn.cluster import KMeans


def transformData(data):
    K = (data + 1) / 2.  
    v = np.sqrt(np.sum(K, axis=1)) 
    A = K/(v[:, None] * v[None, :])  
    del K
    A = np.squeeze(A * [A > 0])
    return A
    
def runEmbed(data, n_components):
    lambdas, vectors = eigsh(data, k=n_components)   
    lambdas = lambdas[::-1]  
    vectors = vectors[:, ::-1]  
    psi = vectors/vectors[:, 0][:, None]  
    lambdas = lambdas[1:] / (1 - lambdas[1:])  
    embedding = psi[:, 1:(n_components + 1)] * lambdas[:n_components][None, :]  
    #embedding_sorted = np.argsort(embedding[:], axis=1)
    return embedding

def kmeans(embedding, n_components):
    est = KMeans(n_clusters=n_components, n_jobs=-1, init='k-means++', n_init=300)
    est.fit_transform(embedding)
    labels = est.labels_
    data = labels.astype(np.float)
    return data
    
def fixCort(cortex):
    cort = [0] * len(cortex)
    count = 0
    for i in cortex:
        cort[count] = int(i)
        count = count + 1
    return np.squeeze(np.sort(cort))
    
def recort(data, cortex):
    d = ([0] * 32492) 
    count = 0
    for i in cortex:
        d[i] = data[count] + 1
        count = count + 1
    return d

    