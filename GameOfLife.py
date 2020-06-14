import sys
import pygame
import numpy as np
import time
import random
  
pygame.init()
size = width, height = 700, 700
bg = 25,25,25 # Fondo de la pantalla
nxC, nyC = 100, 100 # Número de celdas
dimCW, dimCH = (width - 1) / nxC, (height -1) / nyC # Dimensiones de la celda
pauseExecution = True # Control de la ejecición del juego
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# Estados de las celdas. Vivas = 1; Muertas = 0;
gameState = np.zeros((nxC, nyC))
# Autómata palo.
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1
# Autómata móvil.
gameState[11, 11] = 1
gameState[12, 12] = 1
gameState[12, 13] = 1
gameState[11, 13] = 1
gameState[10, 13] = 1

#Bucle de ejecución
while True:
    newGameState = np.copy(gameState)
    # Pintamos el fondo con un color
    screen.fill(bg)
    time.sleep(0.1)

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
        for y in range(0, nyC):
            # Calculamos el número de vecinos cercanos.
            n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                      gameState[(x)     % nxC, (y - 1) % nyC] + \
                      gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                      gameState[(x - 1) % nxC, (y)     % nyC] + \
                      gameState[(x + 1) % nxC, (y)     % nyC] + \
                      gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                      gameState[(x)     % nxC, (y + 1) % nyC] + \
                      gameState[(x + 1) % nxC, (y + 1) % nyC]

            if not pauseExecution:
                # Rule #1: Una célula muerta con exactamente 3 vecinas vivas, "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # Rule #2: Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere".
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            poly = [(int(x     * dimCW), int(y     * dimCH)),
                    (int((x+1) * dimCW), int(y     * dimCH)),
                    (int((x+1) * dimCW), int((y+1) * dimCH)),
                    (int(x     * dimCW), int((y+1) * dimCH))]
            # And draw the cell for each pair of x and y
            if newGameState[x, y] == 0: 
                pygame.draw.polygon(screen, (128,150,128), poly, 1)
            else:
                pygame.draw.polygon(screen, (200,255,200), poly, 0)

    pygame.display.update() 
    # We update the state of the game
    gameState = np.copy(newGameState)