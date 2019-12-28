#cantsleep
import pygame
from pygame.rect import Rect
from pygame.locals import *

import sys
from random import randint

pygame.init()

"""
minesweeper.py

im thinking 16 by 16 with a 1 pxl boarder
keeping it simple, drawn red for mine, dark for flag

will be similar to game of life in structure

loose todo list
---------------
[] scoreboard
[] mouse functionality
[] mine counter / HUD
[] mainloop (new game menu, etc)
[] scrolling / zoom
"""

PW = 16
W, H = 32, 32
D = 5 #DENSITY
FNT = pygame.font.SysFont("Helvetica", PW-2)

#COLORS
CMINE = (255, 100, 100)
C_LIT = (200, 200, 200) #i promise this was an accident
CDARK = (100, 100, 100)
CFLAG = (210, 100, 160)
def get_mines(Density=D):
    mines = set()
    while len(mines) <= (W * H) / Density:
        mines.add((randint(0, W-1), randint(0, H-1)))
    return mines

def nbrs(x, y, mines): return sum([True if (x+i, y+j) in mines else False for i in range(-1, 2) for j in range(-1, 2)])

def drawn(mines, flags, revealed):
    surf = pygame.Surface((W * PW, H * PW))
    for x in range(W):
        for y in range(H):
            n = nbrs(x, y, mines)
            if (x, y) in mines and (x, y) in revealed:
                pygame.draw.rect(surf, CMINE, Rect(((x * PW) + 1, (y * PW) + 1), (PW-2, PW-2)))
            elif (x, y) in revealed:
                pygame.draw.rect(surf, C_LIT, Rect(((x * PW) + 1, (y * PW) + 1), (PW-2, PW-2)))
                if n: surf.blit(FNT.render(str(n), 0, (0, 0, 0)), ((x * PW) + 1, (y * PW) - 1))
            elif (x, y) in flags:
                pygame.draw.rect(surf, CFLAG, Rect(((x * PW) + 1, (y * PW) + 1), (PW-2, PW-2)))
            else:
                pygame.draw.rect(surf, CDARK, Rect(((x * PW) + 1, (y * PW) + 1), (PW-2, PW-2)))
    return surf

def clear_riegon(x, y, mines, revealed):
    checklist = [(x, y)]
    checked = []
    while checklist:
        X, Y = checklist.pop()
        revealed.add((X, Y))
        checked.append((X, Y))
        if nbrs(X, Y, mines) == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if W < X or X < 0 or H < Y or Y < 0: continue
                    if (X+i, Y+j) != (X, Y) and (X+i, Y+j) not in checklist and (X+i, Y+j) not in checked:
                        checklist.append((X+i, Y+j))

if __name__ == "__main__":
    if '-f' in sys.argv:     SCREEN = pygame.display.set_mode((PW * W, PW * H), FULLSCREEN)
    else: SCREEN = pygame.display.set_mode((PW * W, PW * H))

    pygame.display.set_caption("Minesweeping")

    mines = set()
    flags = set()
    revealed = set()
    x, y = W//2, H//2
    while (mines != flags or not mines) and len([x for x in filter(lambda n: n in revealed, mines)]) == 0:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
            if e.type == KEYDOWN:
                if e.key == K_LEFT: x -= 1
                if e.key == K_RIGHT: x += 1
                if e.key == K_UP: y -= 1
                if e.key == K_DOWN: y += 1

            if e.type == KEYDOWN:
                if e.key == K_SPACE and (x, y) not in flags:
                    if len(mines) == 0:
                        mines = get_mines()
                        while nbrs(x, y, mines) != 0:
                            mines = get_mines()
                    revealed.add((x, y))
                    if nbrs(x, y, mines) == 0: clear_riegon(x, y, mines, revealed)
                if e.key == K_z:
                    if (x, y) in flags: flags.remove((x, y))
                    else: flags.add((x, y))
        SCREEN.blit(drawn(mines, flags, revealed), (0, 0))
        pygame.draw.line(SCREEN, (255, 0, 0), (x*PW, y*PW), ((x+1)*PW, (y+1)*PW))
        pygame.draw.line(SCREEN, (255, 0, 0), (x*PW, (y+1)*PW), ((x+1)*PW, y*PW))
        pygame.display.update()
