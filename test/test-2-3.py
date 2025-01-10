from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

class Test(Base):

    def initialize(self):
        print("Initializing program...")
        OpenGLUtils.printSystemInfo()

        # verstex shader
        vsCode = """
            in vec3 position;
            void main() {
                gl_Position = vec4(
                    position.x, position.y, position.z, 1.0
                );
            }
        """

        # fragment shader
        fsCode = """
            out vec4 fragColor;

            void main() {
                fragColor = vec4(1.0, 1.0, 0.0, 1.0);
            }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        
        # set up vertext array object 
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        ### optional render settings ###
        glLineWidth(4)
    
        # set up vertex attribute
        positionData = [
            [0.8,  0.0, 0.0],   #A
            [0.4,  0.6, 0.0],   #B
            [-0.4, 0.6, 0.0],   #C
            [-0.8,  0.0, 0.0],  #D
            [-0.4,  -0.6, 0.0], #E 
            [0.4,  -0.6, 0.0]  #F   
        ]

        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

   
    def update(self):

        glUseProgram(self.programRef)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount)
        pass

Test().run()