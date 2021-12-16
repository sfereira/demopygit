
#-------------------------------------------------------------------------------------------#
# Required Libraries                                                                        #
#                                                                                           #
import math                                                                                 #
import numpy as np                                                                          #
import SharedArray as sa                                                                    #
import pandas as pd                                                                         #
#                                                                                           #
#-------------------------------------------------------------------------------------------#
# Reading the shared memory data                                                            #
mls2 = sa.attach("shm://test2")                                                             # Reading the shared memory data [dataframe of all unit flux points after annealing] shared from main file.
msi2 = sa.attach("shm://size2")                                                             # Reading the shared memory data [size of dataframe of all unit flux points after annealing] shared from main file.
                                                                                            #
ttdf1 = mls2.reshape((int(msi2[0]),int(msi2[1])))                                           # Reshaping the flux region dataframe shared array.
                                                                                            #
ttdf1 = pd.DataFrame(ttdf1, columns=['Points','x','y','Point_charges'])                     # Re-defining the unit flux points dataframe.
ttdf1['x'] = pd.to_numeric(ttdf1['x'], downcast="float")                                    # Changing datatype of x-coordinate from 'object' to 'float'.
ttdf1['y'] = pd.to_numeric(ttdf1['y'], downcast="float")                                    # Changing datatype of y-coordinate from 'object' to 'float'.
ttdf1['Point_charges'] = pd.to_numeric(ttdf1['Point_charges'], downcast="float")            # Changing datatype of Point_Charges [no. of unit flux point per partition] from 'object' to 'float'.
                                                                                            #
#-------------------------------------------------------------------------------------------#
def calc_route2(n0, n1):                                                                    # I/P --> n0 -> point-1 label ; --> n1 -> point-2 label.
    p0 = ttdf1[ttdf1['Points']== n0][['x','y']].values[0]                                   # Point-1 coordinates.
    p1 = ttdf1[ttdf1['Points']== n1][['x','y']].values[0]                                   # Point-2 coordinates.
    dist2 = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)                              # Calculate distance between Point-1 and Point-2.
    return dist2                                                                            # Returns value -> distance between two points.
                                                                                            #
#-------------------------------------------------------------------------------------------#
class tsp2():                                                                               #
    def __init__(self, dist_func, close_loop=False):                                        #
        self.dist_func = dist_func                                                          # function defined -> calculate distance.
                                                                                            #
    def dist2(self,point):                                                                  #
        distt = []                                                                          # List to store calculated distance values.
        for k in range(len(point[0])):                                                      #
            p0 = point[0][k]                                                                #
            p1 = point[1][k]                                                                #
            dist2 = self.dist_func(p0,p1)                                                   # Calculate distance between two points.
            distt.append(self.dist_func(p0,p1))                                             # Append the calculated distance.
        return sum(distt)                                                                   # Returns Total distance value for all points pair.
#                                                                                           #                       (between one +ve flux point and one -ve flux point).
#-------------------------------------------------------------------------------------------#
