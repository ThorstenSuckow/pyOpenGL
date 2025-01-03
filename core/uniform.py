from OpenGL.GL import *

class Uniform(object):

    def __init__(self, dataType, data):

        # type int, bool, float, vec2, vec3, vec4
        self.dataType = dataType

        self.data = data

        self.variableRef = None

    def locateVariable(self, programRef, variableName):

        # similiar to glGetAttribLocation (see attribute.py), 
        # glGetUniformLocation will return a vaue to reference 
        # a uniform variable for programRef, or -1 if not found
        self.variableRef = glGetUniformLocation(programRef, variableName)

    # stores data in previously located uniform variable 
    def uploadData(self):    
        if self.variableRef == -1:
            return 
        
        match (self.dataType):
            case "int":
                glUniform1i(self.variableRef, self.data)
            case "bool":
                glUniform1i(self.variableRef, self.data)
            case "float":
                glUniform1f(self.variableRef, self.data)
            case "vec2":
                glUniform2f(self.variableRef, 
                            self.data[0], self.data[1])
            case "vec3":
                glUniform3f(self.variableRef, 
                            self.data[0], self.data[1], 
                            self.data[2])
            case "vec4":
                glUniform2f(self.variableRef, 
                            self.data[0], self.data[1],
                            self.data[2], self.data[3])

            case _:
                raise Exception(f"unknown dataType {self.dataType} for uniform variable")                 
