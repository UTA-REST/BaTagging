################################################################################
#
#                              reproducability.py
#   Scrapes and processes spectroscope data from directory for use in
#   photobleaching studies.
#
################################################################################

### Declare Global Variables ###
Base="C:\\Users\\mcdonaldad\\Desktop\\Photobleach\\"
verbose = True # Boolean for diagnostic information
Long_Dye = "Fluoroscine-4" # Full name of dye for graph labels
Long_Concentration = "0.5 $\mu$M" # Concentration for graph labels
Integration_Time = "10000 ms" # Integration time of run
Laser_Power = "257 $\mu$W" # Laser power of run
Run = "Run2" # Run number from directory
Dye = "Fluo4" # Dye name from directory
Concentration = "0.5micromol" # Dye concentration from directory
Trace = "Spectrum-b" # Trace name from directory (a is raw, b is averaged[10])
Path = Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+Trace+"\\" # Pathname of .csv file directory
prefix = "Fluo4" # Text appended to the beginning of every file name
suffix = "0.5uMb" # Text appended to the end of every file name
Filter = 515 # Filter used in run (in nm)
ToPlt = "Compare" # Descriminator to make plots ('Raw','Corrected','Compare','Rel','Frac')

OutName=Dye+'_'+Concentration+'_'+Run+'_'+Trace+'_'

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
cDATA = dict()
W,I=[],[] # Arrays for holding lists of raw Wavelength and Intensity values
datacut = dict() # Dictionary for holding relevant wavelengths
intensity = dict() # Dictionary for holding the integral of datacut
INT = [] # Array for holding intensity
leng = len(files) # Length of the list of files.
times = [] # Array for holding a list of the times. Each entry is of form [Hours, Minutes, Seconds, Milliseconds]
clocks = [] # Array for holding a list reformated from times to be of form Hours:Minutes:Seconds:Milliseconds
exposure_time = [] # Array for holding the time, in seconds, from the first file
corrected_time = [] # Array to hold the time corrected for false starts

# <codecell>
### Compile list of files ###

#========================#
# This for loop is nasty #
#========================#

for file in glob.glob(Path+"*.csv"): # Crawls over Path directory looking for .csv files and:
    filename=file.split("\\") # Splits the filename out of the pathname using \\ as the delimiter
    filename2=filename[9]
    filename3=filename2.split(prefix)
    filename4=filename3[1]
    filename5=filename4.split(suffix)
    filename6=filename5[0]
    filename7=filename6.split("_")
    time=filename7[1:]
    times.append(time)
    files.append(filename[9]) # Adds the 10th string value to the files array

if verbose==True: # When True:
    print("Files array:\n",files) # Prints the files array
    print("Times array:\n",times)

t0=(int(times[0][0])*3600)+(int(times[0][1])*60)+(int(times[0][2]))+(int(times[0][3])*0.001)
for each in times:
    clock=each[0] + ":" + each[1] + ":" + each[2] + ":" + each[3]
    elapsed_time=((int(each[0])*3600)+(int(each[1])*60)+(int(each[2]))+(int(each[3])*0.001))-t0
    clocks.append(clock)
    exposure_time.append(int(elapsed_time))

if verbose==True: # When True:
    print("Exposure time array:\n",exposure_time) # Prints the files array
    print("Clocks array:\n",clocks)

#TODO: Rationalize this cell.

# <codecell>
### Scrape data from files array ###
for i, file in enumerate(files): # For each file in files:
    DATA[i]=pd.read_csv(Path+files[i],delimiter=';',names=['Wavelength','Intensity'],
                        skiprows=33,skipfooter=1,engine='python') # Dictionary with key, i, mapped from .csv file
    W.append(np.array(DATA[i]['Wavelength'],dtype=float)) # Wavelength from dictionary appended to array
    I.append(np.array(DATA[i]['Intensity'],dtype=float)) # Intensity from dictionary appended to array

    DATA[i]['diff']=DATA[i]['Intensity'].diff().abs() # Calculates the absolute value of the difference between neighboring intensity values
    DATA[i]=DATA[i][DATA[i]['diff']<0.002] # Descriminates large jumps in intensity out of the DATA dictionary

    datacut[i]=DATA[i][(DATA[i]['Wavelength']>Filter)] #& (DATA[i]['Wavelength']<600)] # Limits the wavelength between two values
    intensity[i] = integrate.trapz(datacut[i]['Intensity'],datacut[i]['Wavelength']) # Calculates the integral of datacut
    INT.append(intensity[i]) # Appends the integral to the INT array

if verbose==True: # When True
    print("Length of DATA dictionary=",len(DATA)) # Prints the number of pairs in the dictionary
    print("Length of INT dictionary=",len(INT))
