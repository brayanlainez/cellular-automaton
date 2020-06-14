import sys
import pygame
import numpy as np
import time
import random

def draw():
    for x in range(0, nxC):
        for y in range(0, nyC):
            poly = [(int(x     * dimCW), int(y     * dimCH)),
                    (int((x+1) * dimCW), int(y     * dimCH)),
                    (int((x+1) * dimCW), int((y+1) * dimCH)),
                    (int(x     * dimCW), int((y+1) * dimCH))]
            # And draw the cell for each pair of x and y
            pygame.draw.polygon(screen, (128,150,128), poly, 1)
    pygame.display.update()
 
while True:
    pygame.init()
    size = width, height = 700, 700
    bg = 25,25,25 # Fondo de la pantalla
    nxC, nyC = 150, 150 # Número de celdas
    dimCW, dimCH = (width - 1) / nxC, (height -1) / nyC # Dimensiones de la celda
    pauseExecution = False # Control de la ejecición del juego
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    screen.fill(bg)

    # Estados de las celdas. Vivas = 1; Muertas = 0;
    gameState = np.zeros((nxC, nyC))
    gameState[int(nxC / 2), 0] = 1
    ruleRandom = np.random.randint(256) # 256 = reglas posibles
    print("Rule: %d" % (ruleRandom))
    listRules = (ruleRandom, 30, 77, 90, 110)
    rules = list(np.binary_repr(listRules[0], width=8))
    rules.reverse()
    draw()

    #Bucle de ejecución
    y = 0
    while True:
        newGameState = np.copy(gameState)
        time.sleep(0.001)

        # Registramos eventos de teclado y ratón.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pauseExecution = not pauseExecution

            mouseClick = pygame.mouse.get_pressed()
            if sum(mouseClick) > 0:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
                newGameState[celX, celY] = not mouseClick[2]

        for x in range(0, nxC):
            if not pauseExecution:
                # Convertir a entero el número binario obternido
                ruleIdx = int(str(int(gameState[(x-1) % nxC, y])) + str(int(gameState[x, y])) + str(int(gameState[(x+1) % nxC, y])), 2)
                newGameState[x, (y+1) % nyC] = rules[ruleIdx]

            poly = [(int(x     * dimCW), int(y     * dimCH)),
                    (int((x+1) * dimCW), int(y     * dimCH)),
                    (int((x+1) * dimCW), int((y+1) * dimCH)),
                    (int(x     * dimCW), int((y+1) * dimCH))]
            # And draw the cell for each pair of x and y
            if newGameState[x, y] == 1:
                pygame.draw.polygon(screen, (200,255,200), poly, 0)

        if not pauseExecution: y = (y + 1)
        
        pygame.display.update() 
        # We update the state of the game
        gameState = np.copy(newGameState)
        
        if y == nyC:
            pauseExecution = True
            time.sleep(3)
            break