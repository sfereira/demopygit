#---------------------------------------------------------------------------------------------------#
## Libraries needed                                                                                 #
                                                                                                    #
import numpy as np                                                                                  #
import pandas as pd                                                                                 #
import sys                                                                                          #
                                                                                                    #
#---------------------------------------------------------------------------------------------------#
# Input --> pdf2 -> +ve regions dataframe.                                                          #
#       --> ndf2 -> -ve regions dataframe.                                                          #
#                                                                                                   #
# Output --> updf -> +ve unit flux points dataframe.                                                #
#        --> undf -> -ve unit flux points dataframe.                                                #
#        --> xp1 -> List of +ve x-coord.                                                            #
#        --> yp1 -> List of +ve y-coord.                                                            #
#        --> xn1 -> List of -ve x-coord.                                                            #
#        --> yn1 -> List of -ve y-coord.                                                            #
#---------------------------------------------------------------------------------------------------#
def unit_point(pdf2,ndf2):                                                                          # Define function with required input.
    scharge_signp = []                                                                              # List to store +ve region labels
    scharge_signn = []                                                                              # List to store -ve region labels
    snumber1 = 0                                                                                    # Counter for labeling +ve regions.
    snumber2 = 0                                                                                    # Counter for labeling -ve regions.
    for i in range(len(pdf2['Concentration(G)'])):                                                  #
        scharge_signsp = "P%s" %snumber1                                                            # +ve region Label --> String{P} + int - eg. 'P0','P1'
        scharge_signp.append(scharge_signsp)                                                        #
        snumber1 +=1                                                                                # Increment +ve label counter.
    for i in range(len(ndf2['Concentration(G)'])):                                                  #
        scharge_signsn = "N%s" %snumber2                                                            # -ve region Label --> String{N} + int - eg. 'N0','N1'
        scharge_signn.append(scharge_signsn)                                                        #
        snumber2 +=1                                                                                # Increment -ve label counter.
    scharge_sign1p = np.asarray(scharge_signp)                                                      # List to array.
    scharge_sign1n = np.asarray(scharge_signn)                                                      # List to array.
    if pdf2.columns[0] != 'Label':                                                                  # Condition to check if the 'label' column already exist. [+ve regions]
        pdf2.insert(loc = 0, column='Label', value=scharge_sign1p)                                  # If column doesn't exist, create one and place it in first place in dataframe.
    else:                                                                                           #
        pdf2.update({'Label': scharge_sign1p })                                                     # If column exist, update the values into the 'label' column.
    if ndf2.columns[0] != 'Label':                                                                  # Condition to check if the 'label' column already exist. [-ve regions]
        ndf2.insert(loc = 0, column='Label', value=scharge_sign1n)                                  # If column doesn't exist, create one and place it in first place in dataframe.
    else:                                                                                           #
        ndf2.update({'Label': scharge_sign1n })                                                     # If column exist, update the values into the 'label' column.
    #-----------------------------------------------------------------------------------------------#
    # Printing the +ve and -ve dataframes to check the Labels created.                              #
    print('#################################################################')                      #
    print('\n')                                                                                     #
    print(pdf2)                                                                                     # Print +ve regions dataframe.
    print('\n')                                                                                     #
    print('#################################################################')                      #
    print('\n')                                                                                     #
    print(ndf2)                                                                                     # Print -ve regions dataframe.
    print('\n')                                                                                     #
    print('#################################################################')                      #
    #-----------------------------------------------------------------------------------------------#
    ## Creating Unit flux points based on the min.flux value.                                       #
    ## Based on the number of points charges for a regions,                                         #
    ##     number of unit points are created with the same coordinate (x,y).                        #
    #-----------------------------------------------------------------------------------------------#
    sn1=0                                                                                           # Label counter for +ve unit flux points.
    sn2=0                                                                                           # Label counter for -ve unit flux points.
    sposloc = []                                                                                    # List to store +ve region labels.
    snegloc = []                                                                                    # List to store -ve region labels.
    spflux = []                                                                                     # List to store count of unit flux points for each +ve regions.
    snflux = []                                                                                     # List to store count of unit flux points for each -ve regions.
    xx1 = []                                                                                        # List to store x-coordinate +ve regions.
    xx2 = []                                                                                        # List to store y-coordinate +ve regions.
    yy1 = []                                                                                        # List to store x-coordinate -ve regions.
    yy2 = []                                                                                        # List to store y-coordinate -ve regions.
    for i in range(len(scharge_sign1p)):                                                            # For +ve regions, length of for loop -> number of +ve regions.
        if pdf2['Label'][i] == "P%s" %sn1:                                                          # Check if the value exists.
            spflux1 = pdf2['Point_Charges'][i]                                                      # Select ith count of unit flux points value.
            spos_p = pdf2['Label'][i]                                                               # Select ith Label value.
            xx1s = pdf2['x'][i]                                                                     # Select ith x-coord value.
            yy1s = pdf2['y'][i]                                                                     # Select ith y-coord value.
            sposloc.append(spos_p)                                                                  # Append the +ve region label.
            spflux.append(spflux1)                                                                  # Append count of unit flux point of the +ve region.
            xx1.append(xx1s)                                                                        # Append x-coord of +ve region.
            yy1.append(yy1s)                                                                        # Append y-coord of +ve region.
            sn1 +=1                                                                                 # Update the +ve unit flux points Label counter.
                                                                                                    #
    for i in range(len(scharge_sign1n)):                                                            # For -ve regions, length of for loop -> number of -ve regions.
        if ndf2['Label'][i] == "N%s" %sn2:                                                          # Check if the value exists.
            snflux1 = ndf2['Point_Charges'][i]                                                      # Select ith count of unit flux points value.
            sneg_p = ndf2['Label'][i]                                                               # Select ith Label value.
            xx2s = ndf2['x'][i]                                                                     # Select ith x-coord value.
            yy2s = ndf2['y'][i]                                                                     # Select ith y-coord value.
            snegloc.append(sneg_p)                                                                  # Append the -ve region label.
            snflux.append(snflux1)                                                                  # Append count of unit flux point of the -ve region.
            xx2.append(xx2s)                                                                        # Append x-coord of -ve region.
            yy2.append(yy2s)                                                                        # Append y-coord of -ve region.
            sn2 +=1                                                                                 # Update the -ve unit flux points Label counter.
    #-----------------------------------------------------------------------------------------------#
                                                                                                    #
    ptdf = pd.DataFrame(sposloc, index=None)                                                        # Dataframe creation to store information of +ve unit points.
    ptdf.columns = ['Points']                                                                       # Update dataframe column.
    ptdf['x'] = xx1                                                                                 # Insert +ve x-coord values.
    ptdf['y'] = yy1                                                                                 # Insert +ve y-coord values.
    ptdf['Point_charges'] = spflux                                                                  # Insert +ve labels.
                                                                                                    #
    ntdf = pd.DataFrame(snegloc, index=None)                                                        # Dataframe creation to store information of -ve unit points.
    ntdf.columns = ['Points']                                                                       # Update dataframe column. (count of flux points)
    ntdf['x'] = xx2                                                                                 # Insert -ve x-coord values.
    ntdf['y'] = yy2                                                                                 # Insert -ve x-coord values.
    ntdf['Point_charges'] = snflux                                                                  # Insert -ve labels.
                                                                                                    #
    #-----------------------------------------------------------------------------------------------#
                                                                                                    #
    p1 = []                                                                                         # List to store new labels of +ve unit points.
    xp1 = []                                                                                        # List to store unit points x-coord value.
    yp1 = []                                                                                        # List to store unit points y-coord value.
    ppc1= []                                                                                        # List to store unit points value. (Here all points are assigned '1.0' value)
    for i in range(len(ptdf['Points'])):                                                            # length of for loop --> total number of unit +ve flux points.
        j=0                                                                                         # Counter to track number of +ve unit points and labels created.
        while j <= ptdf['Point_charges'][i]:                                                        # Condition to generate the required number of unit flux points.
            p11 = ptdf['Points'][i]                                                                 # Select ith +ve label.
            x11 = ptdf['x'][i]                                                                      # Select ith +ve x-coord value.
            y11 = ptdf['y'][i]                                                                      # Select ith +ve y-coord value.
            pc11 = 1.0                                                                              # '1.0' assigned for each label.
            p1.append(p11)                                                                          # Append +ve label.
            xp1.append(x11)                                                                         # Append x-coord value.
            yp1.append(y11)                                                                         # Append y-coord value.
            ppc1.append(pc11)                                                                       # Append unit value assigned to each label.
            j +=1                                                                                   # Increment the counter to indicate +ve unit flux point is created.
                                                                                                    #
    n1 = []                                                                                         # List to store new labels of -ve unit points.
    xn1 = []                                                                                        # List to store unit points x-coord value.
    yn1 = []                                                                                        # List to store unit points y-coord value.
    npc1= []                                                                                        # List to store unit points value. (Here all points are assigned '1.0' value)
    for i in range(len(ntdf)):                                                                      # length of for loop --> total number of unit -ve flux points.
        k=0                                                                                         # Counter to track number of -ve unit points and labels created.
        while k <= ntdf['Point_charges'][i]:                                                        # Condition to generate the required number of unit flux points.
            n11 = ntdf['Points'][i]                                                                 # Select ith -ve label.
            x12 = ntdf['x'][i]                                                                      # Select ith -ve x-coord value.
            y12 = ntdf['y'][i]                                                                      # Select ith -ve y-coord value.
            nc11 = 1.0                                                                              # '1.0' assigned for each label.
            n1.append(n11)                                                                          # Append -ve label.
            xn1.append(x12)                                                                         # Append x-coord value.
            yn1.append(y12)                                                                         # Append y-coord value.
            npc1.append(nc11)                                                                       # Append unit value assigned to each label.
            k +=1                                                                                   # Increment the counter to indicate -ve unit flux point is created.
    #-----------------------------------------------------------------------------------------------#
                                                                                                    #
    updf = pd.DataFrame({'Points': p1, 'x': xp1, 'y': yp1, 'Point_charges':ppc1}, index=None)       # updf --> Dataframe with +ve flux unit points. (Lables, Coord[x,y], Unit charge = 1.0 [for all])
    undf = pd.DataFrame({'Points': n1, 'x': xn1, 'y': yn1, 'Point_charges':npc1}, index=None)       # undf --> Dataframe with -ve flux unit points. (Lables, Coord[x,y], Unit charge = 1.0 [for all])
                                                                                                    #
    old_stdout = sys.stdout                                                                         # Command to initiate the print function output into a external log file.
    log_file = open("message3.log","w")                                                             # log file is opened to print the results into it.
    sys.stdout = log_file                                                                           # Start the log file.
    print('####################################################')                                   # """
    print('\n')                                                                                     #
    print('\t After converting point charges to unit charges \t')                                   # *** After converting point charges to unit charges ***
    print('\n')                                                                                     #
    print(updf)                                                                                     # Print +ve unit point dataframe
    print('\n')                                                                                     #
    print(undf)                                                                                     # Print -ve unit point dataframe
    print('\n')                                                                                     #
    print('####################################################')                                   # """
    sys.stdout = old_stdout                                                                         # Update the log file.
    log_file.close()                                                                                # log file is closed.
                                                                                                    #
    return updf,undf, xp1, xn1, yp1, yn1                                                            # return --> updf - [+ve unit flux points dataframe], undf - [-ve unit flux points dataframe]
                                                                                                    #        --> xp1 - [List of +ve x-coord], yp1 - [List of +ve y-coord]
                                                                                                    #        --> xn1 - [List of -ve x-coord], yn1 - [List of -ve y-coord]
    #-----------------------------------------------------------------------------------------------#
