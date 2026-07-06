"""
Inventory management for network devices.
"""
import json
import os
from typing import List, Dict, Any
from config import INVENTORY_FILE
from logger import get_logger

logger = get_logger(__name__)

class InventoryManager:
    """Manages device inventory."""
    
    def __init__(self, filepath: str = INVENTORY_FILE):
        self.filepath = filepath
        self.devices: List[Dict[str, Any]] = []
        self.load_inventory()

    def load_inventory(self) -> None:
        """Load devices from JSON file."""
        if not os.path.exists(self.filepath):
            logger.warning(f"Inventory file {self.filepath} not found. Creating empty inventory.")
            self.save_inventory()
            return
            
        try:
            with open(self.filepath, 'r') as f:
                self.devices = json.load(f)
            logger.info(f"Loaded {len(self.devices)} devices from inventory.")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in {self.filepath}")
            self.devices = []
        except Exception as e:
            logger.error(f"Error loading inventory: {e}")
            self.devices = []

    def save_inventory(self) -> None:
        """Save devices to JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.devices, f, indent=4)
            logger.info("Inventory saved successfully.")
        except Exception as e:
            logger.error(f"Error saving inventory: {e}")

    def add_device(self, device: Dict[str, Any]) -> bool:
        """Add a new device to inventory."""
        required_keys = {'hostname', 'ip', 'username', 'password', 'device_type'}
        if not required_keys.issubset(device.keys()):
            logger.error(f"Missing required device fields. Required: {required_keys}")
            return False
            
        # Check if IP already exists
        if any(d.get('ip') == device.get('ip') for d in self.devices):
            logger.warning(f"Device with IP {device.get('ip')} already exists.")
            return False
            
        self.devices.append(device)
        self.save_inventory()
        return True

    def get_devices(self) -> List[Dict[str, Any]]:
        """Return all devices."""
        return self.devices

    def get_device_by_ip(self, ip: str) -> Dict[str, Any]:
        """Get device by IP address."""
        for device in self.devices:
            if device.get('ip') == ip:
                return device
        return {}
