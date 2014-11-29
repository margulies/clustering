# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/python

import sys, getopt, scipy, h5py
import numpy as np
from myFunctions import fixCort, transformData, runEmbed, recort, kmeans

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hs:f:",["subject=","filename="])
    except getopt.GetoptError:
        print 'embedding.py -s <subject -f <output filebasename>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'embedding.py -s <subject -f <output filebasename>'
            sys.exit()
        elif opt in ("-f", "--filename"):
            filename = arg
        elif opt in ("-s", "--subject"):
            sub = arg
            
    # Import files
    f = h5py.File(('/scr/litauen1/%s.hcp.lh.mat' % sub),'r')
    dataCorr = np.array(f.get('connData'))
    cortex = fixCort(np.array(f.get('cortex')) - 1)
    
    # Run embedding and kmeans
    A = transformData(dataCorr)
    n_components_embedding=50
    embedding = runEmbed(A, n_components_embedding)
    
    for n_components in xrange(2,21):   
        if n_components == 2:
            results = recort(np.squeeze(kmeans(embedding, n_components)), cortex)
        else:
            results = np.vstack((results, recort(np.squeeze(kmeans(embedding, n_components)), cortex)))
    
    scipy.io.savemat(('/scr/litauen1/%s.%s.mat' % sub, filename), {'results':results})


if __name__ == "__main__":
    main(sys.argv[1:])
    

