import pygame
import sys
from core.openGLUtils import OpenGLUtils
import numpy
from OpenGL.GL import *
import ctypes
from sandbox.tools.rulers import Rulers 

pygame.init()
displayFlags = pygame.DOUBLEBUF

screen = pygame.display.set_mode([1280, 720], displayFlags)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

pygame.display.set_caption("Matrix Transformations")

running = True
clock = pygame.time.Clock()
time = 0 

rulers = Rulers(SCREEN_WIDTH, SCREEN_HEIGHT)

while running:

    deltaTime = clock.get_time() / 1000
    time += deltaTime
    
    for event in pygame.event.get():
        mousePos = pygame.mouse.get_pos()
        rulers.updateMousePos(mousePos)
        if event.type == pygame.QUIT:
                running = False

    rulerSurface = rulers.draw()
    
    
    if rulers.x > 0 and rulers.y > 0:
        showMouse = False
    else:
        showMouse = True

    pygame.mouse.set_visible(showMouse) 
    
    screen.blit(rulerSurface, (0,0))
    
    pygame.display.flip()
    
    clock.tick(60.0)

pygame.quit()
sys.exit()


