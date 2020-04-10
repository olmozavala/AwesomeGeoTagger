import os
import re
import pandas as pd
from config.params import DataCols, FileType
from datetime import datetime, timedelta
import time
import numpy as np

def read_all_files(input_folder, goes_input_folder):
    all_files = np.array([os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(input_folder)) for f in fn])
    all_files_goes = np.array([os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(goes_input_folder)) for f in fn])
    all_files.sort()
    all_files_goes.sort()
    files_dic = {FileType.reanalisis: all_files,
                 FileType.goes: all_files_goes}
    return files_dic

def match_files_dates(files, db):
    print("Matching files....")
    t = time.time()
    hurdat_dates = db.index.values

    db[DataCols.cords_file.value] = ''

    reanalisis_files = files[FileType.reanalisis]
    goes_files = files[FileType.goes]

    coords_file_pattern = F'wrfout_c15d.*'
    coords_re = re.compile(coords_file_pattern)
    coords_file = [x for x in files[FileType.reanalisis] if len(coords_re.findall(x)) > 0][0]
    # Iterate over all the hurdat dates
    for i in hurdat_dates:
        if i % 500 == 0:
            print(i)
        c_date_orig = pd.to_datetime(db.loc[i][DataCols.time.value])
        c_date_fixed = c_date_orig + timedelta(hours=0)
        c_year = c_date_fixed.year
        c_month = c_date_fixed.month
        c_day = c_date_fixed.day
        c_hour = c_date_fixed.hour

        # ===== Finding corresponding reanalisis files ====
        file_pattern = F'wrfout_c1h_d01_{c_year}-{c_month:02d}-{c_day:02d}'
        for c_file in reanalisis_files:
            if c_file.find(file_pattern) != -1:
                db.at[i, DataCols.netcdf_file.value] = c_file
                db.at[i, DataCols.cords_file.value] = coords_file
                break

        file_pattern = F'goes13_{c_year}-{c_month:02d}-{c_day:02d}_{c_hour:02d}'
        found = False
        goes_temp_files = []
        for c_file in goes_files:
            if c_file.find(file_pattern) != -1:
                found = True
                goes_temp_files.append(c_file)

        if found:
            db.at[i, DataCols.goes_file.value] = goes_temp_files


    newdb = db[db[DataCols.netcdf_file.value] != '']
    print(F"Done! took: { time.time() - t}")
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
    df[DataCols.goes_file.value] = ''
    if bbox is None:
        return df
    else:
        minlat = bbox[0]
        minlon= bbox[1]
        maxlat = bbox[2]
        maxlon = bbox[3]
        index = (df['lat'] >= minlat) & (df['lon'] >= minlon) & (df['lat'] <= maxlat) & (df['lon'] <= maxlon)
        return df[index]
