from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

class Test(Base):

    def initialize(self):
        print("Initializing program  (using different buffers for rendering)...")
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
        
        
        ### optional render settings ###
        glLineWidth(4)
    
        # set up vertex attribute (triangle)
        positionDataTri = [
            [-0.75,  0.0, 0.0],
            [-0.25,  0.0, 0.0], 
            [-0.5, 0.5, 0.0]  #F   
        ]

        # set up vertex array object (Triangle)
        self.vaoRefTri = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRefTri)
        
        self.vertexCountTri = len(positionDataTri)
        positionAttributeTri = Attribute("vec3", positionDataTri)
        positionAttributeTri.associateVariable(self.programRef, "position")

        # set up vertex attribute (rect)
        positionDataRect = [
            [0.25,  0.0, 0.0],
            [0.75,  0.0, 0.0], 
            [0.75, 0.5, 0.0], 
            [0.25, 0.5, 0.0]   
        ]


        # set up vertex array object (Rect)
        self.vaoRefRect = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRefRect)

        self.vertexCountRect = len(positionDataRect)
        positionAttributeRect = Attribute("vec3", positionDataRect)
        positionAttributeRect.associateVariable(self.programRef, "position")

        
   

    def update(self):

        glUseProgram(self.programRef)
        
        glBindVertexArray(self.vaoRefTri)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCountTri)
        
        glBindVertexArray(self.vaoRefRect)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCountRect)
        
        pass

Test().run()