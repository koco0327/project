from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
# 로드 모듈
from operation.load import LoadData
#from operation.tools import BBox


class LoadUI:
    def __init__(self):
        # 창 크기 설정
        self.window = Tk()
        self.window.title("Load Data")
        self.window.geometry("640x400+100+100")

        # Canvas 생성
        self.canvas = Canvas(self.window, width=300, height=300)
        self.canvas.pack()
        self.loader = LoadData()

        # 버튼 누르면 - 로컬 파일 열기 기능
        button_load = Button(self.window, text="데이터 불러오기 방식 - 수동", command=lambda: self.loader.load_manual(self.canvas))
        button_load.pack()

    def run(self):
        self.window.mainloop()


load = LoadUI()
load.run()
