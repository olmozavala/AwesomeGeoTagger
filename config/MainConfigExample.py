from config.params import ANUMOGET

def get_config():
    cur_config = {
        ANUMOGET.output_folder: 'output',
        ANUMOGET.input_folder_reanalisis: '/home/olmozavala/Dropbox/MyProjects/TROSTDIS_ECMWF/test_data/anumoget',
        ANUMOGET.input_folder_goes: '/home/olmozavala/Dropbox/MyProjects/TROSTDIS_ECMWF/test_data/goes/output',
        ANUMOGET.input_folder_ecmwf: '/home/olmozavala/Dropbox/MyProjects/TROSTDIS_ECMWF/test_data/goes/output',
        ANUMOGET.ts_db_file_name: '/home/olmozavala/Dropbox/MyProjects/TROSTDIS_ECMWF/test_data/hurdat/HURDAT_Export.csv',
        ANUMOGET.port: 8053,
        ANUMOGET.ip: '0.0.0.0'
        # ANUMOGET.port: 8051,
        # ANUMOGET.ip: '0.0.0.0'
    }
    return cur_config
