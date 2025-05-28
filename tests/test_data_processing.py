import pytest
import pandas as pd
from src.data_processing import load_stock_data, preprocess_data
from src.stock_filter import main

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'symbol': ['STOCK1', 'STOCK2', 'STOCK3'],
        'sector': ['technology', 'gambling', 'healthcare'],
        'price': [100, 50, 75],
        'sales_per_share': [20, 10, 15],
        'shares_outstanding': [10, 5, 8],
        'liquidity': [1.5, 0.8, 2.0]
    })

def test_load_stock_data(tmp_path, sample_data):
    # Create temporary CSV file
    file_path = tmp_path / "test_stocks.csv"
    sample_data.to_csv(file_path, index=False)
    
    # Test loading
    loaded_data = load_stock_data(file_path)
    assert len(loaded_data) == 3
    assert 'p/s_ratio' in loaded_data.columns

def test_sector_exclusion(sample_data):
    config = {
        'excluded_sectors': ['gambling'],
        'filters': {
            'liquidity': {'min': 1.0},
            'market_cap': {'min': 100},
            'price_to_sales': {'max': 5.0, 'excellent': 2.0}
        }
    }
    
    processed = preprocess_data(sample_data, config)
    assert len(processed) == 2
    assert 'gambling' not in processed['sector'].values