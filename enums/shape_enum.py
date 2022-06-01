from enum import Enum


class shapeEnum(Enum):
    CIRCLE = ('원형', 1)
    ELLIPSE = ('타원형', 2)
    TRIANGLE = ('삼각형', 4)
    SQUARE = ('사각형', 5)
    PENTAGON = ('오각형', 8)
    HEXAGON = ('육각형', 9)
    OCTAGON = ('팔각형', 10)

    def __init__(self, shape_name, code):
        self.shape_name = shape_name
        self.code = code
