import bcrypt
from tkinter import messagebox
import time
import threading
from uuid import uuid4
from model.DBManager import DBManager
import getmac
import sys
import os

# 로그인 관리
class LoginModel:
    def __init__(self):
        self.db = DBManager()
        self.session_check_thread = None  # 세션 체크 스레드 객체
        self.session_check_running = True  # 스레드 실행 플래그 변수


    # 로그인 체크 함수
    def check_login(self, user_id, user_pwd):
        user = self.db.query_db(query_type='select', columns=['USER_SEQ', 'USER_ID', 'USER_PWD', 'USER_TYPE'], table='BCANT_USER_TB', conditions=['USER_ID'], values=[user_id])
        if user:
            hashed_pwd = user[2].encode('utf-8')
            if bcrypt.checkpw(user_pwd.encode('utf-8'), hashed_pwd):
                user_type = user[3]
                if user_type == 'W':
                    return (user[0], user[1], user[3])
                elif user_type == 'V':
                    return (user[0], user[1], user[3])
        return False

    # 세션 생성 함수
    def create_session(self):
        session_seq = str(uuid4())
        session = {
            'session_seq': session_seq,
            'user_seq': None,
            'user_id': None,
            'user_type': None
        }
        return session

    # DB에 세션 정보 저장
    def save_session(self, session):
        existing_session = self.db.query_db(query_type='select', table='BCANT_SESSION_TB', conditions=['USER_SEQ'], values=[session['user_seq']])
        mac_addr = getmac.get_mac_address()
        if existing_session:
            self.db.query_db(query_type='update', table='BCANT_SESSION_TB', update_data='SESSION_SEQ', condition='USER_SEQ', values=(session['session_seq'], mac_addr, session['user_seq']))
        else:
            self.db.query_db(query_type='insert', table='BCANT_SESSION_TB', columns='SESSION_SEQ, USER_SEQ, LOGIN_TIME, MAC_ADDR', values=(session['session_seq'], session['user_seq'], mac_addr))

    # 중복 로그인 체크를 위한 세션 업데이트
    def update_session(self, session, main_window):
        self.session_check_running = True  # 스레드 실행 플래그 변수 설정
        self.session_thread = threading.Thread(target=self.check_session, args=(session, main_window))
        self.session_thread.start()

    # 세션ID 비교를 통한 중복 로그인 체크
    def check_session(self, session, main_window):
        while self.session_check_running:
            # db 재연결
            self.db = DBManager()
            # 현재 사용자의 세션 정보 가져오기
            current_session = self.db.query_db(query_type='select', table='BCANT_SESSION_TB', conditions=['USER_SEQ'], values=[session['user_seq']])

            # 세션 ID 일치 여부 확인
            if current_session and current_session[0] != session['session_seq']:
                # 세션 정보 삭제 후 로그인 페이지로 이동
                messagebox.showinfo("중복 로그인", "중복 로그인이 감지되었습니다.\n로그아웃됩니다.")
                self.session_check_running = False
                os._exit(0)
            time.sleep(3)  # 3초마다 세션 정보를 업데이트

    # 로그아웃
    def logout(self, session, main_window):
        # 스레드 종료를 위해 플래그 변수 변경
        self.session_check_running = False
        # DB에서 세션 정보 삭제
        result = messagebox.askquestion("종료", "프로그램을 종료하시겠습니까?")
        if result == 'yes':
            self.db.query_db(query_type='delete', table='BCANT_SESSION_TB', condition='USER_SEQ', values=session['user_seq'])
            main_window.destroy()
            sys.exit()

            # #프로세스 종료를 위한 최후의 방법 - 디버깅이 어려울 수도 있음
            # # after() 부분을 고쳐야 함
            # import os
            # os.kill(os.getpid(), 9)