class MyModel:
    def __init__(self):
        self._data = []

    def add_data(self, item):
        self._data.append(item)

    def get_data(self):
        return self._data