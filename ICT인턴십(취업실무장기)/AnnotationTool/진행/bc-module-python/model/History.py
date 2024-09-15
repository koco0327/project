from model import DBManager
import pandas as pd
from tkinter import *
from PIL import Image, ImageTk


class History:
    def __init__(self, session, history_window, color):
        self.session = session
        # self.user_seq = session['user_seq']
        self.user_seq = "USER_23050005"
        self.history_window = history_window
        self.color = color

        self.db = DBManager.DBManager()
        self.image = []

        self.show_val_window = None

    def get_history_df(self):
        columns = ['WORK_DT', 'DATA_SEQ', 'VAL_SEQ']
        work_history = self.db.query_db(query_type='select',
                                        columns=columns,
                                        table='BCANT_WDATA_TB',
                                        conditions=['WORKER_SEQ'],
                                        values=[self.user_seq])

        history_df = pd.DataFrame(work_history, columns=columns)
        history_df['WORK_DT'] = pd.to_datetime(history_df['WORK_DT'], format='%Y%m%d').dt.strftime('%Y-%m-%d')   # WORK_DT 형식 변경

        # '작업일시'열을 'WORK_DT'로 변경
        history_df.rename(columns={'WORK_DT': '작업 일시', 'DATA_SEQ': '데이터 ID'}, inplace=True)

        # 검수 확인 및 수정 열 추가
        history_df['검수'] = history_df['VAL_SEQ'].apply(lambda x: 'check_val' if x is not None else '-')
        history_df['수정'] = history_df['VAL_SEQ'].apply(lambda x: 'modify' if x is None else '-')
        history_df.drop(columns=['VAL_SEQ'], inplace=True)

        return history_df

    def show_history_table(self, canvas_frame):
        # 데이터 가져오기
        self.history_df = self.get_history_df()
        print(self.history_df)

        # 테이블 헤더 생성
        header_labels = list(self.history_df.columns)
        for col, label_text in enumerate(header_labels):
            label = Label(canvas_frame, text=label_text, padx=5, pady=5, width=20, bg=self.color.widget_bg, font=("Consolas", 12, "bold"))
            label.grid(row=0, column=col)

        # 검수 확인 또는 수정하기 버튼 생성 함수
        def history_btn(mode, row):
            if mode == 'check_val':
                text = "검수 확인"
                command = lambda: self.show_val_result(row)
            elif mode == 'modify':
                text = "수정하기"
                command = lambda: self.modify_work_content(row)

            history_btn = Button(canvas_frame, width=18, height=1, text=text, bd=0, bg=self.color.naming_color,
                                           fg=self.color.frame_bg_color,highlightcolor=self.color.widget_bg,
                                           font=("Malgun Gothic", 10, "bold"), command=command, cursor="hand2", pady=5)
            return history_btn

        # 데이터 행 생성
        for row, row_data in self.history_df.iterrows():
            for col, value in enumerate(row_data):
                if pd.isnull(value):  # None 값 처리
                    value = ''
                if value == 'check_val':
                    # 검수 확인 버튼 생성
                    button = history_btn(value, row)
                    button.grid(row=row + 1, column=col)
                elif value == 'modify':
                    # 수정하기 버튼 생성
                    button = history_btn(value, row)
                    button.grid(row=row + 1, column=col)
                else:
                    # 텍스트 삽입
                    label = Label(canvas_frame, text=str(value), padx=10, pady=5, height=2, bg=self.color.frame_bg_color)
                    label.grid(row=row + 1, column=col)

    # 검수 결과 띄우기
    def show_val_result(self, row):

        from view import NewWindowView
        n_widgets = NewWindowView.NewWindowWidgets(self.color)
        if self.show_val_window is None or not self.show_val_window.winfo_exists():        # 창 닫기 전까지 새 창 중복 생성 불가
            self.show_val_window = n_widgets.create_new_window(856, 587, title="검수 결과 보기")

            val_text1 = n_widgets.create_text_label(self.show_val_window, "준비 중 입니다.", font=("Malgun Gothic", 20, "bold"))
            val_text1.place(x=340, y=150)

            icon = Image.open("../bc-module-python/icons/not_ready.png")
            icon = icon.resize((100, 100))
            self.not_ready_icon = ImageTk.PhotoImage(icon)
            not_ready_label = Label(self.show_val_window, image=self.not_ready_icon, width=100, height=100, bg=self.color.bg_color)
            not_ready_label.place(x=378, y=200)

    # 작업 내용 수정하기
    def modify_work_content(self, row):
        data_seq = self.history_df.iloc[row, 1]
        # 그 DATA_SEQ의 파일 위치 잡아서
        # worker_frame.canvas에 로드
        print("수정하기", data_seq)