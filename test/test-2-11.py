from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

class Test(Base):

    def initialize(self):
        print("Initializing program (using uniform variable for wrap-around-animation)...")
        OpenGLUtils.printSystemInfo()

        # vertex shader
        vsCode = """
            in vec3 position;
            uniform vec3 translation;
            
            void main() {
                vec3 pos = position + translation;
                gl_Position = vec4(pos, 1.0);
            }
        """

        # fragment shader
        fsCode = """
            uniform vec3 baseColor;
            out vec4 fragColor;

            void main() {
                fragColor = vec4(baseColor, 1.0);
            }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        
        ### optional render settings ###
        glLineWidth(4)
        glPointSize(10)
    
        # set up vertex attribute
        positionData = [
            [0.2,  0.0, 0.0],   #A
            [0.8,  0.0, 0.0],   #B
            [0.5,  0.5, 0.0]  #F   
        ]

        self.triangleStartXPos = positionData[0][0] 
        self.triangleStartYPos = positionData[0][1] 
        
        self.triangleWidth = abs(abs(positionData[0][0]) + positionData[1][0]) 
        self.triangleHeight = abs(abs(positionData[0][1]) + positionData[2][1]) 

        # set up vertext array object 
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)


        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        self.translations = Uniform("vec3", [0, 0.0, 0.0])
        self.baseColors = Uniform("vec3",  [1.0,  0.5, 0.0])

        self.translations.locateVariable(self.programRef, 'translation')

        self.baseColors.locateVariable(self.programRef, 'baseColor')

        # movement speed
        self.speed = 2

    def update(self):

        x, y, z = self.translations.data

        distance = self.speed * self.deltaTime

        if self.input.isKeyPressed("left"):
            x -= distance
        if self.input.isKeyPressed("right"):
            x += distance
        if self.input.isKeyPressed("up"):
            y += distance
        if self.input.isKeyPressed("down"):
            y -= distance


        if x  >= abs(1 - self.triangleStartXPos):
            x = -(1 - abs(self.triangleStartXPos) + self.triangleWidth)        
        elif x  < -(1 - abs(self.triangleStartXPos) + self.triangleWidth ):
            x = abs(1 - self.triangleStartXPos)
        
        if y  >= abs(1 - self.triangleStartYPos):
            y = -(1 - abs(self.triangleStartYPos) + self.triangleHeight)        
        elif y  < -(1 - abs(self.triangleStartYPos) + self.triangleHeight ):
            y = abs(1 - self.triangleStartYPos)
        

            
        self.translations.data[:] = [x, y, z]
 

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.programRef)
        self.translations.uploadData()
        self.baseColors.uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)
        
        
        pass

Test().run()