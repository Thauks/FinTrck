from abc import ABC, abstractmethod

class Scraper(ABC):
    def __init__(self, config):
        self.config = config
    
    @abstractmethod
    def login(self):
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