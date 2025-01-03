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

        self.triangleStartPos = positionData[0][0] 
        self.triangleWidth = abs(abs(positionData[0][0]) + positionData[1][0]) 

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

        
    def update(self):

        x, y, z = self.translations.data

        x += 0.01

        if x  >= abs(1 - self.triangleStartPos):#self.triangleWidth:
            x = 1 - abs(self.triangleStartPos) + self.triangleWidth        
            x *= -1
            
        self.translations.data[:] = [x, y, z]
 

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.programRef)
        self.translations.uploadData()
        self.baseColors.uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)
        
        
        pass

Test().run()