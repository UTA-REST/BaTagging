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
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from scipy import integrate

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

FileID = ["/control-youmustlearncontrol/", "FC*E0min", "FC*E5min", "FC*E10min", "FC*E20min", "FC*E30min", "FC*E30minD30"]
Names  = ["Control", "O min Exp", "5 min Exp", "10 min Exp", "20 min Exp", "30 min Exp", "30 min Exp + 30 min"]
Types  = [S_control,S_0E ,S_5E ,S_10E ,S_20E ,S_30E, S_30E30L]

Curves=[]
for iCurve,Curves in enumerate(Types):
    for files in glob.glob(Path + FileID[iCurve] + '*.csv'):
        Curves.append(files)
    print(Names[iCurve],Curves)

# last one sees too many files  ¯\_(ツ)_/¯

# <codecell>


for files in glob.glob(Path + '*.csv'):
    Curves.append(files)
print(Curves)
DATA = dict()

for x in range(0,len(files)):
    DATA[x] = pd.read_csv(Sample[x],delimiter=',',names=['Wavelength','Intensity','nah'])
DATA[0]['Wavelength'][0:11]
#os.listdir()

# <codecell>

print(" ")
# <codecell>



######################################################
# # I stil think this should work fine if I spend a bit of time thinking about it / figuring out how in the world one loops over columns
# ######################################################
# # Import pandas and excel thinger
# import pandas as pd
# from openpyxl import load_workbook
#
#  # <codecell>
#
# # Load in the workbook
# wb = load_workbook('../DATA/FC_AllBa.xlsx')
# # Get a sheet by name
# sheet = wb.get_sheet_by_name('FC_AllBa')
#
#  # <codecell>
# # Retrieve the value of a certain cell
# sheet['A1'].value
#
# # Select element 'B2' of your sheet
# c = sheet['B2']
# v = sheet['B2'].value
# # Retrieve the row number of your element
# c.row
# # Retrieve the column letter of your element
# c.column
# # Retrieve the coordinates of the cell
# c.coordinate
# v
#
#  # <codecell>
#
# #FC1E0minC=[]
# DATA= dict()
# for x in range(0,len(sheet.max_column))
#     for cellObj in sheet['B3':'B99']:
#         holder=[]
#         for cell in cellObj:
#             #FC1E0minC.append(cell.value)
#             holder.append(cell.value)
#         DATA
#
# # print (FC1E0minC)
#
#  # <codecell>
