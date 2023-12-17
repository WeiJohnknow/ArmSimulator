# 繼承
class A:
    def __init__(self, Type = "Cycle") -> None:
        self.carType = Type
        pass

class B(A):
    def __init__(self, Type, Size= 5) -> None:
        # 指定A Class繼承
        A.__init__(self, Type)
        # 自動調配父類繼承
        super().__init__(Type)

        self.carSize = Size
        print('Car', self.carSize, self.carType)

class Z(B):
    def __init__(self, Type, Size, color="red") -> None:
        super().__init__(Type, Size)

        self. carColor = "Green"
        print('Car', Type, Size, color)


if __name__ == '__main__':
    a = A
    b = B
    z = Z
    b("clc", 1)
    z("cube", 2, "yellow")
 




    