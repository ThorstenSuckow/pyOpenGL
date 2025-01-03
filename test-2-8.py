from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *
from math import sin, cos

class Test(Base):

    def initialize(self):
        print("Initializing program (sin/cos-animation, shifting colors)...")
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
            [0,  0.0, 0.0],   #A
            [0.2,  0.0, 0.0],   #B
            [0.1,  0.2, 0.0]  #F   
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
        self.baseColors = Uniform("vec3",  [0.0,  0.0, 0.0])

        self.translations.locateVariable(self.programRef, 'translation')

        self.baseColors.locateVariable(self.programRef, 'baseColor')

        
    def update(self):

        x, y, z = self.translations.data
        self.translations.data[:] = [
            0.75 * cos(self.time), 
            0.75 * sin(self.time), 
            z
        ]

        r, g, b = self.baseColors.data
        self.baseColors.data[:] = [
            ((sin(self.time))+1) / 2,
            ((sin(self.time))+0.2) / 2,
            ((sin(self.time))+.04) / 2,
        ]
 
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.programRef)
        self.translations.uploadData()
        self.baseColors.uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)
        
        
        pass

Test().run()