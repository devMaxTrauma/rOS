import pygame


class Pixel:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


screenWidth = 360
screenHeight = 360
startPoint = (320, 320)
degreeAfterEachRect = 1
initialDegree = 90
rectSizeAfterEachRect = 1.02
initialRectSize = 10
distanceFromStartPointAfterEachRect = 1.025
initialDistanceFromStartPoint = 10
rects = 130

screen = [[None for _ in range(screenWidth)] for _ in range(screenHeight)]
startColor = Pixel(0x80, 0xff, 0x00)
endColor = Pixel(0xfe, 0xfd, 0x48)
deltaRed = (endColor.r - startColor.r) / rects
deltaGreen = (endColor.g - startColor.g) / rects
deltaBlue = (endColor.b - startColor.b) / rects


# draw
def fill_rect(start_x, start_, w, h, rotate_angle, color):
    import math
    if w < 0 or h < 0:
        return
    if start_x < 0 or start_ < 0 or start_x >= screenWidth or start_ >= screenHeight:
        return
    if screen[start_x][start_] is None:
        screen[start_x][start_] = color

    local_red = screen[start_x][start_].r
    local_green = screen[start_x][start_].g
    local_blue = screen[start_x][start_].b
    new_red = (local_red + color.r) // 2
    new_green = (local_green + color.g) // 2
    new_blue = (local_blue + color.b) // 2
    color = Pixel(new_red, new_green, new_blue)

    if rotate_angle != 0:
        # rotate the rectangle
        rotate_angle = math.radians(rotate_angle)
        for i in range(h):
            for j in range(w):
                x1 = i * math.cos(rotate_angle) - j * math.sin(rotate_angle)
                y1 = i * math.sin(rotate_angle) + j * math.cos(rotate_angle)
                if 0 <= start_x + x1 < screenWidth and 0 <= start_ + y1 < screenHeight:
                    screen[start_x + int(x1)][start_ + int(y1)] = color
    else:
        for i in range(h):
            for j in range(w):
                if 0 <= start_x + i < screenWidth and 0 <= start_ + j < screenHeight:
                    screen[start_x + i][start_ + j] = color


for countRect in range(rects):
    rectColorRed = startColor.r + deltaRed * countRect
    rectColorGreen = startColor.g + deltaGreen * countRect
    rectColorBlue = startColor.b + deltaBlue * countRect
    rectColor = Pixel(rectColorRed, rectColorGreen, rectColorBlue)

    # draw like snail
    import math

    dFromSP = int(initialDistanceFromStartPoint * math.pow(distanceFromStartPointAfterEachRect, countRect))
    rectSize = int(initialRectSize * math.pow(rectSizeAfterEachRect, countRect))
    degree = initialDegree + degreeAfterEachRect * countRect
    x = startPoint[0] + dFromSP * math.cos(math.radians(degree))
    y = startPoint[1] + dFromSP * math.sin(math.radians(degree))
    fill_rect(int(x), int(y), rectSize, rectSize, degree, rectColor)

# display screen by pygame


pygame.init()
screenSize = 360
pygame_screen = pygame.display.set_mode((screenSize, screenSize))
pygame.display.set_caption("rOS Logo Painter")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for y in range(screenHeight):
        for x in range(screenWidth):
            if screen[y][x] is None:
                pygame_screen.set_at((x, y), (0, 0, 0))
            else:
                pygame_screen.set_at((x, y), (screen[y][x].r, screen[y][x].g, screen[y][x].b))
    pygame.display.flip()

# save screen
pygame.image.save(pygame_screen, "rOSLogo.png")
pygame.quit()
