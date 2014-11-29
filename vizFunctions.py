# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 21:30:49 2014

@author: margulies
"""
import sys, getopt, scipy, os, h5py, matplotlib
import numpy as np, pylab as pl
from sklearn.utils.arpack import eigsh  
from sklearn.cluster import KMeans
from mayavi.mlab import *
import nibabel.gifti.giftiio as gio
from IPython.core.display import Image as im

def viz(data, vert):
    colors = triangular_mesh(vert[:,0],vert[:,1],vert[:,2], facei, colormap='Set1', scalars=data)
    lut = colors.module_manager.scalar_lut_manager.lut.table.to_array()
    lut[0,:] = [0.1, 0.1, 0.1, 255]
    colors.module_manager.scalar_lut_manager.lut.table = lut
    # figure(bgcolor=(1,1,1))
    draw()
    show()

def concatImages(filename):
    from PIL import Image
    images = map(Image.open, ['med.png', 'lat.png', 'ant.png', 'vent.png', 'dors.png'])
    w = sum(i.size[0] for i in images)
    mh = max(i.size[1] for i in images)

    result = Image.new("RGBA", (w, mh*2))
    x = 0
    count = 0
    for i in images:
        if count < 2:
            result.paste(i, (x, 0))
            x += i.size[0]
            count += 1    
        elif count == 2:
            ima = i.crop(((i.size[0]/4), 0, i.size[0]-(i.size[0]/4), i.size[1]))
            result.paste(ima, (x, 0))
            count += 1
        elif count == 3:
            x = 0
            ima = i.crop((0, (i.size[1]/4), i.size[0], i.size[1]-(i.size[1]/4)))
            result.paste(ima, (x, i.size[1]))
            x += i.size[0]  
            count += 1
        elif count == 4: 
            ima = i.crop((0, (i.size[1]/4), i.size[0], i.size[1]-(i.size[1]/4)))
            result.paste(ima, (x, i.size[1]))
            x += i.size[0]  
    result.save(filename)

def vizAll(data, surf, filename):
    viz(data, surf)
    view(0, 90); show(); savefig('med.png')
    view(180, 90); show(); savefig('lat.png')
    view(90, 180); show(); savefig('vent.png')
    view(90, 0); show(); savefig('dors.png')
    view(90, 90); show(); savefig('ant.png')
    concatImages(filename)