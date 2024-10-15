import requests
from dataclasses import asdict

from src.scrapers.scraper import Scraper
from src.models.myinvestor import MyinvestorConfig

class MyinvestorScraper(Scraper):
    def __init__(self, config: MyinvestorConfig):
        super().__init__(config)
        self.session = None
        
    def login(self):
        self.session = self._setup_session(self.config.endpoints.login, self.config.login_info)

    def fetch_liquid(self):
        # Implement liquid funds scraping logic here
        pass

    def fetch_funds(self):
        # Implement mutual funds scraping logic here
        pass

    def fetch_etfs(self):
        # Implement ETFs scraping logic here
        pass

    def fetch_stocks(self):
        pass
    
    def fetch_crypto(self):
        pass

    def fetch_pension_funds(self):
        pass
    
    def _setup_session(self, login_url, payload):
        # Create a new aiohttp.ClientSession object
        session = requests.Session()
        try:
            # Make a POST request to the login endpoint using the login_url and payload arguments
            with session.post(login_url, json=asdict(payload)) as response:
                # Check the status code of the response
                response.raise_for_status()

                # Update the headers attribute of the session object with a new key-value pair
                # The key is 'authorization' and the value is extracted from the response object
                session.headers.update({'authorization': (response.json())['loginFinalizadoDto']['token']})

        except Exception as e:
            # If the status code of the response is not in the 2xx range, raise an error
            raise ValueError(f'Error setting up session: {e}')
        
        # Return the session object
        return session