import pygame, sys
from pygame.locals import *

window_size = (1000, 500)
clock = pygame.time.Clock()
FPS = 60
mousepos = None


screen = pygame.display.set_mode(window_size)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

boxes = []
def setupField():
    gap = 700 #Lücke zwischen den beiden spielfeldseiten
    for i in range(4):
        boxes.append([100 + 100 * i, 100, 99, 99])
    for i in range(2):
        boxes.append([gap + 100 * i, 100, 99, 99])
    for i in range(8):
        boxes.append([100+100*i, 200, 99, 99])
    for i in range(4):
        boxes.append([100 + 100 * i, 300, 99, 99])
    for i in range(2):
        boxes.append([gap + 100 * i, 300, 99, 99])

setupField()
while 1:

    screen.fill(WHITE)  #White Background

    events = pygame.event.get()

    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            mousepos = [event.pos[0], event.pos[1], 100, 100]
            boxes.append(mousepos)



    for box in boxes:
        pygame.draw.rect(screen, BLACK, box, 1)

    pygame.display.update()
    clock.tick(FPS)