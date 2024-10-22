import aiohttp
import asyncio
from dataclasses import asdict
from typing import Any, Dict, List

from src.scrapers.asyncronous.async_scraper import AsyncScraper
from src.models.myinvestor import MyinvestorConfig
from src.models.financial import FinProdType, FinProd
from src.models.platforms import Platform

class AsyncMyinvestorScraper(AsyncScraper):
    """
    Important! Commented by GenAI
    
    An asynchronous scraper for the MyInvestor platform, extending the base AsyncScraper class.
    
    This class allows for concurrent data fetching from various endpoints of the MyInvestor API,
    enabling efficient collection of financial products such as cash accounts, portfolios, ETFs, 
    and real estate.

    Attributes:
        config (MyinvestorConfig): Configuration object containing login info and endpoints.
        session (aiohttp.ClientSession): Asynchronous HTTP session for making API calls.
        platform (Platform): The platform identifier for MyInvestor.
    """

    def __init__(self, config: MyinvestorConfig):
        """
        Initializes the AsyncMyinvestorScraper with the given configuration.

        Args:
            config (MyinvestorConfig): Configuration object with login details and endpoints.
        """
        super().__init__(config)  # Call the parent constructor
        self.session = None  # Initialize session variable
        self.platform = Platform.MYINVESTOR  # Set the platform type

    async def login(self):
        """
        Logs into the MyInvestor platform, establishing an asynchronous session.

        Raises:
            ValueError: If there is an issue with obtaining the access token from the response.
        """
        self.session = await self._setup_session(self.config.endpoints.login, self.config.login_info)

    async def logout(self):
        """
        Logs out from the MyInvestor platform by closing the active session.

        Ensures that the session is properly closed to free up resources.
        """
        if self.session:
            await self.session.close()

    async def fetch_cash(self):
        """
        Fetches the cash accounts for the authenticated user.

        Returns:
            List[FinProd]: A list of cash financial products retrieved from the API.
        """
        async with self.session.get(self.config.endpoints.accounts) as r:
            data = await r.json()  # Parse the JSON response
            return [self._create_fin_prod_from_json(FinProdType.CASH, self.platform, l) for l in data]

    async def fetch_funds(self):
        """
        Fetches the user's investment portfolios and associated funds.

        Returns:
            List[FinProd]: A list of financial products representing the user's investment funds.
        """
        return await self._fetch_portfolios()

    async def fetch_etfs(self):
        """
        Fetches the ETFs (Exchange-Traded Funds) for the authenticated user.

        Returns:
            List[FinProd]: A list of ETF financial products retrieved from the API.
        """
        async with self.session.get(self.config.endpoints.stocks) as r:
            tmp_config = self.config.data_mapping[FinProdType.ETF]  # Get ETF configuration
            data = await r.json()  # Parse the JSON response
            return [
                self._create_fin_prod_from_json(FinProdType.ETF, self.platform, etf)
                for l in data
                for etf in l[tmp_config['etfs']]  # Extract ETFs from the response
            ]

    async def fetch_stocks(self):
        pass
    
    async def fetch_crypto(self):
        pass
    
    async def fetch_pension_funds(self):
        pass
    
    async def fetch_real_estate(self):
        """
        Fetches the real estate investments for the authenticated user.

        Returns:
            List[FinProd]: A list of real estate financial products retrieved from the API.
        """
        async with self.session.get(self.config.endpoints.real_state) as r:
            data = await r.json()  # Parse the JSON response
            return [self._create_fin_prod_from_json(FinProdType.REAL_ESTATE, self.platform, l) for l in data]

    async def fetch_all_products(self):
        """
        Fetches all financial products (cash accounts, portfolios, ETFs, and real estate) concurrently.

        Returns:
            List[FinProd]: A combined list of all financial products retrieved from the API.
        """
        print("Login...")  # Indicate login process
        await self.login()  # Log in to the platform

        print("Fetching all financial products concurrently...")  # Indicate the fetching process
        # Gather all product data concurrently using asyncio.gather
        cash_accounts, portfolios, etfs, real_estate = await asyncio.gather(
            self.fetch_cash(),
            self.fetch_funds(),
            self.fetch_etfs(),
            self.fetch_real_estate(),
        )

        # Combine all fetched products into a single list
        all_products = cash_accounts + portfolios + etfs + real_estate

        print("Logging out...")  # Indicate logout process
        await self.logout()  # Log out from the platform

        return all_products  # Return the combined list of products
    
    async def _setup_session(self, login_url, payload):
        """
        Sets up the asynchronous HTTP session, logging into the platform and obtaining an access token.

        Args:
            login_url (str): The login URL for the MyInvestor API.
            payload (Dict[str, Any]): The login information including username and password.

        Returns:
            aiohttp.ClientSession: The session object configured with the access token.

        Raises:
            ValueError: If there is an error setting up the session or obtaining the access token.
        """
        session = aiohttp.ClientSession()  # Create a new aiohttp ClientSession

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

        try:
            # Make a POST request to log in and obtain the access token
            async with session.post(login_url, json=asdict(payload), headers=headers) as response:
                response.raise_for_status()  # Raise an error for bad responses
                data = await response.json()  # Parse the JSON response

                access_token = data.get('payload', {}).get('data', {}).get('accessToken')  # Extract access token

                if not access_token:
                    raise ValueError("Access token not found in response")

                session.headers.update({'Authorization': f'Bearer {access_token}'})  # Update session headers with token

        except Exception as e:
            raise ValueError(f'Error setting up session: {e}')  # Handle session setup errors

        return session  # Return the configured session

    async def _fetch_portfolios(self) -> List[FinProd]:
        """
        Fetches the user's portfolios from the MyInvestor API.

        Returns:
            List[FinProd]: A list of financial products representing the user's portfolios.
        """
        async with self.session.get(self.config.endpoints.portfolios) as r:
            portfolios_data = await r.json()  # Parse the JSON response

        tmp_config = self.config.data_mapping[FinProdType.PORTFOLIO]  # Get portfolio configuration
        fetched_portfolios = [
            self._create_fin_prod_from_json(FinProdType.PORTFOLIO, self.platform, l, labels=l.get(tmp_config['id'], ''))
            for l in portfolios_data
        ]

        # Adding funds from portfolios
        fetched_portfolios += await self._fetch_funds(portfolios_data, tmp_config['acc'], tmp_config['funds'])
        return fetched_portfolios

    async def _fetch_funds(self, portfolio_data: List[Dict[str, Any]], acc_str: str, funds_str: str) -> List[FinProd]:
        """
        Fetches funds from the user's portfolios.

        Args:
            portfolio_data (List[Dict[str, Any]]): The portfolio data retrieved from the API.
            acc_str (str): The key for accessing account data in the portfolio.
            funds_str (str): The key for accessing fund data in the account.

        Returns:
            List[FinProd]: A list of financial products representing the user's funds.
        """
        fetched_funds = []  # Initialize list to hold fetched funds

        tmp_config = self.config.data_mapping[FinProdType.PORTFOLIO]  # Get portfolio configuration

        for portfolio in portfolio_data:
            accs = portfolio.get(acc_str, {})  # Get accounts from the portfolio
            for acc_key, acc_value in accs.items():
                if isinstance(acc_value, dict):
                    funds = acc_value.get(funds_str, [])  # Get funds from the account
                    for fund in funds:
                        fetched_funds.append(fund)  # Add funds to the list

        # Create financial product objects from the fetched funds
        return [
            self._create_fin_prod_from_json(FinProdType.FUND, self.platform, f, labels=f.get(tmp_config['id'], ''))
            for f in fetched_funds
        ]
