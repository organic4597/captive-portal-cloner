import subprocess

# Handshake 캡처를 실행하는 함수
def capture_handshake(ap_mac, interface, output_file):
    try:
        # airodump-ng 명령어를 실행하여 핸드쉐이크 캡처
        print(f"핸드쉐이크 캡처 시작: {ap_mac}")
        subprocess.run(['sudo', 'airodump-ng', '--bssid', ap_mac, '-c', '6', '--write', output_file, interface])
    except Exception as e:
        print(f"Handshake 캡처 중 오류 발생: {e}")
