#---------------------------------------------------------------------------#
# Required Libraries                                                        #
#                                                                           #
import numpy as np                                                          #
from skimage import morphology                                              #
#---------------------------------------------------------------------------#
# Input --> Bz - 2d array of Bz field concentration. [ndarray]              #
#       --> Bz_threshold - Threshold value for filtering. [int]             #
#                                                                           #
# Output --> bz_filtered -> filtered bz field by the threshold. [ndarray]   #
#        --> p -> mask image of +ve regions. [ndarray]                      #
#        --> n -> mask image of -ve regions. [ndarray]                      #
#---------------------------------------------------------------------------#
def filtering(Bz, Bz_thershold):                                            #
    a = np.zeros_like(Bz)                                                   # Create array of shape of the original array.
    p = np.zeros_like(Bz)                                                   # Create array of shape of the original array. (for +ve regions)
    n = np.zeros_like(Bz)                                                   # Create array of shape of the original array. (for -ve regions)
    for i in range(len(Bz)):                                                #
        for j in range(len(Bz[i])):                                         #
            if Bz[i,j] < - Bz_thershold :                                   # Condition for -ve values.
                a[i,j] = -1                                                 #
                n[i,j] = -1                                                 #
                p[i,j] = 0                                                  #
            elif Bz[i,j] > Bz_thershold :                                   # Condition for +ve values.
                a[i,j] = 1                                                  #
                p[i,j] = 1                                                  #
                n[i,j] = 0                                                  #
            else :                                                          #
                a[i,j] = 0                                                  #
                                                                            #
    a1 = np.array(p,bool)                                                   # Array with +ve regions.
    a2 = np.array(n,bool)                                                   # Array with -ve regions.
                                                                            #
    b1 = morphology.remove_small_objects(a1,20,connectivity=2)              # Small regions are removed to reduce error 
    b2 = morphology.remove_small_objects(a2,20,connectivity=2)              # Small regions are removed to reduce error
                                                                            #
    bz_filterd = np.zeros_like(Bz)                                          #
    for i in range(len(p)):                                                 #
        for j in range(len(p[i])):                                          #
            if b1[i,j] == True:                                             # Combining the result of filtering and removing small regions (+ve)
                bz_filterd[i,j] = Bz[i,j]                                   #
            elif b2[i,j] == True:                                           # Combining the result of filtering and removing small regions (-ve)
                bz_filterd[i,j] = Bz[i,j]                                   #
            else:                                                           #
                pass                                                        #
                                                                            #
    return bz_filterd,p,n                                                   # Return --> bz_filtered -> [Filtered Bz fieild by the threshold].
                                                                            #        --> p -> [mask image of +ve regions].
                                                                            #        --> n -> [mask image of -ve regions].
