from enum import Enum


class colorEnum(Enum):
    WHITE = ('하양', 16384)
    YELLOW = ('노랑', 8)
    ORANGE = ('주황', 512)
    PINK = ('분홍', 32)
    RED = ('빨강', 64)
    BROWN = ('갈색', 1)
    GREEN = ('초록', 2048)
    TURQUOISE = ('청록', 2048)
    BLUE = ('파랑', 8196)
    PURPLE = ('보라', 16)
    GRAY = ('회색', 32768)

    def __init__(self, color_name, code):
        self.color_name = color_name
        self.code = code
