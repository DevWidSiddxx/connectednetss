"""
Configuration backup module.
"""
import os
from typing import List, Dict, Any
from ssh_client import SSHClient
from config import OUTPUTS_DIR
from logger import get_logger
from utils import get_timestamp

logger = get_logger(__name__)

class BackupManager:
    """Manages device configuration backups."""
    
    def __init__(self, devices: List[Dict[str, Any]]):
        self.devices = devices

    def backup_running_config(self, device: Dict[str, Any]) -> bool:
        """Backup running configuration for a single device."""
        client = SSHClient(device)
        
        # Command depends on platform, defaulting to cisco ios
        cmd = "show running-config"
        if "arista" in device.get("device_type", ""):
            cmd = "show running-config"
        elif "juniper" in device.get("device_type", ""):
            cmd = "show configuration"
            
        results = client.execute_commands([cmd], save_output=False)
        
        if "error" in results:
            return False
            
        output = results.get(cmd, "")
        if not output:
            return False
            
        hostname = device.get('hostname', device.get('ip'))
        timestamp = get_timestamp()
        filename = f"{hostname}_backup_{timestamp}.txt"
        filepath = os.path.join(OUTPUTS_DIR, filename)
        
        try:
            with open(filepath, 'w') as f:
                f.write(output)
            logger.info(f"Configuration backup successful for {hostname}: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error writing backup file for {hostname}: {e}")
            return False

    def backup_all(self) -> Dict[str, str]:
        """Backup all devices."""
        results = {}
        for device in self.devices:
            success = self.backup_running_config(device)
            status = "Success" if success else "Failed"
            results[device.get('hostname', device.get('ip'))] = status
            
        return results
