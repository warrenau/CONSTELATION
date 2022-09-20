#################################
#     Shock Tube simulation     #
#       for CONSTELATION        #
#                               #
# Austin Warren    Sept 8, 2022 #
#################################


import numpy as np
import sodshock as shock
import time
import csv
import os



# initialize shock tube
dt = 5e-6    # serpent time step. star solves with 5e-8 time step, but only sends data at 5e-6

spec_heat_ratio = 1.67      # ratio of specific heats
dustFrac = 0.0              # dust fraction -- not used for this simulation
npts = 500*2                  # number of points (using the same as star simulations - multiplied by 2 to make up for the part of the shock tube not in the reactor)
left_state = (1.72e6,2,0)   # pressure, density, velocity left of shock
right_state = (0.1,0.01,0)  # pressure, density, velocity right of shock
geometry = (0,1.276,0.638)  # left, right, shock position in meters
t = 0                       # time in shock progression



# solve in loop that waits for serpent done text file before moving onto next time step
# output csv file of solution in manner that CONSTELATION expects

filename = r'./ExtractedData/He3Data_table.csv'
columns = ['Position in Cartesian 1[X] (cm)', 'Density(g/cm^3) (kg/m^3)', 'Temperature (K)']




t_max = 5e-3
simulating = 1

while simulating == 1:
    # solve shock tube for time step
    positions, regions, values = shock.solve(left_state=left_state, right_state=right_state,geometry=geometry,t=t,gamma=spec_heat_ratio,npts=npts, dustFrac=dustFrac)

    # write data out to file
    with open(filename,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for i in range(int(len(values['x'])/2),int(len(values['x']))):
            writer.writerow([values['x'][i],values['rho'][i],values['p'][i]])

    # update values
    t += dt
    filename = r'./ExtractedData/He3Data_table_'+str(t)+'.csv'

    # write done file for current loop
    file_out = open('./STARTopDone.txt','w')
    file_out.write('Done')
    file_out.close
    
    # wait for serpent to finish current time step
    time_to_wait = 100
    time_counter = 0

    while not os.path.exists('./SerpentDone.txt'):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            simulating = 0
            break
            



    # end loop after end time or serpent is finished?
    if t > t_max:
        simulating = 0










