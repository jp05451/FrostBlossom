import turtle
import math


class vector:
    def __init__(self, x=0, y=0, length=1, angle=0):
        self.x = x
        self.y = y
        self.angle = angle % 360
        self.length = length

    def getEnd(self):
        return self.x + self.length * math.cos(
            math.radians(self.angle)
        ), self.y + self.length * math.sin(math.radians(self.angle))

    def begin(self):
        return self.x, self.y

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 360

    def scale(self, scale):
        self.length *= scale

    def move(self, x, y):
        self.x += x
        self.y += y

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def setAngle(self, angle):
        self.angle = angle
        self.angle %= 360


class FrostBlossom:
    def __init__(self, level=3):
        self.screen = turtle.Screen()
        self.screen.bgcolor("white")
        self.screen.title("FrostBlossom")
        self.screen.setup(width=1920, height=1080)
        self.screen.tracer(0)
        self.pen = turtle.Turtle()
        self.pen.speed(1)

        self.level = level
        # self.rootCursor = (x,y)
        # self.length = length

    def drawVector(self, v: vector):
        self.pen.penup()
        self.pen.goto(v.begin())
        self.pen.pendown()
        self.pen.goto(v.getEnd())
        self.pen.penup()

    def drawLine(self, beginXY: tuple, targetXY: tuple):
        self.pen.penup()
        self.pen.goto(beginXY[0], beginXY[1])
        self.pen.pendown()
        self.pen.goto(targetXY[0], targetXY[1])
        self.pen.penup()

    def drawTree(self, beginCursor, angle, length, level):
        if level == self.level:
            return
        else:
            tempV = vector(beginCursor[0], beginCursor[1], length, angle)
            self.drawVector(tempV)
            endCursor = tempV.getEnd()

            self.drawTree(endCursor, angle + 60, length * 0.5, level +1)
            self.drawTree(endCursor, angle - 60, length * 0.5, level +1)


if __name__ == "__main__":
    F = FrostBlossom(3)

    for i in range(0,360,60):
        F.drawTree((0, 0), i, 200, 0)
    turtle.done()
