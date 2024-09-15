from tkinter import *
from model import LoginModel


class ValidatorFrame:
    def __init__(self, session):
        self.session = session
        self.login = LoginModel.LoginModel()
        self.root = Tk()
        self.root.title("validator page")
        self.root.geometry("1280x600")

    def create_validator_frame(self):
        # USER_ID
        id_label = Label(self.root, text=self.session['user_id'])
        id_label.pack()

        text_label = Label(self.main_window, text="검수자 페이지 입니다.")
        text_label.pack()

        # 세션 정보 업데이트 스레드 시작
        self.login.update_session(self.session, self.root)

        # 프로그램 종료 (로그아웃)
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.login.logout(self.session, self.root))

        self.root.mainloop()

