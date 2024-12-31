from OpenGL.GL import *

class OpenGLUtils(object):

    @staticmethod
    def initializeShader(shaderCode, shaderType):

        shaderCode = f'#version 330\n{shaderCode}'

        # create empty shader, return ref value
        shaderRef = glCreateShader(shaderType)

        # store source code in shader
        glShaderSource = (shaderRef, shaderCode)

        # compile shader source
        glCompileShader(shaderRef)

        compileSuccess = glGetShaderiv(shaderRef, GL_COMPILE_STATUS)

        if not compileSuccess:
            errorMessage = glGetShaderInfoLog(shaderRef)
            # free memory
            glDeleteShader(shaderRef)
            # convert byte str to character str
            errorMessage = '\n' + errorMessage.decode('utf-8')

            raise  Exception(errorMessage)
        
        # return shader ref value
        return shaderRef