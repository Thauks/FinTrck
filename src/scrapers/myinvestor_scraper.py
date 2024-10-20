import requests
from dataclasses import asdict

from src.scrapers.scraper import Scraper
from src.models.myinvestor import MyinvestorConfig
from src.models.financial import FinProdType, FinProd
from src.models.platforms import Platform

class MyinvestorScraper(Scraper):
    def __init__(self, config: MyinvestorConfig):
        super().__init__(config)
        self.session = None
        self.platform = Platform.MYINVESTOR
        
    def login(self):
        self.session = self._setup_session(self.config.endpoints.login, self.config.login_info)

    def logout(self):
        self.session.close()
    
    def fetch_cash(self):
        r = self.session.get(self.config.endpoints.accounts)
        return [self._create_fin_prod_from_json(FinProdType.CASH, self.platform, l) for l in r.json()]

    def fetch_funds(self):      
        return self._fetch_portfolios()

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
        r = self.session.get(self.config.endpoints.real_state)
        return [self._create_fin_prod_from_json(FinProdType.REAL_ESTATE, self.platform, l) for l in r.json()]
        
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
    
    def _fetch_portfolios(self):
        r = self.session.get(self.config.endpoints.portfolios)
        
        fetched_data = []
        
        for l in r.json():
            tmp_config = self.config.data_mapping[FinProdType.PORTFOLIO]
            portfolio = self._create_fin_prod_from_json(FinProdType.PORTFOLIO, self.platform, l, labels=tmp_config['id'])            
            fetched_data.append(portfolio)    
            #TODO: find a way to fetch funds from the portfolio
            #fetched_data += self._fetch_funds(l[tmp_config['acc']][tmp_config['funds']], label=tmp_config['id'])       
        return fetched_data
    
    def _fetch_funds(self, funds, label):
        return [self._create_fin_prod_from_json(FinProdType.FUND, self.platform, f, label) for f in funds]
        