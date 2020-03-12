from config.params import ANUMOGET

def get_config():
    cur_config = {
        ANUMOGET.input_folder: '/data/UNAM/Air_Pollution_Forecast/Data/WRF_Kraken/old_model_v4',
        ANUMOGET.output_folder: 'output',
        ANUMOGET.ts_db_file_name: '/home/olmozavala/Dropbox/TutorialsByMe/Python/PythonExamples/Python/TropicalStormDiscoverer/TestData/HURDAT_Export.csv'
        # ANUMOGET.ts_db_file_name: '/home/olmozavala/Dropbox/TutorialsByMe/Python/PythonExamples/Python/TropicalStormDiscoverer/TestData/HURDAT_Export_test.csv'
    }
    return cur_config
