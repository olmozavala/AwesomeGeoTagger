import os
import re
import pandas as pd
from config.params import DataCols, FileType
from datetime import datetime, timedelta, date
import time
import numpy as np

def read_all_files(input_folder, goes_input_folder, ecmwf_input_folder):
    all_files = np.array([os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(input_folder)) for f in fn if f[0:6] == 'wrfout'])
    all_files_goes = np.array([os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(goes_input_folder)) for f in fn])
    all_files_ecmwf= np.array([os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(ecmwf_input_folder)) for f in fn])
    all_files.sort()
    all_files_goes.sort()
    files_dic = {FileType.reanalisis: all_files,
                 FileType.goes: all_files_goes,
                 FileType.ecmwf: all_files_ecmwf}
    return files_dic

def match_files_dates(files, db):
    print("Matching files....")
    t = time.time()
    hurdat_dates = db.index.values

    db[DataCols.cords_file.value] = ''

    reanalisis_files = files[FileType.reanalisis]
    goes_files = files[FileType.goes]
    ecmwf_files = files[FileType.ecmwf]

    coords_file_pattern = F'wrfout_c15d.*'
    coords_re = re.compile(coords_file_pattern)
    coords_file = [x for x in files[FileType.reanalisis] if len(coords_re.findall(x)) > 0][0]

    print(F"Sizes HURDAT: {len(hurdat_dates)} Reanalisis: {len(reanalisis_files)}  GOES: {len(goes_files)}  ECMWF: {len(ecmwf_files)} ")

    # ============= Verifyin years for each dataset ============
    reanalisis_years = [int(os.path.basename(x).split('_')[3].split('-')[0]) for x in reanalisis_files
                        if os.path.basename(x).split('_')[3].split('-')[0][0] != 'd']

    min_year_reanalisis = np.amin(reanalisis_years)
    max_year_reanalisis = np.amax(reanalisis_years)

    goes_years = [int(os.path.basename(x).split('_')[1].split('-')[0]) for x in goes_files]
    min_year_goes = np.amin(goes_years)
    max_year_goes = np.amax(goes_years)

    ecmwf_years = [int(os.path.basename(x).split('_')[0].split('-')[0]) for x in ecmwf_files]
    min_year_ecmwf = np.amin(ecmwf_years)
    max_year_ecmwf = np.amax(ecmwf_years)

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
        if (min_year_reanalisis <= c_year <= max_year_reanalisis) and\
                (min_year_goes <= c_year <= max_year_goes) and\
                (min_year_ecmwf <= c_year <= max_year_ecmwf):

            found = False
            file_pattern = F'goes13_{c_year}-{c_month:02d}-{c_day:02d}_{c_hour:02d}'
            goes_temp_files = []
            ecmwf_temp_files = []

            for c_file in goes_files:
                if c_file.find(file_pattern) != -1:
                    found = True
                    goes_temp_files.append(c_file)

            # Forcing to find GOES files. If there is no GOES, then we don't add that TS
            if found:
                db.at[i, DataCols.goes_file.value] = goes_temp_files

                file_pattern = F'wrfout_c1h_d01_{c_year}-{c_month:02d}-{c_day:02d}'
                for c_file in reanalisis_files:
                    if c_file.find(file_pattern) != -1:
                        db.at[i, DataCols.netcdf_file.value] = c_file
                        db.at[i, DataCols.cords_file.value] = coords_file
                        break

                found = False
                for c_file in ecmwf_files:
                    base_name = os.path.basename(c_file)
                    min_date_str = base_name.split('_')[0].split('-')
                    max_date_str = base_name.split('_')[1].split('-')
                    min_date = date(int(min_date_str[0]), int(min_date_str[1]), int(min_date_str[2]))
                    max_date = date(int(max_date_str[0]), int(max_date_str[1]), int(max_date_str[2]))
                    if min_date <= c_date_orig <= max_date:
                        ecmwf_temp_files.append(c_file)
                        found = True

                if found:
                    db.at[i, DataCols.ecmwf_file.value] = ecmwf_temp_files

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
    df[DataCols.ecmwf_file.value] = ''
    if bbox is None:
        return df
    else:
        minlat = bbox[0]
        minlon= bbox[1]
        maxlat = bbox[2]
        maxlon = bbox[3]
        index = (df['lat'] >= minlat) & (df['lon'] >= minlon) & (df['lat'] <= maxlat) & (df['lon'] <= maxlon)
        return df[index]
