from OpenGL.GL import *

class OpenGLUtils(object):

    @staticmethod
    def initializeShader(shaderCode, shaderType):

        shaderCode = f'#version 330\n{shaderCode}'

        # create empty shader, return ref value
        shaderRef = glCreateShader(shaderType)

        # store source code in shader
        glShaderSource(shaderRef, shaderCode)

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


    @staticmethod
    def initializeProgram(vertexShaderCode, fragmentShaderCode):
        vertexShaderRef = OpenGLUtils.initializeShader(vertexShaderCode, GL_VERTEX_SHADER)
        fragmentShaderRef = OpenGLUtils.initializeShader(fragmentShaderCode, GL_FRAGMENT_SHADER)

        programRef = glCreateProgram()

        # attach previously compiled shader programs
        glAttachShader(programRef, vertexShaderRef)
        glAttachShader(programRef, fragmentShaderRef)

        # link vertex shader w/ fragment shader
        glLinkProgram(programRef)

        # check if linking was succesfull
        linkSuccess = glGetProgramiv(programRef, GL_LINK_STATUS)

        if not linkSuccess:
            errorMessage = glGetProgramInfoLog(programRef)
            # free memory used to store program
            glDeleteProgram(programRef)
            errorMessage = '\n' + errorMessage.decode('utf-8')
            raise Exception(errorMessage)

        return programRef

    @staticmethod
    def printSystemInfo():
        print(f"   Vendor: {glGetString(GL_VENDOR).decode('utf-8')}")
        print(f"   Renderer: {glGetString(GL_RENDERER).decode('utf-8')}")
        print(f"   OpenGL version supported: {glGetString(GL_VERSION).decode('utf-8')}")
        print(f"   GLSL version supported: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')}")
