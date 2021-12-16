
#-----------------------------------------------------------------------------------------------------------#
# Required Libraries                                                                                        #
#                                                                                                           #
import numpy as np                                                                                          #
import sys                                                                                                  #
import pandas as pd                                                                                         #
import SharedArray as sa                                                                                    #
import random                                                                                               #
import math                                                                                                 #
#                                                                                                           #
#-----------------------------------------------------------------------------------------------------------#
def generate_points(center_x, center_y, mean_radius, sigma_radius, num_points):                             #
    points = []                                                                                             # List to store generated boundary points.
    for i in range(num_points):                                                                             # run for loop for number of points defined.
        theta = random.uniform(0, 2*math.pi)                                                                # Theta function to uniformly spaced the point on a circular path.
        radius = mean_radius                                                                                # Radius of the circular path.
        xa = center_x + radius * math.cos(theta)                                                            # x-coordinate of the boundary point.
        ya = center_y + radius * math.sin(theta)                                                            # y-coordinate of the boundary point.
        points.append([xa,ya])                                                                              # Append the coordinates into the list.
    return points                                                                                           # Returns all the boundary points generated.
#                                                                                                           #
#-----------------------------------------------------------------------------------------------------------#
def boundary_points(ppoints,npoints,xp1,xn1,yp1,yn1):                                                       #
                                                                                                            #
    updf = ppoints                                                                                          # +ve unit flux points from the image.
    undf = npoints                                                                                          # -ve unit flux points from the image.
                                                                                                            #
    if len(ppoints) > len(npoints):                                                                         # Condition check if no. of +ve unit flux points are more than -ve unit flux points.
        c = len(ppoints) - len(npoints)                                                                     # diff. between number of +ve and -ve unit flux points.
        ncir = generate_points(1.0, 1.0, 700.0, 0.1, c+10)                                                  # Returns -ve boundary points.
        ncirx = np.asarray(ncir)                                                                            # List to array.
        xb = []                                                                                             # List to store new x coordinates. [original + boundary points]
        yb = []                                                                                             # List to store new y coordinates. [original + boundary points]
        for i in range(len(ncirx)):                                                                         #
            xb1 = ncirx[:,0][i]                                                                             #
            yb1 = ncirx[:,1][i]                                                                             #
            xb.append(xb1)                                                                                  # Append -ve boundary points. [x-coordinate]
            yb.append(yb1)                                                                                  # Append -ve boundary points. [y-coordinate]
        xv = xn1 + xb                                                                                       #
        yv = yn1 + yb                                                                                       #
        nx1 = []                                                                                            # List to store new unit point labels.
        npx = []                                                                                            # List to store unit flux value (for all -> '1.0')
        for i in range(len(xv)):                                                                            #
            nx11 = 'N%s' %i                                                                                 # Generates unit -ve flux points labels.
            npx1 = 1.0                                                                                      # unit point charge.
            nx1.append(nx11)                                                                                #
            npx.append(npx1)                                                                                #
        undf1 = pd.DataFrame({'Points': nx1, 'x': xv, 'y': yv, 'Point_charges':npx}, index=None)            # Create dataframe to store -ve unit flux point info.
        for k in range(len(updf)):                                                                          #
            updf.at[k,'Points']='P%s' %k                                                                    # Update the original dataframe of +ve unit flux point.
        print('#################################################################')                          #
        print('\n')                                                                                         # Print functions
        print(' ********------     Negative Boundary Points     ------********  ')                          #
        print('\n')                                                                                         #
        print('*- Remaining Positive Points Will be Connected to the Boundary -*')                          #
        print('\n')                                                                                         #
        print('#################################################################')                          #
        return updf , undf1                                                                                 # Returns [new -ve unit flux point dataframe] and [original +ve unit flux point dataframe]
    if len(npoints) > len(ppoints):                                                                         # Condition check if no. of -ve unit flux points are more than +ve unit flux points.
        c = len(npoints) - len(ppoints)                                                                     # diff. between number of +ve and -ve unit flux points.
        pcir = generate_points(1.0, 1.0, 700.0, 0.1, c+10)                                                  # Returns +ve boundary points.
        pcirx = np.asarray(pcir)                                                                            # List to array.
        xb = []                                                                                             # List to store new x coordinates. [original + boundary points]
        yb = []                                                                                             # List to store new y coordinates. [original + boundary points]
        for i in range(len(pcirx)):                                                                         #
            xb1 = pcirx[:,0][i]                                                                             #
            yb1 = pcirx[:,1][i]                                                                             #
            xb.append(xb1)                                                                                  # Append +ve boundary points. [x-coordinate]
            yb.append(yb1)                                                                                  # Append +ve boundary points. [y-coordinate]
        xv = xp1 + xb                                                                                       #
        yv = yp1 + yb                                                                                       #
        nx1 = []                                                                                            # List to store new unit point labels.
        npx = []                                                                                            # List to store unit flux value (for all -> '1.0')
        for i in range(len(xv)):                                                                            #
            nx11 = 'P%s' %i                                                                                 # Generates unit +ve flux points labels.
            npx1 = 1.0                                                                                      # unit point charge.
            nx1.append(nx11)                                                                                #
            npx.append(npx1)                                                                                #
        updf1 = pd.DataFrame({'Points': nx1, 'x': xv, 'y': yv, 'Point_charges':npx}, index=None)            # Create dataframe to store +ve unit flux point info.
        for k in range(len(undf)):                                                                          #
            undf.at[k,'Points']='N%s' %k                                                                    # Update the original dataframe of -ve unit flux point.
        print('#################################################################')                          #
        print('\n')                                                                                         #
        print(' ********------     Positive Boundary Points     ------********  ')                          # Print functions
        print('\n')                                                                                         #
        print('*- Remaining Negative Points Will be Connected to the Boundary -*')                          #
        print('\n')                                                                                         #
        print('#################################################################')                          #
        return updf1, undf                                                                                  # Returns [new +ve unit flux point dataframe] and [original -ve unit flux point dataframe]
    if len(npoints) == len(ppoints):                                                                        # Condition check if no. of -ve unit flux points are equal to no. +ve unit flux points.
        print('#################################################################')                          #
        print('\n')                                                                                         #
        print('   ********-------     Flux Is Balanced      -------********     ')                          # Prints
        print('\n')                                                                                         #
        print('#################################################################')                          #
        return 'ignore'                                                                                     # Returns string-{ignore} - No need of boundary points.
#-----------------------------------------------------------------------------------------------------------#
