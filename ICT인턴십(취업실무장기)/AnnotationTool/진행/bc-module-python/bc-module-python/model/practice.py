
#
# from math import sqrt
# import tkinter as tk
#
# class Cube:
#     def __init__(self, canvas):
#         self.canvas = canvas
#         self.canvas.pack()
#         self.start_point = None
#         self.end_point = None
#         # 꼭짓점 리스트
#         self.points = []
#         # 사각형 색
#         self.color = None
#
#     def fill_color(self):
#         if self.color is None:
#             r, g, b, a = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200), 30)
#             self.color = '#%02x%02x%02x' % (r, g, b)
#
#
#     def draw_cuboid(self):
#         if self.start_point and self.end_point:
#             width = abs(self.start_point[0] - self.end_point[0])
#             height = abs(self.start_point[1] - self.end_point[1])
#             depth = sqrt(width ** 2 + height ** 2)
#             diagonal = int(round(sqrt(width ** 2 + height ** 2 + depth ** 2)))
#             x_center = (self.start_point[0] + self.end_point[0]) // 2
#             y_center = (self.start_point[1] + self.end_point[1]) // 2
#
#             x1 = x_center - width // 2
#             y1 = y_center - height // 2
#             x2 = x_center + width // 2
#             y2 = y_center + height // 2
#
#             self.draw_3d_cuboid(x1, y1, x2, y2, diagonal)
#
#     def draw_3d_cuboid(self, x1, y1, x2, y2, diagonal):
#         # 색 설정
#         self.fill_color()
#         # 전면 그리기
#         self.canvas.create_rectangle(x1, y1, x2, y2, tags="cuboid", fill = self.color, stipple="gray50")
#
#         # 뒷면 그리기
#         back_x1 = x1 + diagonal // 10
#         back_y1 = y1 + diagonal // 10
#         back_x2 = x2 + diagonal // 10
#         back_y2 = y2 + diagonal // 10
#         self.canvas.create_rectangle(back_x1, back_y1, back_x2, back_y2, tags="cuboid", fill=self.color,
#                                      stipple="gray25")
#
#         # 선 연결
#         self.canvas.create_line(x1, y1, back_x1, back_y1, fill="black", tags="cuboid")
#         self.canvas.create_line(x2, y1, back_x2, back_y1, fill="black", tags="cuboid")
#         self.canvas.create_line(x2, y2, back_x2, back_y2, fill="black", tags="cuboid")
#         self.canvas.create_line(x1, y2, back_x1, back_y2, fill="black", tags="cuboid")
#
#     def on_mouse_click(self, event):
#         self.start_point = (event.x, event.y)
#
#
#     def on_mouse_drag(self, event):
#         self.end_point = (event.x, event.y)
#         self.canvas.delete("cuboid")  # 이전 큐보이드 삭제
#         self.draw_cuboid()
#
#     def on_mouse_release(self, event):
#         self.end_point = (event.x, event.y)
#         self.canvas.delete("cuboid")  # 이전 큐보이드 삭제
#         self.draw_cuboid()
#
#
#     def cuboid_bind_events(self):
#         self.canvas.bind("<Button-1>", self.on_mouse_click)
#         self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
#         self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
#
#     def cuboid_unbind(self):
#         self.canvas.unbind("<Button-1>")
#         self.canvas.unbind("<B1-Motion>")
#         self.canvas.unbind("<ButtonRelease-1>")
#


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
