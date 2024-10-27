import pygame
from pygame import draw
from vector import vector

screenWith = 1920
screenHigh = 1080


class FrostBlossom:
    def __init__(self, level=3, width=1920, high=1080):
        self.level = level
        self.penColor = (55, 155, 255)
        self.maxLevel = 9
        self.centerCursor = (width / 2, high / 2)

        pygame.init()
        pygame.display.set_caption("FrostBlossom")
        self.high = high
        self.width = width
        self.screen = pygame.display.set_mode((width, high))

        self.tree = pygame.Surface((width, high), pygame.SRCALPHA)
        self.star = pygame.Surface((width, high), pygame.SRCALPHA)

        self.drawIncreaseButton()
        self.drawDecreaseButton()
        self.levelDisplayBar()

    def levelDisplayBar(self):
        self.levelBar = pygame.Surface((90, 20))
        pygame.draw.rect(self.levelBar, (255, 255, 255), (0, 0, 90, 20))
        pygame.draw.rect(self.decreaseButton, (128, 128, 128), (0, 0, 90, 20), 1)
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.level), True, (0, 0, 0))
        text_rect = text.get_rect(center=(90 / 2, 20 / 2))
        self.levelBar.blit(text, text_rect)

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

    def drawStar(self, centerCursor, radius=100):
        color = (255, 255, 0)
        points = []
        v = vector(centerCursor[0], centerCursor[1], radius, 270)
        for i in range(5):
            x, y = v.getEnd()
            points.append((x, y))

            v.rotate(36)
            v.scale(0.5)
            x, y = v.getEnd()
            points.append((x, y))

            v.rotate(36)
            v.scale(2)

        pygame.draw.polygon(self.star, color, points)

    def drawStars(self, centerCursor, radius=100):
        self.star = pygame.surface.Surface((self.width, self.high), pygame.SRCALPHA)
        self.drawStar(centerCursor, radius)
        v = vector(centerCursor[0], centerCursor[1], radius * 0.7, 90)
        for i in range(5):
            self.drawStar(v.getEnd(), radius * 0.1)
            v.rotate(72)

    def drawForrest(self):
        if self.level == 8:
            self.drawStars((self.width // 2, self.high // 2), 100)
            v = vector(self.width // 2, self.high // 2, 100, 90)
            for i in range(6):
                beginCursor = v.getEnd()
                self.drawTree(beginCursor, 90 + i * 60, 200, 0)
                v.rotate(60)
        else:
            for i in range(6):
                self.drawTree((self.width // 2, self.high // 2), 90 + i * 60, 200, 0)

    def emptyScreen(self):
        self.tree.fill((0, 0, 0))
        self.star.fill((0, 0, 0, 0))

    def placeAllItems(self):
        self.tree = pygame.transform.flip(self.tree, False, True)
        self.screen.blit(self.tree, (0, 0))
        self.screen.blit(self.star, (0, 0))

        # place increase button
        self.increaseButtonPositon = (60, self.high - 100)
        self.screen.blit(self.increaseButton, self.increaseButtonPositon)

        # place decrease button
        self.decreaseButtonPositon = (10, self.high - 100)
        self.screen.blit(self.decreaseButton, self.decreaseButtonPositon)

        # place level bar
        self.screen.blit(
            self.levelBar,
            (self.decreaseButtonPositon[0], self.decreaseButtonPositon[1] - 30),
        )

        pygame.display.update()

    def run(self):
        self.drawForrest()
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
                        self.level = (self.level + 1) % self.maxLevel
                        self.emptyScreen()  # clear screen
                        self.levelDisplayBar()
                        self.drawForrest()
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
                        self.level = (self.level - 1) % self.maxLevel
                        self.emptyScreen()  # clear screen
                        self.levelDisplayBar()
                        self.drawForrest()
                        self.placeAllItems()


if __name__ == "__main__":
    F = FrostBlossom(5, screenWith, screenHigh)

    # F.drawTree(
    #     beginCursor=(screenWith / 2, screenHigh / 2), angle=90, length=200, level=0
    # )
    F.run()
