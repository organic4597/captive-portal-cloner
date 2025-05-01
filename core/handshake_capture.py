# core/handshake_capture.py

import subprocess
import os
import time

def start_capture(ap_bssid, channel, interface="wlan0"):
    """
    Handshake 캡처를 위한 airodump-ng 실행 함수
    """
    print(f"[+] 채널 설정: {channel}")
    subprocess.run(["iwconfig", interface, "channel", str(channel)])

    print(f"[+] Handshake 캡처 시작: {ap_bssid}")
    try:
        subprocess.run([
            "airodump-ng",
            "--bssid", ap_bssid,        # AP BSSID
            "-c", str(channel),         # 채널
            "-w", "output/captured_handshake",  # 저장 위치
            interface
        ])
    except KeyboardInterrupt:
        print("[!] 캡처 종료.")
    except Exception as e:
        print(f"[!] 에러 발생: {e}")

def stop_capture():
    """
    airodump-ng 프로세스 종료
    """
    subprocess.run(["pkill", "airodump-ng"])
    print("[+] 캡처 종료됨.")
