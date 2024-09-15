from math import sqrt


class BBoxModel:
    def __init__(self, controller, canvas):
        self.canvas = canvas
        self.controller = controller
        self.active_point = None        #사각형 꼭짓점 순서
        # 수정에 필요한 사각형 꼭짓점
        self.start = None # 시작점 x, y 좌표
        self.end = None# 끝점 x, y 좌표
        self.threshold = 5       # 꼭짓점으로 부터 마우스 오버 범위 5
        self.bbox_points = []  # 사각형 꼭짓점 저장 / 캔버스가 왼쪽 위가 0,0 오른쪽, 아래쪽으로 가면 양수 / 캔버스 기준 왼쪽 위 부터 시계방향
        self.circles = []  # 꼭짓점 원
        # 사각형 꼭짓점 좌표
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None

        self.image_bbox_points = [] # 이미지 변환에 따른 bbox 좌표

    def min_max(self, x, y, min_x, min_y, max_x, max_y):
        # 주어진 좌표 (x, y)에 대하여 x, y 축을 기준으로 한 반대편 좌표를 반환합니다.
        opposite_x = max_x if x == min_x else min_x
        opposite_y = max_y if y == min_y else min_y
        return opposite_x, opposite_y

    def find_point(self, bbox_points, x, y):
        if bbox_points is None:
            return None
        # 선택된 꼭짓점에서 가장 가까운 꼭짓점 찾기
        self.active_point = None
        for i, point in enumerate(bbox_points):
            distance = ((point[0] - x) ** 2 + (point[1] - y) ** 2) ** 0.5

            if distance < self.threshold:
                self.active_point = i
                break
            else:
                self.active_point = None

    # bbox_points에서 주어진 좌표 (x, y)와 threshold 값을 사용하여 활성화할 포인트를 찾습니다.
    def start_bbox_point(self, x, y):
        self.start = [x, y]


    # 좌표 저장
    def first_bbox_points(self, x1, y1, x2, y2, canvas_width, canvas_height):
        # 좌표의 최소값, 최대값 확인, 네 꼭짓점 항상 동일하게 고정 + 캔버스 범위 벗어나지 않게 함
        self.min_x = min(max(3, x1), canvas_width-3)
        self.min_y = min(max(3, y1), canvas_height-3)
        self.max_x = max(min(x2, canvas_width-3), 3)
        self.max_y = max(min(y2, canvas_height-3), 3)

        self.bbox_points.clear()
        # 꼭짓점 저장 - (수정시 꼭짓점 계속해서 바뀜)
        self.bbox_points = [(self.min_x, self.min_y), (self.max_x, self.min_y), (self.max_x, self.max_y),
                            (self.min_x, self.max_y)]  # 꼭짓점 위치 업데이트

    # bbox 좌표 수정 - 활성화 점을 마우스 지점으로 변경
    def bbox_points_update(self, x, y, canvas_width, canvas_height):
        self.end = [min(max(x, 3), canvas_width-3), min(max(y, 3), canvas_height-3)]
        end_x, end_y = self.end
        if self.active_point is not None:
            # active_point 지점 변경
            self.bbox_points[self.active_point] = (end_x, end_y)
            # bbox_points의 양 옆 꼭짓점 수정
            self.bbox_points[3 - self.active_point] = (end_x, self.bbox_points[3 - self.active_point][1])

            ap = (self.active_point + 1) % 4 if self.active_point % 2 == 0 else (self.active_point - 1) % 4
            self.bbox_points[ap] = (self.bbox_points[ap][0], end_y)

            return self.bbox_points


