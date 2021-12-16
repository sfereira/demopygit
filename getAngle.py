
#-------------------------------------------------------------------------------------------------------------------------------#
# Required Libraries                                                                                                            #
#                                                                                                                               #
import numpy as np                                                                                                              #
import math                                                                                                                     #
#                                                                                                                               #
#-------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                               #
def getAngle(a, b, c):                                                                                                          # return angles between three points.
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))                                     #
    if ang < 0 :                                                                                                                # Condition if angle < 0
        return -ang                                                                                                             #              Return -angle.
    elif ang > 180:                                                                                                             # Condition if angle > 180
        return 360 - ang                                                                                                        #              Return 360 - angle.
    else:                                                                                                                       #
        return ang                                                                                                              # else return the angle.
                                                                                                                                #
                                                                                                                                #
def getAngle1(a, b, c):                                                                                                         # return angles between three points.
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))                                     #
    if ang < 0 :                                                                                                                # Condition if angle < 0
        return -ang                                                                                                             #              Return -angle.
    elif ang > 180:                                                                                                             # Condition if angle > 180
        return 360 - ang                                                                                                        #             Return 360 - angle.
    else:                                                                                                                       #
        return ang                                                                                                              #  else return the angle.
#                                                                                                                               #
#-------------------------------------------------------------------------------------------------------------------------------#
                                                                                                                                #
def on_segment(p, q, r):                                                                                                        # returns if the points are on a segment. (check if points lie on line)
    if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):             #
        return True                                                                                                             # True -> points on line.
    return False                                                                                                                # False -> points not on line.
                                                                                                                                #
#-------------------------------------------------------------------------------------------------------------------------------#
                                                                                                                                #
def orientation(p, q, r):                                                                                                       # returns direction of angle calculation between points
    val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))                                                     #
    if val == 0 : return 0                                                                                                      #
    return 1 if val > 0 else -1                                                                                                 #
                                                                                                                                #
#-------------------------------------------------------------------------------------------------------------------------------#
                                                                                                                                #
def intersects(seg1, seg2):                                                                                                     # returns if the flux ropes are intersecting or not.
    p1, q1 = seg1                                                                                                               #
    p2, q2 = seg2                                                                                                               #
                                                                                                                                #
    o1 = orientation(p1, q1, p2)                                                                                                #
    o2 = orientation(p1, q1, q2)                                                                                                #
    o3 = orientation(p2, q2, p1)                                                                                                #
    o4 = orientation(p2, q2, q1)                                                                                                #
                                                                                                                                #
    if o1 != o2 and o3 != o4:                                                                                                   #
                                                                                                                                #
        return True                                                                                                             # True -> Flux ropes are intersecting.
                                                                                                                                #
    if o1 == 0 and on_segment(p1, q1, p2) : return True                                                                         #
    if o2 == 0 and on_segment(p1, q1, q2) : return True                                                                         #
    if o3 == 0 and on_segment(p2, q2, p1) : return True                                                                         #
    if o4 == 0 and on_segment(p2, q2, q1) : return True                                                                         #
    return False                                                                                                                # False -> Flux ropes are non-intersecting.
#                                                                                                                               #
#-------------------------------------------------------------------------------------------------------------------------------#
