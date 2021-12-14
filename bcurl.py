#-----------------------------------------------------------#
# Required Libraries                                        #
#                                                           #
import numpy as np                                          #
#-----------------------------------------------------------#
# Input --> bx_filt -> Filtered Bx field. [2d-array]        #
#       --> by_filt -> Filtered By field. [2d-array]        #
#       --> bz_filt -> Filtered Bz field. [2d-array]        #
#       --> direction -> ['x','y','z'] -- default -> 'z'    #
#                                                           #
# Output --> zz -> Curl B of desired direction calculated,  #
#                       shape of original array [2d-array]. #
#-----------------------------------------------------------#
def bcurl(bx_filt,by_filt,bz_filt,direction = 'z'):         #
    xx = np.zeros_like(bx_filt)                             # Create Array of shape/size of filtered field. shape -> [nx,ny]
    yy = np.zeros_like(bx_filt)                             # Create Array of shape/size of filtered field. shape -> [nx,ny]
    zz = np.zeros_like(bx_filt)                             # Create Array of shape/size of filtered field. shape -> [nx,ny]
    z1 = np.arange(len(bz_filt[1]))                         # Create Array of size of nx.
    z2 = np.arange(len(bz_filt))                            # Create Array of size of ny.
    for i in range(len(bx_filt)):                           # Length of for loop -> ny.
        for j in range(len(bx_filt[i])):                    # Length of for loop -> nx.
            bx = np.gradient(bx_filt[i,:],z1)               # Return the gradient of filtered Bx field w.r.t. z1.
            by = np.gradient(by_filt[:,j],z2)               # Return the gradient of filtered By field w.r.t. z2.
            bz1 = np.gradient(bz_filt[i,:])                 # Return the gradient of filtered Bz field along y-axis.
            bz2 = np.gradient(bz_filt[:,j])                 # Return the gradient of filtered Bz field along x-axis.
            if direction == 'z':                            # Condition check for direction = 'z'.
                zz[i][j] = bx[j] - by[i]                    # Bcurl_z-component.
            elif direction == 'x':                          # Condition check for direction = 'x'.
                xx[i][j] = bz1[j] - 0                       # Bcurl_x-component.
            elif direction == 'y':                          # Condition check for direction = 'y'.
                yy[i][j] = 0 - bz2[i]                       # Bcurl_y-component.
    if direction == 'z':                                    #
        return zz                                           # Return Bz_curl. [2d-array]
    elif direction == 'x':                                  #
        return xx                                           # Return Bx_curl. [2d-array]
    elif direction == 'y':                                  #
        return yy                                           # Return By_curl. [2d-array]
#-----------------------------------------------------------#
