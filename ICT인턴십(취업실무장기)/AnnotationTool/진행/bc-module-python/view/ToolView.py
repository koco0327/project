import random
import math
class BBoxView:
    def __init__(self, controller, canvas):
        self.canvas = canvas
        self.controller = controller
        self.canvas.focus_set()  # 캔버스에 포커스 설정 - 이거 안하면 키보드 이벤트 인식 못함
        # 캔버스 크기
        self.canvas_width = None
        self.canvas_height = None

        self.rect = None  # 사각형

        self.circles = []  # 꼭짓점 원
        self.color = None  # 사각형 내부 색(랜덤)
        # 원 바뀌는 색 및 크기
        self.change_circle_size = 6
        self.change_circle_color = "yellow"
        self.over_circle = []  # 바뀌는 원 저장 리스트


    # 켄버스 크기
    def update_canvas_size(self):
        self.canvas.update()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

    # 사각형 음영 색 랜덤- view
    def fill_color(self):
        if self.color is None:
            r, g, b, a = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200), 30)
            self.color = '#%02x%02x%02x' % (r, g, b)


    # 사각형 꼭짓점 원 - view
    def circle(self, bbox_points, circle_size=3, circle_color="red"):
        # 기존에 그려진 원 삭제
        for circle in self.circles:
            self.canvas.delete(circle)
        self.circles.clear()

        # 꼭짓점 좌표를 사용하여 원 생성
        points = bbox_points

        for point in points:
            x, y = point
            circle = self.canvas.create_oval(x - circle_size, y - circle_size,
                                             x + circle_size, y + circle_size,
                                             fill=circle_color, tag='bbox_circle')
            self.circles.append(circle)



    # view
    def delete_over_circle(self, circle_name):
        self.canvas.delete(circle_name)


    # bbox 그리기 - view
    def draw_bbox(self, bbox_points):
        # 이미 그려진 사각형 있으면 삭제
        if self.rect is not None:
            self.canvas.delete(self.rect)
        # 사각형 그리기 - (point에 따라)
        self.rect = self.canvas.create_rectangle(*bbox_points[0], *bbox_points[2], outline='red', width=2,
                                                 dash=(100, 100), tag='bbox')
        # 꼭짓점 원
        self.circle(bbox_points)
        # 사각형 음영 색
        self.fill_color()
        self.canvas.itemconfigure(self.rect, fill=self.color, stipple='gray50')
        # 꼭짓점에 마우스 오버 - 꼭짓점 활성화

    # bbox 그리기 - view
    def delete_bbox(self):
        if self.rect is not None:
            self.canvas.delete(self.rect)

        if self.circles is not None:
            for circle in self.circles:
                self.canvas.delete(circle)


    def create_over_circle(self, active_point, bbox_points):
        if active_point is None:
            return
        # 해당 꼭짓점 오버 원 생성
        point = bbox_points[active_point]
        x, y = point[0], point[1]
        self.canvas.create_oval(x - self.change_circle_size, y - self.change_circle_size,
                                x + self.change_circle_size, y + self.change_circle_size,
                                fill=self.change_circle_color, tag='over_circle')


