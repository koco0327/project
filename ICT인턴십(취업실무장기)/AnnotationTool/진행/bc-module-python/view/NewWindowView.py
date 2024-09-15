from tkinter import *
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox


class NewWindowWidgets:
    def __init__(self, color):
        self.color = color

    # 새 창 생성 함수
    def create_new_window(self, width, height, title, btn=None):
        if btn is not None:
            btn.configure(bg=self.color.btn_active)  # btn 활성화 표시 (색 변환)
        new_window = Toplevel(bg=self.color.bg_color, width=width, height=height)

        from view import BCANTView
        main = BCANTView.MainFrame(self.color)  # center positioning을 위한 객체 생성
        main.geometry_screen(new_window, width, height)
        new_window.resizable(False, False)
        new_window.title(title)

        return new_window

    def close_new_window(self, window, btn, bg=None):
        btn.configure(bg=bg or self.color.frame_bg_color)
        if window.winfo_exists():
            window.destroy()

    # 버튼 생성 함수
    def create_btn(self, window, width, height, text, command=None, font=("Consolas", 16, "bold")):
        check_btn = ctk.CTkButton(window, width=width, height=height, corner_radius=3,
                                  fg_color=self.color.check_btn_color, hover_color=self.color.point_color,
                                  text=text, font=font, text_color=self.color.frame_bg_color,
                                  command=command, cursor="hand2")

        return check_btn

    # text 생성 함수
    def create_text_label(self, window, text, font, wraplength=None):
        text_label = Label(window, text=text, bg=self.color.bg_color, bd=0, font=font, justify="left",
                           wraplength=wraplength)

        return text_label


