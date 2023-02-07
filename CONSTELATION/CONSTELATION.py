############################################################
#                                                           #
#          STAR and Serpent Coupling Script v 0.5           #
#                   CONSTELLATION                           #
#                                                           #
# Created by: Cole Leingang                 2020/01/10      #
#                                                           #
#############################################################

import os
import signal
import math
import time
import csv
import pandas as pd
import numpy as np
import re
from shutil import copyfile
# timestep used for simulation
timestep = 2E-6
# The number of time steps that STAR will simulate before checking for SERPENT completion and then export Data
STAR_STEP = 40
# Second variables used to stay constant in loop
step_length = 40
#######################################################
# Create the Serpent input-file for this run          #
# (process id or communication file must be appended) #
#######################################################

# Open original input for reading

file_in = open(r'Treat', 'r')

# Open a new input file for writing

file_out = open(r'coupledTreat', 'w')

# Write original input to new file

for line in file_in:
    file_out.write(line)

# Close original input file

file_in.close()
# Append Source File Location
file_out.write('\n')
file_out.write('set dynsrc Source 1\n')

# Do not make group constants
file_out.write('\n')
file_out.write('set gcu -1\n')

# Append signalling mode

file_out.write('\n')
file_out.write('set comfile com.in com.out\n')

# Append interface names

file_out.write('\n')
file_out.write('ifc HE3TOP.ifc\n\n')
file_out.write('\n')
file_out.write('ifc HE3BOT.ifc\n\n')
file_out.write('\n')
file_out.write('ifc fuel.ifc\n\n')

# Close new input file

file_out.close()

##############################################
# Write the initial He3 interface file for 1st Star Run                      #
# (He3 temperature and density for top two HENRI's will be updated)          #
##############################################

file_out = open('HE3TOP.ifc', 'w')

# Write the header line (TYPE MAT OUT)

file_out.write('2  He3Top 0\n')

# Write the mesh type

file_out.write('1\n')

# Write the mesh data (NX XMIN XMAX NY YMIN YMAX NZ ZMIN ZMAX)

file_out.write('1 -100 100 1 0 100 500 -60.48375 60.48375\n')

# Write the Mesh Data
STAR_Points = 501
# Check to see if STAR-CCM_ .csv file has been created and wait for a predetermined amount of time if it hasn't
time_to_wait = 10
time_counter = 0
filename = r'./ExtractedData/He3Data_table.csv'
while not os.path.exists(filename):
    time.sleep(1)
    time_counter += 1
    if time_counter > time_to_wait: break
if os.path.isfile(filename):
    # Take the data from STAR-CCM+ .csv file and write to ifc
    columns = ['Position in Cartesian 1[X] (cm)', 'Density(g/cm^3) (kg/m^3)', 'Temperature (K)']
    df = pd.read_csv(filename, usecols=columns)
    # Position = df['Position in Cartesian 1[X] (cm)']
    # Density =  df['Density(g/cm^3) (kg/m^3)']
    # Temp = df['Temperature (K)']
    
    # Sorts data from STAR-CCM+ in ascending order by position
    df_convert = df.to_numpy()
    numpy_array = df_convert[df_convert[:, 0].argsort()]
    
    # Cross Section Data for He-3 in SERPENT2 only exists for 300 K or above, this will only happen early on in the transient and temp
    # should never fall that far below 300K so setting this arbitrary constraint should have minimal change in results
    for i in range(STAR_Points):
        if numpy_array[i, 2] < 300.0:
            numpy_array[i, 2] = 300.0
    denstemp = numpy_array[:, [1, 2]]
    np.savetxt(file_out, denstemp, fmt="%1.6f")
else:
    raise ValueError("%s has not been created or could not be read" % filename)
# Close interface file

file_out.close()

##############################################
# Write the initial He3 interface file for 2nd Star Run                         #
# (He3 temperature and density for bottom two HENRI's will be updated)          #
##############################################

file_out = open('HE3BOT.ifc', 'w')

# Write the header line (TYPE MAT OUT)

file_out.write('2  He3Bot 0\n')

# Write the mesh type

file_out.write('1\n')

# Write the mesh data (NX XMIN XMAX NY YMIN YMAX NZ ZMIN ZMAX)

file_out.write('1 -100 100 1 -100 0 500 -60.48375 60.48375\n')

