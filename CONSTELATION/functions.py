# Functions and Classes for CONSTELATION
import os
import signal
import math
import time
import csv
import pandas as pd
import numpy as np
import re
from shutil import copyfile
import serpentTools

#################
## CLASSES     ##
#################
# classes for holding info about ifc and csv files
class Serpent_ifc(object):
    """ interface file object

    Attributes
    ----------
    name : name of ifc file 'he3.ifc'
    header : header of ifc file (TYPE MAT OUT) '2 he3 0\n'
    type : mesh type of ifc file '1\n'
    mesh : mesh of ifc file (NX XMIN XMAX NY YMIN YMAX NZ ZMIN ZMAX)
    data : density and temperature data for ifc file
    """
    def __init__(self,name,header,mesh_type,mesh):
        self.name = name
        self.header = header
        self.mesh_type = mesh_type
        self.mesh = mesh
        self.data = np.array([])

class STAR_csv(object):
    """ STAR-CCM+ csv file object

    Attributes
    ----------
    name : name of csv file r'./ExtractedData/He3Data_table.csv'
    header : header of csv file ['Position', 'Density', 'Temperature']
    data : density and temperature data from csv file
    """
    def __init__(self,name,header):
        self.name = name
        self.header = header
        self.data = np.array([])


#################
## FUNCTIONS   ##
#################

def position_Serpent_to_STAR(data,reference_conversion,unit_conversion):
    """ Converts position values from Serpent reference frame to STAR reference frame.

    Parameters
    ----------
    data : float,int,array
        data to be converted
    reference_conversion : float,int
        translation from Serpent reference to STAR reference
    unit_conversion : float,int
        unit conversion factor from Serpent reference to STAR reference

    Returns
    -------
    data : float,int,array
        converted data
    """
    data = (data-reference_conversion)*unit_conversion
    return data

# function to write out Serpent heating data to STAR csv
def SerpentHeat_to_Star_csv(detector,STAR_csv,reference_conversion,unit_conversion):
    """ Writes Serpent heating detector data out to csv file for STAR to read.

    Parameters
    ----------
    detector : serpentTools Detector object

    outfile : str
        file to open and write to
    title : str or list of str
        header to write on first row of csv file
    """
    outfile = STAR_csv.name
    title = STAR_csv.header
    row = np.zeros(4)
    with open(outfile, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(title)
        for zpoint in range(detector.tallies.shape[0]):
            for ypoint in range(detector.tallies.shape[1]):
                row[0] = position_Serpent_to_STAR(detector.grids['Z'][zpoint,2],reference_conversion[2],unit_conversion[2])
                row[1] = position_Serpent_to_STAR(detector.grids['Y'][ypoint,2],reference_conversion[1],unit_conversion[1])
                row[2] = position_Serpent_to_STAR(detector.grids['X'][0,2],reference_conversion[0],unit_conversion[0])
                row[3] = detector.tallies[zpoint,ypoint]*cm3_to_m3/timestep     # required to match units between the two sims. from J/cm^3 to W/m^3
                csv_writer.writerow(row)

# functions for writing data to ifc files
# function to fix any temps below 300K for helium-3 cross sections
def min_temp_fix(array):
    """ Fixes any temperatures below 300K to be 300K for Serpent 2 cross section data

    Parameters
    ----------
    array : numpy array [position, density, temperature]

    Returns
    -------
    array : numpy array [position, density, temperature] with fixed values
    
    """
    for point in range(len(array)):
        if array[point,2] < 300.0:
            array[point,2] = 300.0
    return array

# function to read in csv and convert from pandas to numpy array (should maybe just use numpy array to read in the first place?)
def read_to_numpy(STAR_csv):
    """ Reads in data from STAR-CCM+ csv file, converts the data to a numpy array, and sorts the data by position.

    Parameters
    ----------
    STAR_csv : STAR_csv object

    Returns
    -------
    data : numpy array
    
    """
    file_in = STAR_csv.name
    columns = STAR_csv.header
    data = pd.read_csv(file_in,usecols=columns)
    data = data.to_numpy()
    data = data[data[:,0].argsort()]
    return data

# function to fix density units from STAR to Serpent 2
def density_STAR_to_Serpent(density):
    density = density / 1000 * -1
    return density

# function to write data from csv file to ifc file
# writes only the density and temperature data, not the position values
# the Serpent interface does not use the position values, since the positions are defined in the Serpent model
def csv_to_ifc(STAR_csv,Serpent_ifc):
    """ Reads in density and temperature data from STAR-CCM+ csv file and writes it to a Serpent 2 ifc file.

    Parameters
    ----------
    STAR_csv : STAR_csv object
        csv file to read from
    Serpent_ifc : Serpent_ifc object
        ifc file to write to
    """
    f = open(Serpent_ifc.name,'w')
    f.write(Serpent_ifc.header)
    f.write(Serpent_ifc.mesh_type)
    f.write(Serpent_ifc.mesh)

    data = read_to_numpy(STAR_csv)
    data[:,1] = density_STAR_to_Serpent(data[:,1])
    data = min_temp_fix(data)
    np.savetxt(f, data[:,[1,2]], fmt="%1.6f")

    f.close()

# function to pull keff from _res.m file and append it to a csv file
def keff_res_to_csv(f_in,f_out,time):
    """ Reads in Keff from Serpent 2 results file and appends it to a csv file

    Parameters
    ----------
    f_in : str
        Serpent 2 results file (_res.m)
    f_out : str
        csv file to append to
    """
    res = serpentTools.read(f_in)
    array = np.zeros([1,3])
    array[0,0] = time
    array[0,1] = res.resdata['anaKeff'][0]   # k value
    array[0,2] = res.resdata['anaKeff'][1]   # associated error value
    with open(f_out,'a') as csvfile:
        np.savetxt(csvfile,array,delimiter=',',fmt='%.8e')

# function to handle waiting for file creation which happens a lot during the execution
def wait_for_file(file,wait):
    time_count = 0
    while not os.path.isfile(file):
        time.sleep(1)
        time_count += 1
        if time_count > wait:
            raise ValueError("%s has not been created or could not be read" % file)
        
# function to check if a com file has a number
def com_check_digit(line,sig_notdigit):
    f_digit = line.strip('-\n\r').isdigit()
    if f_digit:
        line_int = int(line)
    elif not f_digit:
        line_int = sig_notdigit
    else:
        print('The com.out file does not exist or cannot be read.')
    return line_int

