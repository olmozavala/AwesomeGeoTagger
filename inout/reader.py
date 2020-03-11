import xarray as xr
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

    print(db)
    return db


