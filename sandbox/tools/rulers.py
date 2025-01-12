import pygame
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *

class Rulers:

    _surface = None
    _mousePos = None

    def __init__(self, width, height):
        self.offsetLeft = 50
        self.offsetBottom = 50
        self.width = width
        self.height = height
        
    def updateMousePos(self, mousePos):
        
        screenX, screenY = mousePos
        
        self.x = max(0, screenX - self.offsetLeft)
        self.y = max(0, abs(screenY - self.height) - self.offsetBottom)

        self._mousePos = mousePos

    def drawMousePos(self, mousePos: tuple):

        screenX, screenY = mousePos

        x1y1 = (screenX - 10, screenY)
        x2y2 = (screenX + 10, screenY)
        pygame.draw.line(self._surface, (255, 255, 255), x1y1, x2y2)
        
        x1y1 = (screenX, screenY - 10)
        x2y2 = (screenX, screenY + 10)
        pygame.draw.line(self._surface, (255, 255, 255), x1y1, x2y2)
        

    def surface(self):
        return self._surface

    def draw(self):

        width = self.width
        height = self.height
        offsetLeft = self.offsetLeft
        offsetBottom = self.offsetBottom


        #if not self._surface:
        surface = pygame.Surface((width, height))
        self._surface = surface
        #else:
        #    surface = self._surface

        if offsetLeft % 10 != 0 or offsetBottom % 10 != 0:
            raise Exception()

        x1 = offsetLeft
        y1 = height - offsetBottom

        pygame.draw.line(surface, (255, 255, 255), (x1, 0), (x1, height), 1)
        pygame.draw.line(surface, (255, 255, 255), (0, y1), (width, y1), 1)

        tickX = 50
        tickY = y1
        for _ in range(0, int(width / 10)):
            if tickX % 50 == 0:
                offset = 20
            else: 
                offset = 10
            

            tickX1 = (tickX, y1 + offset)
            tickX2 = (tickX, y1)
            pygame.draw.line(surface, (255, 255, 255),  tickX1, tickX2)
            tickX += 10
        
        for i in range(0, int(height / 10)):
            if tickY <= 0:
                break
            if i * 10 % 50 == 0:
                offset = 20
            else: 
                offset = 10
            
            tickY1 = (x1 - offset, tickY)
            tickY2 = (x1, tickY)
            pygame.draw.line(surface, (255, 255, 255),  tickY1, tickY2)
            tickY -= 10

        if self.x > 0 and self. y > 0:
            self.drawMousePos(self._mousePos)

        return self._surface
    
