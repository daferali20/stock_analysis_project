"""
Report Generation Module
Handles output generation in various formats
"""

import pandas as pd
import plotly.express as px
from typing import List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def generate_excel_report(df: pd.DataFrame, output_path: str) -> None:
    """
    Generate Excel report with recommended stocks
    Args:
        df: Filtered DataFrame
        output_path: Output file path
    """
    try:
        # Create a Pandas Excel writer
        writer = pd.ExcelWriter(output_path, engine='openpyxl')
        
        # Write each rating category to separate sheet
        for rating in ['excellent', 'good']:
            subset = df[df['rating'] == rating]
            if not subset.empty:
                subset.to_excel(writer, sheet_name=f"{rating}_stocks", index=False)
        
        # Save the Excel file
        writer.close()
        logger.info(f"Excel report generated at {output_path}")
    except Exception as e:
        logger.error(f"Error generating Excel report: {e}")
        raise

def generate_html_report(df: pd.DataFrame, output_path: str, config: dict) -> None:
    """
    Generate interactive HTML report with visualizations
    Args:
        df: Filtered DataFrame
        output_path: Output file path
        config: Configuration dictionary
    """
    try:
        # Create output directory if not exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Generate visualizations
        fig1 = px.scatter(
            df,
            x='p/s_ratio',
            y='liquidity',
            color='rating',
            hover_data=['symbol', 'sector'],
            title='Price/Sales vs Liquidity'
        )
        
        fig2 = px.box(
            df,
            x='sector',
            y='p/s_ratio',
            color='rating',
            title='P/S Ratio Distribution by Sector'
        )
        
        # Generate HTML
        html_content = f"""
        <html>
            <head>
                <title>Stock Analysis Report</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            </head>
            <body>
                <h1>Stock Analysis Report</h1>
                <p>Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}</p>
                
                <h2>Key Statistics</h2>
                <div id="chart1">{fig1.to_html(full_html=False)}</div>
                
                <h2>Sector Analysis</h2>
                <div id="chart2">{fig2.to_html(full_html=False)}</div>
                
                <h2>Top Recommendations</h2>
                {df[df['rating'] == 'excellent'].to_html(index=False)}
            </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated at {output_path}")
    except Exception as e:
        logger.error(f"Error generating HTML report: {e}")
        raise

def generate_reports(df: pd.DataFrame, config: dict, output_dir: str = 'outputs') -> None:
    """
    Generate all configured reports
    Args:
        df: Filtered DataFrame
        config: Configuration dictionary
        output_dir: Output directory path
    """
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        report_settings = config.get('report_settings', {})
        formats = report_settings.get('output_formats', [])
        
        if 'excel' in formats:
            excel_path = f"{output_dir}/recommended_stocks.xlsx"
            generate_excel_report(df, excel_path)
        
        if 'html' in formats:
            html_path = f"{output_dir}/analysis_summary.html"
            generate_html_report(df, html_path, config)
            
        logger.info("All reports generated successfully")
    except Exception as e:
        logger.error(f"Error in report generation: {e}")
        raise