from abc import ABC, abstractmethod
from typing import Dict, Any
from src.models.financial import FinProd, FinProdType 

class Scraper(ABC):
    def __init__(self, config):
        self.config = config
    
    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def logout(self):
        pass
    
    @abstractmethod
    def fetch_cash(self):
        pass
    
    @abstractmethod
    def fetch_funds(self):
        pass
    
    @abstractmethod
    def fetch_etfs(self):
        pass
    
    @abstractmethod
    def fetch_stocks(self):
        pass
    
    @abstractmethod
    def fetch_crypto(self):
        pass
    
    @abstractmethod
    def fetch_pension_funds(self):
        pass
    
    @abstractmethod
    def fetch_real_estate(self):
        pass
    
    @staticmethod
    def _create_fin_prod_from_json(data: Dict[str, Any], mapping: Dict[str, str]) -> FinProd:
        """
        Converts a dictionary representing a financial product to a FinProd instance
        using a mapping from FinProd attributes to external data keys.

        Args:
            data (Dict[str, Any]): A dictionary containing the attributes for the FinProd.
            mapping (Dict[str, str]): A mapping of FinProd attributes to keys in the external data model.

        Returns:
            FinProd: An instance of FinProd populated with the data.
        """
        return FinProd(
            id=data.get(mapping['id'], ''),
            name=data.get(mapping['name'], ''),
            type=mapping['type'],
            initial_value=data.get(mapping['initial_value'], 0.0),
            value=data.get(mapping['value'])
        )