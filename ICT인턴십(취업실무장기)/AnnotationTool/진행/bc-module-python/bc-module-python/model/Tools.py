from tkinter import *
import random
class BBox:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.focus_set() # 캔버스에 포커스 설정 - 이거 안하면 키보드 이벤트 인식 못함
        self.rect = None        # 사각형
        self.bbox_points = []   #사각형 꼭짓점 저장 / 캔버스가 왼쪽 위가 0,0 오른쪽, 아래쪽으로 가면 양수 / 캔버스 기준 왼쪽 위 부터 시계방향
        self.active_point = None        #사각형 꼭짓점 순서
        #사각형 꼭짓점 좌표
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        # 수정에 필요한 사각형 꼭짓점
        self.start = [] # 시작점 x, y 좌표
        self.end = []# 끝점 x, y 좌표
        self.threshold = 5       # 꼭짓점으로 부터 마우스 오버 범위 5
        self.circles = []        # 꼭짓점 원
        self.color = None        # 사각형 내부 색(랜덤)
        self.points_history = []        # 이전 사각형 꼭짓점 좌표들을 저장하는 리스트
        # 원 원본 색 및 크기
        self.origin_circle_size = 3
        self.origin_circle_color = "red"
        # 원 바뀌는 색 및 크기
        self.change_circle_size = 6
        self.change_circle_color = "yellow"
        self.change_circles = []        # 바뀌는 원 저장 리스트

    # 사각형 음영 색 랜덤
    def fill_color(self):
        if self.color is None:
            r, g, b, a = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200), 30)
            self.color = '#%02x%02x%02x' % (r, g, b)
        self.canvas.itemconfigure(self.rect, fill=self.color, stipple='gray50')

    # 사각형 꼭짓점 원
    def circle(self, circle_size, circle_color):
        # 사각형 완료 전에 그려지는 원 삭제
        if self.circles is not None:
            for circle in self.circles:
                self.canvas.delete(circle)
            self.circles.clear() #리스트 안 삭제

        self.circles.append(
            self.canvas.create_oval(self.min_x - circle_size, self.min_y - circle_size, self.min_x + circle_size, self.min_y + circle_size, fill=circle_color))
        self.circles.append(
            self.canvas.create_oval(self.max_x - circle_size, self.min_y - circle_size, self.max_x + circle_size, self.min_y + circle_size, fill=circle_color))
        self.circles.append(
            self.canvas.create_oval(self.max_x - circle_size, self.max_y - circle_size, self.max_x + circle_size, self.max_y + circle_size, fill=circle_color))
        self.circles.append(
            self.canvas.create_oval(self.min_x - circle_size, self.max_y - circle_size, self.min_x + circle_size, self.max_y + circle_size, fill=circle_color))

    def draw_bbox(self, x1, y1, x2, y2):
        # 이미 그려진 사각형 있으면 삭제
        if self.rect is not None:
            self.canvas.delete(self.rect)

        # 좌표의 최소값, 최대값 확인, 네 꼭짓점 항상 동일하게 고정 + 캔버스 범위 벗어나지 않게 함
        self.min_x = min(max(0, x1), self.canvas.winfo_width())
        self.min_y = min(max(0, y1), self.canvas.winfo_height())
        self.max_x = max(min(x2, self.canvas.winfo_width()), 0)
        self.max_y = max(min(y2, self.canvas.winfo_height()), 0)

        #기존 꼭짓점 삭제
        for point in self.bbox_points:
            self.canvas.delete(point)
        self.bbox_points.clear() # 리스트 안 삭제

        # 꼭짓점 저장 - (수정시 꼭짓점 계속해서 바뀜)
        self.bbox_points = [(self.min_x, self.min_y), (self.max_x, self.min_y), (self.max_x, self.max_y), (self.min_x, self.max_y)]  # 꼭짓점 위치 업데이트

        # 사각형 그리기 - (point에 따라)
        self.rect = self.canvas.create_rectangle(self.min_x, self.min_y, self.max_x, self.max_y, outline='red', width=2,
                                                 dash=(100, 100))
        # 꼭짓점 원
        self.circle(self.origin_circle_size, self.origin_circle_color)
        # 사각형 음영 색
        self.fill_color()

    # 꼭짓점 위치 찾기
    def find_point(self, bbox_points, x, y):
        # 선택된 꼭짓점에서 가장 가까운 꼭짓점 찾기
        if self.active_point is not None:
            current_point = bbox_points[self.active_point]
            distance = ((current_point[0] - x) ** 2 + (current_point[1] - y) ** 2) ** 0.5
            if distance >= self.threshold:
                self.active_point = None
        else:
            for i, point in enumerate(bbox_points):
                distance = ((point[0] - x) ** 2 + (point[1] - y) ** 2) ** 0.5
                if distance < self.threshold:
                    self.active_point = i
                    break

    # 버튼을 누러면 사각형 시작점 좌표
    def start_bbox(self, event):
        self.active_point = None  # 수정하려는 꼭짓점의 index 초기화
        self.start = [self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)]
        # active_point 찾기
        if self.bbox_points is not None:
            self.find_point(self.bbox_points, *self.start)

        # change_circles 원 흔적 안남도록
        for circle in self.change_circles:
            self.canvas.delete(circle)
        self.change_circles.clear()  # 리스트 비우기

    # 버튼 누르면 사각형 끝점 및 수정, 이에 따라 사각형 그림
    def drag_bbox(self, event):
        self.end = [self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)]
        end_x, end_y = self.end

        # 사각형이 캔버스 범위를 벗어나지 않도록 조정
        end_x = min(max(end_x, 0), self.canvas.winfo_width())
        end_y = min(max(end_y, 0), self.canvas.winfo_height())

        if self.active_point is not None:
            # 기존 사각형 수정하는 경우
            self.bbox_points[self.active_point] = (end_x, end_y)

            #나머지 꼭짓점 위치 계산
            if self.active_point == 0:
                self.bbox_points[3] = (self.bbox_points[3][0], end_y)
                self.bbox_points[1] = (end_x, self.bbox_points[1][1])
            elif self.active_point == 1:
                self.bbox_points[2] = (end_x, self.bbox_points[2][1])
                self.bbox_points[0] = (self.bbox_points[0][0], end_y)
            elif self.active_point == 2:
                self.bbox_points[1] = (self.bbox_points[1][0], end_y)
                self.bbox_points[3] = (end_x, self.bbox_points[3][1])
            elif self.active_point == 3:
                self.bbox_points[0] = (end_x, self.bbox_points[0][1])
                self.bbox_points[2] = (self.bbox_points[2][0], end_y)

            self.draw_bbox(*self.bbox_points[0], *self.bbox_points[2])
        else:
            # 새로운 사각형을 그리는 경우
            self.draw_bbox(*self.start, *self.end)

    #꼭짓점에 마우스 오버 - 꼭짓점 활성화
    def on_mouse_point(self, event):
        # 사각형 없으면 그만
        if self.rect is None:
            return

        # 현재 마우스 위치
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.bbox_points is not None:
            self.find_point(self.bbox_points, x, y)

        # 기존의 change_circles 삭제
        for circle in self.change_circles:
            self.canvas.delete(circle)
        self.change_circles.clear()  # 리스트 비우기

        # 해당 꼭짓점 모션 변경
        if self.active_point == 0:
            self.change_circles.append(
                self.canvas.create_oval(self.min_x - self.change_circle_size, self.min_y - self.change_circle_size,
                                        self.min_x + self.change_circle_size, self.min_y + self.change_circle_size,
                                        fill=self.change_circle_color))
        elif self.active_point == 1:
            self.change_circles.append(
                self.canvas.create_oval(self.max_x - self.change_circle_size, self.min_y - self.change_circle_size,
                                        self.max_x + self.change_circle_size, self.min_y + self.change_circle_size,
                                        fill=self.change_circle_color))
        elif self.active_point == 2:
            self.change_circles.append(
                self.canvas.create_oval(self.max_x - self.change_circle_size, self.max_y - self.change_circle_size,
                                        self.max_x + self.change_circle_size, self.max_y + self.change_circle_size,
                                        fill=self.change_circle_color))
        elif self.active_point == 3:
            self.change_circles.append(
                self.canvas.create_oval(self.min_x - self.change_circle_size, self.max_y - self.change_circle_size,
                                        self.min_x + self.change_circle_size, self.max_y + self.change_circle_size,
                                        fill=self.change_circle_color))

