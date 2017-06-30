import sys
sys.path.append("//home//sahil//Downloads//Project2017_SahilKhanna_114840134")
import supportingMethods as sm
import LossCalculations as lc
import numpy as np
import math

# Basestation details
BST_HEIGHT = 50 # meters
BST_MAX_TX_POW = 42 # dBm
LINE_CONNECTOR_LOSS = 2.1 # dB
ANTENNA_GAIN = 12.1 # dB
FREQ_C = 1900 # MHz
Cd = 20
Ci = 15

# CDMA system
BW_C = 1.25 # MHz
BIT_RATE = 12.5 # kbps
PROCESSOR_GAIN = 20 # dB
NOISE_LEVEL = -110 # dBm
REQ_SINR = 6 # dB
MIN_PILOT_RSL = -107 # dBm
NUM_TRAFFIC_CHANNELS = 56

# Users properties
CALL_RATE = 6 # calls per hour
AVG_CALL_DURATION = 1 # min
NUM_USERS = 10000

# Users sets with each user has a list with properties such as
# [Location (x,y), Calling tries, Drop tries, call duration, call time]
# Index of the properties are fixed according to the above structure
active_users = []
users_attempts_call = []
inactive_users = NUM_USERS
free_channels = NUM_TRAFFIC_CHANNELS
completed_calls = 0
dropped_calls = 0
blocked_calls = 0
MU = 0
SIGMA = 2

# Summary
num_call_attempts = 0
num_call_attempts_with_retries = 0
num_blocked_calls_signal_strength = 0
num_blocked_calls_channel_capacity = 0
num_failed_calls = 0
num_retries = 0

# Make a table for shadowing loss lookup
table = lc.calShadow()
           
# Simulation loop for 2 hours or 7200 sec, assumes each sec as one iteration
current_time = 0 # sec
radius = 10 # km

# Paramters for the execution
eirp_pilot = sm.calEIRP(BST_MAX_TX_POW, LINE_CONNECTOR_LOSS, ANTENNA_GAIN)
eirp = eirp_pilot

for i in range(1, 7201):

    # Display simulation after every sec
    #sm.displayCircle(active_users, radius)

    num_retries += len(users_attempts_call)
    
    # Users of active call
    for j in active_users:
        user = j

        # Call ended if user's call duration is less than current time minus call start time
        if user[3] < current_time - user[4]:
            active_users.remove(user)
            inactive_users += 1
            free_channels += 1
            completed_calls += 1
        else:
            dist = np.sqrt(np.square(user[0][0]) + np.square(user[0][1]))
            location = (user[0][0]*1000, user[0][1]*1000) # in meters for shadowing look up
            numUsers = len(active_users)
            rsl = sm.calRsl(eirp, FREQ_C, dist, BST_HEIGHT, MU, SIGMA, table, location)
            user_sinr = sm.calSINR(rsl, numUsers, NOISE_LEVEL, PROCESSOR_GAIN)

        # Decide whether to drop the call or wait for three consecutive tries
            if user_sinr < REQ_SINR:
                if user[2] > 2:
                   active_users.remove(user)
                   inactive_users += 1
                   free_channels += 1
                   dropped_calls += 1
                else:
                    user[2] += 1
            else:
                user[2] = 0

    # Users attempting to call
    call_attempts = sm.getUsersCallAttempts(inactive_users, CALL_RATE/3600)
    num_call_attempts += call_attempts

    # Add users in the list of users which attempts call
    for i in range(0, call_attempts):
        user = [sm.randomLocation(), 0, 0, np.random.exponential(AVG_CALL_DURATION * 60), current_time]
        users_attempts_call.append(user)

    inactive_users -= call_attempts

    # Check how many user can make a call and add it to the active users list
    for user in users_attempts_call:
        dist = np.sqrt(np.square(user[0][0]) + np.square(user[0][1]))
        location = (user[0][0]*1000, user[0][1]*1000) # in meters for shadowing look up
        user_rsl = sm.calRsl(eirp_pilot, FREQ_C, dist, BST_HEIGHT, MU, SIGMA, table, location)

        # Check whether it can connect to the call
        if user_rsl < MIN_PILOT_RSL:
            user[1] += 1
        else:
            if free_channels > 0:
                users_attempts_call.remove(user)
                active_users.append(user)
                free_channels -= 1
            else:
                blocked_calls += 1
                users_attempts_call.remove(user)
                inactive_users += 1
                num_blocked_calls_channel_capacity += 1
        
        # Check if the user has attempted 3 consecutive attempts
        if user[1] > 2:
            blocked_calls += 1
            users_attempts_call.remove(user)
            inactive_users += 1
            num_blocked_calls_signal_strength += 1

    num_failed_calls = dropped_calls + blocked_calls
    num_call_attempts_with_retries = num_call_attempts + num_retries
    current_time += 1
    radius = sm.getCurrentCellRad(active_users)
    
    # Print summary every 2 min
    if current_time % 120 == 0:
        sm.summary(num_call_attempts, num_call_attempts_with_retries, dropped_calls, num_blocked_calls_signal_strength, num_blocked_calls_channel_capacity, completed_calls, len(active_users), num_failed_calls, radius)
    
    # Admission Control
    if len(active_users) > Cd and eirp_pilot > 30:
        eirp_pilot -= 0.5

    if len(active_users) < Ci and eirp_pilot < eirp:
        eirp_pilot += 0.5

            
        
    
