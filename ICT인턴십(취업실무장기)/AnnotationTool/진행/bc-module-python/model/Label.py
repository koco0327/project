from model import DBManager, Load
import tkinter as tk
from tkinter import messagebox
import json
import os


class Label:
    def __init__(self, btn_controller):
        self.btn_controller = btn_controller
        self.canvas = btn_controller.canvas
        self.with_label_btns = self.btn_controller.with_label_btns

        self.db = DBManager.DBManager()
        self.save_select = {'label_depth': 0, 'label_nm': []}

    # DB 쿼리, 결과 반환
    def query_database(self, query_type, columns, table, conditions, values):
        result = self.db.query_db(query_type=query_type, columns=columns, table=table, conditions=conditions,
                                  values=values)
        return result if len(result) > 0 else []

        # 라벨에 대한 데이터 불러오기 (worker 페이지 data_id 표기 / 업로드 기능과 병합 후 수정 예정)

    def load_label(self, data_seq):
        self.save_select['label_depth'] = 1
        # 데이터 seq에 따른 프로젝트 seq 찾기
        self.prj_seq = self.query_database('select', ['PRJ_SEQ'], 'BCANT_WDATA_TB', ['DATA_SEQ'], [data_seq])
        # 프로젝트 seq에 따른 라벨 이름 찾기
        self.label_nm = self.query_database('select', ['LABEL_NM'], 'BCANT_LABEL_TB', ['PRJ_SEQ', 'LABEL_DEPTH'],
                                            [self.prj_seq[0][0], self.save_select['label_depth']])
        return self.label_nm

        # 라벨 seq에 대한 하위 라벨 nm 값 가져오기

    def load_low_label(self, label_seq):
        self.low_label_nm = self.query_database('select', ['LABEL_NM'], 'BCANT_LABEL_TB',
                                                ['UPPER_LABEL', 'LABEL_DEPTH'],
                                                [label_seq[0], self.save_select['label_depth'] + 1])
        return self.low_label_nm

        # 현재 선택한 라벨 값 저장

    def save_select_label(self):
        # 깊이 값, 라벨 이름 저장
        self.save_select_label_dict = {'label_depth': 0, 'label_nm': []}
        return self.save_select_label_dict

        # 하위 라벨에 대한 리스트 박스 요소 업데이트

    def update_listbox(self, low_label, listbox1, save_btn, depth_result):
        if depth_result: self.save_select['label_depth'] += 1
        # if 문에서 값이 존재하면 리스트 요소 업데이트 / 없으면 아무 동작x
        if len(low_label) == 0:
            save_btn.configure(state=tk.NORMAL)  # 버튼 활성화
        else:
            # listbox1 요소 업데이트
            listbox1.delete(0, tk.END)
            # listbox1.config(selectmode=tk.MULTIPLE)
            for item in low_label:
                listbox1.insert(tk.END, item)

        # 선택한 라벨 값 표시

    def update_label(self, label_route, selected_label):
        # 선택한 라벨의 깊이 찾기
        select_label_depth = self.query_database('select', ['LABEL_DEPTH'], 'BCANT_LABEL_TB', ['LABEL_NM'],
                                                 [selected_label[0]])
        # 선택한 라벨의 깊이와 현재 깊이가 같으면 전 라벨 nm을 pop 하는 코드 추가
        if select_label_depth[0][0] == str(self.save_select['label_depth'] - 1): self.save_select['label_nm'].pop()
        self.save_select['label_nm'].append(selected_label[0])
        save_select = ' + '.join(self.save_select['label_nm'])
        label_route.configure(text=save_select)

        return select_label_depth[0][0] != str(self.save_select['label_depth'] - 1)

        # 상위 라벨 찾기

    def load_high_label(self):
        # 깊이가 1이면 프로젝트 아이디로 불러오기 / 아니면 popped_item의 상위 라벨 찾기
        if self.save_select['label_depth'] == 1:
            # 라벨 이름에 대한 PRJ_SEQ 찾기
            high_label_seq = self.query_database('select', ['PRJ_SEQ'], 'BCANT_LABEL_TB', ['LABEL_NM'],
                                                 [self.popped_label_nm])
            # 깊이가 1인 PRJ_SEQ의 NM 가져오기
            high_label_nm = self.query_database('select', ['LABEL_NM'], 'BCANT_LABEL_TB', ['PRJ_SEQ', 'LABEL_DEPTH'],
                                                [high_label_seq[0][0], self.save_select['label_depth']])
        else:
            # 라벨 이름에 대한 UPPER_LABEL 찾기
            high_label_seq = self.query_database('select', ['UPPER_LABEL'], 'BCANT_LABEL_TB', ['LABEL_NM'],
                                                 [self.popped_label_nm])
            # UPPER_LABEL의 하위 LABEL 찾아서 NM 가져오기
            high_label_nm = self.query_database('select', ['LABEL_NM'], 'BCANT_LABEL_TB', ['UPPER_LABEL'],
                                                [high_label_seq[0][0]])
        return high_label_nm

        # 선택한 라벨 값 삭제 (이전 버튼 클릭시 이전 라벨로 돌아가기)

    def delete_select_label(self, label_route, listbox1, save_btn):
        # 버튼 숨기기
        if save_btn.cget('state') == tk.NORMAL:
            save_btn.configure(state=tk.DISABLED)
            save_btn.pack_forget()
        self.popped_label_nm = self.save_select['label_nm'].pop()
        save_select = ' + '.join(self.save_select['label_nm'])
        label_route.configure(text=save_select)

        self.save_select['label_depth'] -= 1

        high_label_list = self.load_high_label()

        # listbox 요소를 하위 요소 라벨 값으로 변경
        listbox1.delete(0, tk.END)
        # listbox1.config(selectmode=tk.MULTIPLE)
        for item in high_label_list:
            listbox1.insert(tk.END, item)

        # 작업현황 창에 임시저장 내용 띄우기

    def temporary_save(self, close, temporary_save_listbox):
        close
        if self.btn_controller.bbox_active == True:
            self.btn_controller.toggle_bbox()
        if self.btn_controller.seg_active == True:
            self.btn_controller.toggle_seg()

        temporary_save_listbox.insert(tk.END, ' > '.join(self.save_select['label_nm']))
        self.btn_controller.set_btns_state(self.with_label_btns, tk.NORMAL)

    # JSON에 자표값 및 라벨값 저장
    def label_save(self, get_data_seq, listbox_values, temporary_save_listbox):
        result = messagebox.askquestion("전체 저장", "리스트 목록을 전체 저장하시겠습니까?")
        if result == 'yes':
            # 작업현황 목록 삭제
            temporary_save_listbox.delete(0, tk.END)

            data_seq_list = []
            data_id_list = [str(get_data_seq)]
            path_list = ["0"]
            label_list = []
            sub_labels_list = []
            position_list = [
                [{"x": "x11", "y": "y11"}, {"x": "x12", "y": "y12"}]
            ]
            listbox_values_list = list(listbox_values)

            # 리스트박스의 항목 분리 및 저장
            for item in listbox_values_list:
                items = item.split(" > ")
                label_list.append(items[0])
                sub_labels_list.append(items[1:])

            # JSON 파일 생성
            for i in range(len(label_list)):
                # 현재 스크립트 파일의 경로
                script_directory = os.path.dirname(os.path.abspath(__file__))
                # json 폴더의 상대 경로 계산
                json_directory = os.path.join(script_directory, "..", "json")
                # json 폴더에 존재하는 파일 가져오기 (파일 개수 카운트를 통한 파일 이름 지정을 위해)
                existing_files = os.listdir(json_directory)
                # json 폴더의 기존 파일 개수 계산
                existing_file_count = sum(1 for file in existing_files if file.endswith(".json"))
                # 파일 이름을 "data_00000001.json", "data_00000002.json"와 같은 형식으로 생성
                file_index = existing_file_count + 1
                file_name = f"data_{str(file_index).zfill(8)}.json"
                # data_seq 지정
                data_seq = f"data_{str(file_index).zfill(8)}"
                data_seq_list.append(data_seq)

                data = {
                    "data_seq": data_seq,
                    "data_id": data_id_list[0],
                    "path": path_list[0],
                    "label": label_list[i],
                    "sub_labels": sub_labels_list[i],
                    "position": position_list[0]
                }
                # JSON 데이터를 문자열로 변환하고 들여쓰기 적용
                json_data = json.dumps(data, indent=4, ensure_ascii=False)

                file_path = os.path.join(json_directory, file_name)
                with open(file_path, "w", encoding='utf-8') as file:
                    file.write(json_data)

                from model.SFTPManager import SFTPClient
                sftpclient = SFTPClient()
                local_path = file_path
                remote_path = f'/home/bc/hdd/Annotation/json/{file_name}'
                sftpclient.upload_file(local_path, remote_path)

            self.canvas.delete("all")

    # 작업현황 항목 수정
    def status_update(self):
        None

    # 작업 현황 항목 삭제
    def status_delete(self, temporary_save_listbox):
        selected_item = temporary_save_listbox.curselection()
        if selected_item:
            temporary_save_listbox.delete(selected_item[0])
        if temporary_save_listbox.size() < 1:
            self.btn_controller.set_btns_state(self.with_label_btns, tk.DISABLED)


    # 작업현황 항목 전체 삭제
    def status_delete_all(self, temporary_save_listbox):
        result = messagebox.askquestion("전체 삭제", "리스트 목록을 전체 삭제하시겠습니까?")
        if result == 'yes':
            temporary_save_listbox.delete(0, tk.END)
            self.btn_controller.set_btns_state(self.with_label_btns, tk.DISABLED)

    # 작업현황 항목 보기
    def status_view(self, temporary_save_listbox, loader):
        selected_item = temporary_save_listbox.curselection()
        if selected_item:
            selected_value = temporary_save_listbox.get(selected_item[0])
            # 괄호 사이의 값 추출
            start_index = selected_value.find('(') + 1
            end_index = selected_value.find(')')
            selected_value_image_index = selected_value[start_index:end_index]
            # 이미지 불러오기
            loader.load_auto_list()

    # 작업현황 항목 전체보기
    def status_fullview(self):
        None
