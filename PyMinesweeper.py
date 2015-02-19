import sys
import math
import random
import pygame

MINE_CELL = -1

HIDDEN_CELL = -42
VISIBLE_CELL = -1337
MARKED_CELL = -9001

def Start():
    pygame.init()

    clock = pygame.time.Clock()
    done = False
    lost = False
    won = False

    fieldWidth = int(raw_input("Field width: "))
    fieldHeight = int(raw_input("Field height: "))
    mineCount = 0
    while True:
        mineCount = int(raw_input("Mine count: "))
        if mineCount < fieldWidth * fieldHeight: break
    
    field = BuildField(fieldWidth, fieldHeight, mineCount)
    visibility = [[HIDDEN_CELL for i in range(fieldWidth)] for j in range(fieldHeight)]
    
    CheckAdjMines(field)
    cellSize = 20

    marked = 0
    
    screenWidth = len(field[0]) * cellSize
    screenHeight = len(field) * cellSize

    screen = pygame.display.set_mode((screenWidth, screenHeight))
    font = pygame.font.SysFont("monospace", 16)

    while not done:
        pos = (-1, -1)
        button = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos
                pos = (int(math.floor(pos[0] / cellSize)), pos[1])
                pos = (pos[0], int(math.floor(pos[1] / cellSize)))
                if pos[0] >= fieldWidth: pos = (fieldWidth - 1, pos[1])
                if pos[1] >= fieldHeight: pos = (pos[0], fieldHeight - 1)
                button = event.button

        #Flagging toggle, kun flagged mineCountin verran ja loput visible nii win

        if not lost and not won:
            if pos[0] > -1 and pos[1] > -1:
                if button == 1: #left-click
                    if visibility[pos[1]][pos[0]] == HIDDEN_CELL:
                        if field[pos[1]][pos[0]] == MINE_CELL:
                            visibility[pos[1]][pos[0]] = VISIBLE_CELL
                            lost = True
                            print "You lost..."
                        elif field[pos[1]][pos[0]] >= 0:
                            visibility[pos[1]][pos[0]] = VISIBLE_CELL
                            ShowField(field, visibility, pos[0], pos[1])
                elif button == 3: #right-click
                    if visibility[pos[1]][pos[0]] == HIDDEN_CELL and marked < mineCount:
                        visibility[pos[1]][pos[0]] = MARKED_CELL
                        marked += 1
                    elif visibility[pos[1]][pos[0]] == MARKED_CELL:
                        visibility[pos[1]][pos[0]] = HIDDEN_CELL
                        marked -= 1

        #Voitto, kun kaikki paitsi minet visible
        if not won and not lost:
            hiddenCount = 0
            quitEarly = False
            for x in range(0, len(field[0])):
                for y in range(0, len(field)):
                    if visibility[y][x] == HIDDEN_CELL or visibility[y][x] == MARKED_CELL:
                        hiddenCount += 1
                    if hiddenCount > mineCount:
                        quitEarly = True
                        break
                if quitEarly: break
            if hiddenCount == mineCount: won = True

        #Voitto, kun right-clickattu kaikki minet
        #if marked == mineCount and not won:
        #    quitEarly = False
        #    for x in range(0, len(field[0])):
        #        for y in range(0, len(field)):
        #            if visibility[y][x] == HIDDEN_CELL:
        #                quitEarly = True
        #                break
        #        if quitEarly: break
        #        if x == len(field[0]) - 1:
        #            won = True
        #            print "YOU WIN!"
        
        DrawField(screen, font, field, visibility, cellSize)

        if won:
            text = font.render("YOU WIN!", 1, (255, 255, 255))
            screen.blit(text, (screenWidth / 2 - text.get_width() / 2, screenHeight / 2 - text.get_height() / 2))
        if lost:
            text = font.render("You lost...", 1, (255, 255, 255))
            screen.blit(text, (screenWidth / 2 - text.get_width() / 2, screenHeight / 2 - text.get_height() / 2))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]: done = True

        if done:
            pygame.quit()
            sys.exit(1)
        else:
            pygame.display.flip()
        
        clock.tick(60)


def BuildField(fieldWidth, fieldHeight, mineCount):
    field = [[0 for i in range(fieldWidth)] for j in range(fieldHeight)]
    
    x = random.randint(0, fieldWidth - 1)
    y = random.randint(0, fieldHeight - 1)
    for i in range(0, mineCount):
        while field[y][x] == MINE_CELL:
            x = random.randint(0, fieldWidth - 1)
            y = random.randint(0, fieldHeight - 1)
        field[y][x] = MINE_CELL

    return field


