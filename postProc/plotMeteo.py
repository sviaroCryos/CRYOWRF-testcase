#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from dataclasses import dataclass
from pathlib import Path
import numpy as np


# create a class to store meteo data
@dataclass
class MeteoData:
    times: list
    T2: list
    WS10: list
    WD10: list
    RH: list



    


meteos = {} #array
numSim = 1 #number of simulations to store



###
#| --- Load CSV file
###
df = pd.read_csv('./observations/meteo/NW.csv', sep=';')

# Convert the datetime column to proper datetime objects
df['reference_timestamp'] = pd.to_datetime(
    df['reference_timestamp'],
    format='%d.%m.%Y %H:%M'
)

# Sort by datetime (optional but good practice)
df = df.sort_values(by='reference_timestamp')



###
#| --- Load timeseries files for comparison with outhist
###
plotTimeseries=False
if plotTimeseries == True:
    data = np.loadtxt("../sim6/results/timeseries/restart/jfj.d03.TS_orig", skiprows=1)

    # start time
    t0 = datetime(2014, 1, 25, 0, 0, 0)
    
    # Extract columns (Python is 0-based!)
    time_h = data[:, 1]   # column 2
    y = data[:, 5]-273.15   # column 6: 2m Temperature
                            # column 8: 10m U
                            # column 10: surface pressure
    time_dt = [t0 + timedelta(hours=h) for h in time_h]

                 









###
#| --- WRF files ---
###     
for X in range(1,numSim+1,1): 
    meteos[X] = MeteoData([], [], [], [], [])  #array of MeteoData
    meteo=meteos[X]

    file_path = Path(f"./meteoTS_sim{X}.txt")

    if file_path.is_file():
        print(f"File *_sim{X} exists")

        with open(file_path, "r") as f:
            next(f)
            for line in f:
                dt_str, t2, ws10, wd10, rh = line.strip().split("\t")
                
                meteo.times.append(datetime.strptime(dt_str, "%d/%m/%y_%H:%M"))
                meteo.T2.append(float(t2))
                meteo.WS10.append(float(ws10))
                meteo.WD10.append(float(wd10))
                meteo.RH.append(float(rh))
    else:
        print(f"File *_sim{X} does NOT exists")

        




        
###
#| --- plot ---
###     
# Create a figure with  vertical subplots
fig, (pltT2m,pltWS,pltWD,pltRH) = plt.subplots(4, 1,
                                               figsize=(8, 10),
                                               sharex=True)



# Plot wind speed vs Datetime
pltWS.scatter(df['reference_timestamp'], df['fkl010z0'],
            label='measured', 
            facecolors='none', 
            edgecolors='gray')
pltWS.plot(meteos[1].times, meteos[1].WS10,
           color='black', linestyle='-', marker='',label='CTRL')

pltWS.set_ylabel(r'WS10m [$\mathregular{m s^{-1}}$]')
#pltWS.legend()
pltWS.grid(True)



# Plot wind direction vs Datetime
pltWD.scatter(df['reference_timestamp'], df['dkl010z0'],
            label='measured', 
            facecolors='none', 
            edgecolors='gray')
pltWD.plot(meteos[1].times, meteos[1].WD10,
           color='black', linestyle='-', marker='')

pltWD.set_ylabel('WD10m [°]')
pltWD.grid(True)
pltWD.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m_%H'))



# Plot relative humidity vs Datetime
pltRH.scatter(df['reference_timestamp'], df['ure200s0'],
            label='measured', 
            facecolors='none', 
            edgecolors='gray')
pltRH.plot(meteos[1].times, meteos[1].RH,
           color='black', linestyle='-', marker='')
pltRH.set_ylabel(r'[$\mathregular{RH2m_{w}}$] [%]')
pltRH.grid(True)
pltRH.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m_%H'))




# Plot Temperature at 2m vs Datetime
pltT2m.scatter(df['reference_timestamp'], df['tre200s0'],
            label='measured', 
            facecolors='none', 
            edgecolors='gray')
pltT2m.plot(meteos[1].times, meteos[1].T2,
            color='black', linestyle='-', marker='',
            label='CTRL')

#pltT2m.plot(time_dt, y, linestyle='--',
#             color='green',label='sim6_TS') #timeseries data
pltT2m.set_ylabel('T2m [°C]')
pltT2m.grid(True)
pltT2m.legend(ncol=3)


# --- Set x-axis limits for all subplots ---
x_start = datetime.strptime('26/01/14_00:00', '%d/%m/%y_%H:%M')
x_end   = datetime.strptime('28/01/14_00:00', '%d/%m/%y_%H:%M')
pltT2m.set_xlim([x_start, x_end]) 

# Adjust layout so labels/titles don't overlap
plt.tight_layout()
#fig.autofmt_xdate()

# x axis format
plt.xlabel('Date (dd/mm_hh)')
fig.subplots_adjust(bottom=0.08)  # increase as needed

# show the figure
plt.show()
