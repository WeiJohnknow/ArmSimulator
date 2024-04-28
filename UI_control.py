# # controller.py
# from PyQt5.QtWidgets import QApplication
# import sys
# import time
# from UI_model import MyModel
# from UI_view import MyView

# class MyController:
#     def __init__(self, model, view):
#         self._model = model
#         self._view = view

#         self._view.get_add_button1().clicked.connect(self._add_item1)  # 連接第一組按鈕的點擊事件
#         self._view.get_add_button2().clicked.connect(self._add_item2)  # 連接第二組按鈕的點擊事件

#     def _add_item1(self):
#         new_item = self._view.get_input_text1()  # 取得第一組輸入框中的文字
#         if new_item:  # 確認輸入框不為空
#             self._model.add_data(new_item)
#             self._update_view()
#             self._view.clear_input_text()  # 清空輸入框
        
#             return new_item
#         return None

#     def _add_item2(self):
#         new_item1 = self._view.get_input_text2_1()  # 取得第二組第一個輸入框中的文字
#         new_item2 = self._view.get_input_text2_2()  # 取得第二組第二個輸入框中的文字
#         if new_item1 and new_item2:  # 確認兩個輸入框都不為空
#             combined_item = f"{new_item1}, {new_item2}"  # 將兩個輸入框的值結合起來
#             self._model.add_data(combined_item)
#             self._update_view()
#             self._view.clear_input_text()  # 清空輸入框

#     def _update_view(self):
#         self._view.get_list_widget().clear()
#         for item in self._model.get_data():
#             self._view.get_list_widget().addItem(item)

    

# def main():
#     app = QApplication(sys.argv)

#     model = MyModel()
#     view = MyView()
#     controller = MyController(model, view)


#     view.show()
#     sys.exit(app.exec_())
    

# if __name__ == '__main__':
#     main()

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
import sys
from UI_model import MyModel
from UI_view import MyView



class MyController:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._last_added_item_1st = None  # 上次剛寫入的數據
        self._last_added_item_2nd_1 = None  # 上次剛寫入的數據
        self._last_added_item_2nd_2 = None  # 上次剛寫入的數據

        
        self._view.get_add_button1().clicked.connect(self._add_item1)  # 連接第一組按鈕的點擊事件
        self._view.get_add_button2().clicked.connect(self._add_item2)  # 連接第二組按鈕的點擊事件

        self.timer = QTimer()  # 創建 QTimer
        self.timer.timeout.connect(self._get_latest_data)  # 連接 QTimer 的 timeout 信號到 _get_latest_data 方法
        self.timer.start(10)  # 每 1000 毫秒（1 秒）觸發一次 timeout 信號

    def _add_item1(self):
        new_item = self._view.get_input_text1()  # 取得第一組輸入框中的文字
        if new_item:  # 確認輸入框不為空
            self._model.add_data(new_item)
            self._last_added_item_1st = new_item  # 更新上次剛寫入的數據
            self._update_view()
            self._view.clear_input_text()  # 清空輸入框
            return new_item
        return None

    def _add_item2(self):
        new_item1 = self._view.get_input_text2_1()  # 取得第二組第一個輸入框中的文字
        new_item2 = self._view.get_input_text2_2()  # 取得第二組第二個輸入框中的文字
        if new_item1 and new_item2:  # 確認兩個輸入框都不為空
            combined_item = f"{new_item1}, {new_item2}"  # 將兩個輸入框的值結合起來

            self._model.add_data(combined_item)

            self._last_added_item_2nd_1 = new_item1  # 更新上次剛寫入的數據
            self._last_added_item_2nd_2 = new_item2

            self._update_view()
            self._view.clear_input_text()  # 清空輸入框

    def _update_view(self):
        self._view.get_list_widget().clear()
        for item in self._model.get_data():
            self._view.get_list_widget().addItem(item)
            

    def _get_latest_data(self):
        if self._last_added_item_1st is not None:
            print(f"銲接走速: {self._last_added_item_1st}")
            self._last_added_item_1st = None  # 重置上次剛寫入的數據為 None

        if self._last_added_item_2nd_1 is not None and self._last_added_item_2nd_2 is not None:
            print(f"銲接電流(AC): : {self._last_added_item_2nd_1}")
            print(f"銲接電流(AVP): : {self._last_added_item_2nd_2}")
            self._last_added_item_2nd_1 = None  # 重置上次剛寫入的數據為 None
            self._last_added_item_2nd_2 = None  # 重置上次剛寫入的數據為 None

def main():
    app = QApplication(sys.argv)

    model = MyModel()
    view = MyView()
    controller = MyController(model, view)

    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()