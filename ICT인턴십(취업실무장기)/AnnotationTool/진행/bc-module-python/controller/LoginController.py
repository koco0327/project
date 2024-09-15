from tkinter import messagebox


class LoginController:
    def __init__(self, color):
        self.color = color

    # 로그인 버튼 클릭시 처리
    def handle_login(self, user_id, user_pwd, login_window):

        from model.LoginModel import LoginModel
        login_model = LoginModel()  # 인스턴스 생성

        result = login_model.check_login(user_id, user_pwd)  # 로그인 일치 여부 및 권한 확인

        if result:
            # 로그인 창 닫기
            login_window.destroy()

            # 로그인시 세션 생성 및 저장
            session = login_model.create_session()
            session['user_seq'] = result[0]
            session['user_id'] = result[1]
            session['user_type'] = result[2]
            login_model.save_session(session)

            if result[2] == 'W':
                from view import WorkerView, BCANTView
                main = BCANTView.MainFrame(self.color)
                root = main.create_main_frame()

                worker_frame = WorkerView.WorkerFrame(session, root, self.color)
                worker_frame.create_worker_frame()

            elif result[2] == 'V':
                from view.ValidatorView import ValidatorFrame
                validator_frame = ValidatorFrame(session)
                validator_frame.create_validator_frame()

        else:
            # 로그인 실패 시 메시지 박스 출력
            messagebox.showerror("로그인 실패", "로그인 정보가 잘못되었습니다. 다시 시도해주세요.")