#TODO: Save data for time profile

# <codecell>
################################################################################
#                                                                              #
#     **Skip this Cell to show graphs with no files removed from the lists**   #
#                                                                              #
################################################################################

### Dispose of data preceeding max ###
Cut=INT.index(max(INT)) # Identifies the file number with the maximum intensity
Redundant = np.arange(0,Cut) # An array with sequential integer values up to the Cut
for n in Redundant: # For each number in Redundant:
    del DATA[n] # Delete the key and value in DATA related to that number
for i,trace in enumerate(DATA): # For each key in DATA
    DATA[i] = DATA.pop(i+Cut) # Map the old key to the new key
del W[:Cut] # Delete the wavelength data preceeding the cut
del I[:Cut] # Delete the intensity data preceeding the cut
del INT[:Cut] # Delete the integral data preeceeding the cut
del exposure_time[:Cut] # Delete the time data preceeding the cut

corrected_time = []
for i, m in enumerate(exposure_time):
    corrected_time.append(exposure_time[i]-exposure_time[0])

if verbose == True:
    print(len(DATA))
    print(len(INT))
    print(corrected_time)

# <codecell>
### Plots spectroscope data ###
peak=max(datacut[Cut]["Intensity"])

#for i in range(len(DATA)): # For each file:
for i in np.arange(0,9): # For a small script-testing sample:
    textstr="{}\nConcentration={}\nIntegration Time={}\nLaser Power={}\nFilter={} nm\n{}".format(Long_Dye,Long_Concentration,Integration_Time,Laser_Power,Filter,clocks[i])

    yfrac = 1-((peak-DATA[i]["Intensity"])/peak)
    yrel = 1-(peak-DATA[i]["Intensity"])

    if ToPlt == "Frac":
        if verbose == True:
            print("Plot is ","Fractional")

        plt.Figure()
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i]))
        plt.scatter(DATA[i]["Wavelength"],yfrac,linewidth=1)
        plt.xlim(400,600)
        plt.ylim(0,1)
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top')
        plt.show()

    if ToPlt == "Rel":
        if verbose == True:
            print("Plot is ","Relative")

        plt.Figure()
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i]))
        plt.scatter(DATA[i]["Wavelength"],yrel,linewidth=1)
        plt.xlim(400,600)
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top')
        plt.show()

    if ToPlt == "Compare":
        if verbose == True:
            print("Plot is ","Comparative")

        plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i]))
        plt.scatter(W[i],I[i],color="r",linewidth=1) # Plots the wavelength versus intensity using raw data
        plt.scatter(DATA[i]["Wavelength"],DATA[i]["Intensity"],color="b",linewidth=1) # Plots the wavelength versus intensity
        plt.axvline(x=Filter, color="k", linestyle="dashed") # Adds a vertical, dashed line to the graph at the filter location
        plt.xlim(400,600) # Narrows the x-axis to the relevant field of view
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top')
        plt.show() # Outputs plot

    if ToPlt == "Corrected":
        if verbose == True:
            print("Plot is ","Corrected")

        plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i]))
        plt.scatter(DATA[i]["Wavelength"],DATA[i]["Intensity"],color="b",linewidth=1) # Plots the wavelength versus intensity
        plt.axvline(x=Filter, color="k", linestyle="dashed") # Adds a vertical, dashed line to the graph at the filter location
        plt.xlim(400,600) # Narrows the x-axis to the relevant field of view
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top')
        plt.show() # Outputs plot

    if ToPlt == "Raw":
        if verbose == True:
            print("Plot is ","Raw")

        plt.Figure()
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i]))
        plt.scatter(W[i],I[i],color="r",linewidth=1) # Plots the wavelength versus intensity using raw data
        plt.xlim(400,600) # Narrows the x-axis to the relevant field of view
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top')
        plt.show() # Outputs plot

#TODO: Save all figures

# <codecell>
### Graphs the time profile ###
figuretext="{}\nConcentration={}\nIntegration Time={}\nLaser Power={}\nFilter={} nm".format(Dye,Concentration,Integration_Time,Laser_Power,Filter)
plt.figure(figsize=(10,10),linewidth=2)
plt.scatter(corrected_time,INT/max(INT), linewidth=1)
plt.title("Relative Integral of Spectra",fontsize=15)
plt.xlabel("Time (seconds)", fontsize=15)
plt.ylabel("Light yield (arb. units)",fontsize=15)
plt.annotate(figuretext, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
            horizontalalignment='right', verticalalignment='top')
plt.xlim(0,corrected_time[len(corrected_time)-1])
plt.savefig(Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+OutName+'.pdf')
plt.show()

# <codecell>