class SegView:
    def __init__(self, controller, canvas):
        self.canvas = canvas
        self.controller = controller

        self.color = None  # 사각형 내부 색(랜덤)
        self.change_circle_size = 6  # 변경된 원의 크기
        self.change_circle_color = "yellow"  # 변경된 원의 색상
        # 다각형
        self.polygon = None
        # 선id
        self.line = None
    def create_circle(self, x, y, circle_size = 3, circle_color = "red", tag = 'circle'):
        # 원 생성
        circle = self.canvas.create_oval(
            x - circle_size,
            y - circle_size,
            x + circle_size,
            y + circle_size,
            fill = circle_color,
            tags = tag
        )
        return circle

    # 원과 원 연결 - view
    def connect_circles(self, circle1, circle2):
        # 원과 원을 선으로 연결
        coords1 = self.canvas.coords(circle1) # 객체의 좌표 가져오기
        coords2 = self.canvas.coords(circle2)

        x1 = (coords1[0] + coords1[2]) / 2
        y1 = (coords1[1] + coords1[3]) / 2
        x2 = (coords2[0] + coords2[2]) / 2
        y2 = (coords2[1] + coords2[3]) / 2

        self.line = self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2, dash=(100, 100), tags="line")
        return self.line


    def over_circle(self, circle):
        # 오버 원 생성
        circle_coords = self.canvas.coords(circle)
        circle_x = (circle_coords[0] + circle_coords[2]) / 2
        circle_y = (circle_coords[1] + circle_coords[3]) / 2
        # 오버 원 생성
        self.create_circle(circle_x, circle_y, self.change_circle_size, self.change_circle_color, "over_circle")

    def delete_over_circle(self, circle_name):
        # 모든 오버 원 삭제
        self.canvas.delete(circle_name)


    def last_line(self, last_line, points, start_circle):
        self.canvas.delete(last_line)

        # 마지막 원과 첫 번째 원을 연결하는 선 그리기
        self.connect_circles(points[-2], start_circle)
        # 마지막 원 삭제
        self.canvas.delete(points[-1])

    def fill_color(self):
        if self.color is None:
            r, g, b = (random.randint(0, 240), random.randint(0, 240), random.randint(0, 240))
            self.color = '#%02x%02x%02x' % (r, g, b)


    # seg에 맞는 다각형
    def seg_polygon(self, seg_points):
        if self.polygon:
            # 기존의 다각형이 존재하는 경우 다각형을 삭제합니다.
            self.canvas.delete(self.polygon)

        if len(seg_points) >= 3:
            # 선분 좌표를 사용하여 다각형을 생성합니다.
            flattened_points = [coord for point in seg_points for coord in point]
            self.polygon = self.canvas.create_polygon(flattened_points, fill=self.color, outline='', stipple='gray50', tag='polygon')

    # 새로운 선 추가
    def new_line(self, endpoint_circles_ids, new_circle_id, tagged_line_id):
        # 현재 마우스 위치와 가장 가까운 선의 양 끝 원 ID 가져오기
        if len(endpoint_circles_ids) == 2:
            circle1, circle2 = endpoint_circles_ids
            # 객체의 좌표 가져오기
            coords1 = self.canvas.coords(circle1)
            coords2 = self.canvas.coords(circle2)
            coords3 = self.canvas.coords(new_circle_id)

            x1 = (coords1[0] + coords1[2]) / 2
            y1 = (coords1[1] + coords1[3]) / 2
            x2 = (coords2[0] + coords2[2]) / 2
            y2 = (coords2[1] + coords2[3]) / 2
            x3 = (coords3[0] + coords3[2]) / 2
            y3 = (coords3[1] + coords3[3]) / 2

            # 기존 선 삭제 - 기존선 말고 테그선만 삭제해야할 수도
            self.canvas.delete(tagged_line_id)

            # 새로운 선1 생성
            line1_id = self.canvas.create_line(x1, y1, x3, y3, fill='red', width=2, dash=(100, 100), tags="line")
            # 새로운 선2 생성
            line2_id = self.canvas.create_line(x2, y2, x3, y3, fill='red', width=2, dash=(100, 100), tags="line")

            return line1_id, line2_id

    def update_circle(self, closest_point):
        if closest_point is not None:
            # 수정원 생성
            new_circle_id = self.create_circle(*closest_point, circle_size=3, circle_color="yellow", tag="new_circle")
            return new_circle_id

    # bbox 그리기 - view
    def delete_seg(self):
        self.canvas.delete('circle')
        self.canvas.delete('line')
        self.canvas.delete('polygon')