class SegModel:
    def __init__(self, controller, canvas):
        self.canvas = canvas
        self.controller = controller

        self.threshold = 5  # 시작점 반경 설정 (픽셀)
        self.points = []  # 원(꼭짓점)의 ID
        self.seg_points = []  # seg 좌표 (생기는 다각형의 꼭짓점 좌표)
        self.circle = None
        self.lines = []  # 선의 ID
        self.start_circle = None  # 시작점 원의 ID를 저장하는 변수입니다.
        self.active_point = None
        self.last_line = None
        self.selected_circle = None # 수정할 원, 선 선택

        self.image_seg_points = [] # 이미지 변환에 따른 bbox 좌표

    def circle_id(self, circle):
        self.points.append(circle)

    def line_id(self, line):
        self.lines.append(line)

# 공통
    def find_circle_point(self, x, y):
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

    def seg_completed(self):
        # points에 저장된 원의 개수가 3개 이상이며

        if self.start_circle is None or len(self.points) >= 3:
            # 시작 원의 좌표를 가져옴
            start_coords = self.canvas.coords(self.start_circle)

            if len(start_coords) >= 2:
                # 마지막 원
                last_circle_id = self.points[-1]
                last_circle_coords = self.canvas.coords(last_circle_id)
                # 처음과 마지막 원의 좌표를 비교하여 seg 완성 여부를 판단
                x1, y1 = start_coords[0:2]
                x2, y2 = last_circle_coords[0:2]

                if abs(x1 - x2) <= self.threshold and abs(y1 - y2) <= self.threshold:
                    return True

        return False


    def update_last_circle(self):
        # 마지막으로 그려진 선 삭제
        if self.lines:
            self.last_line = self.lines.pop()
        # 마지막으로 찍힌 원의 좌표 업데이트
        self.canvas.coords(self.points[-1], *self.canvas.coords(self.start_circle))

    def delete_last_circle(self, line):
        self.line_id(line)
        self.points[-1] = self.start_circle # seg 완성
        # 시작 원 초기화
        self.start_circle = None


    # seg 좌표 - 이미지 비율에따라 정확히 바꿔주기
    def seg_point(self):
        self.seg_points = []  # 다각형의 좌표를 초기화합니다.
        for line in self.lines:
            coords = self.canvas.coords(line)
            if len(coords) >= 2:
                self.seg_points.append((coords[0], coords[1]))  # 선분의 시작 좌표를 추가합니다.



    # seg 완성 후 마우스 - 원 오버시
    def mouse_point_after_seg(self, event):
        # 세그먼트가 완성된 상태인 경우, 오버된 원 찾기.
        # 수정 - 드래그할 꼭지점(원) 설정합니다.
        self.selected_circle = self.points[self.active_point] if self.active_point >= 0 else None


    # seg 완성 후 수정 - 공통
    def circle_drag(self, x, y):
        if self.selected_circle is not None:
            # 캔버스의 크기 가져오기
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # 드래그하려는 원의 반지름 계산
            circle_radius = (self.canvas.coords(self.selected_circle)[2] - self.canvas.coords(self.selected_circle)[0]) / 2

            # 원의 중심 좌표 계산
            circle_center_x = min(max(circle_radius, x), canvas_width - circle_radius)
            circle_center_y = min(max(circle_radius, y), canvas_height - circle_radius)

            # 원을 새로운 좌표로 이동
            self.canvas.coords(self.selected_circle,
                               circle_center_x - circle_radius,
                               circle_center_y - circle_radius,
                               circle_center_x + circle_radius,
                               circle_center_y + circle_radius)


    def update_lines(self): # 좌표 앞뒤만 찾아서 수정
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

