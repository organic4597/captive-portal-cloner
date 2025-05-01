# core/scan_wifi.py

import subprocess
import platform
import re

def get_wifi_list():
    wifi_list = []
    os_type = platform.system()

    if os_type == "Windows":
        result = subprocess.run(['netsh', 'wlan', 'show', 'network'], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if "SSID" in line:
                match = re.search(r"SSID\s+\d+\s*:\s*(.+)", line)
                if match:
                    ssid = match.group(1).strip()
                    if ssid and ssid not in wifi_list:
                        wifi_list.append(ssid)
    else:
        result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines()[1:]:
            if line.strip():
                ssid = line.split()[0]
                if ssid and ssid not in wifi_list:
                    wifi_list.append(ssid)

    return wifi_list
