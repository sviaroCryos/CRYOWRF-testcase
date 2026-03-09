#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.ticker import LogLocator
from dataclasses import dataclass
from pathlib import Path





# create a class to store particle data
@dataclass
class PartData:
    time: list
    valNisg: list
    valIWC: list
    valLWC: list


parts = {} #array

numSim = 1 #number of simulations to store


###
#| --- Load CSV file
###
### --- ICNC
dfICNC = pd.read_csv('./observations/precipitation/ICNC_obs_NW.csv', sep=';')
# Convert the datetime column to proper datetime objects
dfICNC['Datetime(dd/mm/yyyy h:mm)'] = pd.to_datetime(
    dfICNC['Datetime(dd/mm/yyyy h:mm)'],
    format='%d/%m/%Y %H:%M'
)
# Sort by datetime (optional but good practice)
dfICNC = dfICNC.sort_values(by='Datetime(dd/mm/yyyy h:mm)')

### --- IWC
dfIWC = pd.read_csv('./observations/precipitation/IWC_obs_NW.csv', sep=';')
# Convert the datetime column to proper datetime objects
dfIWC['Datetime(dd/mm/yyyy h:mm)'] = pd.to_datetime(
    dfIWC['Datetime(dd/mm/yyyy h:mm)'],
    format='%d/%m/%Y %H:%M'
)
# Sort by datetime (optional but good practice)
dfIWC = dfIWC.sort_values(by='Datetime(dd/mm/yyyy h:mm)')

### --- LWC
dfLWC = pd.read_csv('./observations/precipitation/LWC_obs_NW.csv', sep=';')
# Convert the datetime column to proper datetime objects
dfLWC['Datetime(dd/mm/yyyy h:mm)'] = pd.to_datetime(
    dfLWC['Datetime(dd/mm/yyyy h:mm)'],
    format='%d/%m/%Y %H:%M'
)
# Sort by datetime (optional but good practice)
dfLWC = dfLWC.sort_values(by='Datetime(dd/mm/yyyy h:mm)')








###
#| --- Load WRF timeseries files from .nc 
###
for X in range(1,numSim+1,1): 
    parts[X] = PartData([],[],[],[])  #array of PartData
    part=parts[X]

    file_path = Path(f"./NisgTS_sim{X}.txt")

    if file_path.is_file():
        print(f"File *_sim{X} exists")

        with open(file_path, "r") as ff:
            next(ff)  # skip header
            for line in ff:
                dt_strBS, val_strNisg, val_strIWC, val_strLWC = line.split()
        
                part.time.append(datetime.strptime(dt_strBS, "%d/%m/%y_%H:%M"))
                part.valNisg.append(float(val_strNisg))
                part.valIWC.append(float(val_strIWC))
                part.valLWC.append(float(val_strLWC))
    else:
        print(f"File *_sim{X} does NOT exists")







###
#| --- Create a figure with 2 vertical subplots
###
fig, (pltNisg,pltIWC,pltLWC) =plt.subplots(3, 1,
                                           figsize=(8, 10),
                                           sharex=True)

col1 = 'black'
col2 = 'black'
lst1 = '-'
lst2 = '--'
mkr = ''


###
#|  - - - ICNC plots - - - 
###
pltNisg.scatter(dfICNC['Datetime(dd/mm/yyyy h:mm)'], dfICNC['ICNC(L-1)'],
                label='measured', 
                facecolors='none', 
                edgecolors='gray')
pltNisg.plot(parts[1].time, parts[1].valNisg,
             color='black', linestyle='-', marker=mkr)#CTRL


pltNisg.set_xlabel('Datetime')
pltNisg.set_ylabel(r'ICNC [$\mathregular{L^{-1}}$]')
pltNisg.set_yscale('log')
#pltNisg.set_title('ICNC over Time')
pltNisg.set_ylim(0.001, 10000)
#pltNisg.legend()
pltNisg.grid(True)



###
#|  - - - IWC plots - - - 
###
pltIWC.scatter(dfIWC['Datetime(dd/mm/yyyy h:mm)'], dfIWC['IWC(gm-3)'],
               label=r'IWC [$\mathregular{gm^{-3}}$]',
               facecolors='none', 
               edgecolors='gray')
pltIWC.plot(parts[1].time, parts[1].valIWC,
            color='black', linestyle='-',
            marker=mkr)#CTRL


pltIWC.set_ylabel(r'IWC [$\mathregular{gm^{-3}}$]')
pltIWC.set_yscale('log')
pltIWC.yaxis.set_major_locator(
    LogLocator(base=10, subs=(1.0,), numticks=100))
#pltIWC.set_title('IWC over Time')
pltIWC.set_ylim(0.00000001, 100)
#pltIWC.legend()
pltIWC.grid(True)


###
#|  - - - LWC plots - - - 
###
pltLWC.scatter(dfLWC['Datetime(dd/mm/yyyy h:mm)'], dfLWC['LWC(gm-3)'],
               label=r'measured',
               facecolors='none', 
               edgecolors='gray')
pltLWC.plot(parts[1].time, parts[1].valLWC,
            color='black', linestyle='-', marker=mkr,
            label='sim1')#sim1


pltLWC.set_xlabel('Date (dd/mm_hh)')
pltLWC.set_ylabel(r'LWC [$\mathregular{gm^{-3}}$]')
#pltLWC.set_yscale('log')
#pltLWC.set_title('LWC over Time')
#pltLWC.set_ylim(0.1, 10000)
pltLWC.legend()
pltLWC.grid(True)
pltLWC.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m_%H'))
pltLWC.tick_params(axis='x', rotation=45) #labelsize=12)  # horizontal x labels




# --- Set x-axis limits for all subplots ---
x_start = datetime.strptime('26/01/14_00:00', '%d/%m/%y_%H:%M')
x_end   = datetime.strptime('26/01/14_06:00', '%d/%m/%y_%H:%M')
pltNisg.set_xlim([x_start, x_end]) 



# rotate x-axis to prevent overlap
fig.autofmt_xdate()
# Adjust layout so labels/titles don't overlap
plt.tight_layout()

# Show the figure
plt.show()

