import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("//home//sahil//Downloads//Project2017_SahilKhanna_114840134")
import LossCalculations as lc


def displayCircle(users, r = 10):
    ''' This methods plots the station situation
        @parameters: list of users on call, float radius
        @return: display of the simulation'''
    x = []
    y = []
    # Take position of all the users
    for user in users:
        x.append(user[0][0])
        y.append(user[0][1])

    plt.axis([-10,10,-10,10])
    ax = plt.subplot(1,1,1)
    circ = plt.Circle((0,0), radius=r, color='black', fill=False, label = 'cell radius')
    bst = ax.scatter(0,0, c = 'r', label = 'basestation')
    users = ax.scatter(x,y, c = 'b', label = 'users at one time instant')
    ax.legend(handles = [circ, bst, users])
    ax.add_patch(circ)
    plt.pause(0.001)
    plt.show(block = False)
    #plt.show()

def calEIRP(maxTxPow, lineLoss, antGain):
    ''' This method calculates the transmitted power of base station
        @parameters: float max transmitter power(dB), float line and connector loss(dB)
        float antenna gain(dB)
        @return: float EIRP(dB)'''
    return maxTxPow - lineLoss + antGain

    
def calRsl(eirp, freq, dist, bstHeight, mu, sigma, table, location):
    ''' This method calculates the received signal at the mobile: RSL = EIRP – PL + S + F
    @parameters: All parameters are in float
    @return: received signal level(dBm)'''

    pathloss = lc.pathLoss(freq, dist, bstHeight)
    shadow = lc.getShadowLoss(table, location)
    fading = lc.calFading()
    rsl = eirp - pathloss + shadow + fading
    return rsl

def calSINR(rsl, numUsers, noise = -110, recGain = 20):
    ''' It will calculate the SINR = Signal/Noise where Signal = RSL + PG
        Noise = Noise Level + Interference Level; Interference Level = RSL + 10*log10(N-1)
        @parameters: All ate floats
        @return: float signal to interference with noise ratio'''
    # To avoid illegal parameter condition in np.log10() function
    if numUsers <= 1:
        numUsers = 2
    
    signal_level = rsl + recGain
    noise = np.power(10, noise/10)
    interference_level = rsl + 10*np.log10(numUsers - 1)
    noise_level = 10*np.log10((noise + np.power(10,interference_level/10)))
    return signal_level - noise_level

def randomLocation(r = 10):
    ''' This method will generate a uniformally distributed random location of the user
        @parameter: float radius of the circle
        @return: tuple of x and y coordinates'''
    #angle = np.random.uniform(0, 2*np.pi, 1)
    #rad = np.random.uniform(0, r, 1)
    angle = 2*np.pi*np.random.random(1)
    rad = 10*np.sqrt(np.random.random(1))
    x = rad * np.cos(angle)
    y = rad * np.sin(angle)
    return (x, y)

def getCurrentCellRad(users):
    ''' This method calculates the farthest user's distance from the basestation
        @parameters: list of active users
        @return: float radius of the cell'''
    max_dist = 0
    for user in users:
        dist = np.sqrt(np.square(user[0][0]) + np.square(user[0][1]))
        if dist > max_dist:
            max_dist = dist

    return max_dist

def getUsersCallAttempts(total_users, lam = 0.0017):
    ''' This method will returns number of users who attempts to call at every second
        @parameters: float call rate per sec and number of total users
        @return: int number of users'''
    #prob = np.random.poisson(lam, 1000)
    #ran_users = list(prob).count(1)
    ran_users = 0
    users = 1
    #while users <= total_users:
        #ran_users += np.random.choice([1,0], p = [1/600, 599/600])
        #users += 1
    ran_users = list(np.random.choice([1,0], size = total_users, p = [1/600, 599/600])).count(1)
    return ran_users

def summary(num_call_attempts, num_call_attempts_with_retries, dropped_calls, num_blocked_calls_signal_strength, num_blocked_calls_channel_capacity, completed_calls, calls_in_prog, failed_calls, radius):
    ''' This method print the report of the parameters at give time
        @return: String'''
    print('Number of call attempts not counting retries: {0}'.format(num_call_attempts))
    print('Number of call attempts including retries: {0}'.format(num_call_attempts_with_retries))
    print('Number of dropped calls: {0}'.format(dropped_calls))
    print('Number of blocked calls due to signal strength: {0}'.format(num_blocked_calls_signal_strength))
    print('Number of blocked calls due to channel capacity: {0}'.format(num_blocked_calls_channel_capacity))
    print('Number of successfully completed calls: {0}'.format(completed_calls))
    print('Number of calls in progress at any given time: {0}'.format(calls_in_prog))
    print('Number of failed calls (blocks + drops): {0}'.format(failed_calls))
    print('Cell Radius: {0}\n'.format(radius))
    return