# Write the Mesh Data
STAR_Points = 501
# Check to see if STAR-CCM_ .csv file has been created and wait for a predetermined amount of time if it hasn't
time_to_wait = 10
time_counter = 0
filename = r'./ExtractedData/He3Data_table.csv'
while not os.path.exists(filename):
    time.sleep(1)
    time_counter += 1
    if time_counter > time_to_wait: break
if os.path.isfile(filename):
    # Take the data from STAR-CCM+ .csv file and write to ifc
    columns = ['Position in Cartesian 1[X] (cm)', 'Density(g/cm^3) (kg/m^3)', 'Temperature (K)']
    df = pd.read_csv(filename, usecols=columns)
    # Position = df['Position in Cartesian 1[X] (cm)']
    # Density =  df['Density(g/cm^3) (kg/m^3)']
    # Temp = df['Temperature (K)']
    
    # Sorts data from STAR-CCM+ in ascending order by position
    df_convert = df.to_numpy()
    numpy_array = df_convert[df_convert[:, 0].argsort()]
    
    # Cross Section Data for He-3 in SERPENT2 only exists for 300 K or above, this will only happen early on in the transient and temp
    # should never fall that far below 300K so setting this arbitrary constraint should have minimal change in results
    for i in range(STAR_Points):
        if numpy_array[i, 2] < 300.0:
            numpy_array[i, 2] = 300.0
    denstemp = numpy_array[:, [1, 2]]
    np.savetxt(file_out, denstemp, fmt="%1.6f")
else:
    raise ValueError("%s has not been created or could not be read" % filename)
# Close interface file

file_out.close()

##############################################
# Write the initial fuel interface           #
##############################################

file_out = open('fuel.ifc', 'w')

# Write the header line (TYPE MAT OUT)

file_out.write('2  fuel1 0\n')

# Write the mesh type

file_out.write('1\n')

# Write the mesh data (NX XMIN XMAX NY YMIN YMAX NZ ZMIN ZMAX)

file_out.write('1 -200 200 1 -200 200 10 -60.48375 60.48375\n')

# Write initial fuel temperatures and densities
# TREAT has graphite mixed fuel (hence low density close to graphite)

for i in range(10):
    file_out.write('-1.72 300.0\n')
    if i == 7:
        file_out.write('-1.72 330.0\n')

# Close interface file

file_out.close()

############################################
# Initialize the fuel temperature solution #
############################################

TBOI = []
TEOI = []

for i in range(10):
    TBOI.append(300.0)
    TEOI.append(300.0)

################################
# Start the Serpent simulation #
################################

# Submit SERPENT2 submission script to server
run_SERP = "qsub SERPENT_job.sh"
os.system(run_SERP)


# Reset time step
curtime = 0
# Pause Simulation unitl SERPENT2 starts simulating
SERPENTWait = 500000000 
time_counter = 0
Serpname = r'com.out'
while not os.path.exists(Serpname):
    time.sleep(5)
    time_counter += 1
    if time_counter > SERPENTWait:
        raise ValueError("%s has not been created or could not be read" % Serpname)
        break
#######################
# Loop over time steps #
########################

simulating = 1

