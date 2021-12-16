
#-------------------------------------------------------------------------------------------------------------------------------#
# Required Libraries                                                                                                            #
#                                                                                                                               #
import numpy as np                                                                                                              #
import pandas as pd                                                                                                             #
import math                                                                                                                     #
import sys                                                                                                                      #
from getAngle import getAngle, getAngle1, on_segment, orientation, intersects                                                   #
#                                                                                                                               #
#-------------------------------------------------------------------------------------------------------------------------------#
# Input --> pc -> list containing +ve point labels after minimizing run.                                                        #
#       --> nc -> list containing -ve point labels after minimizing run.                                                        #
#       --> tdf2 -> datafram consisting info about both the regions.                                                            #
#                    eg.                                                                                                        #
#        Label  Concentration(G)      x          y        Pixel_area  Point_Charges      Flux(Mx)  Total_current   Alpha(m^-1)  #
#         P0         696756.35  106.841760  136.026921      1523.0            8.0  8.723316e+20   1.551761e+21  7.451298e-10    #
#         P1         447806.99  205.785495  219.512768       979.0            5.0  5.606496e+20   1.612203e+21  1.204528e-09    #
#         N0        -226931.93  156.817444  329.849899       986.0            2.0  2.841164e+20  -1.361105e+21 -2.006708e-09    #
#         N1        -122087.09  162.402041  383.314286       490.0            1.0  1.528517e+20  -2.226125e+20 -6.100533e-10    #
#         N2       -1017796.39  227.628788  351.050587      4092.0           11.0  1.274270e+21  -1.298535e+22 -4.268554e-09    #
#                                                                                                                               #
#       --> sha2 -> input to check if Larch calculations is requested. [y or n]                                                 #
#       --> sha3 -> input to check if detail cal. is requested. [y or n]                                                        #
#                                                                                                                               #
# Output --> LLac -> List containing Larch calculations for line 'a' sees 'c'.                                                  #
#        --> LLca -> List containing Larch calculations for line 'c' sees 'a'.                                                  #
#                                                                                                                               #
#-------------------------------------------------------------------------------------------------------------------------------#
def Larch(pc,nc,tdf2,sha2,sha3):                                                                                                #
    print('\t ***---  Completing Larch calculations  ---*** \t')                                                                #
    print('\n')                                                                                                                 #
                                                                                                                                #
    LL_ca = []                                                                                                                  # List to store Larch c->a calculations.
    LL_ac = []                                                                                                                  # List to store Larch a->c calculations.
                                                                                                                                #
    old_stdout = sys.stdout                                                                                                     # Used by the interpreter for standard output.
    log_file = open("message1.log","w")                                                                                         # Open a log file to print the outputs
    sys.stdout = log_file                                                                                                       # Write all the output in the log file till the stdout is running.
    # Angle calculation is between four points. [2 -> +ve points & 2 -> -ve points]                                             #
    # One +ve and -ve points make one flux rope. (line a) ; similarly for line c.                                               #
    for i in range(len(pc)):                                                                                                    #
        for j in range(len(nc)):                                                                                                #
            p0 = tdf2[tdf2['Label']== pc[i]][['x','y']].values[0]                                                               # p0 - 1st +ve point. (line a)
            n0 = tdf2[tdf2['Label']== nc[i]][['x','y']].values[0]                                                               # n0 - 1st -ve point. (line a)
            p1 = tdf2[tdf2['Label']== pc[j]][['x','y']].values[0]                                                               # p1 - 2nd +ve point. (line c)
            n1 = tdf2[tdf2['Label']== nc[j]][['x','y']].values[0]                                                               # n1 - 2nd -ve point. (line c)
            #-------------------------------------------------------------------------------------------------------------------#
            if p0[0] != n0[0]:                                                                                                  #
                f0 = [p0,n0]                                                                                                    # line a [flux rope-1]
                f1 = [p1,n1]                                                                                                    # line c [flux rope-2]
                segment_one = (f0[0], f0[1])                                                                                    #
                segment_two = (f1[0], f1[1])                                                                                    #
                inter = intersects(segment_one, segment_two)                                                                    #  Return 'True' or 'False'. If 'True' -> line a and c intersect orelse they don't.
                #---------------------------------------------------------------------------------------------------------------#
                                                                                                                                #
                # Matching negative footpoints                                                                                  # Common -ve region.
                if f0[1][0] == f1[1][0] and f0[1][1] == f1[1][1]:                                                               # Condition check for matching -ve points (x,y).
                    # Angles in degrees                                                                                         #
                    Angle_phi_ac_deg = getAngle(f0[0],f0[1],f1[0])                                                              # Returns angle between points -> p0-n0-p1 (Here, n0 == n1) [deg]
                    Angle_alpha_c_plus_deg = getAngle(f0[1],f1[0],f0[0])                                                        # Returns angle between points -> n0-p1-p0 (Here, n0 == n1) [deg]
                    Angle_alpha_a_plus_deg = getAngle(f1[1],f0[0],f1[0])                                                        # Returns angle between points -> n0-p0-p1 (Here, n0 == n1) [deg]
                    # Angles in radians                                                                                         #
                    Angle_phi_ac_rad = math.radians(Angle_phi_ac_deg)                                                           # Angles deg to rad.
                    Angle_alpha_c_plus_rad = math.radians(Angle_alpha_c_plus_deg)                                               # Angles deg to rad.
                    Angle_alpha_a_plus_rad = math.radians(Angle_alpha_a_plus_deg)                                               # Angles deg to rad.
                    Angle_alpha_a_minus_rad = 0                                                                                 #
                    Angle_alpha_c_minus_rad = 0                                                                                 #
                    # pi                                                                                                        #
                    z_pi = Angle_phi_ac_rad + Angle_alpha_c_plus_rad + Angle_alpha_a_plus_rad                                   # pi -> total of all the angles calculated.
                    # Error cal.                                                                                                #
                    err_z = (z_pi - math.pi)/math.pi * 100                                                                      # % Error in value of pi --> ( (expri. pi - theor. pi)/theor. pi * 100 )
                                                                                                                                #
                    # Flux tube a 'sees' flux tube c                                                                            #
                    L_ac = 1/(2*math.pi)*(Angle_alpha_a_plus_rad + Angle_alpha_a_minus_rad)                                     # Larch calculations - Flux tube a 'sees' flux tube c.
                    # Flux tube c 'sees' flux tube a                                                                            #
                    L_ca = 1/(2*math.pi)*(Angle_alpha_c_plus_rad + Angle_alpha_c_minus_rad)                                     # Larch calculations - Flux tube c 'sees' flux tube a.
                                                                                                                                #
                    LL_ac.append([L_ac,f0,f1])                                                                                  # Append the Larch_ac value, both flux ropes coords ([x1,y1],[x2,y2]).
                    LL_ca.append([L_ca,f0,f1])                                                                                  # Append the Larch_ca value, both flux ropes coords ([x1,y1],[x2,y2]).
                    #-----------------------------------------------------------------------------------------------------------#
                    if sha2 == 'y':                                                                                             #
                        print('###########################################################')                                    #
                        print('\n')                                                                                             #
                        print('----------Matching negative footpoints----------')                                               #
                        print('\n')                                                                                             #
                        if sha3 == 'y':                                                                                         # if sha3 is 'y' - detail calculations are results are printed
                            print('---------------------------------------------------------')                                  #
                            print('Angle_phi_ac_deg:',Angle_phi_ac_deg)                                                         #
                            print('Angle_alpha_c_plus_deg:',Angle_alpha_c_plus_deg)                                             #
                            print('Angle_alpha_a_plus_deg:',Angle_alpha_a_plus_deg)                                             #
                            print('---------------------------------------------------------')                                  #
                            print('Angle_phi_ac_rad:',Angle_phi_ac_rad)                                                         #
                            print('Angle_alpha_c_plus_rad:',Angle_alpha_c_plus_rad)                                             #
                            print('Angle_alpha_a_plus_rad:',Angle_alpha_a_plus_rad)                                             #
                            print('Angle_alpha_c_minus_rad:',Angle_alpha_c_minus_rad)                                           #
                            print('Angle_alpha_a_minus_rad:',Angle_alpha_a_minus_rad)                                           #
                            print('---------------------------------------------------------')                                  #
                            print('z_pi:',z_pi)                                                                                 #
                            print('% Err_z_pi:',err_z)                                                                          #
                            print('---------------------------------------------------------')                                  #
                        print('Larch_ac:',L_ac)                                                                                 #
                        print('Larch_ca :',L_ca)                                                                                #
                        print('L_ac*L_ca :',L_ac*L_ca)                                                                          #
                        print('\n')                                                                                             #
                        print('###########################################################')                                    #
                #---------------------------------------------------------------------------------------------------------------#
                else: pass                                                                                                      #   if not matching -ve region then pass.
                #---------------------------------------------------------------------------------------------------------------#
                                                                                                                                #
                # Matching positive footpoints                                                                                  # Common +ve region.
                if f0[0][0] == f1[0][0] and f0[0][1] == f1[0][1]:                                                               # Condition check for matching +ve points (x,y).
                    # Angles in degrees                                                                                         #
                    Angle_phi_ac_deg = getAngle(f0[1],f0[0],f1[1])                                                              # Returns angle between points -> n0-p0-n1 (Here, p0 == p1). [deg]
                    Angle_alpha_c_minus_deg = getAngle(f0[0],f1[1],f0[1])                                                       # Returns angle between points -> p0-n1-n0 (Here, p0 == p1). [deg]
                    Angle_alpha_a_minus_deg = getAngle(f0[0],f0[1],f1[1])                                                       # Returns angle between points -> p0-n0-n1 (Here, p0 == p1). [deg]
                    # Angles in radians                                                                                         #
                    Angle_phi_ac_rad = math.radians(Angle_phi_ac_deg)                                                           # Angles deg to rad.
                    Angle_alpha_c_minus_rad = math.radians(Angle_alpha_c_minus_deg)                                             # Angles deg to rad.
                    Angle_alpha_a_minus_rad = math.radians(Angle_alpha_a_minus_deg)                                             # Angles deg to rad.
                    Angle_alpha_a_plus_rad = 0                                                                                  #
                    Angle_alpha_c_plus_rad = 0                                                                                  #
                    # pi                                                                                                        #
                    z_pi = Angle_phi_ac_rad + Angle_alpha_c_plus_rad + Angle_alpha_a_plus_rad                                   # pi -> total of all the angles calculated.
                    # Error cal.                                                                                                #
                    err_z = (z_pi - math.pi)/math.pi * 100                                                                      # % Error in value of pi --> ( (expri. pi - theor. pi)/theor. pi * 100 )
                                                                                                                                #
                    # Flux tube a 'sees' flux tube c                                                                            #
                    L_ac = 1/(2*math.pi)*(Angle_alpha_a_plus_rad + Angle_alpha_a_minus_rad)                                     # Larch calculations - Flux tube a 'sees' flux tube c.
                    ## Flux tube c 'sees' flux tube a                                                                           #
                    L_ca = 1/(2*math.pi)*(Angle_alpha_c_plus_rad + Angle_alpha_c_minus_rad)                                     # Larch calculations - Flux tube c 'sees' flux tube a.
                                                                                                                                #
                    LL_ac.append([L_ac,f0,f1])                                                                                  # Append the Larch_ac value, both flux ropes coords ([x1,y1],[x2,y2]).
                    LL_ca.append([L_ca,f0,f1])                                                                                  # Append the Larch_ca value, both flux ropes coords ([x1,y1],[x2,y2]).
                    ##----------------------------------------------------------------------------------------------------------#
                    if sha2 == 'y':                                                                                             #
                        print('###########################################################')                                    #
                        print('\n')                                                                                             #
                        print('----------Matching positive footpoints----------')                                               #
                        print('\n')                                                                                             #
                        if sha3 == 'y':                                                                                         # if sha3 is 'y' - detail calculations are results are printed
                            print('---------------------------------------------------------')                                  #
                            print('Angle_phi_ac_deg:',Angle_phi_ac_deg)                                                         #
                            print('Angle_alpha_c_plus_deg:',Angle_alpha_c_minus_deg)                                            #
                            print('Angle_alpha_a_plus_deg:',Angle_alpha_a_minus_deg)                                            #
                            print('---------------------------------------------------------')                                  #
                            print('Angle_phi_ac_rad:',Angle_phi_ac_rad)                                                         #
                            print('Angle_alpha_c_minus_rad:',Angle_alpha_c_minus_rad)                                           #
                            print('Angle_alpha_a_minus_rad:',Angle_alpha_a_minus_rad)                                           #
                            print('Angle_alpha_c_plus_rad:',Angle_alpha_c_plus_rad)                                             #
                            print('Angle_alpha_a_plus_rad:',Angle_alpha_a_plus_rad)                                             #
                            print('---------------------------------------------------------')                                  #
                            print('z_pi:',z_pi)                                                                                 #
                            print('% Err_z_pi:',err_z)                                                                          #
                            print('---------------------------------------------------------')                                  #
                        print('Larch_ac',L_ac)                                                                                  #
                        print('Larch_ca:',L_ca)                                                                                 #
                        print('L_ac*L_ca :',L_ac*L_ca)                                                                          #
                        print('\n')                                                                                             #
                        print('###########################################################')                                    #
                #---------------------------------------------------------------------------------------------------------------#
                else: pass                                                                                                      # if not matching +ve region then pass.
                #---------------------------------------------------------------------------------------------------------------#
                if f0[0][0] != f1[0][0] and f0[0][1] != f1[0][1] and f0[1][0] != f1[1][0] and f0[1][1] != f1[1][1]:             # To check if there are any matching footpoints and allow only if no matching footpoints.
                #---------------------------------------------------------------------------------------------------------------#
                    #-----------------------------------------------------------------------------------------------------------#
                                                                                                                                #
                    # Non-Intersecting footpoints                                                                               #
                    if inter == False:                                                                                          # Check if the flux ropes are non-intersecting.
                        # Angles in degrees                                                                                     #
                        Angle_alpha_a_plus_deg = getAngle(f0[1],f1[0],f0[0])                                                    # Returns angle between points -> n0-p1-p0 [deg]
                        Angle_alpha_a_minus_deg = getAngle(f0[1],f1[1],f0[0])                                                   # Returns angle between points -> n0-n1-p0 [deg]
                        Angle_alpha_c_plus_deg = getAngle(f1[1],f0[0],f1[0])                                                    # Returns angle between points -> n1-p0-p1 [deg]
                        Angle_alpha_c_minus_deg = getAngle(f1[1],f0[1],f1[0])                                                   # Returns angle between points -> n1-n0-p1 [deg]
                        # Angles in radians                                                                                     #
                        Angle_alpha_a_plus_rad = math.radians(Angle_alpha_a_plus_deg)                                           # Angles deg to rad.
                        Angle_alpha_a_minus_rad = math.radians(Angle_alpha_a_minus_deg)                                         # Angles deg to rad.
                        Angle_alpha_c_plus_rad = math.radians(Angle_alpha_c_plus_deg)                                           # Angles deg to rad.
                        Angle_alpha_c_minus_rad = math.radians(Angle_alpha_c_minus_deg)                                         # Angles deg to rad.
                                                                                                                                #
                        # Flux tube a 'sees' flux tube c                                                                        #
                        L_ac = (1/(2*math.pi))*(Angle_alpha_a_plus_rad + Angle_alpha_a_minus_rad)                               # Larch calculations - Flux tube a 'sees' flux tube c.
                        # Flux tube c 'sees' flux tube a                                                                        #
                        L_ca = (1/(2*math.pi))*(Angle_alpha_c_plus_rad + Angle_alpha_c_minus_rad)                               # Larch calculations - Flux tube c 'sees' flux tube a.
                                                                                                                                #
                        LL_ac.append([L_ac,f0,f1])                                                                              # Append the Larch_ac value, both flux ropes coords ([x1,y1],[x2,y2]).
                        LL_ca.append([L_ca,f0,f1])                                                                              # Append the Larch_ca value, both flux ropes coords ([x1,y1],[x2,y2]).
                        #-------------------------------------------------------------------------------------------------------#
                        if sha2 == 'y':                                                                                         #
                            print('###########################################################')                                #
                            print('\n')                                                                                         #
                            print('----------Non-Intersecting footpoints----------')                                            #
                            print('\n')                                                                                         #
                            if sha3 == 'y':                                                                                     # if sha3 is 'y' - detail calculations are results are printed.
                                print('---------------------------------------------------------')                              #
                                print('Angle_alpha_a_plus_deg:',Angle_alpha_a_plus_deg)                                         #
                                print('Angle_alpha_a_minus_deg:',Angle_alpha_a_minus_deg)                                       #
                                print('Angle_alpha_c_plus_deg:',Angle_alpha_c_plus_deg)                                         #
                                print('Angle_alpha_c_minus_deg:',Angle_alpha_c_minus_deg)                                       #
                                print('---------------------------------------------------------')                              #
                                print('Angle_alpha_a_plus_rad:',Angle_alpha_a_plus_rad)                                         #
                                print('Angle_alpha_a_minus_rad:',Angle_alpha_a_minus_rad)                                       #
                                print('Angle_alpha_c_plus_rad:',Angle_alpha_c_plus_rad)                                         #
                                print('Angle_alpha_c_minus_rad:',Angle_alpha_c_minus_rad)                                       #
                                print('----------------------------------------------------------')                             #
                            print('Larch_ac',L_ac)                                                                              #
                            print('Larch_ca:',L_ca)                                                                             #
                            print('Larch_ac - Larch_ca :',L_ac-L_ca)                                                            #
                            print('\n')                                                                                         #
                            print('###########################################################')                                #
                    #-----------------------------------------------------------------------------------------------------------#
                                                                                                                                #
                    # Intersecting footpoints                                                                                   #
                    elif inter == True:                                                                                         # Check if the flux ropes are intersecting.
                        # Angles in degrees                                                                                     #
                        Angle_alpha_a_plus_deg = getAngle(f0[1],f1[1],f0[0])                                                    # Returns angle between points -> n0-n1-p0 [deg]
                        Angle_alpha_a_minus_deg = getAngle(f0[1],f1[0],f0[0])                                                   # Returns angle between points -> n0-p1-p0 [deg]
                        Angle_alpha_c_plus_deg = getAngle(f1[1],f0[0],f1[0])                                                    # Returns angle between points -> n1-p0-p1 [deg]
                        Angle_alpha_c_minus_deg = getAngle(f1[1],f0[1],f1[0])                                                   # Returns angle between points -> n1-n0-p1 [deg]
                        # Angles in radians                                                                                     #
                        Angle_alpha_a_plus_rad = math.radians(Angle_alpha_a_plus_deg)                                           # Angles deg to rad.
                        Angle_alpha_a_minus_rad = math.radians(Angle_alpha_a_minus_deg)                                         # Angles deg to rad.
                        Angle_alpha_c_plus_rad = math.radians(Angle_alpha_c_plus_deg)                                           # Angles deg to rad.
                        Angle_alpha_c_minus_rad = math.radians(Angle_alpha_c_minus_deg)                                         # Angles deg to rad.
                                                                                                                                #
                        # Flux tube a 'sees' flux tube c                                                                        # Larch calculations - Flux tube a 'sees' flux tube c.
                        L_ac = (1/(2*math.pi))*(Angle_alpha_a_plus_rad + Angle_alpha_a_minus_rad)                               #
                        # Flux tube c 'sees' flux tube a                                                                        # Larch calculations - Flux tube c 'sees' flux tube a.
                        L_ca = (1/(2*math.pi))*(Angle_alpha_c_plus_rad + Angle_alpha_c_minus_rad)                               #
                                                                                                                                #
                        LL_ac.append([L_ac,f0,f1])                                                                              # Append the Larch_ac value, both flux ropes coords ([x1,y1],[x2,y2]).
                        LL_ca.append([L_ca,f0,f1])                                                                              # Append the Larch_ca value, both flux ropes coords ([x1,y1],[x2,y2]).
                        #-------------------------------------------------------------------------------------------------------#
                        if sha2 == 'y':                                                                                         #
                            print('###########################################################')                                #
                            print('\n')                                                                                         #
                            print('----------Intersecting footpoints----------')                                                #
                            print('\n')                                                                                         #
                            if sha3 == 'y':                                                                                     # if sha3 is 'y' - detail calculations are results are printed.
                                print('---------------------------------------------------------')                              #
                                print('Angle_alpha_a_plus_deg:',Angle_alpha_a_plus_deg)                                         #
                                print('Angle_alpha_a_minus_deg:',Angle_alpha_a_minus_deg)                                       #
                                print('Angle_alpha_c_plus_deg:',Angle_alpha_c_plus_deg)                                         #
                                print('Angle_alpha_c_minus_deg:',Angle_alpha_c_minus_deg)                                       #
                                print('---------------------------------------------------------')                              #
                                print('Angle_alpha_a_plus_rad:',Angle_alpha_a_plus_rad)                                         #
                                print('Angle_alpha_a_minus_rad:',Angle_alpha_a_minus_rad)                                       #
                                print('Angle_alpha_c_plus_rad:',Angle_alpha_c_plus_rad)                                         #
                                print('Angle_alpha_c_minus_rad:',Angle_alpha_c_minus_rad)                                       #
                                print('---------------------------------------------------------')                              #
                            print('Larch_ac',L_ac)                                                                              #
                            print('Larch_ca:',L_ca)                                                                             #
                            print('Larch_ac - Larch_ca :',L_ac-L_ca)                                                            #
                            print('\n')                                                                                         #
                            print('###########################################################')                                #
                    #-----------------------------------------------------------------------------------------------------------#
            else: pass                                                                                                          #
            #-------------------------------------------------------------------------------------------------------------------#
    sys.stdout = old_stdout                                                                                                     # stop writing into log file.
    log_file.close()                                                                                                            # close the log file
    print('\t ***--- Updating previous calculations ---*** \t')                                                                 # Indicates larch calculations are complete.
                                                                                                                                #
    return LL_ac, LL_ca                                                                                                         # Returns two lists --> Larch_ac cal. and Larch_ca cal. and the flux ropes footpoints.
#                                                                                                                               #
#-------------------------------------------------------------------------------------------------------------------------------#
