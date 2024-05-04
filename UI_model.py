
class MyModel:
    def __init__(self):
        self._data = []
        self.WeldingParameter = []
        self.WeldingSpeed = []
        

    def add_data(self, item):
        self._data.append(item)

    def add_WeldingParameter(self, item):
        self.WeldingParameter.append(item)

    def add_WeldingSpeed(self, item):
        self.WeldingSpeed.append(item)
    


    def get_data(self):
        return self._data
    
    def get_WeldingParameter(self):
        return self.WeldingParameter

    def get_WeldingSpeed(self):
        return self.WeldingSpeed