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
from collections import defaultdict
import os

date = "06-27-18" #Date of code run
Path="C:\\Users\\mcdonaldad\\Desktop\\Photobleach\\TimeProfileData\\" #BasePath


if not os.path.exists("C:\\Users\\mcdonaldad\\Desktop\\Photobleach\\TimeProfileData\\Saved Plots"+"\\"+date+"\\"): #Creates directory to store plots
    os.makedirs("C:\\Users\\mcdonaldad\\Desktop\\Photobleach\\TimeProfileData\\Saved Plots"+"\\"+date+"\\")

files1=[] #Declares files1 array
files3=[] #Declares files3 array

for file in glob.glob(Path+"*.csv"): # Crawls over Path directory looking for .csv files and:
    filename=file.split("\\") # Splits the filename out of the pathname using \\ as the delimiter
    filename1=filename[6] # Declares variable for the 7th array value
    files1.append(filename1) #Stores all the files inside the TimeProfileData folder

files2=sorted(set(files1)) #Removes duplicates and sorts in alphabetical order

for i in range(0,len(files2)):  #Splits each .csv file by "_" into individual arrays withn a master array
    temp1=files2[i].split("_");
    files3.append(temp1)

files4=[[] for _ in range(100000)]   #Define arbritarily large array for ech individual concentration and concentration

i=0; #Reset Counters
j=0;

while(i<(len(files3)-1)): #Split into individual dyes and concentrations
    if (files3[i][1]==files3[1+i][1])and(files3[i][2]==files3[1+i][2]):
        files4[j].append(files3[i])
        files4[j].append(files3[i+1])
        i += 1;
    else:
        files4[j].append(files3[i])
        i+=1
        j+=1;

i=0; #Reset Counters
j=0;

files5 = [x for x in files4 if x != []] #Removes empty elements

for i in range(0,len(files5)):  #Changes back to original filename
    for j in range(0,len(files5[i])):
        files5[i][j]=("tpd"+"_"+files5[i][j][1]+"_"+files5[i][j][2]+"_"+files5[i][j][3])

for i in range(len(files5)): #Removes dupilcates
    files5[i]=sorted(set(files5[i]))

#Filenames by concentration and dye have been split up into runs and saved in files5#

#Modifications to plots to be done beyond this point#

for i in range(len(files5)): #BEHOLD !
    print(files5[i])
    print("\n")

colorarray = ["g","r","b","o","k","c","m"] #Colors for legends

for i in range(len(files5)):                #Data Plotter
    for j in range(len(files5[i])):
        plotterdata= pd.read_csv(Path+files5[i][j],header = None)
        titletemp=files5[i][j].split("_")
        plot1=plt.scatter(plotterdata[0],plotterdata[1],color=colorarray[j],linewidth=1,label=titletemp[3][0]+titletemp[3][1]+titletemp[3][2]+" "+titletemp[3][3])
        plt.Figure(figsize=(10,10),linewidth=2)
        plt.xlim(xmin=0)
        plt.xlabel("Time (s)",fontsize=15) # Adds a label to the x axis and declares the font size
        plt.ylabel("Intensity (arb. units)",fontsize=15) # Adds a label to the y axis and declares the font size
        plt.title("Time Profile Data: {} @ {}".format(titletemp[1],titletemp[2])) # Adds title to the figure
    plt.legend(loc='upper center',ncol=3)
    plt.grid()
    plt.tight_layout()
    plt.savefig(Path+"Saved Plots"+"\\"+date+"\\"+titletemp[0]+"_"+titletemp[1]+"_"+titletemp[2]+".pdf" ) #Saves to directory
    plt.show()
