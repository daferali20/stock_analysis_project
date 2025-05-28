#!/usr/bin/env python3
"""
Main Stock Filtering Application with Twelve Data Integration
"""
import logging
from pathlib import Path
from typing import Dict
import pandas as pd
from api_integration.screener import StockScreener
from report_generator import generate_reports

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    try:
        logger.info("Starting US stock screening process")
        
        # Initialize screener
        screener = StockScreener()
        
        # Run screenings
        gainers_path, roe_path = screener.save_screened_data()
        
        # Load screened data
        gainers = pd.read_csv(gainers_path)
        high_roe = pd.read_csv(roe_path)
        
        # Generate reports
        generate_reports({
            'top_gainers': gainers,
            'high_roe_stocks': high_roe
        })
        
        logger.info("Process completed successfully")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()