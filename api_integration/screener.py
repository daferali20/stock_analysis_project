"""
Stock screening logic for US market
"""
import pandas as pd
from typing import Tuple, Dict
import logging
from .twelve_data_client import TwelveDataClient
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)

class StockScreener:
    def __init__(self, config_path: str = '../config/twelve_data_config.yaml'):
        self.config = self._load_config(config_path)
        self.client = TwelveDataClient(
            api_key=self.config['twelve_data']['api_key'],
            base_url=self.config['twelve_data']['base_url']
        )
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise

    def screen_gainers(self) -> pd.DataFrame:
        """
        Screen for stocks with:
        - Price > $1
        - Highest percentage gain
        - Good liquidity
        """
        try:
            # Get active stocks (in practice, you might want to get a predefined list)
            stocks = self.client.get_active_stocks()
            
            if stocks.empty:
                return pd.DataFrame()
                
            # Filter and process data
            gainers = []
            for _, row in stocks.iterrows():
                symbol = row['symbol']
                
                # Get quote data
                quote = self.client.get_stock_quote(symbol)
                if not quote:
                    continue
                    
                # Apply filters
                price = float(quote.get('close', 0))
                change_pct = float(quote.get('percent_change', 0))
                volume = int(quote.get('volume', 0))
                
                if (price > self.config['screening']['min_price'] and 
                    volume > self.config['screening']['min_volume']):
                    gainers.append({
                        'symbol': symbol,
                        'name': row.get('name', ''),
                        'price': price,
                        'change_percent': change_pct,
                        'volume': volume,
                        'exchange': row.get('exchange', '')
                    })
            
            # Convert to DataFrame and sort
            df = pd.DataFrame(gainers)
            if not df.empty:
                df = df.sort_values('change_percent', ascending=False)
            return df
            
        except Exception as e:
            logger.error(f"Error in gainers screening: {e}")
            return pd.DataFrame()

    def screen_high_roe(self) -> pd.DataFrame:
        """
        Screen for stocks with:
        - High Return on Equity (ROE)
        - Price > $1
        - Good liquidity
        """
        try:
            stocks = self.client.get_active_stocks()
            
            if stocks.empty:
                return pd.DataFrame()
                
            high_roe = []
            for _, row in stocks.iterrows():
                symbol = row['symbol']
                
                # Get fundamentals
                fundamentals = self.client.get_fundamentals(symbol)
                if not fundamentals:
                    continue
                    
                # Get quote data
                quote = self.client.get_stock_quote(symbol)
                if not quote:
                    continue
                    
                # Extract metrics
                roe = float(fundamentals.get('return_on_equity', 0))
                price = float(quote.get('close', 0))
                volume = int(quote.get('volume', 0))
                
                if (roe >= self.config['screening']['roe_threshold'] and
                    price > self.config['screening']['min_price'] and
                    volume > self.config['screening']['min_volume']):
                    high_roe.append({
                        'symbol': symbol,
                        'name': row.get('name', ''),
                        'price': price,
                        'roe': roe,
                        'volume': volume,
                        'sector': fundamentals.get('sector', ''),
                        'p/s_ratio': float(fundamentals.get('price_to_sales_ttm', 0))
                    })
            
            df = pd.DataFrame(high_roe)
            if not df.empty:
                df = df.sort_values('roe', ascending=False)
            return df
            
        except Exception as e:
            logger.error(f"Error in ROE screening: {e}")
            return pd.DataFrame()

    def save_screened_data(self, output_dir: str = '../outputs') -> Tuple[str, str]:
        """Run all screens and save results"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Run screenings
        gainers = self.screen_gainers()
        high_roe = self.screen_high_roe()
        
        # Save results
        gainers_path = f"{output_dir}/top_gainers.csv"
        roe_path = f"{output_dir}/high_roe_stocks.csv"
        
        gainers.to_csv(gainers_path, index=False)
        high_roe.to_csv(roe_path, index=False)
        
        return gainers_path, roe_path