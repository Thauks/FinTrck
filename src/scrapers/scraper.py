from abc import ABC, abstractmethod
from typing import Dict, Any
from src.models.financial import FinProd 

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
    
    def _create_fin_prod_from_json(self, prod_type: str, platform: str, json_data: Dict[str, Any], labels='') -> 'FinProd':
        """
        Creates a FinProd object from JSON data based on the product type and data mapping.

        Args:
            prod_type (str): The type of financial product (e.g., 'realestate', 'cash', 'stock').
            json_data (Dict[str, Any]): The JSON data to map to a FinProd object.

        Returns:
            FinProd: A populated FinProd instance.
        """
        # Fetch the appropriate mapping from the config
        mapping = self.config.data_mapping[prod_type]

        # Map JSON fields to FinProd attributes using the mapping
        return FinProd(
            id=str.lower(str(json_data.get(mapping['id'], ''))),
            name=str.lower(str(json_data.get(mapping['name'], ''))),
            type=prod_type,
            platform=platform,
            initial_value=json_data.get(mapping['initial_value'], 0.0),
            value=json_data.get(mapping['value'], 0.0),
            labels=labels
        )