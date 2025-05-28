"""
Twelve Data API Client for real-time US stock market data
"""
import requests
import pandas as pd
from typing import List, Dict, Optional
import time
import logging
from datetime import datetime, timedelta
from ratelimit import limits, sleep_and_retry

logger = logging.getLogger(__name__)

class TwelveDataClient:
    def __init__(self, api_key: str, base_url: str = "https://api.twelvedata.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        
    @sleep_and_retry
    @limits(calls=8, period=60)  # Free tier rate limits
    def _make_request(self, endpoint: str, params: dict) -> Optional[Dict]:
        """Make API request with error handling"""
        try:
            params['apikey'] = self.api_key
            response = self.session.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None

    def get_active_stocks(self, exchange: str = 'NYSE') -> pd.DataFrame:
        """Get all active stocks for an exchange"""
        params = {
            'symbol': 'AAPL,MSFT,AMZN,GOOGL,TSLA',  # Example symbols
            'exchange': exchange,
            'country': 'United States'
        }
        data = self._make_request("/stocks", params)
        
        if data and 'data' in data:
            return pd.DataFrame(data['data'])
        return pd.DataFrame()

    def get_stock_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote for a stock"""
        params = {'symbol': symbol}
        return self._make_request("/quote", params)

    def get_fundamentals(self, symbol: str) -> Optional[Dict]:
        """Get fundamental data including ROE"""
        params = {'symbol': symbol}
        data = self._make_request("/fundamentals", params)
        
        if data and 'data' in data:
            return data['data']
        return None

    def get_time_series(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Get historical price data"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        params = {
            'symbol': symbol,
            'interval': '1day',
            'start_date': start_date,
            'end_date': end_date,
            'outputsize': days
        }
        
        data = self._make_request("/time_series", params)
        
        if data and 'values' in data:
            df = pd.DataFrame(data['values'])
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)
            return df
        return pd.DataFrame()