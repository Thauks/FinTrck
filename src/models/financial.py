from dataclasses import dataclass

class FinProdType:
    CASH = "cash"
    STOCK = "stock"
    ETF = "etf"
    FUND = "fund"
    CRYPTO = "crypto"
    BOND = "bond"
    REAL_ESTATE = "realestate"

@dataclass
class FinProd:
    id: str
    name: str
    type: str
    initial_value: float
    value: float
    
    @property
    def roi(self) -> float:
        """Calculates ROI (Return on Investment). Returns 0% if initial investment is 0."""
        return 0.0 if self.initial_value == 0 else (self.value - self.initial_value) / self.initial_value * 100
    
    def __repr__(self):
        return f"FinProd(id={self.id}, name={self.name}, type={self.type}, initial_value={self.initial_value}, value={self.value}, roi={self.roi:.2f}%)"