# import pygame
# from pygame.locals import QUIT

import turtle
import math


class FrostBlossom:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("white")
        self.screen.title("FrostBlossom")
        self.screen.setup(width=600, height=600)
        # self.screen.tracer(0)
        self.pen = turtle.Turtle()
        self.H = 20

    def calculateVector(self, beginXY, length, angle):
        """
        input begin cursor
        output cursor after move length with angle
        """
        x = length * math.cos(angle) + beginXY[0]
        y = length * math.sin(angle) + beginXY[1]
        return x, y

    def scaleVector(self, beginXY, targetXY, scale):
        # input xy cursor
        # output xy cursor after rescale
        x = beginXY[0] + (targetXY[0] - beginXY[0]) * scale
        y = beginXY[1] + (targetXY[1] - beginXY[1]) * scale
        return x, y

    def vectorRotate(self, centerXY: tuple, rotateXY: tuple, angle: float) -> tuple:
        x = rotateXY[0] - centerXY[0]
        y = rotateXY[1] - centerXY[1]
        x1 = x * math.cos(angle) - y * math.sin(angle) + centerXY[0]
        y1 = x * math.sin(angle) + y * math.cos(angle) + centerXY[1]
        return x1, y1

    def drawLine(self, beginXY: tuple, targetXY: tuple):
        self.pen.penup()
        self.pen.goto(beginXY)
        self.pen.pendown()
        self.pen.goto(targetXY)
        self.pen.penup()

    def drawTree(self, beginCursor, beginAngle, length, level):
        if level == 0:
            return
        else:
            x, y = self.calculateVector(beginCursor, beginAngle, 1)


if __name__ == "__main__":
    F = FrostBlossom()
    x, y = (100, 0)
    F.drawTree((0, 0), (x, y))
    x, y = F.vectorRotate((0, 0), (x, y), 50)
    F.drawTree((0, 0), (x, y))
    x, y = F.vectorRotate((0, 0), (x, y), 50)
    F.drawTree((0, 0), (x, y))
    turtle.done()
