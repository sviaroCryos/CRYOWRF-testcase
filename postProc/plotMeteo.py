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
numSim = 3 #number of simulations to store



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
plotTimeseries=True
if plotTimeseries == True:
    data = np.loadtxt("./plot/jfj.d03.TS_sim1", skiprows=1)

    # start time
    t0 = datetime(2014, 1, 26, 0, 0, 0)
    
    # Extract columns (Python is 0-based!)
    time_h = data[:, 1]   # column 2
    y = data[:, 5]-273.15   # column 6: 2m Temperature
    time_dt = [t0 + timedelta(hours=h) for h in time_h]


    data2 = np.loadtxt("./plot/jfj.d02.TS_sim2", skiprows=1)
    time_h2 = data2[:, 1]   # column 2
    y2 = data2[:, 5]-273.15   # column 6: 2m Temperature
    time_dt2 = [t0 + timedelta(hours=h) for h in time_h2]

    data3 = np.loadtxt("./sim3/jfj.d02.TS_sim3", skiprows=1)
    time_h3 = data3[:, 1]   # column 2
    y3 = data3[:, 5]-273.15   # column 6: 2m Temperature
    time_dt3 = [t0 + timedelta(hours=h) for h in time_h3]

                 









###
#| --- WRF files ---
###     
for X in range(1,numSim+1,1): 
    meteos[X] = MeteoData([], [], [], [], [])  #array of MeteoData
    meteo=meteos[X]

    file_path = Path(f"./plot/meteoTS_sim{X}.txt")

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
# pltWS.plot(meteos[1].times, meteos[1].WS10,
#            color='gray', linestyle='-', marker='',label='sim1')
pltWS.plot(meteos[2].times, meteos[2].WS10,
           color='black', linestyle='-', marker='',label='sim2',linewidth=2.0)
pltWS.plot(meteos[3].times, meteos[3].WS10,
           color='red', linestyle=':', marker='',label='sim3',linewidth=2.0)
pltWS.set_ylabel(r'WS10m [$\mathregular{m s^{-1}}$]')
#pltWS.legend()
pltWS.grid(True)



# Plot wind direction vs Datetime
pltWD.scatter(df['reference_timestamp'], df['dkl010z0'],
            label='measured', 
            facecolors='none', 
            edgecolors='gray')
# pltWD.plot(meteos[1].times, meteos[1].WD10,
#            color='gray', linestyle='-', marker='')
pltWD.plot(meteos[2].times, meteos[2].WD10,
           color='black', linestyle='-', marker='',linewidth=2.0)
pltWD.plot(meteos[3].times, meteos[3].WD10,
           color='red', linestyle=':', marker='',linewidth=2.0)

pltWD.set_ylabel('WD10m [°]')
pltWD.grid(True)
pltWD.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m_%H'))



# Plot relative humidity vs Datetime
pltRH.scatter(df['reference_timestamp'], df['ure200s0'],
            label='measured', 
            facecolors='none', 
            edgecolors='gray')
# pltRH.plot(meteos[1].times, meteos[1].RH,
#            color='gray', linestyle='-', marker='')
pltRH.plot(meteos[2].times, meteos[2].RH,
           color='black', linestyle='-', marker='',linewidth=2.0)
pltRH.plot(meteos[3].times, meteos[3].RH,
           color='red', linestyle=':', marker='',linewidth=2.0)

pltRH.set_ylabel(r'[$\mathregular{RH2m_{w}}$] [%]')
pltRH.grid(True)
pltRH.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m_%H'))




# Plot Temperature at 2m vs Datetime
pltT2m.scatter(df['reference_timestamp'], df['tre200s0'],
            label='measured', 
            facecolors='none', 
            edgecolors='gray')
# pltT2m.plot(meteos[1].times, meteos[1].T2,
#             color='gray', linestyle='-', marker='',
#             label='sim1')
pltT2m.plot(meteos[2].times, meteos[2].T2,
            color='black', linestyle='-', marker='',linewidth=2.0,
            label='sim2')
pltT2m.plot(meteos[3].times, meteos[3].T2,
            color='red', linestyle=':', marker='',linewidth=2.0,
            label='sim3')
# pltT2m.plot(time_dt, y,
#             color='orange', linestyle=':', marker='',
#             label='TS_sim1')
pltT2m.plot(time_dt2, y2,
            color='black', linestyle='-.', marker='',
            label='TS_sim2',linewidth=2.0)
pltT2m.plot(time_dt3, y3,
            color='red', linestyle='-.', marker='',
            label='TS_sim3',linewidth=2.0)
#pltT2m.plot(time_dt, y, linestyle='--',
#             color='green',label='sim6_TS') #timeseries data
pltT2m.set_ylabel('T2m [°C]')
pltT2m.grid(True)
pltT2m.legend(ncol=3)


# --- Set x-axis limits for all subplots ---
x_start = datetime.strptime('26/01/14_00:00', '%d/%m/%y_%H:%M')
x_end   = datetime.strptime('26/01/14_06:00', '%d/%m/%y_%H:%M')
pltT2m.set_xlim([x_start, x_end]) 

# Adjust layout so labels/titles don't overlap
plt.tight_layout()
#fig.autofmt_xdate()

# x axis format
plt.xlabel('Date (dd/mm_hh)')
fig.subplots_adjust(bottom=0.08)  # increase as needed

# show the figure
plt.show()
