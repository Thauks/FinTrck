import yaml, os, random
from src.models.myinvestor import MyinvestorConfig, MyLoginInfo, MyEndpoints
from src.models.bsonline import BSOnlineConfig
from src.models.binance import BinanceConfig

def load_myinvestor_config(config_file) -> MyinvestorConfig:
    with open(config_file, 'r') as f:
        data = yaml.safe_load(f)
        
        data['login_info']['customerId'] = os.environ.get('DNI')
        data['login_info']['password'] = os.environ.get('MYINVESTOR_PWD')
        data['login_info']['deviceId'] = os.environ.get('MYINVESTOR_DEVICE')
        
        # Unpack the data into the dataclass structure
        login_info = MyLoginInfo(**data['login_info'])
        endpoints = MyEndpoints(**data['endpoints'])

        return MyinvestorConfig(
            login_info=login_info,
            endpoints=endpoints,
            data_mapping=data['data_mapping']
        )

def load_bsonline_config(config_file) -> BSOnlineConfig:
    pass

def load_binance_config(config_file) -> BinanceConfig:
    pass