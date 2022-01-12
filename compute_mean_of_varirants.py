#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 15:37:31 2021

@author: waterlab
"""

import xarray as xr
from glob import glob
import numpy as np
from time import time

path = "../downloads/GCMs/MRI/"


def main():
    print("computing...")
    t = time()
    uas_list = np.array(
        [xr.open_dataset(file, engine="h5netcdf").uas.transpose('lat', 'lon', 'time').values for file in glob(path+"uas/*")])

    vas_list = np.array(
        [xr.open_dataset(file, engine="h5netcdf").vas.transpose("lat", "lon", "time").values for file in glob(path+"vas/*")])

    print("opened", f"{time()-t:.04f} sec ")
    t = time()

    for file in glob(path+"uas/*"):
        ds = xr.open_dataset(file, engine="h5netcdf")
        break

    u_data = np.mean(uas_list, axis=0)
    v_data = np.mean(vas_list, axis=0)
    new = xr.Dataset(
        {
            "uas": (["lat", "lon", "time"], u_data),
            "vas": (["lat", "lon", "time"], v_data),
        },
        coords={
            "lat": (["lat"], ds.lat.to_index()),
            "lon": (["lon"], ds.lon.to_index()),
            'time': (['time'], ds.time.to_index())
        },
    )
    print("created", f"{time()-t:.04f} sec")
    t = time()
    new.to_netcdf(path+"MRI.nc", engine="h5netcdf")
    print("writed", f"{time()-t:.04f} sec")


main()
# for file in glob(path+"uas/*"):
#     ds = xr.open_dataset(file, engine="h5netcdf")

#     print(ds)
