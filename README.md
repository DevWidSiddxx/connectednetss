# Network Automation Toolkit

## Project Overview
The **Network Automation Toolkit** is a robust, production-quality Python application designed for Network Automation Engineers. It automates common operational tasks such as device discovery, inventory management, automated configuration backups, state verification, and reporting. 

It provides both a Command-Line Interface (CLI) for script-based automation and a Flask Web Dashboard for a GUI experience.

## Features
1. **Network Scanner**: Multi-threaded ping sweep to discover reachable devices in a subnet.
2. **Device Inventory**: JSON-based inventory system mapping devices, platforms, credentials, and locations.
3. **SSH Automation**: Secure remote execution on network devices (Cisco IOS, Arista, Juniper, etc.) using `netmiko`.
4. **Configuration Backup**: Automated backups of running configurations stored with timestamps.
5. **Verification Module**: Automatically check hostname, VLAN existence, interface status, and routing table integrity.
6. **Logging**: Comprehensive rotating logs for auditing and troubleshooting.
7. **Report Generator**: Export network data to CSV, JSON, and HTML.
8. **Flask Dashboard**: A web interface to view inventory, trigger scans, perform backups, and monitor logs.

## Architecture
The toolkit is built using a modular, object-oriented approach:
- **Core Modules**: `scanner.py`, `ssh_client.py`, `backup.py`, `verifier.py`
- **Data Management**: `inventory.py`, `reports.py`
- **Interfaces**: `main.py` (CLI), `dashboard.py` (Web UI)
- **Shared Utilities**: `logger.py`, `utils.py`, `config.py`

## Folder Structure
```
network-automation-toolkit/
│
├── main.py                # CLI Entrypoint
├── config.py              # Application settings and paths
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
│
├── scanner.py             # Network scanning module
├── inventory.py           # Inventory management
├── ssh_client.py          # Netmiko SSH interaction
├── backup.py              # Configuration backup module
├── verifier.py            # Device state verification
├── logger.py              # Logging configuration
├── reports.py             # Report generation (CSV/JSON/HTML)
├── dashboard.py           # Flask web application
├── utils.py               # Helper functions
│
├── inventory/             # Directory for inventory files
│   └── devices.json       # Sample JSON inventory
├── logs/                  # Directory for application logs
├── reports/               # Directory for generated reports
├── outputs/               # Directory for raw CLI outputs/backups
├── templates/             # HTML templates for Flask
│   └── index.html
├── static/                # Static web assets (CSS/JS)
└── screenshots/           # UI screenshots
```

## Requirements
- Python 3.12+
- Network connectivity to target devices.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/network-automation-toolkit.git
cd network-automation-toolkit
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Populate your device inventory in `inventory/devices.json`.

## Running the Project

### Command-Line Interface
- Scan a subnet:
  ```bash
  python main.py --scan 192.168.1.0/24
  ```
- Backup all configurations:
  ```bash
  python main.py --backup
  ```
- Generate reports:
  ```bash
  python main.py --report
  ```

### Flask Web Dashboard
- Start the dashboard:
  ```bash
  python main.py --dashboard
  ```
- Open your browser to `http://127.0.0.1:5000`

## Screenshots

*(Placeholders for future screenshots)*
- `screenshots/dashboard_home.png`
- `screenshots/cli_scan_progress.png`
- `screenshots/html_report_sample.png`

## Future Improvements
- **Configuration Templates**: Use Jinja2 to push standard configuration templates to devices (e.g., NTP, Syslog servers).
- **REST API integration**: Query modern SDN controllers (like Cisco DNA Center or Arista CloudVision).
- **Concurrency for SSH**: Parallelize SSH sessions using ThreadPoolExecutor or AsyncIO (Netmiko/Scrapli).
- **Database Backend**: Migrate inventory from JSON to SQLite or PostgreSQL.

## Networking Concepts Covered
- Subnetting and ICMP Ping Sweeps
- Device Management protocols (SSH/Telnet)
- Network Operating Systems (Cisco IOS)
- Running configurations vs. Startup configurations
- VLANs and Interface states

