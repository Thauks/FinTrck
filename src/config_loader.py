import yaml
from src.models.myinvestor import MyinvestorConfig, MyLoginInfo, MyEndpoints

def load_myinvestor_config(config_file) -> MyinvestorConfig:
    with open(config_file, 'r') as f:
        data = yaml.safe_load(f)
        
        # Unpack the data into the dataclass structure
        login_info = MyLoginInfo(**data['login_info'])
        endpoints = MyEndpoints(**data['endpoints'])

        return MyinvestorConfig(
            login_info=login_info,
            endpoints=endpoints
        )