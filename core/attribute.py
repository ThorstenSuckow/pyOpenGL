from OpenGL.GL import *
import numpy

'''
    Class does not store names of variables or references to the program 
    that will access the buffer, because there may be more than one program 
    that does so, and the variables in each program may have different names
'''
class Attribute(object):
    
    def __init__(self, dataType, data):

        # type of elements in the data array
        # int, float, vec2, vec3, vec4
        self.dataType = dataType

        # data array to be stored
        self.data = data

        # reference of available buffer from GPU
        # glGenBuffers returns a set of available vertex buffer references
        # the number of references returned is specified by the passed
        # parameter
        # @see uploadData (glBindBuffer)
        self.bufferRef = glGenBuffers(1)

        # upload data to GPU
        self.uploadData()

    '''
        Separating uploadData() from __init__ alows for updates
        if self.data has been changed and the buffer needs to be updated 
    '''
    def uploadData(self):
        # convert data to numpy array
        # (32 bit floats)
        data = numpy.array(self.data).astype(numpy.float32)

        # creates a buffer object references by the 2nd 
        # parameter
        # GL_ARRAY_BUFFER indicates that vertex attributes
        # are handled by the buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        # ... and store tha data in the bound buffer
        # glBufferData allocates storage for the buffer object
        # and stores the information from the 2nd paramater - any
        # existing (buffered) data will be discarded
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)


    # associate variable in program with this buffer
    def associateVariable(self, programRef, variableName):
        # glGetAttribLocation returns a value used to reference an attribute variable 
        # (type "in") with the name indicated by variableName
        # and declared in the vertex shader of the program referenced by
        # programRef - returns -1 if no such attribute is found/used
        variableRef = glGetAttribLocation(programRef, variableName)

        if variableRef == -1:
            return
        
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)

        # specify how data will be read from the currently bound buffer
        # into the specified variable
        # glVertexAttribPointer specifies that the referenced variable (see
        # glGetAttribLocation) will receive data from the array stored in
        # the vertex buffer currently bound to GL_ARRAY_BUFFER
        #
        # !!! associations between vertex buffers and program variables is stored
        # by whichever VAO was bound PRIOR to the following function calls
        #
        match (self.dataType):
            case "int":
                glVertexAttribPointer(variableRef, 1, GL_INT, False, 0, None)
            case "float":
                glVertexAttribPointer(variableRef, 1, GL_FLOAT, False, 0, None)
            case "vec2":
                glVertexAttribPointer(variableRef, 2, GL_FLOAT, False, 0, None)
            case "vec3":
                glVertexAttribPointer(variableRef, 3, GL_FLOAT, False, 0, None)
            case "vec4":
                glVertexAttribPointer(variableRef, 4, GL_FLOAT, False, 0, None)
            case _:
                raise Exception(f"Attribute {variableName} has unknown type {self.dataType}")

        # indicate data will be streamed to this variable
        # during the redering process
        glEnableVertexAttribArray(variableRef)