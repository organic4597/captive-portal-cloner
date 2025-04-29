import customtkinter as ctk
import subprocess

# Wi-Fi 목록을 가져오는 함수 (단순 예시)
def get_wifi_list():
    wifi_list = []
    # 실제 Wi-Fi 목록을 얻는 명령어는 사용 환경에 따라 다를 수 있음
    result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], stdout=subprocess.PIPE, text=True)
    for line in result.stdout.splitlines()[1:]:
        ssid = line.split()[0]
        wifi_list.append(ssid)
    return wifi_list

# Wi-Fi 연결 시도하는 함수 (단순 예시)
def connect_wifi(ssid):
    print(f"{ssid} 네트워크에 연결 시도 중...")  # 실제 연결 코드를 작성해야 함
    # 실제로는 Wi-Fi 연결 코드를 작성해야 함

# GUI 설정
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# 창 만들기
root = ctk.CTk()
root.title("Captive Portal Cloner")
root.geometry("400x300")

# Wi-Fi 목록 가져오기
wifi_list = get_wifi_list()

# Wi-Fi 선택 드롭다운
wifi_dropdown = ctk.CTkComboBox(root, values=wifi_list)
wifi_dropdown.set("Wi-Fi 선택")
wifi_dropdown.pack(pady=20)

# 연결 버튼
def on_connect_button_click():
    selected_wifi = wifi_dropdown.get()
    connect_wifi(selected_wifi)
    result_label.configure(text=f"선택한 Wi-Fi: {selected_wifi} 연결 시도 중...")

connect_button = ctk.CTkButton(root, text="연결 시도", command=on_connect_button_click)
connect_button.pack(pady=10)

# 상태 라벨
result_label = ctk.CTkLabel(root, text="")
result_label.pack(pady=10)

# 실행
root.mainloop()
