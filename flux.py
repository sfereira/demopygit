#---------------------------------------------------------------------------------------------------------------#
# Libraries needed                                                                                              #
import numpy as np                                                                                              #
import pandas as pd                                                                                             #
#---------------------------------------------------------------------------------------------------------------#
#                                                                                                               #
# Input  --> pdf2 -> Dataframe containing positive regions information.                                         #
#                           (Bz concentration value[in Gauss], Coordinates[x,y], Pixel area of the region).     #
#        --> ndf2 -> Dataframe containing negative regions information.                                         #
#                           (Bz concentration value[in Gauss], Coordinates[x,y], Pixel area of the region).     #
#        --> lamda1 -> length scale in x-direction. [in cm]                                                     #
#        --> lamda2 -> length scale in y-direction. [in cm]                                                     #
#                                                                                                               #
# Output --> pdf2 -> Dataframe containing positive regions information with flux value calculated. [in Mx^2]    #
#        --> ndf2 -> Dataframe containing negative regions information with flux value calculated. [in Mx^2]    #
#                                                                                                               #
#---------------------------------------------------------------------------------------------------------------#
def flux(pdf2,ndf2,lamda1,lamda2):                                                                              #
    fluxn = []                                                                                                  # List to store flux values from -ve regions.
    for i in range(len(ndf2)):                                                                                  # Length of for loop -> number of -ve regions.
        fluxn1 =  lamda1 * lamda2 * abs(ndf2['Concentration(G)'][i])                                            # Flux = Total Bz concentration in the region times the length scales. (-ve regions)
        fluxn.append(fluxn1)                                                                                    # Append flux value.
    ndf2['Flux(Mx)'] = fluxn                                                                                    # Update the original dataframe with flux values
                                                                                                                #
    fluxp = []                                                                                                  # List to store flux values from +ve regions
    for i in range(len(pdf2)):                                                                                  # Length of for loop -> number of +ve regions.
        fluxp1 =  lamda1 * lamda2 * abs(pdf2['Concentration(G)'][i])                                            # Flux = Total Bz concentration in the region times the length scales. (+ve regions)
        fluxp.append(fluxp1)                                                                                    # Append flux value.
    pdf2['Flux(Mx)'] = fluxp                                                                                    # Update the original dataframe with flux values
                                                                                                                #
    return pdf2,ndf2                                                                                            # Return +ve and -ve dataframe with flux values calculated.
#---------------------------------------------------------------------------------------------------------------#
