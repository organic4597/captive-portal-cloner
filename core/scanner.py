import subprocess
import os
import time

def run_cmd(cmd, desc=None):
    if desc:
        print(f"[*] {desc}... {' '.join(cmd)}")
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] 명령어 실패: {' '.join(cmd)}")

def set_monitor_mode(interface):
    run_cmd(['sudo', 'systemctl', 'stop', 'NetworkManager'], "NetworkManager 중지")
    run_cmd(['sudo', 'ip', 'link', 'set', interface, 'down'], f"{interface} 비활성화")
    run_cmd(['sudo', 'iw', interface, 'set', 'monitor', 'none'], f"{interface} 모니터 모드로 설정")
    run_cmd(['sudo', 'ip', 'link', 'set', interface, 'up'], f"{interface} 활성화")

def restore_managed_mode(interface):
    run_cmd(['sudo', 'ip', 'link', 'set', interface, 'down'], f"{interface} 비활성화")
    run_cmd(['sudo', 'iw', interface, 'set', 'type', 'managed'], f"{interface} Managed 모드로 복귀")
    run_cmd(['sudo', 'ip', 'link', 'set', interface, 'up'], f"{interface} 활성화")
    run_cmd(['sudo', 'systemctl', 'start', 'NetworkManager'], "NetworkManager 재시작")

def get_wifi_list(interface="wlan0"):
    try:
        print("[*] 모니터 모드 설정 중...")
        set_monitor_mode(interface)

        print("[*] Wi-Fi 스캔 중...")
        scan_dir = "/tmp"
        scan_file = os.path.join(scan_dir, "scan-01.csv")
        scan_prefix = os.path.join(scan_dir, "scan")

        print(f"[*] airodump-ng 실행 시작: {interface}")
        proc = subprocess.Popen(
            ['sudo', 'airodump-ng', interface, '--write', scan_prefix, '--output-format', 'csv'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # 일정 시간 대기 (15초 권장)
        print("[*] airodump-ng 실행 중... 15초 대기")
        time.sleep(15)

        print("[*] airodump-ng 종료 시도")
        proc.terminate()
        time.sleep(1)
        proc.kill()

        print("[*] CSV 파일 생성 대기 중...")
        time.sleep(3)

        if not os.path.exists(scan_file):
            print(f"[!] scan-01.csv 파일이 존재하지 않습니다: {scan_file}")
            return []

        print(f"[*] scan-01.csv 파일 발견. 파싱 시작.")
        with open(scan_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        wifi_list = []
        parsing = False
        for line in lines:
            if line.strip() == "":
                parsing = True
                continue
            if parsing:
                fields = [x.strip() for x in line.split(',')]
                if len(fields) >= 14:
                    bssid = fields[0]
                    channel = fields[3]
                    ssid = fields[13]
                    if ssid:
                        print(f"  [+] 발견된 SSID: {ssid}, BSSID: {bssid}, 채널: {channel}")
                        wifi_list.append({
                            "SSID": ssid,
                            "BSSID": bssid,
                            "CHAN": channel
                        })
        return wifi_list

    except Exception as e:
        print(f"[!] Wi-Fi 목록 가져오기 실패: {e}")
        return []

    finally:
        print("[*] 네트워크 상태 복구 중...")
        restore_managed_mode(interface)