# hotkey 스크립트로 빼야할것 같음

    # ctrl + z 을 위해 전 좌표 저장
    def save_points(self, event = None):
        # 현재 사각형의 꼭짓점 좌표를 points_history에 저장
        self.points_history.append(self.bbox_points.copy())

    # ctrl + z 작동시 사각형 삭제 및 그리기
    def step_back(self, event):
        if len(self.points_history) > 1:
            # 이전 사각형 꼭짓점 좌표들을 가져와서 현재 꼭짓점 좌표로 설정
            self.bbox_points = self.points_history[-2].copy()

            # 이전 사각형 그리기
            self.draw_bbox(*self.bbox_points[0], *self.bbox_points[2])

            # 마지막 사각형 꼭짓점 좌표 삭제
            self.points_history.pop()
        # 맨처음 그린 사각형은 ctrl + z 하면 삭제
        else: # 리스트에 하나 남았을때
            # 사각형 삭제 및 bbox_points 삭제
            self.canvas.delete(self.rect)
            self.bbox_points.clear()
            # 꼭짓점 원 삭제
            for circle in self.circles:
                self.canvas.delete(circle)


    def bbox_bind_events(self):
        # 좌클릭 시 bbox 시작
        self.canvas.bind("<ButtonPress-1>", self.start_bbox)
        # 좌클릭 - 모션(드래그) 중 bbox 그려짐
        self.canvas.bind("<B1-Motion>", self.drag_bbox)
        # 꼭짓점 마우스 오버시 활성화 (커지게)
        self.canvas.bind("<Motion>", self.on_mouse_point)
        # Ctrl + Z를 누를 때 undo 함수 호출 -(canvas.focus_set() 안해주면 키보드는 인식 못함)
        self.canvas.bind("<Control-z>", self.step_back)
        # 좌표 저장
        self.canvas.bind("<ButtonRelease-1>", self.save_points)

    def bbox_unbind(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Control-z>")
        self.canvas.unbind("<ButtonRelease-1>")

    def bbox_reset(self):
        self.bbox_points = []
        self.start = []
        self.end = []
        self.circles = []
        self.change_circles = []
        self.rect = None
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        self.color = None



class Seg:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.focus_set()
        self.threshold = 5  # 시작점 반경 설정 (픽셀)
        self.color = None  # 다각형 색상
        self.points = []  # 원(꼭짓점)의 ID
        self.seg_points = []  # seg 좌표 (생기는 다각형의 꼭짓점 좌표)
        self.circle = None
        self.lines = []  # 선의 ID
        self.start_circle = None  # 시작점 원의 ID를 저장하는 변수입니다.
        self.polygon = None  # 그려진 다각형의 ID를 저장하는 변수입니다.
        self.origin_circle_size = 3  # 원의 초기 크기
        self.origin_circle_color = "red"  # 원의 초기 색상
        self.change_circle_size = 6  # 변경된 원의 크기
        self.change_circle_color = "yellow"  # 변경된 원의 색상
        # 수정할 원, 선 선택
        self.selected_circle = None

    # 원 생성
    def create_circle(self, x, y):
        # 원 생성
        circle = self.canvas.create_oval(
            x - self.origin_circle_size,
            y - self.origin_circle_size,
            x + self.origin_circle_size,
            y + self.origin_circle_size,
            fill=self.origin_circle_color
        )
        return circle

    # 원과 원 연결
    def connect_circles(self, circle1, circle2):
        # 원과 원을 선으로 연결
        coords1 = self.canvas.coords(circle1) # 객체의 좌표 가져오기
        coords2 = self.canvas.coords(circle2)

        x1 = (coords1[0] + coords1[2]) / 2
        y1 = (coords1[1] + coords1[3]) / 2
        x2 = (coords2[0] + coords2[2]) / 2
        y2 = (coords2[1] + coords2[3]) / 2

        line = self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2, dash=(100, 100))
        return line

    def on_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        # 원 생성
        circle = self.create_circle(x, y)
        self.points.append(circle)
        # 원이 2개 이상부터 연결
        if len(self.points) > 1:
            line = self.connect_circles(self.points[-2], self.points[-1])
            self.lines.append(line)
        # 1개는 연결안함
        if len(self.points) == 1 or self.start_circle is None:
            self.start_circle = circle

        # seg 완성되었을 경우
        if self.seg_completed():
            self.seg_unbind()
            # 마지막 원, 선 연결 수정
            self.connect_last_circle()
            # 내부 음영 색
            self.fill_color()
            # 내부 음영, 다각형 생성
            self.seg_polygon()
            # 노란색 원 삭제
            self.canvas.delete("over_circle")
            # -----------------------------------
            # 수정을 위한 바인드 수정
            self.canvas.bind("<B1-Motion>", self.on_circle_drag)
            #
            self.canvas.bind("<Motion>", self.mouse_point_after_seg)


            return

            #==================================
            # 여기에 라벨 선택할 수 있는 창이 뜨게 해야함.
            # 여기에 라벨 선택할 수 있는 창이 뜨게 해야함.
            # 여기에 라벨 선택할 수 있는 창이 뜨게 해야함.
            # 여기에 라벨 선택할 수 있는 창이 뜨게 해야함.


    def connect_last_circle(self):
        # 마지막으로 찍힌 원의 좌표를 첫 번째 원의 좌표로 업데이트합니다.
        self.canvas.coords(self.points[-1], *self.canvas.coords(self.start_circle))
        # 마지막으로 찍힌 원과 첫 번째 원을 연결하는 선 그리기
        line = self.connect_circles(self.points[-1], self.start_circle)
        # 마지막 선 추가
        self.lines.append(line)
        self.canvas.delete(self.points[-1])
        # 마지막으로 찍힌 원을 첫 번째 원으로 대체합니다.
        self.points[-1] = self.start_circle
        # 시작 원 초기화
        self.start_circle = None


    def find_circle_index(self, x, y):
        # 주어진 좌표에 가장 가까운 원의 인덱스를 찾는 함수
        for i, circle in enumerate(self.points):
            coords = self.canvas.coords(circle)
            if len(coords) >= 4:  # coords 리스트의 길이가 충분한지 확인
                # 원의 중앙
                cx = (coords[0] + coords[2]) / 2
                cy = (coords[1] + coords[3]) / 2
                if cx - self.threshold <= x <= cx + self.threshold and cy - self.threshold <= y <= cy + self.threshold:
                    return i
        return -1


    # seg 완성 전 마우스 - 원 오버시
    def mouse_point_befor_seg(self, event):
        # 마우스 오버 이벤트 처리 함수
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        # 원의 인덱스 찾기
        index = self.find_circle_index(x, y)
        if index is None:
            return
        # 모든 오버 원 삭제
        self.canvas.delete("over_circle")
        # 첫 번째 원에 대해서만 오버 원 생성
        if index == 0 and self.start_circle is not None:
            start_circle_coords = self.canvas.coords(self.start_circle)
            start_circle_x = (start_circle_coords[0] + start_circle_coords[2]) / 2
            start_circle_y = (start_circle_coords[1] + start_circle_coords[3]) / 2

            # 오버 원 생성
            self.canvas.create_oval(
                start_circle_x - self.change_circle_size,
                start_circle_y - self.change_circle_size,
                start_circle_x + self.change_circle_size,
                start_circle_y + self.change_circle_size,
                fill=self.change_circle_color,
                tags="over_circle")


    # seg 완성 후 마우스 - 원 오버시
    def mouse_point_after_seg(self, event):
        # 마우스 오버 이벤트 처리 함수
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        # 원의 인덱스 찾기
        index = self.find_circle_index(x, y)
        if index is None:
            return
        # 모든 오버 원 삭제
        self.canvas.delete("over_circle")
        # 세그먼트가 완성된 상태인 경우, 전체 원에 대해 오버 원 생성
        if index >= 0:
            circle = self.points[index]
            coords = self.canvas.coords(circle)
            if len(coords) >= 4:  # coords 리스트의 길이가 충분한지 확인
                cx = (coords[0] + coords[2]) / 2
                cy = (coords[1] + coords[3]) / 2
                self.canvas.create_oval(
                    cx - self.change_circle_size,
                    cy - self.change_circle_size,
                    cx + self.change_circle_size,
                    cy + self.change_circle_size,
                    fill=self.change_circle_color,
                    tags="over_circle")

        # 수정 - 드래그할 꼭지점(원) 설정합니다.
        if index >= 0:
            self.selected_circle = self.points[index]


    # 다각형 완성됬는지 확인
    def seg_completed(self):
        # points에 저장된 원의 개수가 3개 이상이며
        if self.start_circle is None or len(self.points) < 3:
            return False

        # 시작 원의 좌표를 가져옴
        start_coords = self.canvas.coords(self.start_circle)
        if len(start_coords) < 2:
            return False

        # 마지막 원
        last_circle_id = self.points[-1]
        last_circle_coords = self.canvas.coords(last_circle_id)
        if len(last_circle_coords) < 4:  # 좌표가 충분하지 않은 경우
            return False

        x1, y1 = start_coords[0:2]
        x2, y2 = last_circle_coords[0:2]
        if abs(x1 - x2) <= self.threshold and abs(y1 - y2) <= self.threshold:
            return True

        return False


    # seg 완성 후 수정
    def on_circle_drag(self, event):
        if self.selected_circle is not None:
            # 드래그된 원의 좌표를 가져옵니다.
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            # 드래그된 원을 새로운 좌표로 이동시킵니다.
            self.canvas.coords(self.selected_circle, x - self.origin_circle_size, y - self.origin_circle_size,
                               x + self.origin_circle_size, y + self.origin_circle_size)
            # 연결된 선의 좌표를 업데이트합니다.
            self.update_connect_lines()
            # 다각형 모양을 업데이트합니다.
            self.seg_polygon()
            # 오버 원 삭제
            self.canvas.delete("over_circle")


    def fill_color(self):
        if self.color is None:
            r, g, b = (random.randint(0, 240), random.randint(0, 240), random.randint(0, 240))
            self.color = '#%02x%02x%02x' % (r, g, b)


    # seg에 맞는 다각형
    def seg_polygon(self):
        if len(self.lines) > 1:
            self.seg_points = []  # 다각형의 좌표를 초기화합니다.
            for line in self.lines[:-1]:
                coords = self.canvas.coords(line)
                self.seg_points.append((coords[0], coords[1]))  # 선분의 시작 좌표를 추가합니다.

            if self.polygon:
                # 기존의 다각형이 존재하는 경우 다각형을 업데이트합니다.
                self.canvas.delete(self.polygon)

            if len(self.seg_points) > 2:
                # 선분 좌표를 사용하여 다각형을 생성합니다.
                self.polygon = self.canvas.create_polygon(self.seg_points, fill=self.color, outline='',
                                                          stipple='gray50')




    def update_connect_lines(self):
        for i in range(len(self.points) - 1):
            circle1 = self.points[i]
            circle2 = self.points[i + 1]

            # 연결된 선의 좌표를 업데이트합니다.
            coords1 = self.canvas.coords(circle1)
            coords2 = self.canvas.coords(circle2)
            # 원의 중앙
            x1 = (coords1[0] + coords1[2]) / 2
            y1 = (coords1[1] + coords1[3]) / 2
            x2 = (coords2[0] + coords2[2]) / 2
            y2 = (coords2[1] + coords2[3]) / 2
            line = self.lines[i]
            self.canvas.coords(line, x1, y1, x2, y2)


    #ctrl + z -> bbox와 다르게 이전 좌표를 저장할 필요가 없음, 그냥 하나씩 삭제하면 됨.
    def step_back(self, event):
        if self.points:
            circle = self.points.pop()
            if self.lines:
                line = self.lines.pop()
                self.canvas.delete(line)
                if self.seg_points:
                    self.seg_points.pop()
            self.canvas.delete(circle)

    def seg_bind_events(self):
        # 마우스 클릭 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        # 마우스 오버 이벤트 바인딩
        self.canvas.bind("<Motion>", self.mouse_point_befor_seg)
        # ctrl + z
        self.canvas.bind("<Control-z>", self.step_back)

    def seg_unbind(self):
        # 도형이 완성되었을 경우 마우스 클릭 이벤트 작동안하게 바인드 해제
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Control-z>")


    # 이초기화가 안됀다아아아아ㅏ
    def seg_reset(self):
        # 모든 변수와 그리기 요소 초기화
        self.points = []
        self.seg_points = []
        self.lines = []
        self.start_circle = None
        self.polygon = None
        self.color = None
        self.selected_circle = None


