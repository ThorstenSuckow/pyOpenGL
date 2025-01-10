from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

class Test(Base):

    def initialize(self):
        print("Initializing program (using uniforms for two shapes and different colors)...")
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
            [-0.8,  0.0, 0.0],   #A
            [-0.2,  0.0, 0.0],   #B
            [-0.5,  0.5, 0.0]  #F   
        ]

        # set up vertext array object 
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)


        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        translations = [
            [0.0, 0.0, 0.0],
            [1, 0.0, 0.0]
        ]

        baseColors =  [
            [1.0,  0.0, 0.0],   
            [0.5,  0.0, 1.0]    
        ]

        self.translations = [
            Uniform('vec3', translations[0]),
            Uniform('vec3', translations[1])
        ]

        self.translations[0].locateVariable(self.programRef, 'translation')
        self.translations[1].locateVariable(self.programRef, 'translation')
        

        self.baseColors = [
            Uniform('vec3', baseColors[0]),
            Uniform('vec3', baseColors[1])
        ]

        self.baseColors[0].locateVariable(self.programRef, 'baseColor')
        self.baseColors[1].locateVariable(self.programRef, 'baseColor')
        
    def update(self):

        glUseProgram(self.programRef)

        self.translations[0].uploadData()
        self.baseColors[0].uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)
        
        self.translations[1].uploadData()
        self.baseColors[1].uploadData()
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)
        
        
        pass

Test().run()