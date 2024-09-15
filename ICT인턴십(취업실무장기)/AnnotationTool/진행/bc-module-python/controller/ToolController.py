from tkinter import *
import random
from model.ToolModel import BBoxModel, SegModel, CubeModel
from view.ToolView import BBoxView, SegView, CubeView
from model.Hotkey import BBoxHotkeys, SegHotkeys, CubeHotkeys

from model.Load import Load



class BBoxController:
    def __init__(self, canvas, btn_controller):
        self.canvas = canvas
        self.canvas.focus_set()  # 캔버스에 포커스 설정 - 이거 안하면 키보드 이벤트 인식 못함

        # 캔버스 위 마우스 좌표
        self.x = None
        self.y = None

        # 수정에 필요한 사각형 꼭짓점
        self.points_history = []  # 이전 사각형 꼭짓점 좌표들을 저장하는 리스트

        # BBoxView
        self.bbox_view = BBoxView(self, self.canvas)

        # 캔버스 사이즈
        self.bbox_view.update_canvas_size()

        # BBoxModel
        self.bbox_model = BBoxModel(self, self.canvas)
        # BBoxHotkeys - 컨지
        # self.hotkeys = BBoxHotkeys(self.canvas)
        self.hotkeys = BBoxHotkeys(self, self.canvas)

        #load 이미지,x, y 좌표 변환
        self.load = Load(btn_controller)  # Load 객체 생성

    # 꼭짓점에 마우스 오버 - 꼭짓점 활성화
    def on_mouse_point(self, event, rect):
        # 사각형 없으면 그만
        if rect is None:
            return

        if self.bbox_model.bbox_points is not None:
            self.bbox_model.find_point(self.bbox_model.bbox_points, self.x, self.y)

        # 기존의 over_circle 삭제
        self.bbox_view.delete_over_circle("over_circle")
        # 해당 꼭짓점 오버 원 생성
        if self.bbox_model.active_point is not None:
            self.bbox_view.create_over_circle(self.bbox_model.active_point, self.bbox_model.bbox_points)

    # bbox 생성
    def creat_bbox(self, event):
        self.bbox_model.end = [self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)]
        end_x, end_y = self.bbox_model.end

        # bbox_point 맨 처음 그릴때
        if self.bbox_model.active_point is None:
            self.bbox_model.first_bbox_points(*self.bbox_model.start, end_x, end_y, self.bbox_view.canvas_width,
                                          self.bbox_view.canvas_height)

        # active_point 있을시 - 드래그 수정 - else 바꾸기
        if self.bbox_model.active_point is not None:
            self.bbox_model.bbox_points = self.bbox_model.bbox_points_update(end_x, end_y, self.bbox_view.canvas_width,
                                                                     self.bbox_view.canvas_height)

        if len(self.bbox_model.bbox_points) >= 4: # 0 or not
            self.bbox_view.draw_bbox(self.bbox_model.bbox_points)

        self.resizing()

    def resizing(self):
        # 이미지에 따른 좌표 저장
        if self.bbox_model.bbox_points:
            self.bbox_model.image_bbox_points = [(int(point[0] * self.load.x_ratio), int(point[1] * self.load.y_ratio)) for point in
                                                 self.bbox_model.bbox_points]
        print(self.bbox_model.image_bbox_points)

    def start_process(self):
        #model bbox 시작점
        self.bbox_model.start_bbox_point(self.x, self.y)

        # view 바뀐원 삭제 - 그려지는 도중 오버원이 남아있어서
        self.bbox_view.delete_over_circle("over_circle")


    # 활성화 마우스 이벤트
    def motion_mouse(self, event):
        # 캔버스 위 마우스 위치
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)

        # 꼭짓점 찾기
        self.on_mouse_point(event, self.bbox_view.rect)

    def buttonpress_mouse(self, event = None):
        self.start_process()

    def press_motion(self, event):
        self.creat_bbox(event)


    # 바인드
    def bbox_bind_events(self):
        # 캔버스 위 마우스 좌표
        self.canvas.bind("<Motion>", self.motion_mouse)
        # 좌클릭 시 bbox 시작
        self.canvas.bind("<ButtonPress-1>", self.buttonpress_mouse)
        # 좌클릭 - 모션(드래그) 중 bbox 그려짐
        self.canvas.bind("<B1-Motion>", self.press_motion)

        # Ctrl + Z를 누를 때 undo 함수 호출 -(canvas.focus_set() 안해주면 키보드는 인식 못함)
        self.hotkeys.bind_hotkeys()

    # 바인드 해제 - control
    def bbox_unbind(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Motion>")
        self.hotkeys.unbind_hotkeys()


    def bbox_reset(self):
        # 그려졌던 bbox 삭제
        self.bbox_view.delete_bbox()
        #model
        self.bbox_model.start = []
        self.bbox_model.end = []
        self.bbox_model.rect = None
        self.bbox_model.min_x = None
        self.bbox_model.min_y = None
        self.bbox_model.max_x = None
        self.bbox_model.max_y = None
        #view
        self.bbox_view.rect = None  # 사각형
        self.bbox_view.circles = []  # 꼭짓점 원
        self.bbox_view.color = None  # 사각형 내부 색(랜덤)
        self.bbox_view.over_circle = []  # 바뀌는 원 저장 리스트
        self.bbox_view.delete_over_circle("over_circle")

class SegController:
    def __init__(self, canvas, btn_controller):
        self.canvas = canvas
        self.canvas.focus_set()  # 캔버스에 포커스 설정 - 이거 안하면 키보드 이벤트 인식 못함

        # 캔버스 위 마우스 좌표
        self.x = None
        self.y = None

        # SegView
        self.seg_view = SegView(self, self.canvas)
        # SegModel
        self.seg_model = SegModel(self, self.canvas)
        # SegHotkeys - 컨지
        self.hotkeys = SegHotkeys(self, self.canvas)
        # self.hotkeys = SegHotkeys(self.canvas)

        self.ctrl_key_pressed = False

        #load 이미지,x, y 좌표 변환
        self.load = Load(btn_controller)  # Load 객체 생성


# 클릭시 - contorl
    def on_click(self, event):
        # 원 생성
        circle = self.seg_view.create_circle(self.x, self.y)
        self.seg_model.circle_id(circle)

        # 원이 2개 이상부터 연결
        if len(self.seg_model.points) > 1:
            line = self.seg_view.connect_circles(self.seg_model.points[-2], self.seg_model.points[-1])

            self.seg_model.line_id(line)

        # 1개는 연결안함 - elif 사용
        if len(self.seg_model.points) == 1 or self.seg_model.start_circle is None:
            self.seg_model.start_circle = circle

        # seg 완성되었을 경우
        if self.seg_model.seg_completed():
            self.seg_unbind()
            # 마지막 원, 선 연결 수정
            self.finish_seg()
            # 내부 음영 색
            self.seg_view.fill_color()
            # 내부 음영, 다각형 생성
            self.seg_color()
            # 노란색 원 삭제
            self.seg_view.delete_over_circle("over_circle")
            #=================================
            # 수정을 위한 바인드 수정
            self.canvas.bind("<B1-Motion>", self.on_circle_drag)
            # SEG후 마우스 이벤트
            self.canvas.bind("<Motion>", self.after_seg_motion)

            self.canvas.tag_bind("line", "<Motion>", self.line_over)

    def before_seg_motion(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)

        # 활성화 원 찾기
        self.seg_model.active_point = self.seg_model.find_circle_point(self.x, self.y)

        self.seg_view.delete_over_circle("over_circle")
        # 첫 번째 원에 대해서만 오버 원 생성
        if self.seg_model.active_point == 0 and self.seg_model.start_circle is not None:
            self.seg_view.over_circle(self.seg_model.start_circle)

    def after_seg_motion(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)

        # 활성화 원 찾기
        self.seg_model.active_point = self.seg_model.find_circle_point(self.x, self.y)
        # 활성화원 몇번째 point 찾기
        self.seg_model.mouse_point_after_seg(event)
        # 오버원 삭제
        self.seg_view.delete_over_circle("over_circle")
        # 활성화 원 오버 원 생성
        if self.seg_model.selected_circle is not None:
            self.seg_view.over_circle(self.seg_model.selected_circle)

    def on_circle_drag(self, event):
        # 드래그된 원의 좌표를 가져옵니다.
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        self.seg_model.circle_drag(x, y)
        # 연결된 선의 좌표를 업데이트합니다.
        self.seg_model.update_lines()
        # 오버원 삭제
        self.seg_view.delete_over_circle("over_circle")
        self.seg_view.delete_over_circle("new_circle")
        # seg 다시 완성 시 다각형 모양 다시 생성
        self.seg_color()

        self.resizing()

    def resizing(self):
        # 이미지에 따른 좌표 저장 - seg가 완성되고 seg_point함수로 set_point에 좌표가 생성되고나서
        if self.seg_model.seg_points:
            self.seg_model.image_seg_points = [(int(point[0] * self.load.x_ratio), int(point[1] * self.load.y_ratio)) for point in
                                                 self.seg_model.seg_points]
        print(self.seg_model.image_seg_points)

    def seg_color(self):
        self.seg_model.seg_point()
        self.seg_view.seg_polygon(self.seg_model.seg_points)

    def finish_seg(self):
        self.seg_model.update_last_circle()
        self.seg_view.last_line(self.seg_model.last_line, self.seg_model.points, self.seg_model.start_circle)
        self.seg_model.delete_last_circle(self.seg_view.line)

    def line_over(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        closest_point = self.seg_model.find_closest_point(x, y)
        self.seg_view.delete_over_circle("new_circle")
        self.new_circle_id = self.seg_view.update_circle(closest_point)
        self.tagged_line_id = event.widget.find_withtag(CURRENT)
        self.tagged_line_id = self.tagged_line_id[0]
        self.endpoint_circles_ids = self.seg_model.get_endpoint_circles(self.tagged_line_id)

        if self.new_circle_id:  # 원이 생성된 경우에만 실행
            self.canvas.tag_bind(self.new_circle_id, "<ButtonPress-1>",
                                 lambda event: self.handle_circle_click(event, self.new_circle_id))

    def handle_circle_click(self, event, circle_id):
        if event.widget.find_withtag(circle_id):
            self.seg_model.insert_circle_in_points(self.new_circle_id, self.endpoint_circles_ids)  # 기존 points에 new_circl_id 넣기
            line1_id, line2_id = self.seg_view.new_line(self.endpoint_circles_ids, self.new_circle_id, self.tagged_line_id)  # 새로운 선 생성
            self.seg_model.insert_line_in_lines(self.tagged_line_id, line1_id, line2_id)  # 기존 lines에 self.tagged_line_id 넣기
            self.canvas.itemconfig(self.new_circle_id, fill='red', tags='circle')  # points에 들어간 원 tags 바꿔주기

    def seg_bind_events(self):
        # 마우스 클릭 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.check_ctrl_and_click)

        # 마우스 오버 이벤트 바인딩
        self.canvas.bind("<Motion>", self.before_seg_motion)
        self.hotkeys.bind_hotkeys()


    # ctrl 누르고 클릭하면 작동안됌 - 이미지 이동-> ctrl+마우스여서
    def check_ctrl_and_click(self, event):
        if not event.state & 0x4:
            self.on_click(event)


    def seg_unbind(self):
        # 도형이 완성되었을 경우 마우스 클릭 이벤트 작동안하게 바인드 해제
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<B1-Motion>")
        self.hotkeys.unbind_hotkeys()
        # 수정을 위한 바인드 수정
        # tag_unbind
        self.canvas.tag_unbind("line", "<Motion>")

    def seg_reset(self):
        self.seg_view.delete_seg()
        #model
        self.seg_model.points = []  # 원(꼭짓점)의 ID
        self.seg_model.seg_points = []  # seg 좌표 (생기는 다각형의 꼭짓점 좌표)
        self.seg_model.circle = None
        self.seg_model.lines = []  # 선의 ID
        self.seg_model.start_circle = None  # 시작점 원의 ID를 저장하는 변수입니다.
        self.seg_model.active_point = None
        self.seg_model.last_line = None
        self.seg_model.selected_circle = None # 수정할 원, 선 선택
        #view
        self.seg_view.color = None  # 사각형 내부 색(랜덤)
        self.seg_view.polygon = None# 다각형
        self.seg_view.line = None # 선id
        #기존 seg 영향 안미치게 -> 기존 seg 없에버리면 굳이 필요하나?
        self.canvas.dtag("line", "line")
        self.seg_view.delete_over_circle("new_circle")  # new_circle 삭제
        self.seg_view.delete_over_circle("over_circle")


class CubeController:
    def __init__(self, canvas, btn_controller):
        self.canvas = canvas
        self.canvas.focus_set()

        # CubeView
        self.cube_view = CubeView(self, self.canvas)
        # CubeModel
        self.cube_model = CubeModel(self, self.canvas)


        self.x = None
        self.y = None


        #self.hotkeys = CubeHotkeys(self, self.canvas)


        #load 이미지,x, y 좌표 변환
        self.load = Load(btn_controller)  # Load 객체 생성


    def resizing(self):
        # 이미지에 따른 좌표 저장
        if self.cube_model.cube_points:
            self.cube_model.image_cube_points = [(int(point[0] * self.load.x_ratio), int(point[1] * self.load.y_ratio)) for point in
                                                 self.cube_model.cube_points]
        print(self.cube_model.image_cube_points)

    def creat_cuboid(self):
        self.cube_model.cuboid_side(self.x, self.y)
        self.cube_view.draw_3d_cuboid(self.cube_model.start, self.cube_model.end, self.cube_model.diagonal)
        self.cube_view.fill_color()

        self.resizing()


    def buttonPress_mouse(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)
        self.cube_model.start = (self.x, self.y)

    def press_motion(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)
        self.cube_model.end = (self.x, self.y)
        # cube 생성
        self.creat_cuboid()

        # cube circle, line id 저장
        self.cube_model.points = []
        self.cube_model.lines = []
        circles = self.canvas.find_withtag('circle')  # 태그로 된 원들의 ID를 가져옴
        lines = self.canvas.find_withtag('line')  # 태그로 된 원들의 ID를 가져옴
        self.cube_model.points.extend(circles)  # 원들의 ID를 points 리스트에 추가
        self.cube_model.lines.extend(lines)  # 원들의 ID를 points 리스트에 추가

        # 음영 - 다각형 생성
        self.cube_view.cube_polygon(self.cube_model.points)
        # cube_point 좌표 업데이트
        self.cube_model.cube_point()

    def buttonRelease_mouse(self, event):
        #cube 한번 그리면 끝, 이후에는 꼭짓점 수정
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<B1-Motion>", self.on_circle_drag)

        self.hotkeys.bind_hotkeys()


    def motion_mouse(self, event):
        self.x = self.canvas.canvasx(event.x)
        self.y = self.canvas.canvasy(event.y)

        # 활성화 원 찾기
        self.cube_model.active_point = self.cube_model.find_circle_point(self.x, self.y)
        self.cube_view.delete_over_circle("over_circle")

        if self.cube_model.active_point >= 0:
            selected_circle = self.cube_model.points[self.cube_model.active_point]
            self.cube_model.selected_circle = selected_circle
            self.cube_view.over_circle(selected_circle)


# 오버원 생기면 드래그 해서 수정 가능하게 해야함
    def on_circle_drag(self, event):
        # 드래그된 원의 좌표를 가져옵니다.
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        self.cube_model.circle_drag(x, y)
        # 연결된 선의 좌표를 업데이트합니다.
        self.cube_model.update_lines()
        # 오버원 삭제
        self.cube_view.delete_over_circle("over_circle")

        # 음영 - 다각형 생성
        self.cube_view.cube_polygon(self.cube_model.points)

        # cube_point 좌표 업데이트
        self.cube_model.cube_point()

    def cube_bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.buttonPress_mouse)
        self.canvas.bind("<ButtonRelease-1>", self.buttonRelease_mouse)
        self.canvas.bind("<B1-Motion>", self.press_motion)
        self.canvas.bind("<Motion>", self.motion_mouse)
    def cube_unbind(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Motion>")
    def cube_reset(self):
        self.cube_view.delete_cube()
        #model
        self.cube_model.start = None
        self.cube_model.end = None
        self.cube_model.diagonal = None
        self.cube_model.points = []  # 원(꼭짓점)의 ID
        self.cube_model.active_point = None  # 활성화 원
        #view
        self.cube_view.color = None  # 활성화 원

        self.canvas.delete('polygon')
        #self.cube_view.delete_over_circle("new_circle")  # new_circle 삭제
        #self.cube_view.delete_over_circle("over_circle")
