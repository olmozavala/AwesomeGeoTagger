from enum import Enum

class ANUMOGET(Enum):
    input_folder_reanalisis = 1  # Folder path where the Numerical Model files will be searched
    input_folder_goes = 10  # Folder path where the GOES files are
    output_folder = 2  # Folder path where the Labels files will be saved
    ts_db_file_name = 5  # File name with the tropical storm database
    output_imgs_folder = 3  # Where to output temporal images
    display_imgs = 4  # Bool, indicates if the images should be displayed
    port = 11 # Which port does the server runs
    ip = 12 # Which ip does the server runs

class DataCols(Enum):
    category = 'category'
    netcdf_file = 'file_name'
    cords_file = 'coords_file_name'
    goes_file = 'goes_file_names'
    center = 'location'
    time = 'time'

class FileType(Enum):
    goes = 1
    reanalisis = 2
