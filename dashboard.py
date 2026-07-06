"""
Flask Dashboard for Network Automation Toolkit.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from inventory import InventoryManager
from scanner import NetworkScanner
from backup import BackupManager
from logger import get_logger
from config import LOG_FILE, REPORTS_DIR

app = Flask(__name__)
app.secret_key = "super_secret_network_key"
logger = get_logger(__name__)

inv_manager = InventoryManager()

@app.route('/')
def index():
    devices = inv_manager.get_devices()
    return render_template('index.html', devices=devices)

@app.route('/scan', methods=['POST'])
def scan():
    subnet = request.form.get('subnet')
    if subnet:
        scanner = NetworkScanner()
        results = scanner.scan_subnet(subnet)
        flash(f"Scan complete. Found {len([r for r in results if r['status'] == 'UP'])} up devices.")
    else:
        flash("Please enter a valid subnet.")
    return redirect(url_for('index'))

@app.route('/backup', methods=['POST'])
def backup():
    devices = inv_manager.get_devices()
    if not devices:
        flash("No devices in inventory to backup.")
        return redirect(url_for('index'))
        
    backup_mgr = BackupManager(devices)
    results = backup_mgr.backup_all()
    success_count = sum(1 for status in results.values() if status == "Success")
    flash(f"Backup complete. {success_count}/{len(devices)} successful.")
    return redirect(url_for('index'))

@app.route('/logs')
def logs():
    log_content = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            log_content = f.readlines()[-50:] # last 50 lines
    return render_template('index.html', devices=inv_manager.get_devices(), logs=log_content)

def start_dashboard(port: int = 5000):
    """Start the Flask dashboard."""
    logger.info(f"Starting Flask dashboard on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    start_dashboard()
