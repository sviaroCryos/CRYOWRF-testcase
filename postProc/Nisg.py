#!/usr/bin/env python3

import numpy as np
from netCDF4 import Dataset
import xarray as xr
from wrf import getvar, ALL_TIMES, ll_to_xy, destagger, extract_times
import wrf
from datetime import datetime
import glob
import sys

"""
Checks and returns the number of time steps in a WRF output file.
"""
def get_num_timesteps(wrf_file_path):
    try:
        # Open the NetCDF file
        ncfile = Dataset(wrf_file_path)

        # Get the 'Time' dimension from the file's dimensions dictionary
        num_timesteps = ncfile.dimensions['Time'].size

        # Close the file
        ncfile.close()

        return num_timesteps
    except FileNotFoundError:
        print(f"Error: File not found at '{wrf_file_path}'")
        return None
    except KeyError:
        print("Error: 'Time' dimension not found in the file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


"""
Calculates the number concentration Nisg of ice-snow-graupel in #/kg dry air
from a WRF output file.
"""
def calculate_QNisg(wrf_file_path):
    try:
        # Open the WRF output file
        ncfile = Dataset(wrf_file_path)

        # Check if QNICE exists in the file
        if "QNICE" not in ncfile.variables:
            print(f"'QNICE' variable not found in file: {wrf_file_path}")
            return None


        if mp_scheme=='morr2mom':    
            # Check if QNSNOW exists in the file
            if "QNSNOW" not in ncfile.variables:
                print(f"'QNSNOW' variable not found in file: {wrf_file_path}")
                return None
            
            # Check if QNGRAUPEL exists in the file
            if "QNGRAUPEL" not in ncfile.variables:
                print(f"'QNGRAUPEL' variable not found in file: {wrf_file_path}")
                return None

            # Ice number mixing ratio [#/kg dry air]
            qnice = wrf.getvar(ncfile, "QNICE", timeidx=wrf.ALL_TIMES)
    
            # Snow number mixing ratio [#/kg dry air]
            qnsnow = wrf.getvar(ncfile, "QNSNOW", timeidx=wrf.ALL_TIMES)
        
            # Graupel number mixing ratio [#/kg dry air]
            qngraupel = wrf.getvar(ncfile, "QNGRAUPEL", timeidx=wrf.ALL_TIMES)


        elif mp_scheme=='ishmael':
            # Check if QNSNOW exists in the file
            if "QNICE2" not in ncfile.variables:
                print(f"'QNICE2' variable not found in file: {wrf_file_path}")
                return None
            
            # Check if QNGRAUPEL exists in the file
            if "QNICE3" not in ncfile.variables:
                print(f"'QNICE3' variable not found in file: {wrf_file_path}")
                return None

            # Ice number mixing ratio [#/kg dry air]
            qnice = wrf.getvar(ncfile, "QNICE", timeidx=wrf.ALL_TIMES)
    
            # "Snow" number mixing ratio [#/kg dry air]
            qnsnow = wrf.getvar(ncfile, "QNICE2", timeidx=wrf.ALL_TIMES)
        
            # "Graupel" number mixing ratio [#/kg dry air]
            qngraupel = wrf.getvar(ncfile, "QNICE3", timeidx=wrf.ALL_TIMES)
        

        
        QNisg=qnice+qnsnow+qngraupel # [#/kg dry air]
        
        return QNisg

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



"""
Calculates the mixing ratio Nisg of ice-snow-graupel in kg/kg dry air
from a WRF output file.
"""
def calculate_Qisg(wrf_file_path):
    try:
        # Open the WRF output file
        ncfile = Dataset(wrf_file_path)

        # Check if QICE exists in the file
        if "QICE" not in ncfile.variables:
            print(f"'QICE' variable not found in file: {wrf_file_path}")
            return None


        if mp_scheme=='morr2mom':

            # Check if QSNOW exists in the file
            if "QSNOW" not in ncfile.variables:
                print(f"'QSNOW' variable not found in file: {wrf_file_path}")
                return None

            # Check if QGRAUPEL exists in the file
            if "QGRAUP" not in ncfile.variables:
                print(f"'QGRAUP' variable not found in file: {wrf_file_path}")
                return None

        
            # Ice mixing ratio [kg/kg dry air]
            qice = wrf.getvar(ncfile, "QICE", timeidx=wrf.ALL_TIMES)
        
            # Snow mixing ratio [kg/kg dry air]
            qsnow = wrf.getvar(ncfile, "QSNOW", timeidx=wrf.ALL_TIMES)

            # Graupel mixing ratio [kg/kg dry air]
            qgraupel = wrf.getvar(ncfile, "QGRAUP", timeidx=wrf.ALL_TIMES)
            
        elif mp_scheme=='ishmael':
            # Check if QICE2 exists in the file
            if "QICE2" not in ncfile.variables:
                print(f"'QICE2' variable not found in file: {wrf_file_path}")
                return None

            # Check if QICE3 exists in the file
            if "QICE3" not in ncfile.variables:
                print(f"'QICE3' variable not found in file: {wrf_file_path}")
                return None

        
            # Ice mixing ratio [kg/kg dry air]
            qice = wrf.getvar(ncfile, "QICE", timeidx=wrf.ALL_TIMES)
        
            # "Snow" mixing ratio [kg/kg dry air]
            qsnow = wrf.getvar(ncfile, "QICE2", timeidx=wrf.ALL_TIMES)

            # "Graupel" mixing ratio [kg/kg dry air]
            qgraupel = wrf.getvar(ncfile, "QICE3", timeidx=wrf.ALL_TIMES)

        
        Qisg=qice+qsnow+qgraupel # [kg/kg dry air]
        
        return Qisg

    except Exception as e:
        print(f"An error occurred: {e}")
        return None




"""
Calculates the QVAPOR: water vapor mixing ratio kg kg-1
"""
def calculate_Qvap(wrf_file_path):
    try:
        # Open the WRF output file
        ncfile = Dataset(wrf_file_path)

        # Check if QVAPOR exists in the file
        if "QVAPOR" not in ncfile.variables:
            print(f"'QVAPOR' variable not found in file: {wrf_file_path}")
            return None

        
        # Ice mixing ratio [kg/kg dry air]
        qvap = wrf.getvar(ncfile, "QVAPOR", timeidx=wrf.ALL_TIMES)
        
        
        return qvap

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


    


"""
Calculates the mixing ratio Nrc of rain-cloud in kg/kg dry air
from a WRF output file.
"""
def calculate_Qrc(wrf_file_path):
    try:
        # Open the WRF output file
        ncfile = Dataset(wrf_file_path)

        # Check if QRAIN exists in the file
        if "QRAIN" not in ncfile.variables:
            print(f"'QRAIN' variable not found in file: {wrf_file_path}")
            return None

        # Check if QCLOUD exists in the file
        if "QCLOUD" not in ncfile.variables:
            print(f"'QCLOUD' variable not found in file: {wrf_file_path}")
            return None

        
        # Rain mixing ratio [kg/kg dry air]
        qrain = wrf.getvar(ncfile, "QRAIN", timeidx=wrf.ALL_TIMES)
    
        # Cloud mixing ratio [kg/kg dry air]
        qcloud = wrf.getvar(ncfile, "QCLOUD", timeidx=wrf.ALL_TIMES)


        
        Qrc=qrain+qcloud # [kg/kg dry air]
        
        return Qrc

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



"""
Calculates the blowing snow number concentration in #/kg dry air
from a WRF output file.
"""
def calculate_QNbs(wrf_file_path):
    try:
        # Open the WRF output file
        ncfile = Dataset(wrf_file_path)
       
        # Check if bs_qni exists in the file
        if "bs_qni" not in ncfile.variables:
            print(f"'bs_qni' variable not found in file: {wrf_file_path}")
            QNbs = 0
        else:
            # blowing snow number mixing ratio [#/kg dry air]
            QNbs = wrf.getvar(ncfile, "bs_qni", timeidx=wrf.ALL_TIMES)    
        
        return QNbs

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


"""
Calculates the blowing snow mixing ratio in kg/kg dry air
from a WRF output file.???
"""
def calculate_Qbs(wrf_file_path):
    try:
        # Open the WRF output file
        ncfile = Dataset(wrf_file_path)

        # Check if bs_qi exists in the file
        if "bs_qi" not in ncfile.variables:
            print(f"'bs_qi' variable not found in file: {wrf_file_path}")
            Qbs = 0
        else:
            # blowing snow number mixing ratio [kg/kg dry air]
            Qbs = wrf.getvar(ncfile, "bs_qi", timeidx=wrf.ALL_TIMES)    
        
        return Qbs

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


    
"""
Calculates the number concentration Nisg of ice-snow-graupel in #/kg dry air
from a WRF output file.
"""
def dryAirDensity(wrf_file_path):
    # open dataset
    ds = xr.open_dataset(wrf_file_path)

    # constant
    Rd = 287.05    #dry-air gas constant [J/kg/K]
    Rv = 641.4     #water vapor gas constant [J/kg/K]
    cp = 1004.0    #average dry-air specific heat [J/kg/K]
    p0 = 100000.0  #reference pressure [Pa]
    kappa = Rd/cp
    epsilon = Rd/Rv
    
    # compute total pressure p from
    #   P = perturbation pressure [Pa]
    #   PB = base pressure
    p = ds['P'] + ds['PB'] 

    # potential temperature theta from
    #   T = perturbation potential temperature [K]
    #   base potential temperature = 300K
    theta = ds['T'] + 300

    # Air temperature from potential temperature and total pressure
    Tair = theta*(p/p0)**kappa

    # water vapor partial pressure e from
    #   p = total pressure
    #   qv = water vapor mixing ratio
    qv = ds['QVAPOR'] #kg vapor/kg dry air
    e = p*qv/(epsilon + qv)

    # density of dry air [kg dry air/m^3]
    rho_dry = (p-e)/(Rd*Tair)

    
    ds.close()

    return rho_dry
    
    


"""
Interpolate a 4D array at a specific latitude and longitude
"""
def interp4D(wrf_file_path, array4D, latIn, lonIn, interp):
    #open the WRF file
    ncfile = Dataset(wrf_file_path)

    
    # Convert target lat/lon to fractional x/y grid coordinates
    xy = wrf.ll_to_xy(ncfile, latIn, lonIn)
    x_idx, y_idx = float(xy[0]), float(xy[1])

   
    if interp:
        nt, nz, ny, nx = array4D.shape
        array2D = np.zeros((nt, nz))

        # Bilinear interpolation manually
        for t in range(nt):
            for k in range(nz):
                field2D = array4D[t, k, :, :]
                
                i, j = int(np.floor(y_idx)), int(np.floor(x_idx))
                dy, dx = y_idx - i, x_idx - j
                
                if i < 0 or j < 0 or i+1 >= ny or j+1 >= nx:
                    array2D[t, k] = np.nan
                else:
                    f00 = field2D[i, j]
                    f10 = field2D[i+1, j]
                    f01 = field2D[i, j+1]
                    f11 = field2D[i+1, j+1]
                    array2D[t, k] = ( 
                        f00*(1-dx)*(1-dy) +
                        f01*dx*(1-dy) +
                        f10*(1-dx)*dy +
                        f11*dx*dy
                    )
    else:
        # Round to nearest integer grid index
        i = int(round(y_idx))
        j = int(round(x_idx))

        #print(f"coordinates (i,j) = ({i},{j})")

        # Extract the value at the closest grid point and convert it to numpy
        array2D = array4D[:, :, i, j].values   # shape: (time, bottom_top)
                
    return array2D



"""
Print timeseries from a 2d array (time,bottom_top)
"""
def printTSfrom2D(wrf_file_path, Nisg, IWC, LWC, simX):
    ncfile = Dataset(wrf_file_path)
    times_var = wrf.getvar(ncfile, "times", timeidx=ALL_TIMES)  
    times = times_var.values # 1D array


    # Save to file with formatted datetime
    with open(f"NisgTS_{simX}.txt", "w") as f:
        #write first line to file
        f.write(
            f"{'DateTime':<16}"
            f"{'Nisg':>18}"
            f"{'IWC':>18}"
            f"{'LWC':>18}\n"
        )
        for i in range(len(times)):
            #time
            dt = times[i].astype("M8[ms]").astype(datetime)
            dt_str = dt.strftime("%d/%m/%y_%H:%M")

            #write to file
            f.write(
                f"{dt_str:<16}"
                f"{Nisg[i,0]:>18.12f}"
                f"{IWC[i,0]:>18.12f}"
                f"{LWC[i,0]:>18.12f}\n"
            )





"""
Print 2d timeseries from a 2d array (time,bottom_top)
"""
def print2dTSfrom2D(wrf_file_path, Nisg, IWC, LWC, Qv, latIn, lonIn, simX):

    ncfile = Dataset(wrf_file_path)
    times_var = getvar(ncfile, "times", timeidx=ALL_TIMES)
    times = times_var.values  # 1D array
    n_times =Nisg.shape[0]
    n_z = Nisg.shape[1]



    # Convert lat/lon to nearest i,j indices
    ij = ll_to_xy(ncfile, latIn, lonIn)
    i_index, j_index = int(ij[0]), int(ij[1])
    # Get height above ground (AGL)
    z_agl = getvar(ncfile, "height_agl", timeidx=0)  
    #1d array of km ABL at JFJ location
    z_km = z_agl[:, j_index, i_index].values / 1000.0

    
    # Open file
    with open(f"Nisg2dTS_{simX}.txt", "w") as f:
        # Header
        f.write(f"{'DateTime':<16}")
        for i_z in range(n_z):
            f.write(f"{'Nisg_z'+str(i_z+1):>18}")
        f.write("\n")

        # Heights row
        f.write(f"{'Height(km)':<16}")
        for z in z_km[:n_z]:
            f.write(f"{z:>18.3f}")
        f.write("\n")

        # Data rows
        for i in range(n_times):
            dt = times[i].astype("M8[ms]").astype(datetime)
            dt_str = dt.strftime("%d/%m/%y_%H:%M")
            f.write(f"{dt_str:<16}")
            for j in range(n_z):
                f.write(f"{Nisg[i,j]:>18.12f}")
            f.write("\n")


    # Open file
    with open(f"IWC2dTS_{simX}.txt", "w") as f:
        # Header
        f.write(f"{'DateTime':<16}")
        for i_z in range(n_z):
            f.write(f"{'IWC_z'+str(i_z+1):>18}")
        f.write("\n")

        # Heights row
        f.write(f"{'Height(km)':<16}")
        for z in z_km[:n_z]:
            f.write(f"{z:>18.3f}")
        f.write("\n")

        # Data rows
        for i in range(n_times):
            dt = times[i].astype("M8[ms]").astype(datetime)
            dt_str = dt.strftime("%d/%m/%y_%H:%M")
            f.write(f"{dt_str:<16}")
            for j in range(n_z):
                f.write(f"{IWC[i,j]:>18.12f}")
            f.write("\n")


    # Open file
    with open(f"LWC2dTS_{simX}.txt", "w") as f:
        # Header
        f.write(f"{'DateTime':<16}")
        for i_z in range(n_z):
            f.write(f"{'LWC_z'+str(i_z+1):>18}")
        f.write("\n")

        # Heights row
        f.write(f"{'Height(km)':<16}")
        for z in z_km[:n_z]:
            f.write(f"{z:>18.3f}")
        f.write("\n")

        # Data rows
        for i in range(n_times):
            dt = times[i].astype("M8[ms]").astype(datetime)
            dt_str = dt.strftime("%d/%m/%y_%H:%M")
            f.write(f"{dt_str:<16}")
            for j in range(n_z):
                f.write(f"{LWC[i,j]:>18.12f}")
            f.write("\n")

            
            
    # Open file
    with open(f"Qvap2dTS_{simX}.txt", "w") as f:
        # Header
        f.write(f"{'DateTime':<16}")
        for i_z in range(n_z):
            f.write(f"{'Qvap_z'+str(i_z+1):>18}")
        f.write("\n")

        # Heights row
        f.write(f"{'Height(km)':<16}")
        for z in z_km[:n_z]:
            f.write(f"{z:>18.3f}")
        f.write("\n")

        # Data rows
        for i in range(n_times):
            dt = times[i].astype("M8[ms]").astype(datetime)
            dt_str = dt.strftime("%d/%m/%y_%H:%M")
            f.write(f"{dt_str:<16}")
            for j in range(n_z):
                f.write(f"{Qv[i,j]:>18.12f}")
            f.write("\n")

            

            
"""
Return height above ground level
"""
def printHeightAGL(wrf_file_path, latIn, lonIn, level):
    # Open WRF file 
    nc = Dataset(wrf_file)
    
    # Convert lat/lon to nearest i,j indices
    ij = ll_to_xy(nc, latIn, lonIn)
    i_index, j_index = int(ij[0]), int(ij[1])
    
    
    # Get height above ground (AGL)
    z_agl = getvar(nc, "height_agl", timeidx=0)  # height AGL at mass levels (m)
    
    # Extract the first level height at your location 
    level_height = float(z_agl[level, j_index, i_index].values)
    print(f"Vertical level {level} height at ({latIn}, {lonIn}) "
          f"= {level_height:.2f} m")

            



###
#| ---__________________  MAIN _________________ ---
#|  this plots the Nisg at the first vertical grid point
###
if __name__ == "__main__":


    # --------- Variables to fix  ----------------------------
    #
    simX = 'sim1'     #name of the simulation
    merge = True      #merge files?
    bs = True        #add blowing snow? (CRYOWRF only)
    #
    #--------------------------------------------------------

    
    if merge == True:
        ### = = = merge outhist files = = = ###
        files = sorted(glob.glob(f"./{simX}/outhist/outhist_d02_*.nc"))

        ds = xr.open_mfdataset(files, combine='nested', concat_dim="Time")
        ds.to_netcdf(f"./{simX}/outhist/merged_d02.nc")

        wrf_file = f'./{simX}/outhist/merged_d02.nc' 
    else:
        wrf_file = f'./{simX}/outhist/outhist_d02_2014-01-25_06:00:00.nc'  


        
    # Detect microphysics scheme
    ncfile = Dataset(wrf_file)
    if ("QNSNOW" not in ncfile.variables and
        "QICE2" in ncfile.variables):
        mp_scheme='ishmael'
        print("ISHMAEL detected!")
    else:
        mp_scheme='morr2mom'
        print("MORRISON detected!")
    


        
        
    # compute the number of timesteps
    num_steps = get_num_timesteps(wrf_file)

    # # If you want all times as datetime objects:
    wrfF =Dataset(wrf_file)
    times_all = extract_times(wrfF, timeidx=None, meta=False)
    
    # Compute timestep in seconds
    dt = times_all[1] - times_all[0]
    dt = dt/np.timedelta64(1, "s")/60

    
    if num_steps is not None:
        print(f"The WRF output file '{wrf_file}' contains {num_steps}"
              f" time steps of {dt} minutes")



    # Check if the file exists before running the calculation
    try:
        with open(wrf_file, 'r'):
            pass
    except FileNotFoundError:
        print(f"Error: WRF output file '{wrf_file}' not found.")
        print("Please provide a valid path to your wrfout file.")
        exit()

        
    # Calculate QNisg from function
    QNisg = calculate_QNisg(wrf_file) #ice,snow,groupel

    # Calculate Qisg from function
    Qisg = calculate_Qisg(wrf_file) #ice,snow,groupel

    # Calculate QVAPOR from function
    Qvap = calculate_Qvap(wrf_file) 

    # Calculate Qrc from function
    Qrc = calculate_Qrc(wrf_file) #rain,cloud
    
    
    # = = =ADD BLOWING SNOW = = =
    if bs == True:
        Qbs = calculate_Qbs(wrf_file)   #blowing snow
        QNbs = calculate_QNbs(wrf_file) #blowing snow
        QNisg = QNisg+QNbs
        Qisg = Qisg+Qbs
    
    
    
    # calculate dry air density from function
    Rho_dry = dryAirDensity(wrf_file)    

    # Calculate ice-snow-graupel numbers over liters
    Nisg = QNisg * Rho_dry / 1000 # [#/L]

    # Calculate g IWC over m3 
    IWC = Qisg * Rho_dry * 1000 # [g/m3]



    
    # Calculate g LWC over m3 
    LWC = Qrc * Rho_dry * 1000 # [g/m3]

    
      
    if Nisg is not None:
        print("Successfully calculated Nisg.")

    # interpolated values at a given latitute and longitude
    targetLat = 46.55 #JFJ lat
    targetLon = 7.98  #JFJ lon


    # (time, bottom_top) array
    Nisg2D = interp4D(wrf_file,
                      Nisg,
                      targetLat,
                      targetLon,
                      interp=False)
 
    # (time, bottom_top) array
    IWC2D = interp4D(wrf_file,
                     IWC,
                     targetLat,
                     targetLon,
                     interp=False)

    # (time, bottom_top) array
    LWC2D = interp4D(wrf_file,
                     LWC,
                     targetLat,
                     targetLon,
                     interp=False)

    # (time, bottom_top) array
    Qvap2D = interp4D(wrf_file,
                      Qvap,
                      targetLat,
                      targetLon,
                      interp=False)
    

    # print to file: This prints Nisg, IWC, LWD at bottom level 
    printTSfrom2D(wrf_file, Nisg2D, IWC2D, LWC2D, simX)  

    # print to file: This prints 2d timeseries
    print2dTSfrom2D(wrf_file, Nisg2D, IWC2D, LWC2D, Qvap2D, 
                    targetLat, targetLon, simX)  


    #print height at lat-lon and specified vertical level
    printHeightAGL(wrf_file,
                   targetLat, targetLon,
                   level=0)