class NewWindow:
    def __init__(self, btn_controller):
        self.btn_controller = btn_controller
        self.root = btn_controller.root
        self.color = btn_controller.color
        self.n_widgets = NewWindowWidgets(self.color)
        self.close_new_w = self.n_widgets.close_new_window
        self.btns = btn_controller.btns

        self.canvas = btn_controller.canvas
        self.temporary_save_listbox = btn_controller.task_board.temporary_save_listbox  # 일단은 temporary_save_listbox 만 사용
        self.worker_frame = btn_controller.worker_frame  # 일단은 question btn 만 사용

        # 창 닫기 전까지 새 창 중복 생성 불가
        self.load_window = None
        self.auto_load_window = None
        self.about_window = None
        self.label_window = None
        self.history_window = None
        self.fullview_window = None

    # 단축키 확인창
    def about_box(self):
        question_btn = self.worker_frame.question_btn
        if self.about_window is None or not self.about_window.winfo_exists():  # 창 닫기 전까지 새 창 중복 생성 불가
            self.about_window = self.n_widgets.create_new_window(534, 293, title="단축키 확인", btn=question_btn)

            hotkey_text = "CTRL + S \nCTRL + Z\nCTRL + (+/-)\nCTRL + Mouse Wheel (UP/DOWN))\nCTRL + Mouse Drag\nArrow Keys"
            hotkey_explain = "임시 저장 \n뒤로 가기\n이미지 확대 및 축소\n이미지 확대 및 축소\n이미지 이동\n이미지 이동"

            about_hotkey1 = self.n_widgets.create_text_label(self.about_window, hotkey_text,
                                                             font=("Malgun Gothic", 12, "normal"))
            about_hotkey1.place(x=50, y=50)
            about_hotkey2 = self.n_widgets.create_text_label(self.about_window, hotkey_explain,
                                                             font=("Malgun Gothic", 12, "bold"))
            about_hotkey2.place(x=330, y=50)

            check_btn = self.n_widgets.create_btn(self.about_window, 151, 45, text="확인",
                                                  command=lambda: self.close_new_w(self.about_window, question_btn,
                                                                                   self.color.bg_color))
            check_btn.place(x=192, y=225)

            self.about_window.protocol("WM_DELETE_WINDOW",
                                       lambda: self.close_new_w(self.about_window, question_btn, self.color.bg_color))

    # 불러 오기 창
    def load_box(self):
        load_btn = self.btns['load_btn']
        if self.temporary_save_listbox.size() >= 1:
            result = messagebox.askquestion("전체 삭제", "리스트 목록을 전체 삭제하시겠습니까?")
            if result == 'yes':
                self.temporary_save_listbox.delete(0, END)
                self.btn_controller.set_btns_state(self.btn_controller.with_label_btns, DISABLED)

        if self.load_window is None or not self.load_window.winfo_exists():  # 창 닫기 전까지 새 창 중복 생성 불가
            self.load_window = self.n_widgets.create_new_window(534, 293, title="불러오기", btn=load_btn)
            self.load_window.grab_set()  # 새 창에 focus

            load_text1 = self.n_widgets.create_text_label(self.load_window, "프로젝트 및 데이터 불러오기 방식을 선택해주세요.",
                                                          font=("Consolas", 10, "bold"))
            load_text1.place(x=125, y=70)

            # 콤보박스의 선택 값을 추적하기 위한 StringVar 변수 생성
            combobox_var = StringVar()

            # 콤보박스 생성
            combobox = ttk.Combobox(self.load_window, values=combobox_var, state="readonly")
            combobox['values'] = ('project 1', 'project 2', 'project 3')
            combobox.place(x=190, y=135)

            from model import Load
            loader = Load.Load(self.btn_controller)
            self.load_auto_btn = self.n_widgets.create_btn(self.load_window, 151, 45, text="자동",
                                                           command=lambda: self.load_auto_box(loader, load_btn))
            self.load_auto_btn.place(x=72, y=222)
            self.load_manual_btn = self.n_widgets.create_btn(self.load_window, 151, 45, text="수동",
                                                             command=lambda: loader.load_manual(self.load_window))
            self.load_manual_btn.place(x=323, y=222)

            self.load_window.protocol("WM_DELETE_WINDOW", lambda: self.close_new_w(self.load_window, load_btn))

    def load_auto_box(self, loader, load_btn):
        self.load_window.destroy()
        if self.auto_load_window is None or not self.auto_load_window.winfo_exists():  # 창 닫기 전까지 새 창 중복 생성 불가
            self.auto_load_window = self.n_widgets.create_new_window(500, 600, title="자동으로 불러오기")
            self.auto_load_window.grab_set()  # 새 창에 focus

            list_frame = self.btn_controller.worker_frame.w_widgets.create_frame(self.auto_load_window, width=430,
                                                                                 height=460)
            list_frame.place(x=36, y=25)

            self.auto_listbox = Listbox(list_frame, width=60, height=28)
            self.auto_listbox.pack(side="left", fill="y")
            # self.auto_listbox.place(x=37, y=25)

            scrollbar = Scrollbar(list_frame, orient="vertical", command=self.auto_listbox.yview)
            scrollbar.pack(side="right", fill="y")

            # for x in range(100):
            #     self.auto_listbox.insert(END, str(x))

            jpg_files = loader.load_auto_list()
            for file in jpg_files:
                self.auto_listbox.insert(END, file)

            check_btn = self.n_widgets.create_btn(self.auto_load_window, 151, 45, text="확인",
                                                  command=lambda: loader.load_auto(self.auto_load_window,
                                                                                   self.auto_listbox))
            check_btn.place(x=174, y=530)

            self.auto_load_window.protocol("WM_DELETE_WINDOW",
                                           lambda: self.close_new_w(self.auto_load_window, load_btn))

    def label_box(self):
        list_btn = self.btns['list_btn']
        if list_btn.cget("state") == NORMAL:
            ######## 리스트박스 예시 ###########################################################
            self.data_seq = 'DATA_00000002'  # load_auto 할 때 가져옴
            self.label_depth = 0
            ###################################################################################

            if self.label_window is None or not self.label_window.winfo_exists():  # 창 닫기 전까지 새 창 중복 생성 불가
                self.label_window = self.n_widgets.create_new_window(316, 464, title="라벨 선택", btn=list_btn)
                self.label_window.grab_set()  # 새 창에 focus

                from controller import LabelController
                self.label_controller = LabelController.LabelController(self.btn_controller)
                self.result = self.label_controller.label_window(self.data_seq)

                self.label_list_box = Listbox(self.label_window, font=("Italic", 11, "bold"),
                                              bg=self.color.frame_bg_color,
                                              selectbackground=self.color.widget_bg,
                                              selectforeground=self.color.text_color,
                                              borderwidth=1, selectmode=SINGLE)
                self.label_list_box.place(x=48, y=39, width=220, height=230)
                for item in self.result:
                    self.label_list_box.insert(END, item)

                # ######## 선택된 라벨 예시 ########################
                selected_label = self.n_widgets.create_text_label(self.label_window, text="",
                                                                  font=("Malgun Gothic", 10, "normal"), wraplength=187)
                selected_label.place(x=64, y=280)
                # ##############################################

                self.lebel_back_btn = self.n_widgets.create_btn(self.label_window, 187, 38, text="이전",
                                                                command=lambda: self.label_controller.delete_select_label(
                                                                    selected_label, self.label_list_box, self.save_btn))
                self.lebel_back_btn.place(x=64, y=360)

                self.save_btn = self.n_widgets.create_btn(self.label_window, 187, 38, text="임시 저장",
                                                          font=("Malgun Gothic", 15, "bold"),
                                                          command=lambda: self.label_controller.temporary_save(
                                                              self.close_new_w(self.label_window, list_btn),
                                                              self.temporary_save_listbox))
                self.save_btn.configure(state=DISABLED)  # 버튼 비활성화
                self.save_btn.place(x=64, y=408)

                # 라벨 선택시 하위라벨 변경 event
                self.label_list_box.bind('<<ListboxSelect>>',
                                         lambda event: self.label_controller.on_selection(event, selected_label,
                                                                                          self.save_btn))

                self.label_window.protocol("WM_DELETE_WINDOW", lambda: self.close_new_w(self.label_window, list_btn))

    # 히스토리 창
    def history_box(self):
        hist_btn = self.btns['hist_btn']
        if self.history_window is None or not self.history_window.winfo_exists():  # 창 닫기 전까지 새 창 중복 생성 불가
            self.history_window = self.n_widgets.create_new_window(856, 587, title="히스토리", btn=hist_btn)
            self.history_window.grab_set()  # 새 창에 focus

            session = self.btn_controller.worker_frame.session

            table_frame = self.btn_controller.worker_frame.w_widgets.create_frame(self.history_window, width=770,
                                                                                  height=400)
            table_frame.place(x=25, y=60)

            scrollbar = Scrollbar(table_frame)
            scrollbar.pack(side="right", fill="y")

            hist_canvas = Canvas(table_frame, yscrollcommand=scrollbar.set, width=770, height=400,
                                 bg=self.color.frame_bg_color)
            hist_canvas.pack(side="left", fill="both", expand=True)
            scrollbar.configure(command=hist_canvas.yview)

            canvas_frame = Frame(hist_canvas, bg=self.color.frame_bg_color)
            hist_canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

            def on_frame_configure(event):
                hist_canvas.configure(scrollregion=hist_canvas.bbox("all"))

            canvas_frame.bind("<Configure>", on_frame_configure)

            # from model import HistoryTree
            # history = HistoryTree.HistoryTree(session, self.history_window, self.color)
            # history.show_history_table()

            from model import History
            history = History.History(session, self.history_window, self.color)
            history.show_history_table(canvas_frame)

            check_btn = self.n_widgets.create_btn(self.history_window, 167, 48, text="확인",
                                                  command=lambda: self.close_new_w(self.history_window, hist_btn))
            check_btn.place(x=356, y=516)

            self.history_window.protocol("WM_DELETE_WINDOW", lambda: self.close_new_w(self.history_window, hist_btn))

    def fullview_box(self):
        fullview_btn = self.btns['fullview_btn']
        if self.fullview_window is None or not self.fullview_window.winfo_exists():  # 창 닫기 전까지 새 창 중복 생성 불가
            self.fullview_window = self.n_widgets.create_new_window(886, 720, title="전체보기", btn=fullview_btn)
            self.fullview_window.grab_set()  # 새 창에 focus

            table_frame = self.btn_controller.worker_frame.w_widgets.create_frame(self.fullview_window, width=770,
                                                                                  height=400)
            table_frame.place(x=20, y=38)

            fullview_canvas = Canvas(table_frame, width=846, height=582, bg=self.color.frame_bg_color)
            fullview_canvas.pack(fill="both")

            check_btn = self.n_widgets.create_btn(self.fullview_window, 167, 48, text="확인",
                                                  command=lambda: self.close_new_w(self.fullview_window, fullview_btn))
            check_btn.place(x=360, y=648)

            self.fullview_window.protocol("WM_DELETE_WINDOW",
                                          lambda: self.close_new_w(self.fullview_window, fullview_btn))

