from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from view import NewWindowView
from model.SFTPManager import SFTPClient


class Load:
    # 좌표 이미지 비율에 따라 - 클래스 변수로 정의
    image_size = (0, 0)  # 이미지 크기를 저장할 변수 선언
    x_ratio = 1
    y_ratio = 1

    def __init__(self, btn_controller):
        self.btn_controller = btn_controller
        self.canvas = btn_controller.canvas

        self.load_btn = btn_controller.toolbar_btns['load_btn']
        self.data_id_label = btn_controller.worker_frame.data_id_label

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

        self.n_widgets = NewWindowView.NewWindowWidgets(btn_controller.color)

        self.filetypes = (('png files', '*.png'), ('jpg files', '*.jpg'), ('jpeg files', '*.jpeg'))


    def show_image(self, path, data_id):
        # DATA_SEQ 화면에 표시
        self.data_id_label.configure(text=data_id)

        image = Image.open(path)

        # 이미지 크기 저장 (좌표 저장시 역산에 필요) - 캔버스 크기로 변환하기 전에 실행
        self.return_image_size(image)

        image = image.resize((self.canvas_width, self.canvas_height), resample=Image.BICUBIC)
        self.tk_image = ImageTk.PhotoImage(image)
        # 캔버스에 image가 있으면 이미지 삭제
        if self.canvas.find_withtag("image"):
            self.canvas.delete("all")
        # 새로운 이미지 캔버스 중앙에 불러오기
        my_image = self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.tk_image,
                                            tags="image")

        # with_load_btns 활성화
        self.btn_controller.set_btns_state(self.btn_controller.with_load_btns, NORMAL)

        # hotkey_bind
        self.btn_controller.activate_hotkeys(image, my_image)
    # 자동으로 불러오기 데이터 리스트
    def load_auto_list(self):

        self.sftp_client = SFTPClient()
        self.file_list = None
        # 원래는 path 를 project 등에서 가져옴
        self.file_list = self.sftp_client.get_files_in_remote_path('/home/bc/hdd/Annotation/dump')
        self.jpg_files = [file for file in self.file_list if file.lower().endswith('.jpg')]
        self.jpg_files.sort()  # 오름차순 정렬

        return self.jpg_files

    # 자동으로 불러오기 - server
    def load_auto(self, auto_load_window, load_listbox):
        if load_listbox.curselection():
            selected_index = load_listbox.index(load_listbox.curselection())
            self.selected_file = self.jpg_files[selected_index]
            local_path = f'./{self.selected_file}'
            remote_path = f'/home/bc/hdd/Annotation/dump/{self.selected_file}'
            self.sftp_client.download_file(remote_path, local_path)

            data_id = load_listbox.get(selected_index).rstrip(".jpg")
            self.show_image(local_path, data_id)

            # 불러오기 완료되면, 버튼 색 변경 및 창닫기
            self.n_widgets.close_new_window(auto_load_window, self.load_btn)

            self.data_seq = 'DATA_00000002'  # project_seq에서 가져오는 거 아닌가?
            self.btn_controller.disabled_btn(self.data_seq)

    # 수동으로 불러오기 - local
    def load_manual(self, load_window):
        load_window.destroy()
        self.filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=self.filetypes)

        if self.filename:
            data_id = self.filename.split('/')[-1]
            self.show_image(self.filename, data_id)

            # 불러오기 완료되면, 버튼 색 변경 및 창닫기
            self.n_widgets.close_new_window(load_window, self.load_btn)

        else:
            self.n_widgets.close_new_window(load_window, self.load_btn)

# 이미지 비율에 따라 좌표저장 할수있게
    def return_image_size(self, image):
        if image is None:
            return
        Load.image_size = image.size
        Load.x_ratio = Load.image_size[0] / self.canvas_width
        Load.y_ratio = Load.image_size[1] / self.canvas_height
        print('x_ratio', Load.x_ratio)
        print('y_ratio', Load.y_ratio)

