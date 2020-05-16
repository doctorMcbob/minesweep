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

mines will be stored as positions in a set

extra credit list
-----------------
[x] scoreboard
[x] mouse functionality
[x] mine counter / HUD
[] mainloop (new game menu, etc)
[] scrolling / zoom
"""

PW = 32
W, H = 20, 20
D = 5 #DENSITY
FNT = pygame.font.SysFont("Helvetica", PW-2)

#COLORS
CMINE = (255, 100, 100)
C_LIT = (200, 200, 200) #i promise this was an accident
CDARK = (100, 100, 100)
CFLAG = (210, 100, 160)
CMENU = (250, 250, 250)

mines = set()
flags = set()
revealed = set()

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

def clear_riegon(x, y, mines, revealed): # think about a recursive solution
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

def get_mouse_logical():
    pygame.display.update()
    x, y = pygame.mouse.get_pos()
    return x // PW, y // PW

def check_mine(pos):
    global mines, revealed
    x, y = pos
    if len(mines) == 0:
        mines = get_mines()
        while nbrs(x, y, mines) != 0:
            mines = get_mines()
    revealed.add((x, y))
    if nbrs(x, y, mines) == 0: clear_riegon(x, y, mines, revealed)

if __name__ == "__main__":
    if '-f' in sys.argv: SCREEN = pygame.display.set_mode((PW * W, PW * H + 32), FULLSCREEN)
    else: SCREEN = pygame.display.set_mode((PW * W, PW * H + 32))
    CLOCK = pygame.time.Clock()
    IGT = 0
    
    pygame.display.set_caption("Minesweeping")

    x, y = W//2, H//2
    while (mines != flags or not mines) and len([x for x in filter(lambda n: n in revealed, mines)]) == 0:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
            if e.type == KEYDOWN:
                if e.key == K_LEFT: x = max(x - 1, 0)
                if e.key == K_RIGHT: x = min(x + 1, W-1)
                if e.key == K_UP: y = max(y - 1, 0)
                if e.key == K_DOWN: y = min(y + 1, H-1)
                if e.key == K_SPACE and (x, y) not in flags: check_mine((x, y))
                if e.key == K_z and (x, y) not in revealed:
                    if (x, y) in flags: flags.remove((x, y))
                    else: flags.add((x, y))
            if e.type == MOUSEBUTTONDOWN and (x, y) not in flags:
                x, y = get_mouse_logical()
                check_mine(get_mouse_logical())
        SCREEN.blit(drawn(mines, flags, revealed), (0, 0))
        surf = pygame.Surface((W * PW, 32))
        surf.fill(CMENU)
        surf.blit(FNT.render("Mines: " + str(len(mines) - len(flags)), 0, (0, 0, 0)), (0, 0))
        SCREEN.blit(surf, (0, H * PW))
        pygame.draw.line(SCREEN, (255, 0, 0), (x*PW, y*PW), ((x+1)*PW, (y+1)*PW))
        pygame.draw.line(SCREEN, (255, 0, 0), (x*PW, (y+1)*PW), ((x+1)*PW, y*PW))
        pygame.display.update()
        IGT += CLOCK.tick()

pygame.quit()
strtime = lambda n: str(n // 60000) +":"+ ("0" + str(n // 1000 % 60))[-2:]
if mines == flags: name = input("name\n> ")

with open("halloffame.txt", "r") as f:
    halloffame = eval(f.read())

if mines == flags:
    for i, data in enumerate(halloffame):
        if data[1] > IGT:
            halloffame.insert(i, (name, IGT))
            break

print(" +##################+ ")
print("+### HALL OF FAME ###+")
print(" +##################+ ")
for NAME, TIME in halloffame:
    print(NAME[0:12] + (" " * (12 - len(NAME))) + "|" + (" " * 4) + strtime(TIME))

with open("halloffame.txt", "w") as f:
    f.write(repr(halloffame))
