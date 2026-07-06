"""
Utility functions for validation, formatting, and general helper tasks.
"""
import re
import ipaddress
from datetime import datetime
import sys

def is_valid_ip(ip: str) -> bool:
    """Validate IPv4 address."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def is_valid_hostname(hostname: str) -> bool:
    """Validate hostname."""
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def get_timestamp(format_str: str = "%Y-%m-%d_%H-%M-%S") -> str:
    """Get current timestamp as formatted string."""
    return datetime.now().strftime(format_str)

def print_progress_bar(iteration: int, total: int, prefix: str = 'Progress', suffix: str = 'Complete', length: int = 50, fill: str = '█', print_end: str = "\r"):
    """
    Call in a loop to create terminal progress bar.
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()
