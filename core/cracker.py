import subprocess
import os

def start_crack(cap_file, wordlist="/usr/share/wordlists/rockyou.txt"):
    try:
        print(f"[*] 딕셔너리 크랙 시도 중: {cap_file}")
        output_file = "crack_result.txt"
        with open(output_file, "w") as f:
            subprocess.run([
                'aircrack-ng',
                '-w', wordlist,
                cap_file
            ], stdout=f)

        with open(output_file, "r") as f:
            for line in f:
                if "KEY FOUND!" in line:
                    password = line.split(":")[-1].strip()
                    print(f"[+] 비밀번호 찾음: {password}")
                    return password
        print("[-] 비밀번호를 찾지 못했습니다.")
        return None
    except Exception as e:
        print(f"[!] 크랙 중 오류 발생: {e}")
        return None
