from config.params import ANUMOGET

def get_config():
    cur_config = {
        ANUMOGET.input_folder: '/data/UNAM/Air_Pollution_Forecast/Data/WRF_Kraken/old_model_v4',
        ANUMOGET.output_folder: 'output'
    }
    return cur_config
