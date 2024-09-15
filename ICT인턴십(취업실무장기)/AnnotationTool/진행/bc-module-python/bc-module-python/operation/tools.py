from tkinter import *
import random
#load 파일 경로

from operation.load import Load

class BBox:
    def __init__(self, canvas):
        self.canvas = canvas
        # 사각형
        self.rect = None
        #사각형 꼭짓점 저장 / 캔버스가 왼쪽 위가 0,0 오른쪽, 아래쪽으로 가면 양수 / 캔버스 기준 왼쪽 위 부터 시계방향
        self.points = []
        #사각형 꼭짓점 순서
        self.active_point = None
        #사각형 꼭짓점 좌표
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        # 수정에 필요한 사각형 꼭짓점
        self.start = [] # 시작점 x, y 좌표
        self.end = []# 끝점 x, y 좌표
        # 꼭짓점으로 부터 마우스 오버 범위 5
        self.threshold = 5 #
        # 마우스 이벤트
        self.bind_events()
        # 꼭짓점 원
        self.circles = []


    def draw(self, x1, y1, x2, y2):
        # 이미 그려진 사각형 있으면 삭제
        if self.rect is not None:
            self.canvas.delete(self.rect)

        # 좌표의 최소값, 최대값 확인, 네 꼭짓점 항상 동일하게 고정
        self.min_x = min(x1, x2)
        self.min_y = min(y1, y2)
        self.max_x = max(x1, x2)
        self.max_y = max(y1, y2)

        # 기존 꼭짓점 삭제 및 사각형 꼭짓점 원 삭제
        for point in self.points:
            self.canvas.delete(point)

        # 꼭짓점 저장 - (수정시 꼭짓점 계속해서 바뀜)
        self.points = [(self.min_x, self.min_y), (self.max_x, self.min_y), (self.max_x, self.max_y), (self.min_x, self.max_y)]  # 꼭짓점 위치 업데이트

        # 사각형 그리기 - (point에 따라)
        self.rect = self.canvas.create_rectangle(self.min_x, self.min_y, self.max_x, self.max_y, outline='red', width=2,
                                                 dash=(100, 100), fill='#%02x%02x%02x' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), stipple='gray50')
        # 꼭짓점 워 원
        self.circle(3, "red")

        #print("꼭짓점 좌표:", self.points)


        # 사각형 꼭짓점 원
    def circle(self, circle_size, circle_color):
        if self.circles is not None:
            for circle in self.circles:
                self.canvas.delete(circle)

        self.circles.append(
            self.canvas.create_oval(self.min_x - circle_size, self.min_y - circle_size, self.min_x + circle_size, self.min_y + circle_size, fill=circle_color))
        self.circles.append(
            self.canvas.create_oval(self.max_x - circle_size, self.min_y - circle_size, self.max_x + circle_size, self.min_y + circle_size, fill=circle_color))
        self.circles.append(
            self.canvas.create_oval(self.max_x - circle_size, self.max_y - circle_size, self.max_x + circle_size, self.max_y + circle_size, fill=circle_color))
        self.circles.append(
            self.canvas.create_oval(self.min_x - circle_size, self.max_y - circle_size, self.min_x + circle_size, self.max_y + circle_size, fill=circle_color))


    # 버튼을 누러면 사각형 시작점 좌표
    def start_bbox(self, event):
        self.active_point = None  # 수정하려는 꼭짓점의 index 초기화
        self.start = [self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)]
        # active_point 찾기
        if self.points is not None:
            self.find_point(self.points, *self.start)

    # 꼭짓점 위치 찾기
    def find_point(self, points, start_x, start_y):
        # 선택된 꼭짓점에서 가장 가까운 꼭짓점 찾기
        for i, point in enumerate(points):
            distance = ((point[0] - start_x) ** 2 + (point[1] - start_y) ** 2) ** 0.5
            if distance < self.threshold:
                self.active_point = i

    # 버튼 누르면 사각형 끝점 및 수정, 이에따라 사각형 그림
    def drag_bbox(self, event):
        self.end = [self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)]
        end_x, end_y = self.end
        if self.active_point is not None:
            # 기존 사각형 수정하는 경우
            self.points[self.active_point] = (end_x, end_y)

            # # (self.active_point + 1) % 4 -> 나머지로 엑티브 포인트 0,1,2,3 -> 3,2,1,0 순서
            # # 엑티브 포인트의 양 꼭짓점
            # b = (self.active_point + 1) % 4
            # bb = (b + 2) % 4
            # self.points[b] = (x, self.points[b][])


            # 나머지 꼭짓점 위치 계산
            if self.active_point == 0:
                self.points[3] = (self.points[3][0], end_y)
                self.points[1] = (end_x, self.points[1][1])
            elif self.active_point == 1:
                self.points[2] = (end_x, self.points[2][1])
                self.points[0] = (self.points[0][0], end_y)
            elif self.active_point == 2:
                self.points[1] = (self.points[1][0], end_y)
                self.points[3] = (end_x, self.points[3][1])
            elif self.active_point == 3:
                self.points[0] = (end_x, self.points[0][1])
                self.points[2] = (self.points[2][0], end_y)

            self.draw(*self.points[0], *self.points[2])
        else:
            # 새로운 사각형을 그리는 경우
            self.draw(*self.start, *self.end)



    # 꼭짓점에 마우스 오버 - 꼭짓점 활성화
    def on_mouse_point(self, event):
        circle_size = 6
        circle_color = "yellow"
        if self.rect is None:
            return
        # 현재 마우스 위치
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        # active_point(꼭짓점 위치) 찾기
        for i, point in enumerate(self.points):
            distance = ((point[0] - x) ** 2 + (point[1] - y) ** 2) ** 0.5
            if distance < self.threshold:
                self.active_point = i

            # 해당 꼭짓점 모션 변경
                if self.active_point == 0:
                    self.circles.append(self.canvas.create_oval(self.min_x - circle_size, self.min_y - circle_size,
                                             self.min_x + circle_size, self.min_y + circle_size, fill=circle_color))
                if self.active_point == 1:
                    self.circles.append(self.canvas.create_oval(self.max_x - circle_size, self.min_y - circle_size,
                                            self.max_x + circle_size, self.min_y + circle_size, fill=circle_color))
                if self.active_point == 2:
                    self.circles.append(self.canvas.create_oval(self.max_x - circle_size, self.max_y - circle_size,
                                            self.max_x + circle_size, self.max_y + circle_size, fill=circle_color))
                if self.active_point == 3:
                    self.circles.append(self.canvas.create_oval(self.min_x - circle_size, self.max_y - circle_size,
                                            self.min_x + circle_size, self.max_y + circle_size, fill=circle_color))
                return

            self.circle(3, "red")
            self.active_point = None  # 활성화된 포인트가 없으면 None으로 설정


    def bind_events(self):
        # 좌클릭 시 bbox 시작
        self.canvas.bind("<ButtonPress-1>", self.start_bbox)
        # 좌클릭 - 모션(드래그) 중 bbox 그려짐
        self.canvas.bind("<B1-Motion>", self.drag_bbox)
        # 꼭짓점 마우스 오버시 활성화 (커지게)
        self.canvas.bind("<Motion>", self.on_mouse_point)


# # 실행
# load = Load()
# BBox(load.canvas)
# load.canvas.mainloop()
