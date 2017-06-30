import numpy as np

def pathLoss(freq, dist, bstHeight, mobHeight = 0, citySize = "small"):
    ''' This function will calculate path loss based on COST-231 model:
        L = 46.3 + 33.9log10(fc) - 13.82log10(hte) - a(hre) + (44.9 - 6.55log(hte)log(d) + Cm
        where Cm = 0 and a(hre) = 0 in this case
        @parameters: float frequency in MHz, float distance in km, float basestation and mobile height in m
        @return: float loss in dB'''

    if freq < 0 or dist < 0 or bstHeight < 0:
        raise Exception("Wrong Input!")
    
    pathLoss = 46.3 + 33.9*np.log10(freq) - 13.82*np.log10(bstHeight) + (44.9 - 6.55*np.log10(bstHeight))*np.log10(dist)
    return pathLoss

def calShadow(mu = 0, sigma = 2):
    ''' This function will calculate the shadowing effect for each 0.01 km by 0.01 km area in the basestation and
    will store it in the dictionary with keys as x and y co-ordinates of the upper right corner of the square.
    @paramters: float mean, float std dev for the normal distribution
    @return: dict (which will be used for lookup table)'''

    if sigma < 0 and mean < 0:
        raise Exception("Wrong Input!")
    
    table = {}
    x_range = np.arange(-10000,10000,10)
    y_range = np.arange(-10000,10000,10)
    for x in x_range:
        for y in y_range:
            table[(x, y)] = np.random.normal(mu, sigma)
           
    return table

def calFading():
    ''' This function calculates the fading effect based on rayleigh distribution
        @parameters: none
        @return: float fading loss in dB'''

    return 20*np.log10(np.random.rayleigh())

def getShadowLoss(table, location):
    ''' This method will be used for value look up from the table
        @parameters: dict table contains value of shadowing corresponds to the x,y
        and float location of the user'''
    x, y = location[0], location[1]

    # Make the coordinates the lower left corner of the square
    if x < 0:
        x = int(x) - 1
        while x % 10 != 0:
            x = int(x) - 1
    else:
        while x%10 != 0:
            x = int(x) - 1
            
    if y < 0:
        y = int(y) - 1
        while y % 10 != 0:
            y = int(y) - 1
    else:
        while y % 10 != 0:
            y = int(y) - 1

    return table[(x,y)]

