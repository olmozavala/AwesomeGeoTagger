from enum import Enum

class ANUMOGET(Enum):
    input_folder = 1  # Folder path where the Numerical Model files will be searched
    output_folder = 2  # Folder path where the Labels files will be saved
    output_imgs_folder = 3  # Where to output temporal images
    display_imgs = 4  # Bool, indicates if the images should be displayed

class DataCols(Enum):
    category = 'Category'
    netcdf_file = 'File_name'
    center = 'Location'
