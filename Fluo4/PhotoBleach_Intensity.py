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

# :)

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

# Non-hobo style
# <codecell>
#
matplotlib.rcParams.update({'font.size': 14})

print ("imported modules..")

# Read in csv
# <codecell>
#
Path =  '../DATA/Fluo-4/'

# Single samples FCN or all FC*
ID = "FC4"

# Raw, Frac(Fraction from the 0min sample) or Irel(above control)
ToPlt = 'Frac'

############################################
# This study had 4 samples + 1 control
# All exposed (or let stand) in intervas
# 1 file = 1 sample at a given interval
############################################

S_control = []
# One array for each exposure time
# By tot minutes exposed (E) and let stand (L)
S_0E     = []
S_5E     = []
S_10E    = []
S_20E    = []
S_30E    = []
S_30E30L = []
S_Ba     = []


SampleID = ["",ID,ID,ID,ID,ID,ID,ID]
FileID   = ["control*/*min.csv","*E0minC.csv", "*E5min*.csv", "*E10min*.csv", "*E20min*.csv", "*E30min.csv", "*E30minD60.csv","*E30minD60Ba.csv"]
Names    = ["Control","O min Exp", "5 min Exp", "10 min Exp", "20 min Exp", "30 min Exp", "30 min Exp + 60 min","Ba"]
Times    = [S_control,S_0E ,S_5E ,S_10E ,S_20E ,S_30E, S_30E30L,S_Ba]

cols     = ['black', cm.summer(1/100), cm.summer(2/15), cm.summer(4/15), cm.summer(6/15), cm.summer(8/15), cm.summer(12/15),'hotpink','xkcd:bubblegum pink']

mark=['s','s','v','v','v','v',"d","^",'d','d']

# <codecell>

# # Print all file names for each exp time
# for iCurve,Curves in enumerate(Times):
#     print(iCurve)

# Figure for all curves
fig,ax = plt.subplots(figsize=(10,10))

# To keep data from the control sample & the t=0
IatT_0, Icontrol = [],[]

## First 2 rows are words, then data up to row 99
i,f = 3,90


# For each exposure time, get all the files (if multiple samples), Make
# and plot curves specified in ToPlt. Does not average yet.
for iCurve,Curves in enumerate(Times):

    Curve=[]
    for files in glob.glob(Path + SampleID[iCurve] + FileID[iCurve] ):
        Curve.append(files)
    # print(Curve)
    # print(Names[iCurve],Curves)

    # One DATA array for each exp time
    DATA = dict()
    W_, I= [],[]
    for x in range(0,len(Curve)):

        DATA[x] = pd.read_csv(Curve[x],delimiter=',',names=['Wavelength','Intensity','nah'])
        # DATA[x]['Wavelength'][3:6]
        # DATA[x]['Intensity'][3:6]

        W.append(np.array(DATA[x]['Wavelength'][i:f],dtype=float))
        I.append(np.array(DATA[x]['Intensity'][i:f],dtype=float))
        MyX=np.array(DATA[x]['Wavelength'][i:f],dtype=float)
        MyY=np.array(DATA[x]['Intensity'][i:f],dtype=float)

        if iCurve == 0:
            Icontrol.append(np.array(DATA[x]['Intensity'][i:f],dtype=float))
        if iCurve == 1:
            IatT_0.append(np.array(DATA[x]['Intensity'][i:f],dtype=float))

        Iemit = 1-((Icontrol[0]-MyY))

        if iCurve > 0:#skip control

            Ifrac = 1-((IatT_0[0]-MyY)/IatT_0[0])

            if ToPlt == 'Frac':
                ax.scatter(  np.array(MyX),np.array(Ifrac),
                color=cols[iCurve],
                label= Names[iCurve],
                marker=mark[iCurve],
                linewidth=1)

            if ToPlt == 'Raw':
                ax.scatter(  np.array(MyX),np.array(MyY),
                color=cols[iCurve],
                label= Names[iCurve],
                marker=mark[iCurve],
                linewidth=1)

            if ToPlt == 'Irel':
                ax.scatter(  np.array(MyX),np.array(Iemit),
                color=cols[iCurve],
                label= Names[iCurve],
                marker=mark[iCurve],
                linewidth=1)

ax.set_xlabel(r'Wavelength [nm]', fontsize=28)

if ToPlt == 'Raw':
    ax.set_ylabel('Intensity [arb. units]', fontsize=28)
    ax.legend(loc='upper right')

if ToPlt == 'Frac':
    ax.set_ylabel('Intensity Fraction  ', fontsize=28)
    ax.legend(loc='upper right',bbox_to_anchor=(0.6, 0.50, 0.1, 0.4),ncol=2) # still don't understand those coordinates..

if ToPlt == 'Irel':
    ax.set_ylabel('Relative Intensity [arb. units]', fontsize=28)
    ax.legend(loc='upper right')

ax.text(0.01,0.96, ' Sample:'+ID,
verticalalignment='bottom',
horizontalalignment='left',
transform=ax.transAxes,
fontsize=18,)

fig.savefig(Path+ToPlt+'_'+ID+'.pdf')
# TODO: Check if these have to be committed for my latex/markup to pull them ok.


# <codecell>
