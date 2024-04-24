# controller.py
from PyQt5.QtWidgets import QApplication
import sys
from UI_model import MyModel
from UI_view import MyView

class MyController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._view.get_add_button().clicked.connect(self._add_item)

    def _add_item(self):
        new_item = self._view.get_input_text()  # 取得輸入框中的文字
        if new_item:  # 確認輸入框不為空
            self._model.add_data(new_item)
            self._update_view()
            self._view.clear_input_text()  # 清空輸入框

    def _update_view(self):
        self._view.get_list_widget().clear()
        for item in self._model.get_data():
            self._view.get_list_widget().addItem(item)

def main():
    app = QApplication(sys.argv)

    model = MyModel()
    view = MyView()
    controller = MyController(model, view)

    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()