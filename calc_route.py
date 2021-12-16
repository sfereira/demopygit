
#---------------------------------------------------------------------------------------#
# Required Libraries                                                                    #
#                                                                                       #
import math                                                                             #
import numpy as np                                                                      #
import SharedArray as sa                                                                #
import pandas as pd                                                                     #
#                                                                                       #
#---------------------------------------------------------------------------------------#
# Reading the shared memory data                                                        #
mls = sa.attach("shm://test")                                                           # Reading the shared memory data [dataframe of all flux regions] shared from main file.
msi = sa.attach("shm://size")                                                           # Reading the shared memory data [size of dataframe of all flux regions] shared from main file.
                                                                                        #
tdf1 = mls.reshape((int(msi[0]),int(msi[1])))                                           # Reshaping the flux region dataframe shared array.
                                                                                        #
tdf1 = pd.DataFrame(tdf1, columns=['Points','x','y','Point_charges'])                   # Re-defining the flux regions dataframe.
tdf1['x'] = pd.to_numeric(tdf1['x'], downcast="float")                                  # Changing datatype of x-coordinate from 'object' to 'float'.
tdf1['y'] = pd.to_numeric(tdf1['y'], downcast="float")                                  # Changing datatype of y-coordinate from 'object' to 'float'.
tdf1['Point_charges'] = pd.to_numeric(tdf1['Point_charges'], downcast="float")          # Changing datatype of y-coordinate from 'object' to 'float'.
                                                                                        #
#---------------------------------------------------------------------------------------#
def calc_route(n0, n1):                                                                 # I/P --> n0 -> point-1 label ; --> n1 -> point-2 label.
    p0 = tdf1[tdf1['Points']== n0][['x','y']].values[0]                                 # Point-1 coordinates.
    p1 = tdf1[tdf1['Points']== n1][['x','y']].values[0]                                 # Point-2 coordinates.
    dist1 = math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)                          # Calculate distance between Point-1 and Point-2.
    return dist1                                                                        # Returns value -> distance between two points.
                                                                                        #
#---------------------------------------------------------------------------------------#
class tsp():                                                                            #
    def __init__(self, dist_func, close_loop=False):                                    #
        self.dist_func = dist_func                                                      # function defined -> calculate distance.
                                                                                        #
    def dist1(self,point):                                                              #
        dist = []                                                                       # List to store calculated distance values.
        for k in range(len(point[0])):                                                  #
            p0 = point[0][k]                                                            #
            p1 = point[1][k]                                                            #
            dist1 = self.dist_func(p0,p1)                                               # Calculate distance between two points.
            dist.append(self.dist_func(p0,p1))                                          # Append the calculated distance.
        return sum(dist)                                                                # Returns Total distance value of the whole run.
#                                                                                       #
#---------------------------------------------------------------------------------------#
