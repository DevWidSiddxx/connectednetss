"""
Generates CSV, JSON, and HTML reports.
"""
import csv
import json
import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from config import REPORTS_DIR, BASE_DIR
from logger import get_logger
from utils import get_timestamp
from typing import List, Dict, Any

logger = get_logger(__name__)

class ReportGenerator:
    """Generates various types of reports."""
    
    def __init__(self, data: List[Dict[str, Any]], report_prefix: str = "report"):
        self.data = data
        self.report_prefix = report_prefix
        self.timestamp = get_timestamp()

    def generate_csv(self) -> str:
        """Generate CSV report."""
        if not self.data:
            logger.warning("No data to generate CSV.")
            return ""
            
        filename = f"{self.report_prefix}_{self.timestamp}.csv"
        filepath = os.path.join(REPORTS_DIR, filename)
        
        try:
            keys = self.data[0].keys()
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.data)
            logger.info(f"CSV report generated: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error generating CSV report: {e}")
            return ""

    def generate_json(self) -> str:
        """Generate JSON report."""
        filename = f"{self.report_prefix}_{self.timestamp}.json"
        filepath = os.path.join(REPORTS_DIR, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
            logger.info(f"JSON report generated: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error generating JSON report: {e}")
            return ""

    def generate_html(self) -> str:
        """Generate HTML report using Jinja2 or Pandas."""
        if not self.data:
            return ""
            
        filename = f"{self.report_prefix}_{self.timestamp}.html"
        filepath = os.path.join(REPORTS_DIR, filename)
        
        try:
            df = pd.DataFrame(self.data)
            # Create a simple HTML table
            html_table = df.to_html(classes='table table-striped', index=False)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{self.report_prefix.capitalize()} Report</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5">
                    <h2>{self.report_prefix.capitalize()} Report</h2>
                    <p>Generated at: {self.timestamp}</p>
                    {html_table}
                </div>
            </body>
            </html>
            """
            
            with open(filepath, 'w') as f:
                f.write(html_content)
            logger.info(f"HTML report generated: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            return ""
