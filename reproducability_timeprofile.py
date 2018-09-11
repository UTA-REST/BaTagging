################################################################################
#
#                              reproducability.py
#   Scrapes and processes spectroscope data from directory for use in
#   photobleaching studies.
#
################################################################################

### Declare Global Variables ###
Base="C:\\Users\\mcdonaldad\\Desktop\\Photobleach\\"
Dye = "Rhod5" # Dye name from directory
Concentration = "1micromol" # Dye concentration from directory
Run = "Run2" # Run number from directory
Trace = "Spectrum-b" # Trace name from directory (a is raw, b is averaged[10])
Path = Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+Trace+"\\" # Pathname of .csv file directory

verbose = True # Boolean for diagnostic information
savefig = True # Boolean for saving images
savedata = True # Boolean for saving data
ToPlt = "Compare" # Descriminator to make plots ('Raw','Corrected','Compare','Rel','Frac')

Long_Dye = "Rhodamine-2" # Full name of dye for graph labels
Long_Concentration = "0.1 $\mu$M" # Concentration for graph labels
Integration_Time = "2000 ms" # Integration time of run
Laser_Power = "698 $\mu$W" # Laser power of run
Filter = 570 # Filter used in run (in nm)

prefix = "Rhod5" # Text appended to the beginning of every file name
suffix = "1uM" # Text appended to the end of every file name

OutName = Dye+'_'+Concentration+'_'+Run+'_'+Trace+'_' # Sets name for output file

if verbose == True:
    print("Figure save=",savefig)
    print("Data save=",savedata)
    print("Plot type=",ToPlt)

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
W,I=[],[] # Arrays for holding lists of raw Wavelength and Intensity values
datacut = dict() # Dictionary for holding relevant wavelengths
intensity = dict() # Dictionary for holding the integral of datacut
INT = [] # Array for holding intensity
times = [] # Array for holding a list of the times. Each entry is of form [Hours, Minutes, Seconds, Milliseconds]
clocks = [] # Array for holding a list reformated from times to be of form Hours:Minutes:Seconds:Milliseconds
exposure_time = [] # Array for holding the time, in seconds, from the first file
corrected_time = [] # Array to hold the time corrected for false starts
time = [] # Array to hold time read out of .csv file
rInt = [] # Array to hold relative integral values read out of .csv file

# <codecell>
### Compile list of files ###

#========================#
# This for loop is nasty #
#========================#

for file in glob.glob(Path+"*.csv"): # Crawls over Path directory looking for .csv files and:
    filename=file.split("\\") # Splits the filename out of the pathname using \\ as the delimiter
    filename2=filename[9] # Declares variable for the 10th array value
    filename3=filename2.split(prefix) # Splits the prefix out of the filename
    filename4=filename3[1] # Declares variable for the 2nd array value
    filename5=filename4.split(suffix) # Splits the suffix out of the filename
    filename6=filename5[0] # Declares variable for the 1st array value
    filename7=filename6.split("_") # Splits the date/time with _ as the delimiter
    filename8=filename7[1:] # Declares variable for the array sliced at the 2nd value
    times.append(filename8) # Adds the array of size 4 to the times array
    files.append(filename2) # Adds the 10th string value to the files array

if verbose==True: # When True:
    print("Files array:\n",files) # Prints the files array
    print("Times array:\n",times) # Prints the times array

t0=(int(times[0][0])*3600)+(int(times[0][1])*60)+(int(times[0][2]))+(int(times[0][3])*0.001) # Determines the initial time of the run
for each in times: # For each value in the times array:
    clock=each[0] + ":" + each[1] + ":" + each[2] + ":" + each[3] # Creates a clock string
    elapsed_time=((int(each[0])*3600)+(int(each[1])*60)+(int(each[2]))+(int(each[3])*0.001))-t0 # Determines the time difference in seconds
    clocks.append(clock) # Adds the clock string to the clocks array
    exposure_time.append(int(elapsed_time)) # Adds the time difference to the exposure_time array

if verbose==True: # When True:
    print("Exposure time array:\n",exposure_time) # Prints the exposure array
    print("Clocks array:\n",clocks) # Prints the clock array

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
    print("Length of DATA dictionary=",len(DATA)) # Prints the number of pairs in the DATA dictionary
    print("Length of INT dictionary=",len(INT)) # Prints the length of the INT array. Must match DATA length

# <codecell>
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

for i, m in enumerate(exposure_time):
    corrected_time.append(exposure_time[i]-exposure_time[0])

if verbose == True:
    print("Length of corrected DATA dictionary=",len(DATA))
    print("Length of corrected INT dictionary=",len(INT))
    print("Corrected time array:\n",corrected_time)

# <codecell>
### Saves the Time Profile Data to .csv in the run directory ###
if savedata == True: # When saving is active:
    save = Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+"tpd"+"_"+Base+Dye+Concentration+Run+".csv" # Path and name of file
    csv = open(save, "w") # Opens the file to write
    for each, value in enumerate(INT): # For the length of INT:
        x = corrected_time[each] # First column is times (x_axis)
        y = INT[each]/max(INT) # Second column is relative integral values (y_axis)
        row = str(x) + "," + str(y) + "\n" # Sets up each row with delimiter
        csv.write(row) # Writes each row to file
    if verbose == True:
        print("File saved as:",save)
    csv.close()

# <codecell>
### Plots spectroscope data ###
peak=max(datacut[Cut]["Intensity"]) # Determines the maxima of the spectrum

