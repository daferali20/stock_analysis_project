"""
Stock Data Processing Module
Handles data loading, cleaning, and preprocessing
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict
import yaml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path: str = 'config/filter_criteria.yaml') -> Dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise

def load_stock_data(file_path: str) -> pd.DataFrame:
    """
    Load stock data from CSV file
    Args:
        file_path: Path to CSV file
    Returns:
        Cleaned DataFrame with stock data
    """
    try:
        df = pd.read_csv(file_path, parse_dates=['date'], infer_datetime_format=True)
        
        # Data cleaning
        df = df.dropna(subset=['symbol', 'sector', 'price', 'sales_per_share'])
        df = df[df['price'] > 0]
        df = df[df['sales_per_share'] > 0]
        
        # Calculate metrics
        df['p/s_ratio'] = df['price'] / df['sales_per_share']
        df['market_cap'] = df['price'] * df['shares_outstanding']
        
        logger.info(f"Successfully loaded {len(df)} records")
        return df
    except Exception as e:
        logger.error(f"Error loading stock data: {e}")
        raise

def preprocess_data(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """
    Apply preprocessing steps to stock data
    Args:
        df: Raw stock DataFrame
        config: Configuration dictionary
    Returns:
        Processed DataFrame
    """
    try:
        # Apply sector filters
        excluded = config.get('excluded_sectors', [])
        df = df[~df['sector'].isin(excluded)]
        
        # Apply basic data quality filters
        df = df[df['liquidity'] >= config['filters']['liquidity']['min']]
        df = df[df['market_cap'] >= config['filters']['market_cap']['min']]
        
        # Categorize stocks
        df['rating'] = np.where(
            df['p/s_ratio'] < config['filters']['price_to_sales']['excellent'],
            'excellent',
            np.where(
                df['p/s_ratio'] < config['filters']['price_to_sales']['max'],
                'good',
                'rejected'
            )
        )
        
        logger.info("Data preprocessing completed")
        return df
    except Exception as e:
        logger.error(f"Error in preprocessing: {e}")
        raise