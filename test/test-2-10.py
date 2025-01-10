from core.base import Base
from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *
from math import sin, cos

class Test(Base):

    def initialize(self):
        print("Initializing program (input handling)...")
        

    def update(self):
        
        if len(self.input.keyUpList) > 0:
            print(f"Keys up: {self.input.keyUpList}")    

        if len(self.input.keyDownList) > 0:
            print(f"Keys down: {self.input.keyDownList}")    

        if len(self.input.keyPressedList) > 0:
            print(f"Keys pressed: {self.input.keyPressedList}")    


Test().run()