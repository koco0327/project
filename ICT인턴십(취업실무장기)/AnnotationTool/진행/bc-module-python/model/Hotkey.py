from PIL import ImageTk, Image
import keyboard
from model.ToolModel import BBoxModel
from view.ToolView import BBoxView, SegView

class Hotkey:
    def __init__(self, root, canvas, image, my_image, new_w, toolbar_btns, bbox_controller):
        self.toolbar_btns = toolbar_btns

        self.root = root
        self.canvas = canvas
        self.image = image
        self.my_image = my_image
        self.new_w = new_w

        self.scale = 1.0
        self.zoomin_scale = 1.2
        self.zoomout_scale = 0.8

        # zoomin, zoomout
        self.root.bind("<Control-KeyPress-plus>", lambda event: self.zoom_in())           # 키보드
        self.root.bind("<Control-KeyPress-minus>", lambda event: self.zoom_out())         # 키보드
        self.canvas.bind("<Control-MouseWheel>", lambda event: self.mouse_wheel(event))   # 마우스

        # 이미지 이동 마우스
        # self.canvas.bind("<ButtonPress-1>", lambda event: self.on_mouse_press(event))
        self.canvas.bind("<Control-B1-Motion>", lambda event: self.move_image_with_mouse(event))
        # self.canvas.bind("<ButtonRelease-1>", lambda event: self.on_mouse_release(event))

        # 이미지 이동 키보드 방향키
        self.root.bind("<Up>", lambda event: self.move_image_with_arrow_keys(event))
        self.root.bind("<Down>", lambda event: self.move_image_with_arrow_keys(event))
        self.root.bind("<Left>", lambda event: self.move_image_with_arrow_keys(event))
        self.root.bind("<Right>", lambda event: self.move_image_with_arrow_keys(event))

        # ctrl + s
        # self.root.bind("<Control-s>", lambda event: self.hotkey_ctrl_s())
        self.root.bind("<Control-s>", lambda event: self.new_w.label_box())
        # self.root.bind("<Control-S>", lambda event: self.new_w.label_box())

        self.bbox_model = bbox_controller.bbox_model

        # bbox 뒤로가기
        self.bbox_hotkeys = BBoxHotkeys(bbox_controller, self.canvas)

        width, height = self.image.size
        # 바운딩 박스 좌표를 이미지의 정중앙을 기준으로 조정
        self.center_x = width / 2
        self.center_y = height / 2

    # 마우스 휠
    def mouse_wheel(self, event):
        if event.delta == 120:     # 휠 위로
            self.zoom_in()
        if event.delta == -120:    # 휠 아래로
            self.zoom_out()

    def zoom_in(self):
        self.zoom(self.zoomin_scale)

    def zoom_out(self):
        self.zoom(self.zoomout_scale)

    def zoom(self, scale_factor):
        width, height = self.image.size
        self.scale *= scale_factor
        new_width, new_height = int(width * self.scale), int(height * self.scale)
        zoomed_image = self.image.resize((new_width, new_height), resample=Image.BICUBIC)
        self.tk_image = ImageTk.PhotoImage(zoomed_image)
        image_id = self.canvas.find_withtag("image")
        self.canvas.itemconfigure(image_id, image=self.tk_image)


        # 좌표 변환 적용 - bbox ######################################
        # 바운딩 박스 원 및 선 좌표 가져오기
        bbox_coords = self.canvas.coords("bbox")
        bbox_circle_ids = self.canvas.find_withtag("bbox_circle")

        # 캔버스 사각형 변환
        new_bbox_coords = self.transform_coords(bbox_coords, self.center_x, self.center_y, scale_factor)
        self.canvas.coords("bbox", *new_bbox_coords)
        # 캔버스 원 변환
        for circle_id in bbox_circle_ids:
            bbox_circle_coords = self.canvas.coords(circle_id)
            new_bbox_circle_coords = self.transform_coords(bbox_circle_coords, self.center_x, self.center_y,
                                                           scale_factor)
            self.canvas.coords(circle_id, *new_bbox_circle_coords)

        # bbox_points 좌표 변환
        bbox_points = self.bbox_model.bbox_points
        new_bbox_points = []
        for point in bbox_points:
            new_point = self.transform_coords(point, self.center_x, self.center_y, scale_factor)
            new_bbox_points.append(new_point)
        self.bbox_model.bbox_points = new_bbox_points
        # 좌표 변환 적용 - seg, cuboid ######################################
        # 세그먼트, 큐보이드 원 및 선 좌표 가져오기
        circle_ids = self.canvas.find_withtag("circle")
        line_ids = self.canvas.find_withtag("line")
        polygon_ids = self.canvas.find_withtag("polygon")

        #  음영 변환
        for polygon_id in polygon_ids:
            polygon_coords = self.canvas.coords(polygon_id)
            new_polygon = self.transform_coords(polygon_coords, self.center_x, self.center_y, scale_factor)
            self.canvas.coords(polygon_id, *new_polygon)

        # 원 변환
        for circle_id in circle_ids:
            circle_coords = self.canvas.coords(circle_id)
            new_circle_coords = self.transform_coords(circle_coords, self.center_x, self.center_y, scale_factor)
            self.canvas.coords(circle_id, *new_circle_coords)

        # 선 변환
        for line_id in line_ids:
            coords = self.canvas.coords(line_id)
            new_coords = self.transform_coords(coords, self.center_x, self.center_y, scale_factor)
            self.canvas.coords(line_id, *new_coords)

        # bbox 뒤로가기 를 위한 저장된 좌표 변환
        for i, bbox_points in enumerate(self.bbox_hotkeys.bbox_points_history):
            new_bbox_points = []
            for point in bbox_points:
                new_point = self.transform_coords(point, self.center_x, self.center_y, scale_factor)
                new_bbox_points.append(tuple(new_point))
            self.bbox_hotkeys.bbox_points_history[i] = new_bbox_points

    def transform_coords(self, coords, center_x, center_y, scale):
        transformed_coords = []
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i + 1]
            new_x = (x - center_x) * scale + center_x
            new_y = (y - center_y) * scale + center_y
            transformed_coords.extend([new_x, new_y])
        return transformed_coords


    # 키보드 방향키
    def move_image_with_arrow_keys(self, event):
        key = event.keysym
        move_amount = 10  # 이동 거리 조절 가능

        x, y = 0, 0

        if key == "Up":
            y = -move_amount
        elif key == "Down":
            y = move_amount
        elif key == "Left":
            x = -move_amount
        elif key == "Right":
            x = move_amount
        else:
            return

        self.canvas.move("all", x, y)
        self.center_x += x  # center_x 업데이트
        self.center_y += y  # center_y 업데이트

        # bbox_points 좌표 이동
        bbox_points = self.bbox_model.bbox_points
        new_bbox_points = []
        for point in bbox_points:
            new_point = [point[0] + x, point[1] + y]
            new_bbox_points.append(new_point)
        self.bbox_model.bbox_points = new_bbox_points

        # bbox_points_history 좌표 이동
        for i, bbox_points in enumerate(self.bbox_hotkeys.bbox_points_history):
            new_bbox_points = []
            for point in bbox_points:
                new_point = [point[0] + x, point[1] + y]
                new_bbox_points.append(tuple(new_point))
            self.bbox_hotkeys.bbox_points_history[i] = new_bbox_points


    # 마우스 이동
    def move_image_with_mouse(self, event):
        prev_x, prev_y = self.canvas.coords(self.my_image)
        x, y = event.x - prev_x, event.y - prev_y
        x /= self.scale  # 현재 확대/축소 비율로 x 이동 거리 조정
        y /= self.scale  # 현재 확대/축소 비율로 y 이동 거리 조정
        self.canvas.move("all", x, y)
        self.center_x += x  # center_x 업데이트
        self.center_y += y  # center_y 업데이트

        # bbox_points 좌표 이동
        bbox_points = self.bbox_model.bbox_points
        new_bbox_points = []
        for point in bbox_points:
            new_point = [point[0] + x, point[1] + y]
            new_bbox_points.append(new_point)
        self.bbox_model.bbox_points = new_bbox_points


        # bbox_points_history 좌표 이동
        for i, bbox_points in enumerate(self.bbox_hotkeys.bbox_points_history):
            new_bbox_points = []
            for point in bbox_points:
                new_point = [point[0] + x, point[1] + y]
                new_bbox_points.append(tuple(new_point))
            self.bbox_hotkeys.bbox_points_history[i] = new_bbox_points


    # 뒤로가기 - control + z 시뮬레이트
    def step_back(self):
        # 키보드 이벤트를 시뮬레이트하면, 다른 응용프로그램에도 영향을 줄 수 있음. 이 부분을 주의하여야 함
        keyboard.press('ctrl')
        keyboard.press('z')
        keyboard.release('z')
        keyboard.release('ctrl')


