from model.DBManager import DBManager
from model import Label

class LabelController:
    def __init__(self, btn_controller):
        self.label = Label.Label(btn_controller)

    def label_window(self, data_seq):
        result = self.label.load_label(data_seq)
        label_seq = result
        return label_seq

    def on_selection(self, event, label_route, save_btn):
        listbox1 = event.widget
        if listbox1.curselection():
            selected_label = listbox1.get(listbox1.curselection())
            # 선택한 라벨 경로 표시 및 동일한 깊이인지 확인
            depth_result = self.label.update_label(label_route, selected_label)
            # 선택한 라벨 이름에 대한 라벨 seq 찾기
            self.db = DBManager()
            self.selected_label_seq = self.label.query_database('select', ['LABEL_SEQ'], 'BCANT_LABEL_TB', ['LABEL_NM'], [selected_label[0]])
            # selected_label_seq 값을 UPPER_LABEL 값으로 가지는 하위라벨이 있는지 확인하여 리스트로 가져오기
            low_label = self.label.load_low_label(self.selected_label_seq[0])
            # listbox 요소를 하위 요소 라벨 값으로 변경
            self.label.update_listbox(low_label, listbox1, save_btn, depth_result)

    def delete_select_label(self, label_route, listbox1, save_btn):
        self.label.delete_select_label(label_route, listbox1, save_btn)

    def temporary_save(self, close, temporary_save_listbox):
        self.label.temporary_save(close, temporary_save_listbox)

    def list_view(self, temporary_save_listbox, loader):
        self.label.status_view(temporary_save_listbox, loader)

    def list_delete(self, temporary_save_listbox):
        self.label.status_delete(temporary_save_listbox)

    def list_delete_all(self, temporary_save_listbox):
        self.label.status_delete_all(temporary_save_listbox)

    def list_save_all(self, get_data_seq, listbox_values, temporary_save_listbox):
        self.label.label_save(get_data_seq, listbox_values, temporary_save_listbox)