# 큐보이드 진행중


from math import sqrt
import tkinter as tk

class Cube:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.pack()
        self.start_point = None
        self.end_point = None
        # 꼭짓점 리스트
        self.points = []
        # 사각형 색
        self.color = None

    def fill_color(self):
        if self.color is None:
            r, g, b, a = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200), 30)
            self.color = '#%02x%02x%02x' % (r, g, b)


    def draw_cuboid(self):
        if self.start_point and self.end_point:
            width = abs(self.start_point[0] - self.end_point[0])
            height = abs(self.start_point[1] - self.end_point[1])
            depth = sqrt(width ** 2 + height ** 2)
            diagonal = int(round(sqrt(width ** 2 + height ** 2 + depth ** 2)))
            x_center = (self.start_point[0] + self.end_point[0]) // 2
            y_center = (self.start_point[1] + self.end_point[1]) // 2

            x1 = x_center - width // 2
            y1 = y_center - height // 2
            x2 = x_center + width // 2
            y2 = y_center + height // 2

            self.draw_3d_cuboid(x1, y1, x2, y2, diagonal)

    def draw_3d_cuboid(self, x1, y1, x2, y2, diagonal):
        # 색 설정
        self.fill_color()
        # 전면 그리기
        self.canvas.create_rectangle(x1, y1, x2, y2, tags="cuboid", fill = self.color, stipple="gray50")

        # 뒷면 그리기
        back_x1 = x1 + diagonal // 10
        back_y1 = y1 + diagonal // 10
        back_x2 = x2 + diagonal // 10
        back_y2 = y2 + diagonal // 10
        self.canvas.create_rectangle(back_x1, back_y1, back_x2, back_y2, tags="cuboid", fill=self.color,
                                     stipple="gray25")

        # 선 연결
        self.canvas.create_line(x1, y1, back_x1, back_y1, fill="black", tags="cuboid")
        self.canvas.create_line(x2, y1, back_x2, back_y1, fill="black", tags="cuboid")
        self.canvas.create_line(x2, y2, back_x2, back_y2, fill="black", tags="cuboid")
        self.canvas.create_line(x1, y2, back_x1, back_y2, fill="black", tags="cuboid")

        # 꼭짓점에 원 그리기
        radius = 5
        for point in self.points:
            x, y = point
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red')

    def on_mouse_click(self, event):
        self.start_point = self.start_point = (event.x, event.y)

    def on_mouse_drag(self, event):
        self.end_point = (event.x, event.y)
        self.canvas.delete("cuboid")  # 이전 큐보이드 삭제
        self.draw_cuboid()

    def on_mouse_release(self, event):
        self.end_point = (event.x, event.y)
        self.canvas.delete("cuboid")  # 이전 큐보이드 삭제
        self.draw_cuboid()

    def on_point_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')

    def cuboid_bind_events(self):
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.canvas.bind("<Button-3>", self.on_point_click)  # 오른쪽 마우스 버튼으로 꼭짓점 추가

    def cuboid_unbind(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Button-3>")
