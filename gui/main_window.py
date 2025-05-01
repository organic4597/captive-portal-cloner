import customtkinter as ctk
from core.scanner import get_wifi_list  # Wi-Fi 목록 가져오기 함수
from core.deauth import deauth_attack  # deauth 공격 함수
from core.handshake_capture import capture_handshake  # handshake 캡처 함수
from core.cracker import start_crack  # 딕셔너리 크랙 함수
from core.evil_twin import start_evil_twin  # Evil Twin 생성 함수
from core.captive_portal import start_captive_portal  # Captive Portal 시작 함수

# GUI 설정
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# 창 만들기
root = ctk.CTk()
root.title("Wi-Fi 공격 시뮬레이터")
root.geometry("500x400")

# Wi-Fi 목록 가져오기
wifi_list = get_wifi_list()

# Wi-Fi 선택 드롭다운
wifi_dropdown = ctk.CTkComboBox(root, values=wifi_list)
wifi_dropdown.set("Wi-Fi 선택")
wifi_dropdown.pack(pady=20)

# 공격 상태 출력 라벨
status_label = ctk.CTkLabel(root, text="상태: 대기 중")
status_label.pack(pady=10)

# Wi-Fi 선택 후 연결 시도
def on_connect_button_click():
    selected_wifi = wifi_dropdown.get()
    status_label.configure(text=f"선택한 Wi-Fi: {selected_wifi} 연결 시도 중...")
    # 연결 시도 로직은 추후에 구현

# 공격 시작 버튼 클릭 시
def on_attack_button_click():
    selected_wifi = wifi_dropdown.get()
    status_label.configure(text=f"{selected_wifi} 공격 시작...")
    
    # 2단계: deauth + Handshake 캡처
    status_label.configure(text=f"{selected_wifi}에서 deauth 공격 및 handshake 캡처 중...")
    capture_handshake(selected_wifi)  # Handshake 캡처 실행

    # 3단계: 딕셔너리 크랙 시도
    status_label.configure(text=f"{selected_wifi} 비밀번호 크랙 시도 중...")
    crack_result = start_crack(selected_wifi)  # 크랙 시도
    if crack_result:
        status_label.configure(text=f"비밀번호 찾음: {crack_result}")
    else:
        # 4단계: 크랙 실패 시 Evil Twin 생성
        status_label.configure(text=f"비밀번호 찾기 실패, Evil Twin 생성 중...")
        start_evil_twin(selected_wifi)  # Evil Twin 실행

        # 5단계: Captive Portal 표시
        start_captive_portal()  # Captive Portal 시작

# 연결 시도 버튼
connect_button = ctk.CTkButton(root, text="연결 시도", command=on_connect_button_click)
connect_button.pack(pady=10)

# 공격 시작 버튼
attack_button = ctk.CTkButton(root, text="공격 시작", command=on_attack_button_click)
attack_button.pack(pady=10)

# 실행
root.mainloop()