class BBoxHotkeys:
    bbox_points_history = []
    def __init__(self, controller, canvas):
        self.controller = controller
        self.canvas = canvas
        self.bbox_view = self.controller.bbox_view
        self.bbox_model = self.controller.bbox_model


    def save_points(self, event=None):
        BBoxHotkeys.bbox_points_history.append(self.bbox_model.bbox_points.copy())

        print('BBoxHotkeys.bbox_points_history', BBoxHotkeys.bbox_points_history)
        # 뒤로가기 횟수가 10번을 초과하는 경우, 이전 기록을 삭제합니다.
        if len(BBoxHotkeys.bbox_points_history) > 9:
            BBoxHotkeys.bbox_points_history.pop(0)

    def step_back(self, event):
        if len(BBoxHotkeys.bbox_points_history) > 1:
            self.bbox_model.bbox_points = BBoxHotkeys.bbox_points_history[-2].copy()
            print('self.bbox_model.bbox_points',self.bbox_model.bbox_points)
            if len(self.bbox_model.bbox_points) >= 4:
                self.bbox_view.draw_bbox(self.bbox_model.bbox_points)
            BBoxHotkeys.bbox_points_history.pop()

    def bind_hotkeys(self):
        self.canvas.focus_set()
        self.canvas.bind("<Control-z>", self.step_back)
        self.canvas.bind("<ButtonRelease-1>", self.save_points)

    def unbind_hotkeys(self):
        self.canvas.unbind("<Control-z>")
        self.canvas.unbind("<ButtonRelease-1>")



