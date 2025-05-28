# Stock Analysis Project

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A professional stock screening tool that filters stocks based on:
- Price-to-Sales ratio
- Liquidity requirements
- Sector exclusions (ethical screening)

## Features

- **Comprehensive Filtering**: P/S ratio, liquidity, market cap
- **Ethical Screening**: Excludes prohibited sectors
- **Multi-format Reports**: Excel and HTML outputs
- **Visual Analytics**: Interactive charts and visualizations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock_analysis_project.git
cd stock_analysis_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your raw stock data in `data/raw_stocks.csv`
2. Configure filters in `config/filter_criteria.yaml`
3. Run the main script:
```bash
python src/stock_filter.py
```

4. Find reports in the `outputs/` directory

## Sample Data Structure

The raw data CSV should contain these columns:
- `symbol`: Stock symbol
- `sector`: Industry sector
- `price`: Current price
- `sales_per_share`: Sales per share
- `shares_outstanding`: Total shares outstanding
- `liquidity`: Average daily trading volume (in millions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.