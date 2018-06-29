### Declare Global Variables ###
Base="C:\\Users\\mcdonaldad\\Desktop\\Photobleach\\"
verbose = True # Boolean for diagnostic information
BinSize = 0 # Number of files to bin together for adding
Dye = "Fluo4"
Concentration = "1micromol"
Run="Run4"
Trace="Spectrum-b"
Path=Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+Trace+"\\"
Filter=500

# <codecell>
### Import Libraries ###
import csv # Module for reading .csv files
import numpy as np # Module for array manipulation
import matplotlib # Module for graphical representation
import matplotlib.pyplot as plt # Module for graphing
import matplotlib.patches as mpatches # Module for label handlers
import matplotlib.cm as cm
import os # Module for operating system manipulation
import glob # Module for file and directory name manipulation
import pandas as pd # Module for database manipulation
import pylab
import math # Module for math functions
from scipy import integrate # Module for integration

# <codecell>
### Instantiate Arrays and Dictionaries ###
files = [] # Array for holding a list of files
DATA = dict() # Dictionary for holding data from files
W,I=[],[] # Arrays for holding lists of Wavelength and Intensity values
datacut = dict() # Dictionary for holding relevant wavelengths
intensity = dict() # Dictionary for holding the integral of datacut
INT = [] # Array for holding intensity
leng = len(files) # Length of the list of files.

# <codecell>
### Compile list of files ###
for file in glob.glob(Path+"*.csv"): # Crawls over Path directory looking for .csv files and:
    filename=file.split("\\") # Splits the filename out of the pathname using \\ as the delimiter
    files.append(filename[9]) # Adds the 10th string value to the files array

if verbose==True: # When True:
    print(files) # Prints the files array

# <codecell>
### Scrape data from files array ###
for i, file in enumerate(files): # For each file in files:
    DATA[i]=pd.read_csv(Path+files[i],delimiter=';',names=['Wavelength','Intensity'],skiprows=33,skipfooter=1,engine='python') # Dictionary with key, i, mapped to .csv file
    W.append(np.array(DATA[i]['Wavelength'],dtype=float)) # Wavelength from dictionary appended to array
    I.append(np.array(DATA[i]['Intensity'],dtype=float)) # Intensity from dictionary appended to array
    DATA[i]['diff']=DATA[i]['Intensity'].diff().abs() # Calculates the absolute value of the difference between neighboring intensity values
    DATA[i]=DATA[i][DATA[i]['diff']<0.002] # Descriminates large jumps in intensity out of the DATA dictionary
    datacut[i]=DATA[i][(DATA[i]['Wavelength']>Filter)] #& (DATA[i]['Wavelength']<600)] # Limits the wavelength between two values
    intensity[i] = integrate.trapz(datacut[i]['Intensity'],datacut[i]['Wavelength']) # Calculates the integral of datacut
    INT.append(intensity[i]) # Appends the integral to the INT array

if verbose==True: # When True:
    print(len(DATA)) # Prints the number of pairs in the dictionary

# <codecell>
### Plots data ###
integration_time_patch=mpatches.Patch(label="Integration Time = 2000ms (avg.10)") # Creates legend handler
Concentration_patch=mpatches.Patch(label="Concentration = 1$\mu$M") # Creates legend handler
Power_patch=mpatches.Patch(label="Laser Power = 249$\mu$W") # Creates legend handler

for i in range(len(DATA)):
    plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
    plt.xlim(400,600) # Narrows the x-axis to the relevant field of view
    plt.scatter(W[i],I[i],color="r") # Plots the wavelength versus intensity using raw data
    plt.scatter(DATA[i]["Wavelength"],DATA[i]["Intensity"],color="b") # Plots the wavelength versus intensity
    plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
    plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
    filterline = plt.axvline(x=Filter, color="k", label="Filter = {}nm".format(Filter), linestyle="dashed") # Adds a vertical, dashed line to the graph at the filter location
    plt.legend(handles=[integration_time_patch, Concentration_patch, Power_patch, filterline],fontsize=7) # Builds the legend
    plt.show() # Outputs plot

x_axis=np.arange(0,len(INT))

plt.figure(linewidth=2)
plt.scatter(x_axis,INT/INT[0])
plt.title("Relative Integral of Spectra",fontsize=15)
plt.xlabel("Time (min)", fontsize=15)
plt.ylabel("Light yield (arb. units)",fontsize=15)
plt.legend(handles=[integration_time_patch, Concentration_patch, Power_patch],fontsize=7)
plt.xlim(0)
plt.show()

# <codecell>
