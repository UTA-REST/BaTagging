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

# Read in csv
# <codecell>
#
Path =  '../DATA/Fluo-4/'

# Single samples FCN or all FC*
ID = "FC1"

# Raw, Frac(Fraction from the 0min sample) or Irel(above control)
ToPlt = 'Irel'

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
S_Ba     = []


SampleID = ["",ID,ID,ID,ID,ID,ID,ID]
FileID = ["control*/*min.csv","*E0minC.csv", "*E5min*.csv", "*E10min*.csv", "*E20min*.csv", "*E30min.csv", "*E30minD60.csv","*E30minD60Ba.csv"]
Names  = ["Control","O min Exp", "5 min Exp", "10 min Exp", "20 min Exp", "30 min Exp", "30 min Exp + 60 min","Ba"]
Times  = [S_control,S_0E ,S_5E ,S_10E ,S_20E ,S_30E, S_30E30L,S_Ba]

cols=['black',cm.summer(1/100),cm.summer(2/15),cm.summer(4/15),cm.summer(6/15),cm.summer(8/15),cm.summer(12/15),'hotpink','xkcd:bubblegum pink']
# cols=['xkcd:wine','DarkRed','orange','hotpink','xkcd:bubblegum pink','xkcd:medium blue','green','black']

mark=['s','s','v','v','v','v',"v","^",'d','d']

# <codecell>

# # Print all file names for each exp time
# for iCurve,Curves in enumerate(Times):
#     print(iCurve)

# Figure for all curves
#fig=plt.figure(figsize=(10,10))
fig,ax = plt.subplots(figsize=(10,10))

IatT_0, Icontrol = [],[]
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
        # print(Curve[x])
        DATA[x] = pd.read_csv(Curve[x],delimiter=',',names=['Wavelength','Intensity','nah'])
        # DATA[x]['Wavelength'][3:6]
        # DATA[x]['Intensity'][3:6]

        W.append(np.array(DATA[x]['Wavelength'][3:30],dtype=float))
        I.append(np.array(DATA[x]['Intensity'][3:30],dtype=float))
        MyX=np.array(DATA[x]['Wavelength'][3:30],dtype=float)
        MyY=np.array(DATA[x]['Intensity'][3:30],dtype=float)

        if iCurve == 0:
            Icontrol.append(np.array(DATA[x]['Intensity'][3:30],dtype=float))
        if iCurve == 1:
            IatT_0.append(np.array(DATA[x]['Intensity'][3:30],dtype=float))

        Iemit = 1-((Icontrol[0]-MyY))#/Icontrol[0])
        if iCurve > 0:
            Ifrac = 1-((IatT_0[0]-MyY)/IatT_0[0])

            if ToPlt == 'Frac':
                ax.scatter(  np.array(MyX),np.array(Ifrac),
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
if ToPlt == 'Frac':
    ax.set_ylabel('Intensity Fraction w.r.t t=0  ', fontsize=28)
if ToPlt == 'Irel':
    ax.set_ylabel('Relative Intensity [arb. units]', fontsize=28)

ax.text(0.01,0.95, ' Sample:'+ID,
verticalalignment='bottom',
horizontalalignment='left',
transform=ax.transAxes,
fontsize=18,)

ax.legend(loc='lower right', bbox_to_anchor=(0.8, 0.0, 0.2, 0.4), ncol=2)
fig.savefig(Path+ToPlt+'_'+ID+'.pdf')


# <codecell>
