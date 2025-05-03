import subprocess
import os
import time
import signal

def get_wifi_list(interface="wlan0"):
    try:
        print("[*] Wi-Fi 스캔 중...")

        scan_dir = "/tmp"
        scan_prefix = os.path.join(scan_dir, "scan")
        scan_file = os.path.join(scan_dir, "scan-01.csv")

        # 이전 파일 제거
        if os.path.exists(scan_file):
            os.remove(scan_file)

        # airodump-ng 백그라운드 실행
        proc = subprocess.Popen(
            ['sudo', 'airodump-ng', interface, '--write', scan_prefix, '--output-format', 'csv'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid  # 프로세스 그룹 생성 (SIGTERM을 전체에 보내기 위해)
        )

        time.sleep(10)  # 수집 시간 조절 가능

        # airodump-ng 종료
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

        # 파일 생성까지 약간 대기
        time.sleep(1)

        if not os.path.exists(scan_file):
            print("[!] scan-01.csv 파일을 찾을 수 없습니다.")
            return []

        # 파일 파싱
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
                        wifi_list.append({
                            "SSID": ssid,
                            "BSSID": bssid,
                            "CHAN": channel
                        })
        return wifi_list

    except Exception as e:
        print(f"[!] Wi-Fi 목록 가져오기 실패: {e}")
        return []

# 테스트
if __name__ == "__main__":
    wifi_data = get_wifi_list("wlan0")
    if wifi_data:
        print("[*] 스캔된 Wi-Fi 목록:")
        for ap in wifi_data:
            print(f"SSID: {ap['SSID']}, BSSID: {ap['BSSID']}, Channel: {ap['CHAN']}")
    else:
        print("[!] Wi-Fi 목록을 가져올 수 없습니다.")
