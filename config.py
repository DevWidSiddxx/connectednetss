"""
Configuration constants and settings for the Network Automation Toolkit.
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories
INVENTORY_DIR = os.path.join(BASE_DIR, "inventory")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# File paths
INVENTORY_FILE = os.path.join(INVENTORY_DIR, "devices.json")
LOG_FILE = os.path.join(LOGS_DIR, "automation.log")

# Ensure required directories exist
for directory in [INVENTORY_DIR, LOGS_DIR, REPORTS_DIR, OUTPUTS_DIR]:
    os.makedirs(directory, exist_ok=True)
