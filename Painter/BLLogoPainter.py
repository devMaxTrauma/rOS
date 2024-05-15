import pygame


class Pixel:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


screenWidth = 360
screenHeight = 360
startPoint = (30, 30)
screen = [[Pixel(0, 0, 0) for _ in range(screenWidth)] for _ in range(screenHeight)]
startColor = Pixel(0x80, 0xff, 0x00)
endColor = Pixel(0xfe, 0xfd, 0x48)
deltaRed = (endColor.r - startColor.r) / 30
deltaGreen = (endColor.g - startColor.g) / 30
deltaBlue = (endColor.b - startColor.b) / 30

# draw
for z in range(30):
    for y in range(30 + z * 4):
        for x in range(30 + z * 4):
            # mix previous color
            localRed = screen[z * 5 + startPoint[1] + y][z * 5 + startPoint[0] + x].r
            localGreen = screen[z * 5 + startPoint[1] + y][z * 5 + startPoint[0] + x].g
            localBlue = screen[z * 5 + startPoint[1] + y][z * 5 + startPoint[0] + x].b
            newRed = int(startColor.r + deltaRed * z)
            newGreen = int(startColor.g + deltaGreen * z)
            newBlue = int(startColor.b + deltaBlue * z)
            screen[z * 5 + startPoint[1] + y][z * 5 + startPoint[0] + x] = Pixel((localRed + newRed) // 2,
                                                                                 (localGreen + newGreen) // 2,
                                                                                 (localBlue + newBlue) // 2)

# display screen by pygame


pygame.init()
screenSize = 360
pygame_screen = pygame.display.set_mode((screenSize, screenSize))
pygame.display.set_caption("BL Logo Painter")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for y in range(screenHeight):
        for x in range(screenWidth):
            pygame_screen.set_at((x, y), (screen[y][x].r, screen[y][x].g, screen[y][x].b))
    pygame.display.flip()

# save screen
pygame.image.save(pygame_screen, "BLLogo.png")
pygame.quit()
