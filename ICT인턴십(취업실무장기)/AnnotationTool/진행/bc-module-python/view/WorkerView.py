from tkinter import *
from PIL import Image, ImageTk
from model import LoginModel
from controller import BtnController


class WorkerWidgets:
    def __init__(self, color):
        self.color = color
        self.icon = []

    # 프레임 생성 함수
    def create_frame(self, frame, width, height=592):
        frame = Frame(frame, width=width, height=height, bg=self.color.frame_bg_color, highlightbackground=self.color.point_color, highlightthickness=3)

        return frame

    # 버튼 생성 함수
    def create_btn(self, frame, path, width=30, height=30, bg=None, command=None):
        path = "../bc-module-python/icons/workerview_icons/" + path + ".png"
        icon = Image.open(path)
        icon = icon.resize((width, height))
        self.icon.append(ImageTk.PhotoImage(icon))
        btn = Button(frame, image=self.icon[(len(self.icon)-1)], width=width, height=height,
                     bg=bg or self.color.frame_bg_color, activebackground=self.color.btn_active,
                     borderwidth=0, command=command, cursor="hand2", state=DISABLED)

        return btn

    # 라벨 생성 함수
    def create_label(self, frame, text, font=("Consolas", 12, "bold")):
        label = Label(frame, text=text, fg=self.color.naming_color, bg=self.color.bg_color, font=font)

        return label


class Toolbar:
    def __init__(self, root, w_widgets):
        self.root = root
        self.w_widgets = w_widgets

        self.toolbar_btns = dict.fromkeys(['load_btn', 'bbox_btn', 'seg_btn', 'cube_btn', 'zoomin_btn', 'zoomout_btn', 'back_btn', 'list_btn', 'hist_btn', 'save_btn'],
                                          None)    # 버튼 dict 초기값 설정 = None

    def create_toolbar(self):
        toolbar = self.w_widgets.create_frame(self.root, 60)
        toolbar.place(x=40, y=72)

        for i, key in enumerate(self.toolbar_btns):
            label = key.split('_')[0]
            button = self.w_widgets.create_btn(toolbar, label)
            button.place(x=12, y=26+56*i)
            self.toolbar_btns[key] = button


class Screen:
    def __init__(self, root, w_widgets, color):
        self.root = root
        self.w_widget = w_widgets
        self.color = color

        self.canvas = None

    def create_screen(self):
        screen = self.w_widget.create_frame(self.root, width=856)
        screen.place(x=128, y=72)

        self.canvas = Canvas(screen, width=846, height=582, bg=self.color.frame_bg_color)
        self.canvas.place(x=0, y=0)


class TaskBoard:
    def __init__(self, root, w_widgets, color):
        self.root = root
        self.color = color
        self.w_widgets = w_widgets

        self.taskboard_btns = dict.fromkeys(['fullview_btn', 'trash_btn'], None)
        self.temporary_save_listbox = None
        self.context_menu = None
        self.preview_canvas = None

    def create_task_board(self):
        task_board = self.w_widgets.create_frame(self.root, width=223)
        task_board.place(x=1017, y=72)

        for i, key in enumerate(self.taskboard_btns):
            label = key.split('_')[0]
            button = self.w_widgets.create_btn(task_board, label, 50, 50)
            button.place(x=97+58*i, y=20)
            self.taskboard_btns[key] = button

        self.temporary_save_listbox = Listbox(task_board, font=("Italic", 10, "bold"), bg=self.color.widget_bg, borderwidth=0,
                                              selectbackground=self.color.frame_bg_color, selectforeground=self.color.text_color,
                                              selectmode=SINGLE)
        self.temporary_save_listbox.place(x=15, y=85, width=173, height=467)

        # x축 스크롤바 생성
        x_scrollbar = Scrollbar(task_board, orient="horizontal", command=self.temporary_save_listbox.xview)
        x_scrollbar.place(x=15, y=552, width=173)
        self.temporary_save_listbox.configure(xscrollcommand=x_scrollbar.set)

        # y축 스크롤바 생성
        y_scrollbar = Scrollbar(task_board, orient="vertical", command=self.temporary_save_listbox.yview)
        y_scrollbar.place(x=188, y=85, height=467)
        self.temporary_save_listbox.configure(yscrollcommand=y_scrollbar.set)

        # for i in range(50):
        #     self.temporary_save_listbox.insert("end", f"Item {i + 1}")

        self.context_menu = Menu(task_board, tearoff=0)
        self.context_menu.add_command(label="보기")
        self.context_menu.add_command(label="수정")
        self.context_menu.add_command(label="삭제")


class WorkerFrame:
    def __init__(self, session, root, color):
        self.session = session
        self.root = root
        self.color = color

        self.w_widgets = WorkerWidgets(self.color)

    def create_worker_frame(self):
        # USER_ID
        id_label = self.w_widgets.create_label(self.root, text=self.session['user_id'])
        id_label.place(x=16, y=19)

        # DATA_SEQ
        data_id_text = self.w_widgets.create_label(self.root, text="DATA_ID:")
        data_id_text.place(x=130, y=37)
        # data_id_text.place(x=766, y=37)
        self.data_id_label = self.w_widgets.create_label(self.root, text="", font=("Consolas", 12, "underline"))  # configure(text=DATA_SEQ)
        self.data_id_label.place(x=210, y=37)
        # self.data_id_label.place(x=846, y=37)

        # question_btn
        self.question_btn = self.w_widgets.create_btn(self.root, "questionmark", 50, 50, bg=self.color.bg_color)
        self.question_btn.place(x=1214, y=14)

        # toolbar
        self.toolbar = Toolbar(self.root, self.w_widgets)
        self.toolbar.create_toolbar()

        # screen
        self.screen = Screen(self.root, self.w_widgets, self.color)
        self.screen.create_screen()

        # task_board
        self.task_board = TaskBoard(self.root, self.w_widgets, self.color)
        self.task_board.create_task_board()

        # Adding command to btns
        btn_controller = BtnController.BtnController(self)
        btn_controller.add_command()

        # 세션 정보 업데이트 스레드 시작
        login = LoginModel.LoginModel()
        login.update_session(self.session, self.root)

        # 프로그램 종료 (로그아웃)
        self.root.protocol("WM_DELETE_WINDOW", lambda: login.logout(self.session, self.root))

        self.root.mainloop()
