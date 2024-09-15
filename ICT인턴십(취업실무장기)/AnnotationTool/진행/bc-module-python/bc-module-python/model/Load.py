from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from Tools import BBox, Seg

class Load:
    def __init__(self):
        self.my_image = None  # 함수에서 이미지를 기억하도록 전역변수 선언
        self.image_size = (0,0)  # 이미지 크기를 저장할 변수 선언
        self.image = None
        self.x_ratio = None
        self.y_ratio = None
        # 이미지 크기 조절 (창 크기에 따라 설정 - 아직 미정)
        self.new_width = 400
        self.new_height = 400

    def show_image(self, filename, canvas):
        # 이미지 불러오기
        self.image = Image.open(filename)

        resized_image = self.image.resize((self.new_width, self.new_height), resample=Image.Resampling.LANCZOS)

        # Image 객체를 PhotoImage 객체로 변환
        self.my_image = ImageTk.PhotoImage(resized_image)
        # Seg 객체 초기화
        #self.seg = Seg(canvas)
        # 캔버스에 image가 있으면 이미지 삭제 (Load 버튼 다시 눌렀을때 기존 이미지 지우기 위함)
        if canvas.find_withtag("image"):
            canvas.delete("all")
            ## Seg 객체의 seg_reset() 메서드 호출
            #if self.seg is not None:
            #    self.seg.seg_reset()


        # 새로운 이미지 캔버스 중앙에 불러오기
        canvas.create_image(self.new_width // 2, self.new_height // 2, image=self.my_image, tags="image")

    def load_manual(self, canvas):
        # askopenfilename -  Open 대화 상자를 만들고 기존 파일(들)에 해당하는 선택된 파일명(들)을 반환합니다.
        filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=(
            ('png files', '*.png'), ('jpg files', '*.jpg'), ('jpeg files', '*.jpeg')))

        # 이미지 로딩
        self.show_image(filename, canvas)
        # 이미지 크기 저장 (좌표 저장시 역산에 필요)
        self.return_image_size(self.image)
        # 불러온 이미지 비율
        self.image_ratio()

    def return_image_size(self, image):
        if image is None:
            return
        self.image_size = image.size

    # 캔버스 오류 - 비율 load에서 정의하고 가기
    def image_ratio(self):
        # 이미지 사이즈의 비율 계산
        self.x_ratio = self.image_size[0] / self.new_width
        self.y_ratio = self.image_size[1] / self.new_height