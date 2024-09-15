
class Label:
    def __init__(self, canvas):
        self.canvas = canvas

    def label_save(self, x_ratio, y_ratio, bbox_points=None, seg_points=None):
        if bbox_points:
            labeled_bbox_points = [(int(point[0] * x_ratio), int(point[1] * y_ratio)) for point in bbox_points]
            print('BBox 원래 좌표:', bbox_points)
            print('BBox 이미지 비율에 따른 좌표:', labeled_bbox_points)

        if seg_points:
            labeled_seg_points = [(int(point[0] * x_ratio), int(point[1] * y_ratio)) for point in seg_points]
            print('Seg 원래 좌표:', seg_points)
            print('Seg 이미지 비율에 따른 좌표:', labeled_seg_points)

        # json으로 저장
        # # json형식 저장
        # data = {
        #     "data_seq": "data_sequence",
        #     "data_id": image_name,
        #     "path": image_path,
        #     "label": "object_label",
        #     "sub_labels": ["sub_label_1", "sub_label_2"],
        #     "position": [{"x": point[0], "y": point[1]} for point in labeled_points]
        # }
        #
        # # Save data as JSON
        # json_data = json.dumps(data, indent=4)
        # with open(f"{image_name}.json", "w") as file:
        #     file.write(json_data)
