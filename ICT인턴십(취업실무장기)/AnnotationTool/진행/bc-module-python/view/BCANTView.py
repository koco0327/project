class ColorConfig:
    def __init__(self):
        self.bg_color = "#E8EAF6"       # 연보라색
        self.point_color = "#7258A8"    # 진보라색
        self.check_btn_color = "#1C3177"  # 남색
        self.text_color = "#000000"     # 검정색
        self.naming_color = "#4F4F4F"   # 진회색
        self.frame_bg_color = "#FFFFFF"   # 흰색
        self.widget_bg = "#D9D9D9"      # 연회색
        self.btn_active = "#E0CFE6"     # 보라색


from tkinter import *
from view import LoginView


class MainFrame:
    def __init__(self, color):
        self.color = color

    # 윈도우 크기 및 포지셔닝(center)
    def geometry_screen(self, window, window_width, window_height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 공통 창
    def create_main_frame(self):
        window = Tk()
        window.title('BCANT')
        self.geometry_screen(window, 1280, 720)
        window.configure(bg=self.color.bg_color)
        window.resizable(False, False)

        return window

    # 실행
    def execute(self):
        root = self.create_main_frame()

        login_frame = LoginView.LoginFrame(root, self.color)  # LoginFrame 객체 생성
        login_frame.create_login_frame()
