from model import DBManager, Hotkey
from view import NewWindowView
from controller import ToolController
from tkinter import *
import tkinter.constants as tk_const


class BtnController:
    def __init__(self, worker_frame):
        self.worker_frame = worker_frame
        self.root = worker_frame.root
        self.color = worker_frame.color

        self.toolbar_btns = worker_frame.toolbar.toolbar_btns
        self.canvas = worker_frame.screen.canvas
        self.task_board = worker_frame.task_board
        self.btns = {**worker_frame.toolbar.toolbar_btns, **self.task_board.taskboard_btns}
        self.new_w = NewWindowView.NewWindow(self)
        self.db = DBManager.DBManager()

        # self.disabled_btns = ['bbox_btn', 'seg_btn', 'cube_btn', 'zoomin_btn', 'zoomout_btn', 'back_btn', 'list_btn', 'save_btn', 'fullview_btn', 'trash_btn']
        self.start_btns = ['load_btn', 'hist_btn']
        self.with_load_btns = ['bbox_btn', 'seg_btn', 'cube_btn', 'zoomin_btn', 'zoomout_btn', 'back_btn']
        self.with_label_btns = ['save_btn', 'fullview_btn', 'trash_btn']

        self.bbox_active = False
        self.seg_active = False
        self.cube_active = False
        self.cube_window = None
        self.label_active = False

        self.bbox = ToolController.BBoxController(self.canvas, self)
        self.seg = ToolController.SegController(self.canvas, self)
        self.cube = ToolController.CubeController(self.canvas,self)

        self.enabled_buttons = []
    # btns 활성화/비활성화 함수
    def set_btns_state(self, btn_list, state):
        for key, value in self.btns.items():
            if key in btn_list:
                value.configure(state=state)

    def activate_hotkeys(self, image, tk_image):
        hotkey = Hotkey.Hotkey(self.root, self.canvas, image, tk_image, self.new_w, self.btns, self.bbox)
        self.btns['zoomin_btn'].configure(command=lambda: hotkey.zoom_in())
        self.btns['zoomout_btn'].configure(command=lambda: hotkey.zoom_out())
        self.btns['back_btn'].configure(command=lambda: hotkey.step_back())

    # 프로젝트에 따라 tool 비활성화
    def disabled_btn(self, data_seq):
        # 입력한 DATA_SEQ 값에 대한 PRJ_SEQ 값을 가져옴
        prj_seq = self.db.query_db(query_type='select', columns=['PRJ_SEQ'], table='BCANT_WDATA_TB',
                                   conditions=['DATA_SEQ'], values=[data_seq])

        # PRJ_SEQ 값에 대한 tool 활성화 여부 값 가져옴
        search_tool = self.db.query_db(query_type='select', columns=['BB_YN', 'SEG_YN', 'CUBE_YN'],
                                       table='BCANT_PRJ_TB', conditions=['PRJ_SEQ'], values=[prj_seq[0][0]])

        # 버튼 활성화 / 비활성화
        for index, btn in enumerate(['bbox_btn', 'seg_btn', 'cube_btn']):
            self.btns[btn].configure(state=tk_const.NORMAL and self.enabled_buttons.append(btn) if search_tool[index] == 'Y' else tk_const.DISABLED)
    # 버튼 클릭시 버튼 색 변경
    def toggle_background(self, btn, active):
        if active == True:
            btn.configure(bg=self.color.btn_active)
        else:
            btn.configure(bg=self.color.frame_bg_color)

    def toggle_bbox(self):
        self.bbox_active = not self.bbox_active
        self.toggle_background(self.toolbar_btns['bbox_btn'], self.bbox_active)
        self.label_active = not self.label_active

        if self.bbox_active:
            self.bbox.bbox_bind_events()
            self.btns['list_btn'].configure(state=NORMAL)

            if self.enabled_buttons:
                for btn in self.enabled_buttons:
                    if btn != 'bbox_btn':
                        self.btns[btn].configure(state=DISABLED)
            else:
                self.btns['seg_btn'].configure(state=tk_const.DISABLED)
                self.btns['cube_btn'].configure(state=tk_const.DISABLED)
        else:
            self.bbox.bbox_unbind()
            self.bbox.bbox_reset()
            self.btns['list_btn'].configure(state=DISABLED)

            if self.enabled_buttons:
                for btn in self.enabled_buttons:
                    self.btns[btn].configure(state=tk_const.NORMAL)
            else:
                self.btns['seg_btn'].configure(state=tk_const.NORMAL)
                self.btns['cube_btn'].configure(state=tk_const.NORMAL)

    def toggle_seg(self):
        self.seg_active = not self.seg_active
        self.toggle_background(self.toolbar_btns['seg_btn'], self.seg_active)
        self.label_active = not self.label_active

        if self.seg_active:
            self.seg.seg_bind_events()
            self.btns['list_btn'].configure(state=NORMAL)

            if self.enabled_buttons:
                for btn in self.enabled_buttons:
                    if btn != 'seg_btn':
                        self.btns[btn].configure(state=DISABLED)
            else:
                self.btns['bbox_btn'].configure(state=tk_const.DISABLED)
                self.btns['cube_btn'].configure(state=tk_const.DISABLED)

        else:
            self.seg.seg_unbind()
            self.seg.seg_reset()
            self.btns['list_btn'].configure(state=DISABLED)

            if self.enabled_buttons:
                for btn in self.enabled_buttons:
                    self.btns[btn].configure(state=tk_const.NORMAL)
            else:
                self.btns['bbox_btn'].configure(state=tk_const.NORMAL)
                self.btns['cube_btn'].configure(state=tk_const.NORMAL)


    def toggle_cube(self):
        self.cube_active = not self.cube_active
        self.toggle_background(self.toolbar_btns['cube_btn'], self.cube_active)
        self.label_active = not self.label_active

        if self.cube_active:
            self.cube.cube_bind_events()
            self.btns['list_btn'].configure(state=NORMAL)

            if self.enabled_buttons:
                for btn in self.enabled_buttons:
                    if btn != 'cube_btn':
                        self.btns[btn].configure(state=DISABLED)
            else:
                self.btns['bbox_btn'].configure(state=tk_const.DISABLED)
                self.btns['seg_btn'].configure(state=tk_const.DISABLED)

        else:
            self.cube.cube_unbind()
            self.cube.cube_reset()
            self.btns['list_btn'].configure(state=DISABLED)

            if self.enabled_buttons:
                for btn in self.enabled_buttons:
                    self.btns[btn].configure(state=tk_const.NORMAL)
            else:
                self.btns['bbox_btn'].configure(state=tk_const.NORMAL)
                self.btns['seg_btn'].configure(state=tk_const.NORMAL)

    ###############################################################################################
    ###############################################################################################

        # from PIL import Image, ImageTk
        # from view import NewWindowView
        # n_widgets = NewWindowView.NewWindowWidgets(self.color)
        # if self.cube_window is None or not self.cube_window.winfo_exists():        # 창 닫기 전까지 새 창 중복 생성 불가
        #     self.cube_window = n_widgets.create_new_window(856, 587, title="큐보이드 공사중")
        #
        #     val_text1 = n_widgets.create_text_label(self.cube_window, "준비 중 입니다.", font=("Malgun Gothic", 20, "bold"))
        #     val_text1.place(x=340, y=150)
        #
        #     icon = Image.open("../bc-module-python/icons/not_ready.png")
        #     icon = icon.resize((100, 100))
        #     self.not_ready_icon = ImageTk.PhotoImage(icon)
        #     not_ready_label = Label(self.cube_window, image=self.not_ready_icon, width=100, height=100, bg=self.color.bg_color)
        #     not_ready_label.place(x=378, y=200)


    ###############################################################################################
    ###############################################################################################
    def show_context_menu(self, event):
        if self.task_board.temporary_save_listbox.curselection():
            self.task_board.context_menu.post(event.x_root, event.y_root)

    ###############################################################################################
    ###############################################################################################

    # 각 버튼에 command 적용
    def add_command(self):
        # 시작 버튼만 활성화
        self.set_btns_state(self.start_btns, NORMAL)

        # worker_frame_btns
        self.worker_frame.question_btn.configure(command=lambda: self.new_w.about_box())

        # toolbar_btns
        self.toolbar_btns['load_btn'].configure(command=lambda: self.new_w.load_box())
        ################ 현중님 코드 변경되면 변경 ##########################################################
        self.toolbar_btns['bbox_btn'].configure(command=lambda: self.toggle_bbox())
        self.toolbar_btns['seg_btn'].configure(command=lambda: self.toggle_seg())
        self.toolbar_btns['cube_btn'].configure(command=lambda: self.toggle_cube())
        ##################################################################################################
        # zoomin, zoomout, back 은 load 후에 command configuring
        self.toolbar_btns['list_btn'].configure(command=lambda: self.new_w.label_box())
        self.toolbar_btns['hist_btn'].configure(command=lambda: self.new_w.history_box())
        ##################################################################################################
        data_seq = 'DATA_00000002'
        ##################################################################################################
        self.toolbar_btns['save_btn'].configure(command=lambda: self.label_controller.list_save_all(data_seq, self.task_board.temporary_save_listbox.get(0, END),self.task_board.temporary_save_listbox))

        # taskboard_btns
        from controller import LabelController
        self.label_controller = LabelController.LabelController(self)

        # self.task_board.taskboard_btns['fullview_btn'].configure(command=)
        self.task_board.taskboard_btns['trash_btn'].configure(command=lambda: self.label_controller.list_delete_all(self.task_board.temporary_save_listbox))

        from model import Load
        loader = Load.Load(self)

        # self.task_board.context_menu.entryconfig("보기", command=lambda: self.label_controller.list_view(self.task_board.temporary_save_listbox, self.task_board.preview_canvas))
        # self.task_board.context_menu.entryconfig("수정", command=lambda: self.label_controller.list_view(self.task_board.temporary_save_listbox, self.canvas))
        self.task_board.context_menu.entryconfig("보기", command=lambda: self.label_controller.list_view(
            self.task_board.temporary_save_listbox, loader))
        self.task_board.context_menu.entryconfig("수정", command=lambda: self.label_controller.list_view(
            self.task_board.temporary_save_listbox, loader))
        self.task_board.context_menu.entryconfig("삭제", command=lambda: self.label_controller.list_delete(self.task_board.temporary_save_listbox))
        self.task_board.temporary_save_listbox.bind("<Button-3>", self.show_context_menu)
