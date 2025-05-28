#!/usr/bin/env python3
"""
Main Stock Filtering Application
"""

import logging
from pathlib import Path
from typing import Dict
import pandas as pd
from .data_processing import load_config, load_stock_data, preprocess_data
from .report_generator import generate_reports

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    try:
        logger.info("Starting stock filtering process")
        
        # Load configuration
        config = load_config()
        
        # Load and process data
        raw_data_path = 'data/raw_stocks.csv'
        stocks_df = load_stock_data(raw_data_path)
        processed_df = preprocess_data(stocks_df, config)
        
        # Filter stocks
        filtered_df = processed_df[processed_df['rating'].isin(['excellent', 'good'])]
        filtered_df = filtered_df.sort_values(
            by=['rating', 'p/s_ratio', 'liquidity'],
            ascending=[True, True, False]
        )
        
        # Generate reports
        generate_reports(filtered_df, config)
        
        logger.info("Process completed successfully")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()