#==================================
    # 선 태그시 위에 생기는 원 - 중심좌표 선으로 하기 위함
    #tag된 선중 가장 가까운 점을 찾는다.
    def find_closest_point(self, x, y):
        segments = self.canvas.find_withtag("line")  # 모든 선을 가져옴
        closest_point = None
        min_distance = float('inf')
        for segment in segments:
            x1, y1, x2, y2 = self.canvas.coords(segment)  # 선의 좌표 가져오기
            if x1 == x2 and y1 == y2:  # 선분이 아닌 점일 경우 건너뜀
                continue
            closest_x, closest_y = self.closest_point_on_segment(x, y, x1, y1, x2, y2)  # 선 위의 가장 가까운 점 찾기
            distance = ((x - closest_x) ** 2 + (y - closest_y) ** 2) ** 0.5  # 마우스 좌표와 가장 가까운 점 사이의 거리 계산
            if distance < min_distance:
                min_distance = distance
                closest_point = (closest_x, closest_y)
        return closest_point

    def closest_point_on_segment(self, x, y, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return x1, y1
        t = ((x - x1) * dx + (y - y1) * dy) / (dx ** 2 + dy ** 2)
        t = max(0, min(1, t))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        return closest_x, closest_y
#=========================
    # # 선의 양 꼭짓점 좌표 가져오기
    def get_endpoint_circles(self, tagged_line_id):
        endpoint_circles = []

        # 선의 양 꼭짓점 좌표 가져오기
        line_coords = self.canvas.coords(tagged_line_id)
        x1, y1, x2, y2 = line_coords[0], line_coords[1], line_coords[2], line_coords[3]

        # 선의 양 꼭짓점에 해당하는 원 ID 가져오기
        for circle_id in self.points:
            circle_coords = self.canvas.coords(circle_id)
            cx, cy = (circle_coords[0] + circle_coords[2]) / 2, (circle_coords[1] + circle_coords[3]) / 2
            if (cx, cy) == (x1, y1) or (cx, cy) == (x2, y2):
                endpoint_circles.append(circle_id)
            # 원 ID가 2개인 경우 종료
            if len(endpoint_circles) == 2:
                break
        # 예외 처리
        if endpoint_circles[0] == self.points[-1] and endpoint_circles[1] == self.points[-2]:
            endpoint_circles[0], endpoint_circles[1] = endpoint_circles[1], endpoint_circles[0]

        return endpoint_circles

    # 새로 생기는 원, points에 어느 원과 원 사이인지 확인 후 위치에 맞게 넣기
    def insert_circle_in_points(self, new_circle_id, endpoint_circles_ids):
        # 꼭짓점 원 ID들 중 첫 번째 원 ID와 마지막 원 ID 가져오기
        left_id = endpoint_circles_ids[0]
        right_id = endpoint_circles_ids[1]

        # 첫 번째 원 ID와 마지막 원 ID 사이에 새로운 원 ID를 삽입
        left_index = self.points.index(left_id)
        right_index = self.points.index(right_id)
        if left_index < right_index:
            self.points.insert(right_index, new_circle_id)
        else:
            self.points.insert(right_index - 1, new_circle_id)

    def insert_line_in_lines(self, tagged_line_id, line1_id, line2_id):
        # 선 ID와 새로운 선 ID들을 연결하여 lines에 추가
        line_index = self.lines.index(tagged_line_id)
        self.lines[line_index:line_index + 1] = [line1_id, line2_id]


class CubeModel:
    def __init__(self, controller, canvas):
        self.canvas = canvas
        self.controller = controller

        self.start = None
        self.end = None
        self.diagonal = None

        self.points = []  # 원(꼭짓점)의 ID
        self.lines = []  # 선의 ID
        self.active_point = None # 활성화 원
        self.threshold = 5
        self.selected_circle = None # 수정할 원, 선 선택
        self.cube_points = []

        self.image_cube_points = [] # 이미지 변환에 따른 bbox 좌표
    def cuboid_side(self, x, y):
        if self.start and self.end:
            width = abs(self.start[0] - self.end[0])
            height = abs(self.start[1] - self.end[1])
            depth = sqrt(width ** 2 + height ** 2)
            self.diagonal = int(round(sqrt(width ** 2 + height ** 2 + depth ** 2)))

# seg 공통
    def circle_id(self, circle):
        self.points.append(circle)


# seg 공통
    def find_circle_point(self, x, y):
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

# seg 공통
    def circle_drag(self, x, y):
        self.selected_circle = self.points[self.active_point] if self.active_point >= 0 else None

        if self.selected_circle is not None:
            # 캔버스의 크기 가져오기
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # 드래그하려는 원의 반지름 계산
            circle_radius = (self.canvas.coords(self.selected_circle)[2] - self.canvas.coords(self.selected_circle)[0]) / 2

            # 원의 중심 좌표 계산
            circle_center_x = min(max(circle_radius, x), canvas_width - circle_radius)
            circle_center_y = min(max(circle_radius, y), canvas_height - circle_radius)

            # 원을 새로운 좌표로 이동
            self.canvas.coords(self.selected_circle,
                               circle_center_x - circle_radius,
                               circle_center_y - circle_radius,
                               circle_center_x + circle_radius,
                               circle_center_y + circle_radius)



    def update_lines(self):
        active_index = self.active_point  # active_point의 인덱스를 찾습니다.

        # active_index에 따라 lines 리스트의 요소들을 업데이트합니다.
        if active_index == 0:
            self.canvas.coords(self.lines[0], *self.get_line_coords(0, 1))
            self.canvas.coords(self.lines[3], *self.get_line_coords(0, 3))
            self.canvas.coords(self.lines[8], *self.get_line_coords(0, 4))
        elif active_index == 1:
            self.canvas.coords(self.lines[0], *self.get_line_coords(1, 0))
            self.canvas.coords(self.lines[1], *self.get_line_coords(1, 2))
            self.canvas.coords(self.lines[9], *self.get_line_coords(1, 5))
        elif active_index == 2:
            self.canvas.coords(self.lines[1], *self.get_line_coords(2, 1))
            self.canvas.coords(self.lines[2], *self.get_line_coords(2, 3))
            self.canvas.coords(self.lines[10], *self.get_line_coords(2, 6))
        elif active_index == 3:
            self.canvas.coords(self.lines[2], *self.get_line_coords(3, 2))
            self.canvas.coords(self.lines[3], *self.get_line_coords(3, 0))
            self.canvas.coords(self.lines[11], *self.get_line_coords(3, 7))
        elif active_index == 4:
            self.canvas.coords(self.lines[4], *self.get_line_coords(4, 5))
            self.canvas.coords(self.lines[7], *self.get_line_coords(4, 7))
            self.canvas.coords(self.lines[8], *self.get_line_coords(4, 0))
        elif active_index == 5:
            self.canvas.coords(self.lines[4], *self.get_line_coords(5, 4))
            self.canvas.coords(self.lines[5], *self.get_line_coords(5, 6))
            self.canvas.coords(self.lines[9], *self.get_line_coords(5, 1))
        elif active_index == 6:
            self.canvas.coords(self.lines[5], *self.get_line_coords(6, 5))
            self.canvas.coords(self.lines[6], *self.get_line_coords(6, 7))
            self.canvas.coords(self.lines[10], *self.get_line_coords(6, 2))
        elif active_index == 7:
            self.canvas.coords(self.lines[6], *self.get_line_coords(7, 6))
            self.canvas.coords(self.lines[7], *self.get_line_coords(7, 4))
            self.canvas.coords(self.lines[11], *self.get_line_coords(7, 3))


    def get_line_coords(self, start, end):
        coords1 = self.canvas.coords(self.points[start])
        coords2 = self.canvas.coords(self.points[end])
        # 원의 중앙
        x1 = (coords1[0] + coords1[2]) / 2
        y1 = (coords1[1] + coords1[3]) / 2
        x2 = (coords2[0] + coords2[2]) / 2
        y2 = (coords2[1] + coords2[3]) / 2
        return x1, y1, x2, y2

    # seg 공통
    def cube_point(self):
        self.cube_points = []  # 다각형의 좌표를 초기화합니다.
        for point in self.points:
            coords = self.canvas.coords(point)
            if len(coords) >= 2:
                self.cube_points.append((coords[0], coords[1]))  # 선분의 시작 좌표를 추가합니다.