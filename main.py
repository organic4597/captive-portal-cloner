import os
import sys
from gui.main_window import launch_gui

# root 권한으로 실행되지 않은 경우, 현재 스크립트를 sudo로 다시 실행
if os.geteuid() != 0:
    print("[*] Root 권한이 필요합니다. sudo로 재실행합니다...")
    # 스크립트를 sudo로 다시 실행
    os.execvp("sudo", ["sudo", "python3"] + sys.argv)
    # root 권한일 때는 GUI 실행
if __name__ == "__main__":
    launch_gui()
