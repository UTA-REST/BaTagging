### Declare Global Variables ###
Path="C:\\Users\\mcdonaldad\\Desktop\\Photobleach\\Fluo4\\1micromol\\Run4\\Spectrum-b\\" # Defines the pathname in the Master Branch
verbose = True # Boolean for diagnostic information
BinSize = 0 # Number of files to bin together for adding
Dye = "Fluo4"
Concentration = "1micromol"

# <codecell>
### Import Libraries ###
import csv # Module for reading .csv files
import numpy as np # Module for array manipulation
import matplotlib # Module for graphical representation
import matplotlib.pyplot as plt # Module for graphing
import matplotlib.cm as cm
import os # Module for operating system manipulation
import glob # Module for file and directory name manipulation
import pandas as pd # Module for database manipulation
import pylab
import math
from scipy import integrate

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
    files.append(filename[9]) # Adds the 2nd string value to the files array

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
    datacut[i]=DATA[i][(DATA[i]['Wavelength']>400) & (DATA[i]['Wavelength']<600)] # Limits the wavelength between two values
    intensity[i] = integrate.trapz(datacut[i]['Intensity'],datacut[i]['Wavelength']) # Calculates the integral of datacut
    INT.append(intensity[i]) # Appends the integral to the INT array

if verbose==True: # When True:
    print(len(DATA)) # Prints the number of pairs in the dictionary

# <codecell>
### Plots data ###
for i in range(len(DATA)):
    plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
    plt.scatter(W[i],I[i],color="r") # Plots the wavelength versus intensity using raw data
    plt.scatter(DATA[i]["Wavelength"],DATA[i]["Intensity"],color="b") # Plots the wavelength versus intensity
    plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
    plt.ylabel("Intensity (arb. Units)",fontsize=15) # Adds a label to the y axis and declares the font size
    plt.show() # Outputs plot

x=np.arange(0,len(INT))
plt.scatter(x,INT)
plt.show()
# <codecell>