class SegHotkeys:
    def __init__(self, controller, canvas):
        self.controller = controller
        self.canvas = canvas

        self.seg_view = self.controller.seg_view
        self.seg_model = self.controller.seg_model

    def step_back(self, event):
        if self.seg_model.points:
            circle = self.seg_model.points.pop()
            if self.seg_model.lines:
                line = self.seg_model.lines.pop()
                self.seg_view.canvas.delete(line)
                if self.seg_model.seg_points:
                    self.seg_model.seg_points.pop()
            self.seg_view.canvas.delete(circle)

    def bind_hotkeys(self):
        # ctrl + z
        self.canvas.bind("<Control-z>", self.step_back)

    def unbind_hotkeys(self):
        self.canvas.unbind("<Control-z>")


class CubeHotkeys:
    def __init__(self, controller, canvas):
        self.controller = controller
        self.canvas = canvas
        self.cube_view = self.controller.cube_view
        self.cube_model = self.controller.cube_model
        self.cube_points_history = []

    def save_points(self, event=None):
        self.cube_points_history.append(self.cube_model.cube_points.copy())

        # 뒤로가기 횟수가 10번을 초과하는 경우, 이전 기록을 삭제합니다.
        if len(self.cube_points_history) > 9:
            self.cube_points_history.pop(0)


##############################################################
    # 수정해야함
    ###################################################
    def step_back(self, event): # 컨지 몇번까지 할 수 있는지 제한 - config
        if len(self.cube_points_history) > 1:
            self.cube_model.cube_points = self.cube_points_history[-2].copy()

            if len(self.cube_model.cube_points) >= 8:

                self.cube_points_history.pop()


    def bind_hotkeys(self):
        self.canvas.focus_set()
        self.canvas.bind("<Control-z>", self.step_back)
        self.canvas.bind("<ButtonRelease-1>", self.save_points)

    def unbind_hotkeys(self):
        self.canvas.unbind("<Control-z>")
        self.canvas.unbind("<ButtonRelease-1>")
