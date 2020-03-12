import pandas as pd
from config.params import DataCols

def read_hurdat_db(file_name):
    df = pd.read_csv(file_name, header=0, index_col=0, parse_dates=True)
    print(df)
    df[DataCols.center.value] = df['lat'].astype('str') + ',' + df['lon'].astype('str')
    df[DataCols.netcdf_file.value] = ''
    return df


if __name__ == '__main__':
    file_name = '/home/olmozavala/Dropbox/TutorialsByMe/Python/PythonExamples/Python/TropicalStormDiscoverer/TestData/HURDAT_Export.csv'
    hurdat_to_json(file_name)
