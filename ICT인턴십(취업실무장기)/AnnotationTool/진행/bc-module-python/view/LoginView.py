from tkinter import *
import customtkinter as ctk
from controller import LoginController


class LoginWidgets:
    def __init__(self, color):
        self.color = color

    # 입력칸 생성 함수
    def create_entry(self, frame, placeholder, show=None):

        entry = ctk.CTkEntry(frame, width=560, height=60,
                                  border_width=2, corner_radius=5, fg_color=self.color.frame_bg_color, border_color=self.color.point_color,
                                  text_color=self.color.point_color, font=("Consolas", 17, 'bold'), placeholder_text=placeholder,
                                  placeholder_text_color=self.color.point_color, show=show)

        return entry


class LoginFrame:
    def __init__(self, root, color):
        self.root = root
        self.color = color

    def create_login_frame(self):
        login_controller = LoginController.LoginController(self.color)  # LoginController 객체 생성
        login_widgets = LoginWidgets(self.color)  # LoginWidgets 객체 생성

        bg_frame = Frame(self.root, width=780, height=427, bg=self.color.frame_bg_color, highlightbackground=self.color.point_color, highlightthickness=3)
        bg_frame.place(x=249, y=143)

        heading = Label(bg_frame, text='LOGIN', fg=self.color.point_color, bg=self.color.frame_bg_color, font=(None, 32, "bold"))
        heading.place(x=322, y=39)

        user_id_entry = login_widgets.create_entry(bg_frame, " ID")
        user_id_entry.place(x=110, y=134)
        self.user_id = user_id_entry

        user_pwd_entry = login_widgets.create_entry(bg_frame, " PW", show='*')
        user_pwd_entry.place(x=110, y=228)
        self.user_pwd = user_pwd_entry

        login_btn = ctk.CTkButton(bg_frame, width=560, height=66, corner_radius=5,
                                       fg_color=self.color.point_color, hover_color=self.color.bg_color,
                                       text="LOGIN", font=("Consolas", 25, 'bold'), text_color=self.color.frame_bg_color,
                                       command=lambda: login_controller.handle_login(self.user_id.get(), self.user_pwd.get(), self.root))
        login_btn.place(x=110, y=322)

        # 엔터 키 이벤트 핸들러 등록
        self.root.bind('<Return>', lambda event: login_controller.handle_login(self.user_id.get(), self.user_pwd.get(), self.root))

        self.root.mainloop()