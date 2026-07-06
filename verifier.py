"""
Verification module to check device states.
"""
from typing import Dict, Any, List
from ssh_client import SSHClient
from logger import get_logger

logger = get_logger(__name__)

class Verifier:
    """Verifies operational state of devices."""
    
    @staticmethod
    def verify_hostname(device: Dict[str, Any]) -> str:
        client = SSHClient(device)
        res = client.execute_commands(["show run | include hostname"], save_output=False)
        if "error" in res:
            return "FAIL"
        
        output = res.get("show run | include hostname", "")
        expected = device.get("hostname", "")
        if expected and expected in output:
            return "PASS"
        return "FAIL"

    @staticmethod
    def verify_vlan_exists(device: Dict[str, Any], vlan_id: str) -> str:
        client = SSHClient(device)
        cmd = f"show vlan id {vlan_id}"
        res = client.execute_commands([cmd], save_output=False)
        if "error" in res:
            return "FAIL"
            
        output = res.get(cmd, "")
        if "not found" in output.lower() or not output.strip():
            return "FAIL"
        return "PASS"

    @staticmethod
    def verify_interface_status(device: Dict[str, Any], interface: str) -> str:
        client = SSHClient(device)
        cmd = f"show interface {interface} status"
        res = client.execute_commands([cmd], save_output=False)
        if "error" in res:
            return "FAIL"
            
        output = res.get(cmd, "")
        if "connected" in output.lower() or "up" in output.lower():
            return "PASS"
        return "FAIL"
