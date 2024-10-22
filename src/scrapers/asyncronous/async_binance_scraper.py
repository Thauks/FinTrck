import aiohttp
import asyncio
from dataclasses import asdict
from typing import Any, Dict, List

from src.scrapers.asyncronous.async_scraper import AsyncScraper
from src.models.binance import BinanceConfig
from src.models.financial import FinProdType, FinProd
from src.models.platforms import Platform

class AsyncBinanceScraper(AsyncScraper):
    def __init__(self, config: BinanceConfig):
        """
        Initializes the AsyncBinanceScraper with the given configuration.

        Args:
            config (BinanceConfig): Configuration object with login details and endpoints.
        """
        super().__init__(config)  # Call the parent constructor
        self.session = None  # Initialize session variable
        self.platform = Platform.MYINVESTOR  # Set the platform type

    async def login(self):
        pass

    async def logout(self):
        pass

    async def fetch_cash(self):
        pass

    async def fetch_funds(self):
        pass

    async def fetch_etfs(self):
        pass

    async def fetch_stocks(self):
        pass

    async def fetch_crypto(self):
        pass

    async def fetch_pension_funds(self):
        pass

    async def fetch_real_estate(self):
        pass

    async def fetch_all_products(self):
        pass

    async def _setup_session(self, login_url: str, payload: Dict[str, Any]):
        pass

    async def _fetch_portfolios(self) -> List[FinProd]:
        pass

    async def _fetch_funds(self, portfolio_data: List[Dict[str, Any]], acc_str: str, funds_str: str) -> List[FinProd]:
        pass
