import pygame
from pygame import draw
import math

screenWith = 1920 * 0.7
screenHigh = 1080 * 0.7


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
        self.drawIncreaseButton()
        self.drawDecreaseButton()



    def drawDecreaseButton(self):
        buttonWidth = 40
        buttonHigh = 20
        self.decreaseButton = pygame.Surface((40, 20))
        pygame.draw.rect(
            self.decreaseButton, (128, 128, 128), (0, 0, buttonWidth, buttonHigh)
        )
        pygame.draw.rect(
            self.decreaseButton, (255, 255, 255), (0, 0, buttonWidth, buttonHigh), 1
        )
        font = pygame.font.Font(None, 20)
        text = font.render("-", True, (0, 0, 0))
        text_rect = text.get_rect(center=(buttonWidth / 2, buttonHigh / 2))
        self.decreaseButton.blit(text, text_rect)

    def drawIncreaseButton(self):
        buttonWidth = 40
        buttonHigh = 20
        self.increaseButton = pygame.Surface((40, 20))
        pygame.draw.rect(
            self.increaseButton, (128, 128, 128), (0, 0, buttonWidth, buttonHigh)
        )
        pygame.draw.rect(
            self.increaseButton, (255, 255, 255), (0, 0, buttonWidth, buttonHigh), 1
        )
        font = pygame.font.Font(None, 20)
        text = font.render("+", True, (0, 0, 0))
        text_rect = text.get_rect(center=(buttonWidth / 2, buttonHigh / 2))
        self.increaseButton.blit(text, text_rect)

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
        print(f"level: {level}, {r, g, b}")
        self.penColor = (r, g, b)

    def drawFlower(self, centerCursor, width, radius, petalNum=6):
        tempV = vector(centerCursor[0], centerCursor[1], radius, 30)

        for i in range(petalNum):
            self.drawRing(tempV.getEnd(), width, radius / 2)
            tempV.rotate(360 / petalNum)

    def drawTree(self, beginCursor, angle, length, level):
        if level == self.level:
            return

        if level <= 4:
            self.changeColor(level)
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

    def placeAllItems(self):
        self.tree = pygame.transform.flip(self.tree, False, True)
        self.screen.blit(self.tree, (0, 0))

        # place increase button
        self.increaseButtonPositon = (60, self.high - 100)
        self.screen.blit(self.increaseButton, self.increaseButtonPositon)

        # place decrease button
        self.decreaseButtonPositon = (10, self.high - 100)
        self.screen.blit(self.decreaseButton, self.decreaseButtonPositon)
        pygame.display.update()

    def run(self):
        self.placeAllItems()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # increase button pressed
                    if (
                        self.increaseButtonPositon[0]
                        <= x
                        <= self.increaseButtonPositon[0] + 40
                        and self.increaseButtonPositon[1]
                        <= y
                        <= self.increaseButtonPositon[1] + 20
                    ):
                        self.level = (self.level + 1) % 8
                        self.tree.fill((0, 0, 0))
                        self.drawTree(
                            beginCursor=(screenWith / 2, screenHigh / 2),
                            angle=90,
                            length=200,
                            level=0,
                        )
                        self.placeAllItems()
                        
                    # decrease button pressed
                    if (
                        self.decreaseButtonPositon[0]
                        <= x
                        <= self.decreaseButtonPositon[0] + 40
                        and self.decreaseButtonPositon[1]
                        <= y
                        <= self.decreaseButtonPositon[1] + 20
                    ):
                        self.level = (self.level - 1) % 8
                        self.tree.fill((0, 0, 0))
                        self.drawTree(
                            beginCursor=(screenWith / 2, screenHigh / 2),
                            angle=90,
                            length=200,
                            level=0,
                        )
                        self.placeAllItems()


if __name__ == "__main__":
    F = FrostBlossom(5, screenWith, screenHigh)

    F.drawTree(
        beginCursor=(screenWith / 2, screenHigh / 2), angle=90, length=200, level=0
    )
    F.run()
