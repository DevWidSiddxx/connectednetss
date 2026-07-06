"""
Network scanner to discover reachable devices.
"""
import subprocess
import platform
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from utils import print_progress_bar
from logger import get_logger

logger = get_logger(__name__)

class NetworkScanner:
    """Scans network for reachable devices."""
    
    def __init__(self, max_threads: int = 20):
        self.max_threads = max_threads

    def _ping_host(self, ip: str) -> Dict[str, any]:
        """Ping a single host and return result."""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip]
        
        try:
            # subprocess.DEVNULL is used to suppress output
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            is_up = (result.returncode == 0)
            return {'ip': ip, 'status': 'UP' if is_up else 'DOWN'}
        except subprocess.TimeoutExpired:
            return {'ip': ip, 'status': 'DOWN'}
        except Exception as e:
            logger.error(f"Error pinging {ip}: {e}")
            return {'ip': ip, 'status': 'ERROR'}

    def scan_subnet(self, subnet: str) -> List[Dict[str, any]]:
        """Scan a subnet (e.g., 192.168.1.0/24) using multithreading."""
        try:
            network = ipaddress.IPv4Network(subnet, strict=False)
            hosts = [str(ip) for ip in network.hosts()]
        except ValueError as e:
            logger.error(f"Invalid subnet {subnet}: {e}")
            return []

        logger.info(f"Scanning {len(hosts)} hosts in subnet {subnet}...")
        return self.scan_ips(hosts)

    def scan_ips(self, ip_list: List[str]) -> List[Dict[str, any]]:
        """Scan a list of IP addresses."""
        results = []
        total = len(ip_list)
        
        print_progress_bar(0, total, prefix='Scanning:', suffix='Complete', length=50)
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_ip = {executor.submit(self._ping_host, ip): ip for ip in ip_list}
            completed = 0
            
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    res = future.result()
                    results.append(res)
                except Exception as e:
                    logger.error(f"Scanner error for {ip}: {e}")
                    results.append({'ip': ip, 'status': 'ERROR'})
                finally:
                    completed += 1
                    print_progress_bar(completed, total, prefix='Scanning:', suffix='Complete', length=50)
                    
        up_count = sum(1 for r in results if r['status'] == 'UP')
        logger.info(f"Scan complete. {up_count}/{total} hosts reachable.")
        return results
