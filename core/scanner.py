import subprocess
import platform
import re

# Wi-Fi 목록을 가져오는 함수
def get_wifi_list():
    wifi_list = []
    os_type = platform.system()

    if os_type == "Darwin":  # macOS 환경
        result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines()[1:]:  # 첫 번째 줄은 헤더라서 제외
            if line.strip():  # 공백 줄 무시
                ssid = line.split()[0]
                if ssid and ssid not in wifi_list:
                    wifi_list.append(ssid)
    else:
        raise NotImplementedError("현재 macOS만 지원됩니다.")

    return wifi_list
