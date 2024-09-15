from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
# 로드 모듈
from Load import Load
from Tools import BBox
from Tools import Seg
from Tools import Cube
from Label import Label

class UI:
    def __init__(self):
        # 창 크기 설정
        self.window = Tk()
        self.window.title("annotation_tool")
        self.window.geometry("800x800+100+100")
        # Canvas 생성
        self.canvas = Canvas(self.window, width=400, height=400)
        self.canvas.pack()
        # 이미지 로드
        self.loader = Load()
        # 버튼 누르면 - 로컬 파일 열기 기능
        button_load = Button(self.window, text="데이터 불러오기 방식 - 수동", command=lambda: self.loader.load_manual(self.canvas))
        button_load.pack()
#-----------------------------------------------------------------------------------------
        # 좌표값 / (loader.image_size->loader에 있음) / (이미지 로드하고 버튼눌렀을때 이미지 크기에 따라 print는 잘 됨)
        self.save = Label(self.canvas)


        # 버튼 누르면 - 좌표 저장
        self.save_button = Button(self.window, text="저장",
                                  command=lambda: self.save.label_save(self.loader.x_ratio, self.loader.y_ratio,
                                                                       self.bbox.bbox_points, self.seg.seg_points))
        self.save_button.pack()

#-----------------------------------------------------------------------------------------
        # bbox
        self.bbox = BBox(self.canvas)

        # 버튼 누르면 - BBox 기능
        self.bbox_active = False
        self.bbox_button = Button(self.window, text="BBox 그리기", command= lambda : self.toggle_bbox())
        self.bbox_button.pack()
#------------------------------------------------------------------------------------------------------
       # seg
        self.seg = Seg(self.canvas)

        # 버튼 누르면 - BBox 기능
        self.seg_active = False
        self.seg_button = Button(self.window, text="Seg 그리기", command= lambda : self.toggle_seg())
        self.seg_button.pack()
#------------------------------------------------------------------------------------------------------

    # cube
        self.cube = Cube(self.canvas)

        # 버튼 누르면 - BBox 기능
        self.cube_active = False
        self.cube_button = Button(self.window, text="Cube 그리기", command=lambda: self.toggle_cube())
        self.cube_button.pack()

# ------------------------------------------------------------------------------------------------------

    # bbox 버튼 한번누르면 실행, 다시한번 누르면 멈춤 반복을 위한 함수 -> Tools로 뺄수 있나?..
    def toggle_bbox(self):
        self.bbox_active = not self.bbox_active
        if self.bbox_active:
            self.bbox.bbox_bind_events()
        else:
            self.bbox.bbox_unbind()
            self.bbox.bbox_reset()

        # seq 버튼 한번누르면 실행, 다시한번 누르면 멈춤 반복을 위한 함수 -> Tools로 뺄수 있나?..
    def toggle_seg(self):
        self.seg_active = not self.seg_active
        if self.seg_active:
            self.seg.seg_bind_events()
            #self.canvas.configure(cursor='crosshair')
        else:
            self.seg.seg_unbind()
            self.seg.seg_reset()
            #self.canvas.configure(cursor='')

    def toggle_cube(self):
        self.cube_active = not self.cube_active
        if self.cube_active:
            self.cube.cuboid_bind_events()
        else:
            self.cube.cuboid_unbind()


    def run(self):
        self.window.mainloop()

load = UI()
load.run()