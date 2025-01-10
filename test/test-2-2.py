from core.base import Base
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *

class Test(Base):

    def initialize(self):
        print("Initializing program...")
        OpenGLUtils.printSystemInfo()

        # verstex shader
        vsCode = """

            void main() {

                gl_Position = vec4(.0, .0, .0, 1.0);
            
            }
        """

        # fragment shader
        fsCode = """
            out vec4 fragColor;

            void main() {
                fragColor = vec4(.0, 1.0, 0.2, 1.0);
            }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        
        # set up vertext array object 
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        ### optional render settings ###
        glPointSize(10)


    def update(self):

        glUseProgram(self.programRef)

        glDrawArrays(GL_POINTS, 0, 1)
        pass

Test().run()