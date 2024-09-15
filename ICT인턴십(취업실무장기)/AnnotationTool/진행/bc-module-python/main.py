from view import BCANTView

# if __name__ == '__main__':
#     color = BCANTView.ColorConfig()     # 색상 객체 생성
#
#     app = BCANTView.MainFrame(color)
#     app.execute()




#=================================================
# 작업자페이지로 바로 시작
from view import WorkerView
from model.LoginModel import LoginModel

if __name__ == '__main__':
    color = BCANTView.ColorConfig()     # 색상 객체 생성

    app = BCANTView.MainFrame(color)
    login_model = LoginModel()  # 인스턴스 생성
    session = login_model.create_session()

    root = app.create_main_frame()

    worker_view = WorkerView.WorkerFrame(session, root, color)
    worker_view.create_worker_frame()