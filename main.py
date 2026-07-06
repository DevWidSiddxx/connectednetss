"""
Main CLI entrypoint for Network Automation Toolkit.
"""
import argparse
import sys
from inventory import InventoryManager
from scanner import NetworkScanner
from backup import BackupManager
from reports import ReportGenerator
from dashboard import start_dashboard
from logger import get_logger
from colorama import init, Fore, Style

init(autoreset=True)
logger = get_logger(__name__)

def print_banner():
    banner = f"""
{Fore.CYAN}===========================================================
               Network Automation Toolkit                  
==========================================================={Style.RESET_ALL}
    """
    print(banner)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Network Automation Toolkit CLI")
    
    parser.add_argument('--scan', type=str, help="Scan a subnet (e.g., 192.168.1.0/24)")
    parser.add_argument('--backup', action='store_true', help="Backup running configurations of all devices in inventory")
    parser.add_argument('--report', action='store_true', help="Generate inventory report (CSV, JSON, HTML)")
    parser.add_argument('--dashboard', action='store_true', help="Start the Flask Web Dashboard")
    
    args = parser.parse_args()
    
    inv_manager = InventoryManager()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.scan:
        print(f"{Fore.YELLOW}Starting scan for {args.scan}...{Style.RESET_ALL}")
        scanner = NetworkScanner()
        results = scanner.scan_subnet(args.scan)
        
        report_gen = ReportGenerator(results, "scan")
        report_gen.generate_csv()
        print(f"{Fore.GREEN}Scan complete. Generated report.{Style.RESET_ALL}")

    if args.backup:
        devices = inv_manager.get_devices()
        if not devices:
            print(f"{Fore.RED}No devices found in inventory.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Starting backup for {len(devices)} devices...{Style.RESET_ALL}")
            backup_mgr = BackupManager(devices)
            results = backup_mgr.backup_all()
            for host, status in results.items():
                color = Fore.GREEN if status == "Success" else Fore.RED
                print(f"{host}: {color}{status}{Style.RESET_ALL}")

    if args.report:
        devices = inv_manager.get_devices()
        if not devices:
            print(f"{Fore.RED}No devices found in inventory.{Style.RESET_ALL}")
        else:
            report_gen = ReportGenerator(devices, "inventory")
            csv_file = report_gen.generate_csv()
            json_file = report_gen.generate_json()
            html_file = report_gen.generate_html()
            print(f"{Fore.GREEN}Reports generated successfully in reports/ folder.{Style.RESET_ALL}")

    if args.dashboard:
        start_dashboard()

if __name__ == "__main__":
    main()
