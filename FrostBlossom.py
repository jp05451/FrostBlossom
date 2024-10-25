import pygame
from pygame import draw
import math

screenWith = 1920 * 0.8
screenHigh = 1080 * 0.8


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
    def __init__(self, level=3, width=1920, high=1080):
        self.level = level
        self.currentLevel = 0
        self.penColor = (55, 155, 255)

        pygame.init()
        pygame.display.set_caption("FrostBlossom")
        self.high = high
        self.width = width
        self.screen = pygame.display.set_mode((width, high))

        self.tree = pygame.Surface((width, high))

    # def drawButton(self, x, y, width=40, high=20):
    #     self.button.penup()
    #     self.button.pencolor("white")
    #     self.button.fillcolor("white")
    #     self.button.goto(x, y)
    #     self.button.pendown()
    #     self.button.begin_fill()
    #     self.button.goto(x + width, y)
    #     self.button.goto(x + width, y + high)
    #     self.button.goto(x, y + high)
    #     self.button.goto(x, y)
    #     self.button.end_fill()
    #     self.button.penup()

    #     # Draw button text
    #     self.button.goto(x + width / 2, y)
    #     self.button.pendown()
    #     self.button.pencolor("black")
    #     self.button.write("up", align="center", font=("Arial", 16, "normal"))
    #     self.button.penup()

    #     # # Define button click area
    #     self.screen.onclick(self.onButtonClick)

    # def onButtonClick(self, x, y):
    #     button_x, button_y = (
    #         -self.screen.window_width() / 2 + 100,
    #         -self.screen.window_height() / 2 + 100,
    #     )
    #     if button_x <= x <= button_x + 40 and button_y <= y <= button_y + 20:
    #         self.level = (self.level + 1) % 8
    #         print(f"Level: {self.level}")
    #         self.pen.clear()
    #         self.drawTree(beginCursor=(0, 0), angle=90, length=200, level=0)
    #         self.screen.update()

    def drawVector(self, v: vector):
        pygame.draw.line(self.tree, self.penColor, v.begin(), v.getEnd())

    def drawLine(self, beginXY: tuple, targetXY: tuple):
        pygame.draw.line(self.tree, self.penColor, beginXY, targetXY)

    def drawRing(self, centerCursor, width, radius):
        color = (247, 202, 201)
        pygame.draw.circle(self.tree, color, centerCursor, radius, width)

    def changeColor(self, level):
        r = min(55 + 40 * level, 255)
        g = min(155 + 20 * level, 255)
        b = 255
        self.penColor = (r, g, b)
        # self.pen.pencolor((r, g, b))

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

    def run(self):
        self.tree = pygame.transform.flip(self.tree, False, True)
        self.screen.blit(self.tree, (0, 0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


if __name__ == "__main__":
    F = FrostBlossom(5, screenWith, screenHigh)

    F.drawTree(
        beginCursor=(screenWith / 2, screenHigh / 2), angle=90, length=200, level=0
    )
    # F.drawTree(beginCursor=(0, 0), angle=90, length=200, level=0)

    F.run()
