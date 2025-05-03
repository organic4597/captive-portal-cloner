import subprocess

def capture_handshake(bssid, channel, interface="wlan0", output_file="handshake"):
    try:
        print(f"[*] {bssid} 채널 {channel}에서 핸드쉐이크 캡처 시작")
        subprocess.run([
            'sudo', 'airodump-ng',
            '--bssid', bssid,
            '-c', str(channel),
            '--write', output_file,
            interface
        ])
    except Exception as e:
        print(f"[!] Handshake 캡처 중 오류 발생: {e}")
