## Required Libraries

import numpy as np
from skimage import morphology

## Input -> Bz - 2d array of Bz field concentration. [ndarray]
##       -> Bz_threshold - Threshold value for filtering.  [int]
##
## Output -> filtered bz field by the threshold.   [ndarray] 
##        -> masked arrays of +ve and -ve regions. [ndarray]

def filtering(Bz, Bz_thershold):
    a = np.zeros_like(Bz)                                           ## create array of size of the original array
    p = np.zeros_like(Bz)                                           ## create array of size of the original array (for positive regions)
    n = np.zeros_like(Bz)                                           ## create array of size of the original array (for negitve regions)
    for i in range(len(Bz)):
        for j in range(len(Bz[i])):
            if Bz[i,j] < - Bz_thershold :                           ## Condition for -ve values
                a[i,j] = -1
                n[i,j] = -1
                p[i,j] = 0
            elif Bz[i,j] > Bz_thershold :                           ## Condition for +ve values
                a[i,j] = 1
                p[i,j] = 1
                n[i,j] = 0
            else :
                a[i,j] = 0


    a1 = np.array(p,bool)                                            ## Array with positive regions
    a2 = np.array(n,bool)                                            ## Array with negative regions

    b1 = morphology.remove_small_objects(a1,20,connectivity=2)       ## small regions are removed to reduce error 
    b2 = morphology.remove_small_objects(a2,20,connectivity=2)       ## small regions are removed to reduce error

    bz_filterd = np.zeros_like(Bz)
    for i in range(len(p)):
        for j in range(len(p[i])):
            if b1[i,j] == True:                                       ## Combining the result of filtering and removing small regions (+ve)
                bz_filterd[i,j] = Bz[i,j]
            elif b2[i,j] == True:                                     ## Combining the result of filtering and removing small regions (-ve)
                bz_filterd[i,j] = Bz[i,j]
            else:
                pass

    return bz_filterd,p,n                                             ## Return -> Filtered Bz fieild by the threshold, and separated mask arrays of +ve and -ve regions 
