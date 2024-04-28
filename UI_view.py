# view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QHBoxLayout

# view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QHBoxLayout

class MyView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MVC 範例')

        self.list_widget = QListWidget()

        # 第一組輸入框與按鈕
        self.input_box1 = QLineEdit()
        self.add_button1 = QPushButton('寫入走速(m/s)')

        # 第二組輸入框與按鈕
        self.input_box2_1 = QLineEdit()
        self.input_box2_2 = QLineEdit()
        self.add_button2 = QPushButton('寫入AC與AVP')

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        # 第一組輸入框與按鈕的水平佈局
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.input_box1)
        hbox1.addWidget(self.add_button1)

        # 第二組輸入框與按鈕的水平佈局
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.input_box2_1)
        hbox2.addWidget(self.input_box2_2)
        hbox2.addWidget(self.add_button2)

        layout.addLayout(hbox1)
        layout.addLayout(hbox2)

        self.setLayout(layout)

    def get_list_widget(self):
        return self.list_widget

    def get_add_button1(self):
        return self.add_button1

    def get_add_button2(self):
        return self.add_button2

    def get_input_text1(self):
        return self.input_box1.text()

    def get_input_text2_1(self):
        return self.input_box2_1.text()

    def get_input_text2_2(self):
        return self.input_box2_2.text()

    def clear_input_text(self):
        self.input_box1.clear()
        self.input_box2_1.clear()
        self.input_box2_2.clear()
    