while simulating == 1:
    ###################
    # Wait for signal #
    ###################
    sleeping = 1
    while sleeping == 1:
        # Sleep for two seconds
        time.sleep(5)
        # Open file to check if we got a signal
        fin = open('com.out', 'r')
        # Read line
        line = fin.readline()
        # Close file
        fin.close()
        # Check signal
        
        if int(line) != -1:
            if int(line) == signal.SIGUSR1:
                # Got the signal to resume
                print(signal.SIGUSR1)
                print("Resume Current Iteration")
                sleeping = 0
            elif int(line) == signal.SIGUSR2:
                # Got the signal to move to next time point
                print(signal.SIGUSR2)
                print('Move to Next Time Step')
                iterating = 0
                sleeping = 0
            elif int(line) == signal.SIGTERM:
                # Got the signal to end the calculation
                print(signal.SIGTERM)
                print('END The Simulation')
                iterating = 0
                sleeping = 0
                simulating = 0
            else:
                # Unknown signal
                print("\nUnknown signal read from file, exiting\n")
                print(line)
                # Exit
                quit()
            # Reset the signal in the file
            file_out = open('com.out', 'w')
            file_out.write('-1')
            file_out.close()
    # Check if simulation has finished and break out of iterating
    # loop
    if simulating == 0:
        break
    ########################
    # Import SERPENT2 Data ##
    #########################
    
    # First Convert given SERPENT2 output of .m file to .txt file to be manipulated            
    outputfile = r'coupledTreat_det'+str(curtime) + '.m'
    textfile = r'coupledTreat_det' + str(curtime) + '.txt'
    time_counter = 0
    while not os.path.exists(outputfile):
        time.sleep(1)
        time_counter += 1
    if time_counter > SERPENTWait:
        raise ValueError("%s has not been created or could not be read" % Serpname)
        break
    copyfile(outputfile, textfile)
    ###########################################
    # Collect Data from converted output file #
    ###########################################

    # if copying error has occured just replace with previous timestep (band-aid fix)
    if os.stat(textfile).st_size == 0:
        name = r'coupledTreat_det'+str(curtime-1)
        outputfile = r'coupledTreat_det'+str(curtime-1) + '.m'
        textfile = r'coupledTreat_det' + str(curtime-1) + '.txt'
        copyfile(outputfile, textfile)
        # print to outfile to keep track of copy errors
        print('Copy Error at TimeStep = ' + str(curtime))
    else:
        name = r'coupledTreat_det'+str(curtime)
    # Finds Heat Production Detector values from SERPENT2 Output
    HeadTop_pattern = re.compile(r"\DETSerpent2STop\s")
    HeadBot_pattern = re.compile(r"\DETSerpent2SBot\s")
    # Finds Fuel Deposition Detector values from SERPENT2 Output
    Fuel_pattern = re.compile(r"\DETFuelDepositon\s")
    # Finds data after initial pattern has been found
    data_pattern = re.compile(r'(\d+)\s*(\d+)\s*(.*)$')
    # Finds Heat Production Detector Z values
    Second_pattern = re.compile(r"DETSerpent2STopZ(.*)$")
    # Second_pattern =  re.compile(r"DETSerpent2SBotZ(.*)$")
    # Number of Z points
    Zpoints = 100
    # Number of Fuel points
    Fpoints = 10
    # Finds Heat Production Detector X values
    Third_pattern = re.compile(r"DETSerpent2STopX(.*)$")
    # ThirdBot_pattern =  re.compile(r"DETSerpent2SBotX(.*)$")
    # Number of X points
    Xpoints = 1
    # Finds Heat Production Detector Y values
    FourthTop_pattern = re.compile(r"DETSerpent2STopY(.*)$")
    FourthBot_pattern = re.compile(r"DETSerpent2SBotY(.*)$")
    # Number of Y points
    Ypoints = 5
    # Number of overall points
    points = Zpoints*Ypoints*Xpoints

    def SERPENTExtract(F1, f2):
        global data
        global data_pass
        global datafuel
        global data_fuelpass
        global data_passBot
        global dataBot
        global YdataBot
        global Xdata
        global Ydata
        global Zdata
        global Fdata
        data_pass = []
        data = []
        data_passBot = []
        dataBot = []
        data_fuelpass = []
        datafuel = []
        Xdata = []
        Ydata = []
        YdataBot = []
        Zdata = []
        for line in f1:
         matchx = Third_pattern.search(line)
         matchyTop = FourthTop_pattern.search(line)
         matchyBot = FourthBot_pattern.search(line)
         matchz = Second_pattern.search(line)
         matchTop = HeadTop_pattern.match(line)
         matchBot = HeadBot_pattern.match(line)
         matchfuel = Fuel_pattern.match(line)
         # Finds Volumetric Heating for Top 2 HENRIs
         if matchTop is not None:
             iter = 0
             for line in f1:
                 matchpoints = data_pattern.search(line)
                 if matchpoints is not None:
                     savepoints = matchpoints.group(0)
                     if iter < 10:
                         # Save Data used to input x,y,z locations
                         cleanpoints = savepoints[34:48]
                         # Save Mean Value of Data
                         cleanpass = savepoints[48:60]
                         data.append(cleanpoints)
                         data_pass.append(cleanpass)
                     if iter < 999 and iter >= 10:
                         # Save Data used to input x,y,z locations
                         cleanpoints = savepoints[35:48]
                         # Save Mean Value of Data
                         cleanpass = savepoints[48:61]
                         data.append(cleanpoints)
                         data_pass.append(cleanpass)
                     if iter >= 999: 
                         # Save Data used to input x,y,z locations
                         cleanpoints = savepoints[34:50]
                         # Save Mean Value of Data
                         cleanpass = savepoints[51:63]
                         data.append(cleanpoints)
                         data_pass.append(cleanpass)
                     iter = iter +1
                     if iter == points:
                         break
         # Finds and saves fuel deposition values
         if matchfuel is not None:
             iter = 0
             for line in f1:
                 matchpoints = data_pattern.search(line)
                 if matchpoints is not None:
                     savepoints = matchpoints.group(0)
                     if iter < 10:
                         # Save Data used to input x,y,z locations
                         cleanpoints = savepoints[34:48]
                         # Save Mean Value of Data
                         cleanpass = savepoints[48:60]
                         datafuel.append(cleanpoints)
                         data_fuelpass.append(cleanpass)
                     if iter < 999 and iter >= 10:
                         # Save Data used to input x,y,z locations
                         cleanpoints = savepoints[35:48]
                         # Save Mean Value of Data
                         cleanpass = savepoints[48:61]
                         datafuel.append(cleanpoints)
                         data_fuelpass.append(cleanpass)
                     if iter >= 999:
                         # Save Data used to input x,y,z locations
                         cleanpoints = savepoints[34:50]
                         # Save Mean Value of Data
                         cleanpass = savepoints[51:63]
                         datafuel.append(cleanpoints)
                         data_fuelpass.append(cleanpass)
                     iter = iter +1
                     if iter == Fpoints:
                         break
        # Finds Volumetric Heating for Bottom 2 HENRIs
         if matchBot is not None:
             iter = 0
             for line in f1:
                 matchpointsBot = data_pattern.search(line)
                 if matchpointsBot is not None:
                     savepointsBot = matchpointsBot.group(0)
                     if iter < 10:
                         # Save Data used to input x,y,z locations
                         cleanpointsBot = savepointsBot[34:48]
                         # Save Mean Value of Data
                         cleanpassBot = savepointsBot[48:60]
                         dataBot.append(cleanpointsBot)
                         data_passBot.append(cleanpassBot)
                     if iter < 999 and iter >= 10:
                         # Save Data used to input x,y,z locations
                         cleanpointsBot = savepointsBot[35:48]
                         # Save Mean Value of Data
                         cleanpassBot = savepointsBot[48:61]
                         dataBot.append(cleanpointsBot)
                         data_passBot.append(cleanpassBot)
                     if iter >= 999: 
                         # Save Data used to input x,y,z locations
                         cleanpointsBot = savepointsBot[34:50]
                         # Save Mean Value of Data
                         cleanpassBot = savepointsBot[51:63]
                         dataBot.append(cleanpointsBot)
                         data_passBot.append(cleanpassBot)
                     iter = iter +1
                     if iter == points:
                         break
         if matchx is not None:
             iterx = 0
             for line in f1:
                 matchx2 = data_pattern.search(line)
                 if matchx2 is not None:
                     savex = matchx2.group(0)
                     cleanx = savex[24:]
                     Xdata.append(cleanx)
                     iterx = iterx +1
                     if iterx == Xpoints:
                         break
         if matchyTop is not None:
             itery = 0
             for line in f1:
                 matchy2 = data_pattern.search(line)
                 if matchy2 is not None:
                     savey = matchy2.group(0)
                     cleany = savey[24:]
                     Ydata.append(cleany)
                     itery = itery +1
                     if itery == Ypoints:
                         break
         if matchyBot is not None:
             itery = 0
             for line in f1:
                 matchyBot = data_pattern.search(line)
                 if matchyBot is not None:
                     saveyBot = matchyBot.group(0)
                     cleanyBot= saveyBot[24:]
                     YdataBot.append(cleanyBot)
                     itery = itery +1
                     if itery == Ypoints:
                         break
         if matchz is not None:
             iterz = 0
             for line in f1:
                 matchz2 = data_pattern.search(line)
                 if matchz2 is not None:
                     savez = matchz2.group(0)
                     cleanz = savez[23:]
                     Zdata.append(cleanz)
                     iterz = iterz +1
                     if iterz == Zpoints:
                         break
    if __name__ == '__main__':
        with open(name+'.txt', 'r') as f1:
         with open('STAR_Heat', 'wb') as f2:
             SERPENTExtract(f1,f2)
    ##########################################################
    #### Print Data to CSV in format recognized by STAR-CCM+ #
    ##########################################################
    Np = range(points)
    nx = range(1,Xpoints+1)
    ny = range(1,Ypoints+1)
    nz = range(1,Zpoints+1)
    data_pass = [float(i) for i in data_pass]
    data_passBot = [float(i) for i in data_passBot]
    Xdata = [float(i) for i in Xdata]
    Ydata = [float(i) for i in Ydata]
    YdataBot = [float(i) for i in YdataBot]
    Zdata = [float(i) for i in Zdata]
    # saves fuel data
    data_fuelpass = [float(i) for i in data_fuelpass]
    # Converts Data to be written to CSV
    for point in Np:
     # Sets first and last set of Volumetric Heating to Zero, since this will define the Volumetric Heating Test Section
     if point <= Ypoints:
         data_pass[point] = data_pass[point]*0
         data_passBot[point] = data_passBot[point]*0
     elif point >= points-Ypoints:
         data_pass[point] = data_pass[point]*0
         data_passBot[point] = data_passBot[point]*0
     else:
     # Converts Mean Values of MeV/cm^3 to J/m^3-s to pass to STAR-CCM+ 
         data_pass[point] = (data_pass[point]*1E6)/timestep
         data_passBot[point] = (data_passBot[point]*1E6)/timestep
    # Converts cm to m
    for xpoint in nx:
     # Note: Due to STAR-CCM+ being a 2-D simulation, X-Values (which would be Z Values) are set to zero
     Xdata[xpoint-1] = (Xdata[xpoint-1]-20.405)*0
    for ypoint in ny:
        # Y-Values stay the same in both codes (subtract SERPENT Distance from Origin to get STAR-CCM+ relative distance)
        Ydata[ypoint-1] = -1*(Ydata[ypoint-1]-40.605)/100
        # Bottom data uses "negative" position values
        YdataBot[ypoint-1] = -1*(YdataBot[ypoint-1]-40.605)/100
    for zpoint in nz:
     # Note: Due to orientation of STAR-CCM+ simulation Z Values are X Values in STAR
     Zdata[zpoint-1] = (Zdata[zpoint-1]/-100)+2.267903
    # Organizes Data to be passed to csv
    # Passes Top Data
    with open(r'STAR_HeatTop.csv', 'wb') as f2:
        # Sets up Title Headers for STAR-CCM+
        Title = ['X(m)', 'Y(m)', 'Z(m)', 'VolumetricHeat(W/m^3)']
        csv_writer = csv.writer(f2)
        csv_writer.writerow(Title)
    # Iterates through the number of points given in the SERPENT Output
        for point in Np:
         # Finds the integers used by SERPENT to show Z,Y,X Locations
         temp = re.findall(r'\d+', data[point])
         res = list(map(int,temp))
         # Replaces X integer with actual location from SERPENT Output
         for xpoint in nx:
             if res[2] == xpoint:
                 res[2] = Xdata[xpoint-1]
         # Replaces Y integer with actual location from SERPENT Output
         for ypoint in ny:
             if res[1] == ypoint:
                 res[1] = Ydata[ypoint-1]
         # Replaces Z Integer with actual location from SERPENT Output
         for zpoint in nz:
             if res[0] == zpoint:
                 res[0] = Zdata[zpoint-1]
         # Adds Mean Value for that location
         res.append(data_pass[point])
         # Writes to csv
         csv_writer.writerow(res)
    # Passes Bottom Data
    with open(r'STAR_HeatBot.csv', 'wb') as f2:
        # Sets up Title Headers for STAR-CCM+
        Title = ['X(m)', 'Y(m)', 'Z(m)', 'VolumetricHeat(W/m^3)']
        csv_writer = csv.writer(f2)
        csv_writer.writerow(Title)
    # Iterates through the number of points given in the SERPENT Output
        for point in Np:
         # Finds the integers used by SERPENT to show Z,Y,X Locations
         temp = re.findall(r'\d+', data[point])
         res = list(map(int,temp))
         # Replaces X integer with actual location from SERPENT Output
         for xpoint in nx:
             if res[2] == xpoint:
                 res[2] = Xdata[xpoint-1]
         # Replaces Y integer with actual location from SERPENT Output
         for ypoint in ny:
             if res[1] == ypoint:
                 res[1] = YdataBot[ypoint-1]
         # Replaces Z Integer with actual location from SERPENT Output
         for zpoint in nz:
             if res[0] == zpoint:
                 res[0] = Zdata[zpoint-1]
         # Adds Mean Value for that location
         res.append(data_passBot[point])
         # Writes to csv
         csv_writer.writerow(res)
        time_counter = 0
    if curtime == 0:
        ##############################################
        # Setup the STAR-CCM+ Simulation             #
        ###############################################
        # Simply submits STAR-CCM+ submission script to server
        run_STAR1 = "qsub STARTop_Job.sh"
        run_STAR2 = "qsub STARBot_Job.sh"
        os.system(run_STAR1)
        os.system(run_STAR2)
    if curtime > 0:
        # Write SERPENTDone.txt file indicating that the current loop has been completed and data extracted
        file_out = open('./SerpentDone.txt','w')
        file_out.write('Done')
        file_out.close
        time.sleep(60)
        os.remove('SerpentDone.txt')

    # check to see if STAR is done executing
    STARBot = r'./STARBotDone.txt'
    STARTop = r'./STARTopDone.txt'
    time_to_wait = 1000000
    time_counter = 0
    while not os.path.exists(STARTop):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:break
    while not os.path.exists(STARBot):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:break
    ###########################
    # Update Top interface        #
    ###########################
    os.remove('HE3TOP.ifc')
    file_out = open('HE3TOP.ifc', 'w')
    
    file_out.write('2  He3Top 0\n')
    
    # Write the mesh type
    
    file_out.write('1\n')
    
    # Write the mesh data (NX XMIN XMAX NY YMIN YMAX NZ ZMIN ZMAX)
    
    file_out.write('1 -100 100 1 0 100 500 -60.48375 60.48375\n')
    
    # Check to see if STAR-CCM_ .csv file has been created and wait for a predetermined amount of time if it hasn't
    time_to_wait = 1000000
    time_counter = 0
    filename = r'./ExtractedData/He3Data_table_'+str(STAR_STEP)+'.csv'
    while not os.path.exists(filename):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:break
    if os.path.isfile(filename):
        # Take the data from STAR-CCM+ .csv file and write to ifc
        columns = ['Position in Cartesian 1[X] (cm)', 'Density(g/cm^3) (kg/m^3)', 'Temperature (K)']
        df = pd.read_csv(filename, usecols=columns)
        # Position = df['Position in Cartesian 1[X] (cm)']
        # Density =  df['Density(g/cm^3) (kg/m^3)']
        # Temp = df['Temperature (K)']
        
        # Sorts data from STAR-CCM+ in ascending order by position
        df_convert = df.to_numpy()
        numpy_array = df_convert[df_convert[:, 0].argsort()]
        
        # Cross Section Data for He-3 in SERPENT2 only exists for 300 K or above, this will only happen early on in the transient and temp
        # should never fall that far below 300K so setting this arbitrary constraint should have minimal change in results
        for i in range(STAR_Points):
            if numpy_array[i,2] < 300.0:
                numpy_array[i,2] = 300.0
        denstemp = numpy_array[:,[1,2]]
        np.savetxt(file_out,denstemp, fmt = "%1.6f")
    else:
        raise ValueError("%s has not been created or could not be read" % filename)
    # Close interface file 
    
    file_out.close()
    ###########################
    # Update Bottom interface        #
    ###########################
    os.remove('HE3BOT.ifc')
    file_out = open('HE3BOT.ifc', 'w')
    
    file_out.write('2  He3Bot 0\n')
    
    # Write the mesh type
    
    file_out.write('1\n')
    
    # Write the mesh data (NX XMIN XMAX NY YMIN YMAX NZ ZMIN ZMAX)
    
    file_out.write('1 -100 100 1 0 -100 500 -60.48375 60.48375\n')
    
    # Check to see if STAR-CCM_ .csv file has been created and wait for a predetermined amount of time if it hasn't
    time_to_wait = 1000000
    time_counter = 0
    filename = r'./ExtractedBotData/He3Data_table_'+str(STAR_STEP)+'.csv'
    while not os.path.exists(filename):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:break
    if os.path.isfile(filename):
        # Take the data from STAR-CCM+ .csv file and write to ifc
        columns = ['Position in Cartesian 1[X] (cm)', 'Density(g/cm^3) (kg/m^3)', 'Temperature (K)']
        df = pd.read_csv(filename, usecols=columns)
        # Position = df['Position in Cartesian 1[X] (cm)']
        # Density =  df['Density(g/cm^3) (kg/m^3)']
        # Temp = df['Temperature (K)']
        
        # Sorts data from STAR-CCM+ in ascending order by position
        df_convert = df.to_numpy()
        numpy_array = df_convert[df_convert[:,0].argsort()]
        
        # Cross Section Data for He-3 in SERPENT2 only exists for 300 K or above, this will only happen early on in the transient and temp
        # should never fall that far below 300K so setting this arbitrary constraint should have minimal change in results
        for i in range(STAR_Points):
            if numpy_array[i,2] < 300.0:
                numpy_array[i,2] = 300.0
        denstemp = numpy_array[:,[1,2]]
        np.savetxt(file_out,denstemp, fmt = "%1.6f")
    else:
        raise ValueError("%s has not been created or could not be read" % filename)
    # Close interface file 
    
    file_out.close()
    # Update STAR_STEP by number of steps that STAR takes before updating data
    STAR_STEP += step_length

    ###########################
    # Calculate TH-solution for fuel   #
    ###########################

    # Fuel specific heat capacity

    cp = 998  # J/(kg*K)

    # Calculate EOI temperatures at (nz) axial nodes
    # No heat transfer, just deposition

    for i in range(10):
        # Calculate EOI temperature based on BOI temperature
        # and energy deposition during current time interval

        # Calculate mass of this node (in kg) (z-slice of reactor)
        #   Area of Active Fuel (cm^2)  * Length of Node (cm) * density (g/cm^3)  * conversion (g to kg)
        #   314 Fuel Assemblies (93.16 cm^2 each)
        #   20 Control Rod Assemblies ( Fuel Assembly Area - Control Rod Area) (65.65 cm^2 each)
        #   4 HENRI Assemblies (Fuel Assembly Area - HENRI Area) (73.53 cm^2)
        #   Density of Fuel assumed to be 1.72 g/cm^3 (mostly Graphite)
        #   z-slice (10 slices / total length of reactor (121 cm))

        m = ((93.16*314)+(65.65*20)+(75.53*4)) * 12.1 * 1.72 * 1e-3

        # Calculate initial heat in this axial node

        Q = TBOI[i] * (cp * m)

        # The interface output is Joules in case of time dependent
        # simulation, no need to multiply with time step

        dQ = data_fuelpass[i]

        # Calculate new temperature based on new amount of heat

        TEOI[i] = (Q + dQ) / (cp * m)

    ###########################
    # Update interface        #
    ###########################

    file_out = open('./fuel.ifc', 'w')

    # Write the header line (TYPE MAT OUT)

    file_out.write('2 fuel 0\n')

    # Write the mesh type

    file_out.write('1\n')

    # Write the mesh size (NX XMIN XMAX NY YMIN YMAX NZ ZMIN ZMAX)

    file_out.write('1 -500 500 1 -500 500 10 -60.48375 60.48375\n')

    # Write updated fuel temperatures

    for i in range(10):
        # Use the base density throughout the simulation
        # Write density and temperature at this layer

        file_out.write('-1.72 {}\n'.format(TEOI[i]))

    file_out.close()

    ##########################################################
    # Tell code to move to next timestep #
    ##########################################################
    file_out = open('com.in','w')
    file_out.write(str(signal.SIGUSR2))
    file_out.close()

    ##########################################################
    # Archive Files                                      #####
    ##########################################################
    copyfile('HE3TOP.ifc','Archive/HE3TOP.ifc'+str(curtime))
    copyfile('HE3BOT.ifc','Archive/HE3BOT.ifc'+str(curtime))
    copyfile('fuel.ifc', 'Archive/fuel.ifc' + str(curtime))
    copyfile('STAR_HeatTop.csv','Archive/Star_HeatTop'+str(curtime)+'.csv')
    copyfile('STAR_HeatBot.csv','Archive/Star_HeatBot'+str(curtime)+'.csv')
    if curtime >= 2:
        copyfile('coupledTreat_res.m','Archive/coupledTreat_res'+str(curtime)+'.m')
    # Delete Files that are not needed between iterations
    os.remove(STARTop)
    os.remove(STARBot)
    os.remove(textfile)
    # Increment time step
    curtime += 1

    # Copy EOI temperatures to BOI vector

    for i in range(10):
        TBOI[i] = TEOI[i]
    ####################################
     # Check if simulation has finished #
    ####################################
    if (simulating == 0):
           break

    time.sleep(5)
    file_out = open('com.in','w')
    file_out.write(str(signal.SIGUSR2))
    file_out.close()