def CheckAdjMines(field):
    for x in range(0, len(field[0])):
        for y in range(0, len(field)):
            if field[y][x] != MINE_CELL:
                #ylävasen
                if y > 0 and x > 0:
                    if field[y-1][x-1] == MINE_CELL: field[y][x] += 1
                #ylä
                if y > 0:
                    if field[y-1][x] == MINE_CELL: field[y][x] += 1
                #yläoikea
                if y > 0 and x < len(field[0]) - 1:
                    if field[y-1][x+1] == MINE_CELL: field[y][x] += 1
                #vasen
                if x > 0:
                    if field[y][x-1] == MINE_CELL: field[y][x] += 1
                #oikea
                if x < len(field[0]) - 1:
                    if field[y][x+1] == MINE_CELL: field[y][x] += 1
                #alavasen
                if x > 0 and y < len(field) - 1:
                    if field[y+1][x-1] == MINE_CELL: field[y][x] += 1
                #ala
                if y < len(field) - 1:
                    if field[y+1][x] == MINE_CELL: field[y][x] += 1
                #alaoikea
                if x < len(field[0]) - 1 and y < len(field) - 1:
                    if field[y+1][x+1] == MINE_CELL: field[y][x] += 1


def ShowField(field, visibility, x, y):
    if field[y][x] > 0:
        return
    
    #ylävasen
    if y > 0 and x > 0:
        if field[y-1][x-1] != MINE_CELL and visibility[y-1][x-1] == HIDDEN_CELL:
            visibility[y-1][x-1] = VISIBLE_CELL
            ShowField(field, visibility, x-1, y-1)
    #ylä
    if y > 0:
        if field[y-1][x] != MINE_CELL and visibility[y-1][x] == HIDDEN_CELL:
            visibility[y-1][x] = VISIBLE_CELL
            ShowField(field, visibility, x, y-1)
    #yläoikea
    if y > 0 and x < len(field[0]) - 1:
        if field[y-1][x+1] != MINE_CELL and visibility[y-1][x+1] == HIDDEN_CELL:
            visibility[y-1][x+1] = VISIBLE_CELL
            ShowField(field, visibility, x+1, y-1)
    #vasen
    if x > 0:
        if field[y][x-1] != MINE_CELL and visibility[y][x-1] == HIDDEN_CELL:
            visibility[y][x-1] = VISIBLE_CELL
            ShowField(field, visibility, x-1, y)
    #oikea
    if x < len(field[0]) - 1:
        if field[y][x+1] != MINE_CELL and visibility[y][x+1] == HIDDEN_CELL:
            visibility[y][x+1] = VISIBLE_CELL
            ShowField(field, visibility, x+1, y)
    #alavasen
    if x > 0 and y < len(field) - 1:
        if field[y+1][x-1] != MINE_CELL and visibility[y+1][x-1] == HIDDEN_CELL:
            visibility[y+1][x-1] = VISIBLE_CELL
            ShowField(field, visibility, x-1, y+1)
    #ala
    if y < len(field) - 1:
        if field[y+1][x] != MINE_CELL and visibility[y+1][x] == HIDDEN_CELL:
            visibility[y+1][x] = VISIBLE_CELL
            ShowField(field, visibility, x, y+1)
    #alaoikea
    if x < len(field[0]) - 1 and y < len(field) - 1:
        if field[y+1][x+1] != MINE_CELL and visibility[y+1][x+1] == HIDDEN_CELL:
            visibility[y+1][x+1] = VISIBLE_CELL
            ShowField(field, visibility, x+1, y+1)
    return


def DrawField(screen, font, field, visibility, cellSize):
    for x in range(0, len(field[0])):
        for y in range(0, len(field)):
            if visibility[y][x] == VISIBLE_CELL:
                if field[y][x] == MINE_CELL:
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize), 0)
                elif field[y][x] == 0:
                    pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize), 0)
                elif field[y][x] > 0:
                    pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize), 0)
                    text = font.render(str(field[y][x]), 1, (255, 255, 255))
                    screen.blit(text, (x * cellSize + 6, y * cellSize + 0))
            elif visibility[y][x] == HIDDEN_CELL:
                pygame.draw.rect(screen, (64, 64, 64), pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize), 0)
                pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize), 1)
            elif visibility[y][x] == MARKED_CELL:
                pygame.draw.rect(screen, (128, 0, 0), pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize), 0)
                pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize), 1)

    return
