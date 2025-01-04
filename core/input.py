import pygame


class Input(object):
    
    def __init__(self):
        self.quit = False
        
        # down / up - discrete key events    
        self.keyDownList = []
        self.keyUpList = []
    
        # pressed - continuous key events
        self.keyPressedList = []


    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownList
    

    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList
    

    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList
    

    def update(self):

        # reset key states
        self.keyDownList = []
        self.keyUpList = []
        
        for event in pygame.event.get():

            match (event.type):
                case pygame.QUIT:
                    self.quit = True
                case pygame.KEYDOWN:
                    keyName = pygame.key.name(event.key)
                    self.keyDownList.append(keyName)
                    self.keyPressedList.append(keyName)
                
                case pygame.KEYUP:
                    keyName = pygame.key.name(event.key)
                    self.keyUpList.append(keyName)
                    self.keyPressedList.remove(keyName)
