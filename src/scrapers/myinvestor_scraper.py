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

    def fetch_cash(self):
        r = self.session.get(self.config.endpoints.accounts)
        return sum([acc['importeCuenta'] for acc in r.json()])

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
    
    def fetch_real_estate(self):
        pass
    
    def _setup_session(self, login_url, payload):
        # Create a new aiohttp.ClientSession object
        session = requests.Session()
        
        session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept": "application/json"    
        })
        
        try:
            # Make a POST request to the login endpoint using the login_url and payload arguments
            with session.post(login_url, json=asdict(payload)) as response:
                # Check the status code of the response
                response.raise_for_status()
                print(response.json())
                # Update the headers attribute of the session object with a new key-value pair
                # The key is 'authorization' and the value is extracted from the response object
                
                access_token = response.json().get('payload', {}).get('data', {}).get('accessToken')

                if not access_token:
                    raise ValueError("Access token not found in response")
                
                session.headers.update({'Authorization': f'Bearer {access_token}'})

        except Exception as e:
            # If the status code of the response is not in the 2xx range, raise an error
            raise ValueError(f'Error setting up session: {e}')
        
        # Return the session object
        return session