import pygame
import sys
from core.openGLUtils import OpenGLUtils
import numpy
from OpenGL.GL import *
import ctypes
from sandbox.tools.rulers import Rulers 

pygame.init()
displayFlags = pygame.DOUBLEBUF

screen = pygame.display.set_mode([512, 512], displayFlags)
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
        if event.type == pygame.QUIT:
            running = False


    screen.blit(rulers.surface(), (0,0))
    
    pygame.display.flip()
    
    clock.tick(60.0)

pygame.quit()
sys.exit()


