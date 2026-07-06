"""
SSH client for interacting with network devices using Netmiko.
"""
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from typing import Dict, Any, List
import os
from config import OUTPUTS_DIR
from logger import get_logger
from utils import get_timestamp

logger = get_logger(__name__)

class SSHClient:
    """Handles SSH connections to devices."""
    
    def __init__(self, device_info: Dict[str, Any]):
        """
        device_info should contain:
        device_type, ip, username, password
        """
        # Mapping our internal keys to Netmiko expected keys if needed
        self.device_config = {
            'device_type': device_info.get('device_type', 'cisco_ios'),
            'ip': device_info.get('ip'),
            'username': device_info.get('username'),
            'password': device_info.get('password'),
            'global_delay_factor': 2,
        }
        if 'secret' in device_info:
            self.device_config['secret'] = device_info['secret']
            
        self.hostname = device_info.get('hostname', self.device_config['ip'])

    def execute_commands(self, commands: List[str], save_output: bool = True) -> Dict[str, str]:
        """Execute a list of commands and optionally save output."""
        results = {}
        connection = None
        try:
            logger.info(f"Connecting to {self.hostname} ({self.device_config['ip']})")
            connection = ConnectHandler(**self.device_config)
            
            # Optionally enter enable mode
            if 'secret' in self.device_config:
                connection.enable()
                
            for cmd in commands:
                logger.info(f"Executing: {cmd} on {self.hostname}")
                output = connection.send_command(cmd)
                results[cmd] = output
                
            if save_output:
                self._save_outputs(results)
                
            return results
            
        except NetmikoAuthenticationException:
            logger.error(f"Authentication failed for {self.hostname}")
            return {"error": "Authentication failed"}
        except NetmikoTimeoutException:
            logger.error(f"Connection timed out for {self.hostname}")
            return {"error": "Connection timed out"}
        except Exception as e:
            logger.error(f"SSH Error on {self.hostname}: {e}")
            return {"error": str(e)}
        finally:
            if connection:
                connection.disconnect()

    def _save_outputs(self, results: Dict[str, str]) -> None:
        """Save command outputs to files."""
        timestamp = get_timestamp()
        for cmd, output in results.items():
            if output and "error" not in results:
                safe_cmd = cmd.replace(" ", "_").replace("/", "-")
                filename = f"{self.hostname}_{safe_cmd}_{timestamp}.txt"
                filepath = os.path.join(OUTPUTS_DIR, filename)
                try:
                    with open(filepath, 'w') as f:
                        f.write(output)
                    logger.info(f"Output saved to {filepath}")
                except Exception as e:
                    logger.error(f"Failed to save output for {cmd}: {e}")
