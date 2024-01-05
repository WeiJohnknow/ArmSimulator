import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QTableWidget, QTableWidgetItem, QLabel,  QPushButton, QMessageBox, QDialog, QTextBrowser, QLineEdit
from PyQt5.QtCore import Qt



class RobotControl(QWidget):
    def __init__(self):
        super().__init__()
        self.nowPos = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
        self.IOdata = "ON"
        self.initUI()
        

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('RobotControl yaskawa MA1440')

        # Create a QVBoxLayout
        layout = QVBoxLayout(self)

        # Add a checkbox with ServoPower
        checkbox = QCheckBox('Servo Power', self)
        checkbox.stateChanged.connect(self.ServoPower)
        layout.addWidget(checkbox)

        # Add a checkbox with ARC
        checkbox = QCheckBox('Arc license', self)
        checkbox.stateChanged.connect(self.Arclicense)
        layout.addWidget(checkbox)

        # Add a checkbox with Sendwire
        checkbox = QCheckBox('send wire license', self)
        checkbox.stateChanged.connect(self.sendWirelicense)
        layout.addWidget(checkbox)

        # Add a QLabel to display the value of the mode variable
        self.Position_label = QLabel(self)
        self.Position_label.setText("Now Position: ")
        layout.addWidget(self.Position_label)

        # Add a button to show variable information
        show_pos_info_button = QPushButton('Read now position', self)
        show_pos_info_button.clicked.connect(self.showNowPositionInfo)
        layout.addWidget(show_pos_info_button)

        # Add a QLineEdit for user input
        self.input_text = QLineEdit(self)
        layout.addWidget(self.input_text)

    
        # Add a QLabel to display the entered text
        self.entered_text_label = QLabel(self)
        layout.addWidget(self.entered_text_label)

        # Add a button to display the entered text
        show_IO_info_button = QPushButton('Read I/O', self)
        show_IO_info_button.clicked.connect(self.showIOInfo)
        layout.addWidget(show_IO_info_button)



        # Add a table widget
        self.table = QTableWidget(self)
        self.table.setRowCount(6)
        self.table.setColumnCount(5)
        layout.addWidget(self.table)
        # 偵測表格的變化
        self.table.cellChanged.connect(self.readTablevlue)

    def ServoPower(self, state):
        # Slot method to handle checkbox state changes
        if state == Qt.Checked:
            print('Servo ON')
        else:
            print('Servo OFF')
        
    def Arclicense(self, state):
        # Slot method to handle checkbox state changes
        if state == Qt.Checked:
            print('Arc ON')
        else:
            print('Arc OFF')

    def sendWirelicense(self, state):
        # Slot method to handle checkbox state changes
        if state == Qt.Checked:
            print('send wire')
        else:
            print('stop send wire')

    def readTablevlue(self, row, col):
        # 讀取表格的值
        item = self.table.item(row, col)
        if item:
            print(f'[{row}, {col}]: {item.text()}')
        else:
            print(f'Cell at Row {row }, Col {col } is now empty')
        
    def showNowPositionInfo(self):
        # 顯示現在位置
        self.Position_label.setText(f"Now Position: {self.nowPos}")

    def showIOInfo(self):
        # Method to display the entered text in a QLabel
        entered_text = self.input_text.text()
        self.entered_text_label.setText(f'Pin No: {entered_text}, status: {self.IOdata}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotControl()
    window.show()
    sys.exit(app.exec_())