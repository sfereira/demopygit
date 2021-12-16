
#-----------------------------------------------------------#
# Required Libraries                                        #
#                                                           #
import numpy as np                                          #
#                                                           #
#-----------------------------------------------------------#
def circle(max_radius,r_space):                             # To create circles of desired max. radius and spacing in each radius increment.
    xd = []                                                 # List to store x-coordinate. [of circle]
    yd = []                                                 # List to store y-coordinate. [of circle]
    theta = np.linspace(0, 2 * np.pi, 200)                  # Theta values for points on circle.
    radius = np.linspace(0,max_radius,r_space)              # Radius values for circle.
    for i in (radius):                                      #
        x = i * np.cos(theta) + 300                         # x-coordinate of points in circular path forming circle.
        y = i * np.sin(theta) + 300                         # y-coordinate of points in circular path forming circle.
        xd.append(x)                                        # Append x-coordinate to list.
        yd.append(y)                                        # Append y-coordinate to list.
    return xd, yd                                           # Returns circle in [x,y] coordinates.
#                                                           #
#-----------------------------------------------------------#