for i in range(len(DATA)): # For each file:
#for i in np.arange(0,9): # For a small test sample:
    textstr="{}\nConcentration={}\nIntegration Time={}\nLaser Power={}\nFilter={} nm\n{}".format(Long_Dye,Long_Concentration,Integration_Time,Laser_Power,Filter,clocks[i])

    yfrac = 1-((peak-DATA[i]["Intensity"])/peak)
    yrel = 1-(peak-DATA[i]["Intensity"])

    if ToPlt == "Frac":
        if verbose == True:
            print("Plot is ","Fractional")

        plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i])) # Adds title to the figure
        plt.scatter(DATA[i]["Wavelength"],yfrac,linewidth=1) # Plots the wavelength versus fractional intensity
        plt.xlim(400,600) # Bounds the x axis
        plt.ylim(0,1) # Bounds the y axis
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top') # Adds text to the figure
        if savefig == True:
            plt.savefig(Path+OutName+"_"+ToPlt+str(i)+'.pdf')
            if verbose == True:
                print("Plot saved to:",Path+OutName+"_"+ToPlt+str(i)+'.pdf')
        plt.show()

    if ToPlt == "Rel":
        if verbose == True:
            print("Plot is ","Relative")

        plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i])) # Adds title to the figure
        plt.scatter(DATA[i]["Wavelength"],yrel,linewidth=1) # Plots the wavelength versus relative intensity
        plt.xlim(400,600) # Bounds the x axis
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top') # Adds text to the figure
        if savefig == True:
            plt.savefig(Path+OutName+"_"+ToPlt+str(i)+'.pdf')
            if verbose == True:
                print("Plot saved to:",Path+OutName+"_"+ToPlt+str(i)+'.pdf')
        plt.show()

    if ToPlt == "Compare":
        if verbose == True:
            print("Plot is ","Comparative")

        plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i])) # Adds title to the figure
        plt.scatter(W[i],I[i],color="r",linewidth=1) # Plots the wavelength versus intensity using raw data
        plt.scatter(DATA[i]["Wavelength"],DATA[i]["Intensity"],color="b",linewidth=1) # Plots the wavelength versus intensity
        plt.axvline(x=Filter, color="k", linestyle="dashed") # Adds a vertical, dashed line to the graph at the filter location
        plt.xlim(400,600) # Bounds the x axis
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top') # Adds text to the figure
        if savefig == True:
            plt.savefig(Path+OutName+"_"+ToPlt+"{}".format(i)+'.pdf')
            if verbose == True:
                print("Plot saved to:",Path+OutName+"_"+ToPlt+str(i)+'.pdf')
        plt.show() # Outputs plot

    if ToPlt == "Corrected":
        if verbose == True:
            print("Plot is ","Corrected")

        plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i])) # Adds title to the figure
        plt.scatter(DATA[i]["Wavelength"],DATA[i]["Intensity"],color="b",linewidth=1) # Plots the wavelength versus intensity
        plt.axvline(x=Filter, color="k", linestyle="dashed") # Adds a vertical, dashed line to the graph at the filter location
        plt.xlim(400,600) # Bounds the x axis
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top') # Adds text to the figure
        if savefig == True:
            plt.savefig(Path+OutName+"_"+ToPlt+str(i)+'.pdf')
            if verbose == True:
                print("Plot saved to:",Path+OutName+"_"+ToPlt+"{}".format(i)+'.pdf')
        plt.show() # Outputs plot

    if ToPlt == "Raw":
        if verbose == True:
            print("Plot is ","Raw")

        plt.Figure(figsize=(10,10),linewidth=2) # Instantiates the figure
        plt.title("{} exposed for {} seconds".format(Long_Dye,corrected_time[i])) # Adds title to the figure
        plt.scatter(W[i],I[i],color="r",linewidth=1) # Plots the wavelength versus intensity using raw data
        plt.xlim(400,600) # Bounds the x axis
        plt.xlabel("Wavelength (nm)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.annotate(textstr, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
                    horizontalalignment='right', verticalalignment='top') # Adds text to the figure
        if savefig == True:
            plt.savefig(Path+OutName+"_"+ToPlt+str(i)+'.pdf')
            if verbose == True:
                print("Plot saved to:",Path+OutName+"_"+ToPlt+str(i)+'.pdf')
        plt.show() # Outputs plot

# <codecell>
### Reads previously saved time profile data ###
Data = pd.read_csv(Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+"tpd"+"_"+Base+Dye+Concentration+Run+".csv",delimiter=',',names=['Time','Integral'],
                    engine='python')
time.append(np.array(Data["Time"],dtype=float))
rInt.append(np.array(Data["Integral"],dtype=float))

# <codecell>
### Graphs the time profile from file ###
figuretext="{}\nConcentration={}\nIntegration Time={}\nLaser Power={}\nFilter={} nm".format(Long_Dye,Long_Concentration,Integration_Time,Laser_Power,Filter)
plt.figure(figsize=(10,10),linewidth=2)
plt.scatter(time,rInt, linewidth=1)
plt.title("Relative Integral of {} Spectra".format(Dye),fontsize=15)
plt.xlabel("Time (seconds)", fontsize=15)
plt.ylabel("Light yield (arb. units)",fontsize=15)
plt.annotate(figuretext, xy=(0.99, 0.99), xycoords='axes fraction', fontsize=11,
            horizontalalignment='right', verticalalignment='top')
plt.xlim(0,corrected_time[len(corrected_time)-1])
if savefig == True:
    plt.savefig(Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+OutName+'.pdf')
    if verbose == True:
        print("Plot saved to:",Base+Dye+"\\"+Concentration+"\\"+Run+"\\"+OutName+'.pdf')
plt.show()

# <codecell>