class CubeView:
    def __init__(self, controller, canvas):
        self.canvas = canvas
        self.controller = controller
        self.change_circle_size = 6
        self.change_circle_color = 'yellow'
        self.color = None  # 큐브의 기본 색상을 저장할 변수
        self.polygons = []  # 면
    def fill_color(self):
        if self.color is None:
            r, g, b, a = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200), 30)
            self.color = '#%02x%02x%02x' % (r, g, b)


    # 큐보이드 모양
    def draw_3d_cuboid(self, start, end, diagonal):
        self.canvas.delete('line')  # 이전 큐보이드 삭제
        self.canvas.delete('circle') # 이전 원 삭제
        # 뒷면 그리기
        x1, y1 = start
        x2, y2 = end
        self.draw_lines([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], fill='red')


        # 앞면 그리기
        front_x1, front_y1 = x1 + diagonal // 10, y1 + diagonal // 10
        front_x2, front_y2 = x2 + diagonal // 10, y2 + diagonal // 10
        self.draw_lines([(front_x1, front_y1), (front_x2, front_y1),
                         (front_x2, front_y2), (front_x1, front_y2)], fill='red')

        # 변 간의 선 그리기
        self.canvas.create_line(x1, y1, front_x1, front_y1, fill='red', width=2, dash=(100, 100), tags='line')
        self.canvas.create_line(x2, y1, front_x2, front_y1, fill='red', width=2, dash=(100, 100), tags='line')
        self.canvas.create_line(x2, y2, front_x2, front_y2, fill='red', width=2, dash=(100, 100), tags='line')
        self.canvas.create_line(x1, y2, front_x1, front_y2, fill='red', width=2, dash=(100, 100), tags='line')


    # 선 생성
    def draw_lines(self, points, fill):
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            self.canvas.create_line(x1, y1, x2, y2, fill=fill, width=2, dash=(100, 100), tags='line')
            self.create_circle(x1, y1)


    def create_circle(self, x, y, circle_size = 3, circle_color = "red", tag = 'circle'):
        # 원 생성
        circle = self.canvas.create_oval(
            x - circle_size,
            y - circle_size,
            x + circle_size,
            y + circle_size,
            fill = circle_color,
            tags = tag
        )
        return circle



    def over_circle(self, circle):
        # 오버 원 생성
        circle_coords = self.canvas.coords(circle)
        circle_x = (circle_coords[0] + circle_coords[2]) / 2
        circle_y = (circle_coords[1] + circle_coords[3]) / 2
        # 오버 원 생성
        self.create_circle(circle_x, circle_y, self.change_circle_size, self.change_circle_color, "over_circle")


    def delete_over_circle(self, circle_name):
        # 모든 오버 원 삭제
        self.canvas.delete(circle_name)

    def delete_cube(self):
        self.canvas.delete('circle')
        self.canvas.delete('line')


    def cube_polygon(self, cube_points):
        # 기존의 다각형이 존재하는 경우 다각형을 삭제합니다.
        for polygon in self.polygons:
            self.canvas.delete(polygon)
        self.polygons = []

        if len(cube_points) >= 8:
            # 점 좌표를 사용하여 면을 생성합니다.
            back_face = [((coord[0] + coord[2]) / 2, (coord[1] + coord[3]) / 2) for coord in
                         [self.canvas.coords(cube_points[i]) for i in range(4)]]
            front_face = [((coord[0] + coord[2]) / 2, (coord[1] + coord[3]) / 2) for coord in
                          [self.canvas.coords(cube_points[i]) for i in range(4, 8)]]
            top_face = [((coord[0] + coord[2]) / 2, (coord[1] + coord[3]) / 2) for coord in
                        [self.canvas.coords(cube_points[i]) for i in [0, 1, 5, 4]]]
            bottom_face = [((coord[0] + coord[2]) / 2, (coord[1] + coord[3]) / 2) for coord in
                           [self.canvas.coords(cube_points[i]) for i in [3, 2, 6, 7]]]
            left_face = [((coord[0] + coord[2]) / 2, (coord[1] + coord[3]) / 2) for coord in
                         [self.canvas.coords(cube_points[i]) for i in [0, 4, 7, 3]]]
            right_face = [((coord[0] + coord[2]) / 2, (coord[1] + coord[3]) / 2) for coord in
                          [self.canvas.coords(cube_points[i]) for i in [1, 5, 6, 2]]]

            self.polygons = [
                self.canvas.create_polygon(back_face, fill=self.color, outline='', stipple='gray25',
                                           tags='polygon'),
                self.canvas.create_polygon(front_face, fill=self.color, outline='', stipple='gray50',
                                           tags='polygon'),
                self.canvas.create_polygon(top_face, fill=self.color, outline='', stipple='gray50',
                                           tags='polygon'),
                self.canvas.create_polygon(bottom_face, fill=self.color, outline='', stipple='gray50',
                                           tags='polygon'),
                self.canvas.create_polygon(left_face, fill=self.color, outline='', stipple='gray50',
                                           tags='polygon'),
                self.canvas.create_polygon(right_face, fill=self.color, outline='', stipple='gray50',
                                           tags='polygon')
            ]