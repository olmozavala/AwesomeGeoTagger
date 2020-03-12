import xarray as xr
import netCDF4 as nc
from os.path import join
import os
import re
import pandas as pd
from config.params import DataCols

def read_all_files(input_folder):
    all_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(input_folder)) for f in fn]
    return all_files

def match_files_dates(files, db):
    date_format_ext = '%Y-%m-%dT%H:%M:%S'
    dates_orig = db.index

    for c_date_orig in dates_orig:
        c_date = pd.to_datetime(c_date_orig)
        c_year = c_date.year
        c_month = c_date.month
        c_day = c_date.day
        c_hour = c_date.hour

        file_pattern = F'wrfout_c1h.*{c_year}-{c_month:02d}-{c_day:02d}_{c_hour:02d}'
        file_re = re.compile(file_pattern)
        for c_file in files:
            c_file_name = os.path.basename(c_file)
            m = file_re.findall(c_file_name)
            if len(m) > 0:
                db.loc[c_date_orig][DataCols.netcdf_file.value] = c_file

    newdb = db[db[DataCols.netcdf_file.value] != '']
    print(newdb)
    return newdb


def read_ts_db(file_name):
    df = pd.read_csv(file_name, header=0, index_col=0, parse_dates=True)
    print(df)
    df[DataCols.center.value] = df['lat'].astype('str') + ',' + df['lon'].astype('str')
    df[DataCols.netcdf_file.value] = ''
    return df
