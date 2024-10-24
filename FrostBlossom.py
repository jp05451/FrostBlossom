import turtle
import math


class vector:
    def __init__(self, x=0, y=0, length=1, angle=0):
        self.x = x
        self.y = y
        self.angle = angle % 360
        self.length = length
        self.color = (55, 155, 255)

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
        self.screen.bgcolor("black")
        self.screen.title("FrostBlossom")
        self.screen.setup(width=1920, height=1080)
        self.screen.tracer(0)

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(1)
        self.pen.pencolor((55 / 255, 155 / 255, 255 / 255))

        self.level = level
        self.currentLevel = 0

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

    def drawRing(self, centerCursor, width, radius):
        color = self.pen.pencolor()

        self.pen.penup()
        self.pen.color((247 / 255, 202 / 255, 201 / 255))
        self.pen.goto(centerCursor[0], centerCursor[1] - radius)
        self.pen.width(width)
        self.pen.pendown()
        self.pen.circle(radius)
        self.pen.penup()

        self.pen.width(1)
        self.pen.color(color)

    def changeColor(self,level):

        r = min(55 + 40 * level, 255) / 255
        g = min(155 + 20 * level, 255) / 255
        b = 255 / 255
        # print(f"New color: R={r * 255}, G={g * 255}, B={b * 255}")
        self.pen.pencolor((r, g, b))

    def drawFlower(self, centerCursor, width, radius, petalNum=6):
        tempV = vector(centerCursor[0], centerCursor[1], radius, 30)
        self.pen.width(width)

        for i in range(petalNum):
            self.drawRing(tempV.getEnd(), width, radius / 2)
            tempV.rotate(360 / petalNum)

        self.pen.width(1)

    def drawTree(self, beginCursor, angle, length, level):
        if level == self.level:
            return

        if level <= 4:
            tempV = vector(beginCursor[0], beginCursor[1], length, angle)
            self.drawVector(tempV)
            endCursor = tempV.getEnd()

            self.changeColor(level)
            self.drawTree(endCursor, angle + 60, length * 0.5, level + 1)
            self.changeColor(level)
            self.drawTree(endCursor, angle - 60, length * 0.5, level + 1)

        if level == 5:
            self.drawRing(beginCursor, 5, 14)
            self.drawTree(beginCursor, angle, length, level + 1)

        if level == 6:
            self.drawFlower(beginCursor, 3, 14)
            self.drawTree(beginCursor, angle, length, level + 1)


if __name__ == "__main__":
    F = FrostBlossom(7)

    F.drawTree(beginCursor=(0, 0), angle=90, length=200, level=0)

    turtle.done()
