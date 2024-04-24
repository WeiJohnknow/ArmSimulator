# view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit

class MyView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MVC 範例')

        self.list_widget = QListWidget()
        self.add_button = QPushButton('寫入')
        self.input_box = QLineEdit()  # 新增 QLineEdit 作為輸入框

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.input_box)  # 將輸入框加入布局
        layout.addWidget(self.add_button)
        self.setLayout(layout)

    def get_list_widget(self):
        return self.list_widget

    def get_add_button(self):
        return self.add_button

    def get_input_text(self):  # 取得輸入框的文字
        return self.input_box.text()

    def clear_input_text(self):  # 清空輸入框
        self.input_box.clear()
    