#!/usr/bin/env python3

import numpy as np
from netCDF4 import Dataset
import xarray as xr
from wrf import getvar, ALL_TIMES, ll_to_xy
import wrf
from datetime import datetime
import glob

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
Interpolate a 3D array at a specific latitude and longitude
"""
def interpT2m(wrf_file_path, latIn, lonIn, interp):
    #open the WRF file
    ncfile = Dataset(wrf_file_path)

    
    T2m = getvar(ncfile, "T2", timeidx=ALL_TIMES)

#    print(f"   size of T2m:{T2m.shape}")
    
    # get lat/lon grid
    lats, lons = wrf.latlon_coords(T2m) 

    # Convert target lat/lon to fractional x/y grid coordinates
    xy = wrf.ll_to_xy(ncfile, latIn, lonIn)
    x_idx, y_idx = float(xy[0]), float(xy[1])

    
    if interp:
        nt, ny, nx = T2m.shape
        T2m_TS = np.zeros(nt)

        # Bilinear interpolation manually
        for t in range(nt):
            field2D = T2m[t, :, :]
            
            i, j = int(np.floor(y_idx)), int(np.floor(x_idx))
            dy, dx = y_idx - i, x_idx - j
            
            if i < 0 or j < 0 or i+1 >= ny or j+1 >= nx:
                T2m_TS[t] = np.nan
            else:
                f00 = field2D[i, j]
                f10 = field2D[i+1, j]
                f01 = field2D[i, j+1]
                f11 = field2D[i+1, j+1]
                T2m_TS[t, k] = (
                    f00*(1-dx)*(1-dy) +
                    f01*dx*(1-dy) +
                    f10*(1-dx)*dy +
                    f11*dx*dy
                )
    else:
        # Round to nearest integer grid index
        i = int(round(y_idx))
        j = int(round(x_idx))

        # Extract the value at the closest grid point and convert it to numpy
        T2m_TS = T2m[:, i, j].values -273.15   # shape: (time, bottom_top)
                
    return T2m_TS





"""
Interpolate a 3D array at a specific latitude and longitude
"""
def interpU10m(wrf_file_path, latIn, lonIn, interp):
    #open the WRF file
    ncfile = Dataset(wrf_file_path)

    
    U10m = getvar(ncfile, "U10", timeidx=ALL_TIMES)

#    print(f"   size of T2m:{T2m.shape}")
    
    # get lat/lon grid
    lats, lons = wrf.latlon_coords(U10m) 

    # Convert target lat/lon to fractional x/y grid coordinates
    xy = wrf.ll_to_xy(ncfile, latIn, lonIn)
    x_idx, y_idx = float(xy[0]), float(xy[1])

    # Interpolate U10m
    if interp:
        nt, ny, nx = U10m.shape
        U10m_TS = np.zeros(nt)

        # Bilinear interpolation manually
        for t in range(nt):
            field2D = U10m[t, :, :]
            
            i, j = int(np.floor(y_idx)), int(np.floor(x_idx))
            dy, dx = y_idx - i, x_idx - j
            
            if i < 0 or j < 0 or i+1 >= ny or j+1 >= nx:
                U10m_TS[t] = np.nan
            else:
                f00 = field2D[i, j]
                f10 = field2D[i+1, j]
                f01 = field2D[i, j+1]
                f11 = field2D[i+1, j+1]
                U10m_TS[t, k] = (
                    f00*(1-dx)*(1-dy) +
                    f01*dx*(1-dy) +
                    f10*(1-dx)*dy +
                    f11*dx*dy
                )
    else:
        # Round to nearest integer grid index
        i = int(round(y_idx))
        j = int(round(x_idx))

        # Extract the value at the closest grid point and convert it to numpy
        U10m_TS = U10m[:, i, j].values   # shape: (time, bottom_top)
      
    return U10m_TS




"""
Interpolate a 3D array at a specific latitude and longitude
"""
def interpV10m(wrf_file_path, latIn, lonIn, interp):
    #open the WRF file
    ncfile = Dataset(wrf_file_path)

    
    V10m = getvar(ncfile, "V10", timeidx=ALL_TIMES)

#    print(f"   size of T2m:{T2m.shape}")
    
    # get lat/lon grid
    lats, lons = wrf.latlon_coords(V10m) 

    # Convert target lat/lon to fractional x/y grid coordinates
    xy = wrf.ll_to_xy(ncfile, latIn, lonIn)
    x_idx, y_idx = float(xy[0]), float(xy[1])

    # Interpolate V10m
    if interp:
        nt, ny, nx = V10m.shape
        V10m_TS = np.zeros(nt)

        # Bilinear interpolation manually
        for t in range(nt):
            field2D = V10m[t, :, :]
            
            i, j = int(np.floor(y_idx)), int(np.floor(x_idx))
            dy, dx = y_idx - i, x_idx - j
            
            if i < 0 or j < 0 or i+1 >= ny or j+1 >= nx:
                V10m_TS[t] = np.nan
            else:
                f00 = field2D[i, j]
                f10 = field2D[i+1, j]
                f01 = field2D[i, j+1]
                f11 = field2D[i+1, j+1]
                V10m_TS[t, k] = (
                    f00*(1-dx)*(1-dy) +
                    f01*dx*(1-dy) +
                    f10*(1-dx)*dy +
                    f11*dx*dy
                )
    else:
        # Round to nearest integer grid index
        i = int(round(y_idx))
        j = int(round(x_idx))

        # Extract the value at the closest grid point and convert it to numpy
        V10m_TS = V10m[:, i, j].values   # shape: (time, bottom_top)
      
    return V10m_TS







"""
Interpolate a 3D array at a specific latitude and longitude
"""
def rh2D(wrf_file_path, latIn, lonIn, zIdx):
    #constants
    P0=100000  #[Pa]
    Rd=287.05  #[J/kg/K] gas constant dry air
    Rv=461.5   #[J/kg/K] gas constant water vapor
    cp=1004.0  #[J/kg/K] specific heat dry air
    
    
    #open the WRF file
    ncfile = Dataset(wrf_file_path)

    
    P  = getvar(ncfile, "P", timeidx=ALL_TIMES)      # Perturbation pressure [Pa]
    PB = getvar(ncfile, "PB", timeidx=ALL_TIMES)     # Base state pressure [Pa]
    theta  = getvar(ncfile, "T", timeidx=ALL_TIMES)  # Perturbation theta [K]
    qv = getvar(ncfile, "QVAPOR", timeidx=ALL_TIMES) # kg_vapor/kg_dry_air

    #total pressure
    Ptot = P + PB

    #total temperature theta
    thetaTot = theta + 300



    # Convert target lat/lon to fractional x/y grid coordinates
    xy = wrf.ll_to_xy(ncfile, latIn, lonIn)
    x_idx, y_idx = float(xy[0]), float(xy[1])

    # Round to nearest integer grid index
    i = int(round(y_idx))
    j = int(round(x_idx))
    

    
    # Extract the value at the closest grid point and convert it to numpy
    # shape:(time,bottom_top)
    Ptot_TS = Ptot[:, :, i, j].values 
    thetaTot_TS = thetaTot[:, :, i, j].values
    qv_TS = qv[:, :, i, j].values

    

    #temperature
    T_TS = thetaTot_TS*(Ptot_TS/P0)**(Rd/cp)

    #water vapor partial pressure [hPa]
    e_TS = (qv_TS*Ptot_TS/(qv_TS+Rd/Rv))/100

    #water vapor saturation pressure with respect to water (Tetans)
    e_sw_TS = 6.1078*np.exp(17.269*(T_TS-273.15)/(T_TS-35.86))

    #water vapor saturation pressure with respect to ice (Tetans)
    e_si_TS = 6.1078*np.exp(21.874*(T_TS-273.15)/(T_TS-7.66))

    # relative humidity with respect to water
    RHw_TS=e_TS/e_sw_TS*100

    #relative humidity with respect to ice
    RHi_TS=e_TS/e_si_TS*100

    # 1D vector (time)
    rh2D_TS= RHw_TS[:,zIdx]
      
    return rh2D_TS





"""
Print timeseries from a 2d array (time,bottom_top)
"""
def printTS(wrf_file_path, T2, WS10, WD10, RH):
    ncfile = Dataset(wrf_file_path)
    times_var = wrf.getvar(ncfile, "times", timeidx=ALL_TIMES)  
    times = times_var.values # 1D array
   
    
    # Save to file with formatted datetime
    with open(f"./plot/meteoTS_{simX}.txt", "w") as f:
        f.write("DateTime\tT2\tWS10\tWD10\tRH\n")
        for i in range(len(times)):
            #time
            dt = times[i].astype("M8[ms]").astype(datetime)
            dt_str = dt.strftime("%d/%m/%y_%H:%M")

            #write to file
            f.write(
                f"{dt_str}\t{T2[i]:.2f}\t{WS10[i]:.2f}"
                f"\t{WD10[i]:.2f}\t{RH[i]:.2f}\n"
            )
        


"""
Compute wind direction (in degrees) from u and v components.
u : East-west wind component (m/s, positive eastward)
v : North-south wind component (m/s, positive northward)
"""        
def wind_direction(u, v):
    WD = (np.degrees(np.arctan2(-u, -v)) + 360) % 360

    return WD


            

#| ------------------------------------------------------------------- |#



###
#| --- MAIN ---
###
if __name__ == "__main__":


    # --------- Variables to fix  ----------------------------
    #
    simX = 'sim3'     #name of the simulation
    merge = True      #merge files?
    #
    #--------------------------------------------------------

    

    if merge == True:
        ### = = = merge outhist files = = = ###
        files = sorted(glob.glob(f"./{simX}/outhist/outhist_d02_*.nc"))
        ds = xr.open_mfdataset(files, combine='nested', concat_dim="Time")
        ds.to_netcdf(f"./{simX}/outhist/merged_d02.nc")

        wrf_file = f'./{simX}/outhist/merged_d02.nc' 
    else:
        wrf_file = f'./{simX}/outhist/outhist_d03_2014-01-26_00:00:00.nc'  

        
    # compute the number of timesteps
    num_steps = get_num_timesteps(wrf_file)
    if num_steps is not None:
        print(f"The WRF file '{wrf_file}' contains {num_steps} time steps.")



    # Check if the file exists before running the calculation
    try:
        with open(wrf_file, 'r'):
            pass
    except FileNotFoundError:
        print(f"Error: WRF output file '{wrf_file}' not found.")
        print("Please provide a valid path to your wrfout file.")
        exit()


    # interpolated values at a given latitute and longitude
    targetLat = 46.55 #JFJ lat
    targetLon = 7.98  #JFJ lon

    
    ### Temperature
    ##
    # (time, bottom_top) array
    T2m_TS = interpT2m(wrf_file,
                       targetLat,
                       targetLon,
                       interp=False)
    
    ### Wind Speed
    ##
    # U velocity
    U10m_TS = interpU10m(wrf_file,
                         targetLat,
                         targetLon,
                         interp=False)

    # V velocity
    V10m_TS = interpV10m(wrf_file,
                         targetLat,
                         targetLon,
                         interp=False)

    # compute wind speed magnitude
    WS10m_TS = (U10m_TS**2+V10m_TS**2)**0.5


    ### Wind direction
    ##
    #
    WD10m_TS = wind_direction(U10m_TS, V10m_TS)

    
    ### Relative Humidity (time, bottom_top)
    ##
    #
    RH_TS = rh2D(wrf_file,
                 targetLat,
                 targetLon,
                 zIdx=0) #vertical level
    


    ###
    #| - - - print to file
    ###
    printTS(wrf_file, T2m_TS, WS10m_TS, WD10m_TS, RH_TS)

