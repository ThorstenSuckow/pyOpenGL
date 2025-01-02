from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

class Test(Base):

    def initialize(self):
        print("Initializing program (passing data between shaders)...")
        OpenGLUtils.printSystemInfo()

        # verstex shader
        vsCode = """
            in vec3 position;
            in vec3 vertexColor;
            out vec3 color;
            void main() {
                gl_Position = vec4(
                    position.x, position.y, position.z, 1.0
                );
                color = vertexColor;
            }
        """

        # fragment shader
        fsCode = """
            in vec3 color;
            out vec4 fragColor;

            void main() {
                fragColor = vec4(color.r, color.g, color.b, 1.0);
            }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        
        ### optional render settings ###
        glLineWidth(4)
        glPointSize(10)
    
        # set up vertex attribute
        positionData = [
            [0.8,  0.0, 0.0],   #A
            [0.4,  0.6, 0.0],   #B
            [-0.4, 0.6, 0.0],   #C
            [-0.8,  0.0, 0.0],  #D
            [-0.4,  -0.6, 0.0], #E 
            [0.4,  -0.6, 0.0]  #F   
        ]

        # set up colors
        colors = [
            [1.0,  0.0, 0.0],   
            [1.0,  0.5, 0.0],   
            [1.0,  1.0, 0.0],   
            [0.0,  1.0, 0.0],  
            [0.0,  0.0, 1.0],  
            [0.5,  0.0, 1.0]    
        ]

        # set up vertext array object 
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)


        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        colorAttribute = Attribute("vec3", colors)
        colorAttribute.associateVariable(self.programRef, "vertexColor")


   
    def update(self):

        glUseProgram(self.programRef)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)
        pass

Test().run()