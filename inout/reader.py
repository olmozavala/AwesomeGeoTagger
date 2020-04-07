import os
import re
import pandas as pd
from config.params import DataCols
from datetime import datetime, timedelta

def read_all_files(input_folder):
    all_files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(input_folder)) for f in fn]
    return all_files

def match_files_dates(files, db):
    ts_id = db.index.values

    db[DataCols.cords_file.value] = ''

    coords_file_pattern = F'wrfout_c15d.*'
    coords_re = re.compile(coords_file_pattern)
    coords_file = [x for x in files if len(coords_re.findall(x)) > 0][0]
    for i in ts_id:
        c_date_orig = db.loc[i][DataCols.time.value]
        c_date_orig = pd.to_datetime(c_date_orig)
        # c_date_fixed = c_date_orig + timedelta(hours=-6)
        c_date_fixed = c_date_orig + timedelta(hours=0)
        c_year = c_date_fixed.year
        c_month = c_date_fixed.month
        c_day = c_date_fixed.day

        file_pattern = F'wrfout_c1h.*{c_year}-{c_month:02d}-{c_day:02d}.*'
        file_re = re.compile(file_pattern)
        for c_file in files:
            c_file_name = os.path.basename(c_file)
            m = file_re.findall(c_file_name)
            if len(m) > 0:
                db.at[i, DataCols.netcdf_file.value] = c_file
                db.at[i, DataCols.cords_file.value] = coords_file
                break

    newdb = db[db[DataCols.netcdf_file.value] != '']
    return newdb


def read_ts_db(file_name, bbox=None):
    """
    Reads the Hurdat database, restricting the tropical storms by a bounding box.
    :param file_name:
    :param bbox:
    :return:
    """
    df = pd.read_csv(file_name, header=0, parse_dates=['time'])
    print(df)
    df[DataCols.center.value] = df['lat'].astype('str') + ',' + df['lon'].astype('str')
    df[DataCols.netcdf_file.value] = ''
    if bbox is None:
        return df
    else:
        minlat = bbox[0]
        minlon= bbox[1]
        maxlat = bbox[2]
        maxlon = bbox[3]
        index = (df['lat'] >= minlat) & (df['lon'] >= minlon) & (df['lat'] <= maxlat) & (df['lon'] <= maxlon)
        return df[index]
