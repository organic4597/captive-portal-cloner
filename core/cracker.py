import subprocess

# 딕셔너리 크랙을 실행하는 함수
def start_crack(handshake_file, wordlist_file="rockyou.txt"):
    try:
        # hashcat을 사용하여 딕셔너리 공격
        print(f"핸드쉐이크 파일: {handshake_file}, 딕셔너리 파일: {wordlist_file}")
        result = subprocess.run(
            ['sudo', 'hashcat', '-m', '22000', handshake_file, wordlist_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 크랙 결과 확인
        if result.returncode == 0:
            print("비밀번호 크랙 성공!")
            # 결과에서 비밀번호 추출
            cracked_password = extract_password(result.stdout)
            return cracked_password
        else:
            print("비밀번호 크랙 실패!")
            return None
    except Exception as e:
        print(f"크랙 중 오류 발생: {e}")
        return None

def extract_password(output):
    # hashcat의 결과에서 비밀번호 추출하는 로직
    for line in output.splitlines():
        if line.startswith("SESSION"):
            continue
        parts = line.split(':')
        if len(parts) > 1:
            return parts[1].strip()
    return None
