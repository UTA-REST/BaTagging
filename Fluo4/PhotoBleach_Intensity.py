###############################################################################
#
#   Fluo4/PhotoBleach_Intensity.py
#   Average bg substract and plot intensity of various samples. Used for the
#   photo-bleaching characterization of Fluo-4
#
#                                                  psihas@fnal.gov
###############################################################################

# Running with atom's Hydrogen requires cell 'markers'.
# Please do not delete cell comments # <codecell>

 # <codecell>

import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import glob
import pandas as pd
import pylab
# from scipy.optimize import curve_fit
# from scipy.signal import savgol_filter
# from scipy import integrate

# Non-hobo style
# <codecell>
#
matplotlib.rcParams.update({'font.size': 14})

print ("imported modules..")
cols=['xkcd:medium blue','xkcd:wine','xkcd:bubblegum pink','black','DarkRed','cornflowerblue','hotpink']

# Read in csv
# <codecell>
#
Path =  '../DATA/Fluo-4/'

############################################
# This study had 4 samples + 1 control
# All exposed (or let stand) in intervas
# 1 file = 1 sample at a given interval
############################################

# One array for each exposure time
S_control = []
# By tot minutes exposed (E) and let stand (L)
S_0E     = []
S_5E     = []
S_10E    = []
S_20E    = []
S_30E    = []
S_30E30L = []

FileID = ["FC*E0min", "FC*E5min", "FC*E10min", "FC*E20min", "FC*E30min", "FC*E30minD30","contol*/"]
Names  = ["O min Exp", "5 min Exp", "10 min Exp", "20 min Exp", "30 min Exp", "30 min Exp + 30 min","Control"]
Types  = [S_0E ,S_5E ,S_10E ,S_20E ,S_30E, S_30E30L,S_control]
# <codecell>

for iCurve,Curves in enumerate(Types):
    print(iCurve)

for iCurve,Curves in enumerate(Types):
    Curve=[]
    for files in glob.glob(Path + FileID[iCurve] + '*.csv'):
        Curve.append(files)
    print(Curve)
    print(Names[iCurve],Curves)
    # last one sees too many files  ¯\_(ツ)_/¯

    plt.figure(figsize=(10,10))

    DATA = dict()
    for x in range(0,len(Curve)):
        print(Curve[x])
        DATA[x] = pd.read_csv(Curve[x],delimiter=',',names=['Wavelength','Intensity','nah'])
        # DATA[x]['Wavelength'][3:6]
        # DATA[x]['Intensity'][3:6]

        MyX=np.array(DATA[x]['Wavelength'][3:30],dtype=float)
        MyY=np.array(DATA[x]['Intensity'][3:30],dtype=float)

        plt.plot(  np.array(MyX),np.array(MyY),color=cm.gist_heat((0+1)/7),label= r'$460 \mu M$'+' $Ba^{++}$',linewidth=2)

    plt.xlabel(r'Wavelength / nm', fontsize=28)
    plt.ylabel('Intensity (arb. units)', fontsize=28)
    plt.show()


# <codecell>
