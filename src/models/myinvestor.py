from dataclasses import dataclass
from typing import Optional

@dataclass
class MyLoginInfo:
    accessType: str
    code: Optional[str]          
    customerId: str
    deviceId: str 
    otpId: Optional[str]         
    password: str 
    plataform: Optional[str] 

@dataclass
class MyEndpoints:
    login: str
    accounts: str
    portfolios: str
    movements: str
    positions: str
    real_state: str

@dataclass
class MyinvestorConfig:
    login_info: MyLoginInfo
    endpoints: MyEndpoints
    data_mapping: Optional[dict]
    