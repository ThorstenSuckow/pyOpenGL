import pygame
import numpy
from OpenGL.GL import *
from core.openGLUtils import OpenGLUtils

pygame.init()
size = 512, 512
pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Primitive Restart")

vertexShader = """
    in vec3 position;

    void main() {
        gl_Position = vec4(position, 1);
    }
"""

fragmentShader = """
    out vec4 FragColor; 

    void main() {
        FragColor = vec4(1, 0, 0, 1);
    }
"""

vertices = [
    -0.5, 0.2, 0,
    0.5, 0.2, 0,
    0, 0.5, 0,
    
    0, -0.5, 0
]

indices = [
    0, 1, 2, 99, 3
]

programRef = OpenGLUtils.initializeProgram(vertexShader, fragmentShader)

vaoHandle = glGenVertexArrays(1)
vboHandle = glGenBuffers(1)
iboHandle = glGenBuffers(1)

glBindVertexArray(vaoHandle)
glBindBuffer(GL_ARRAY_BUFFER, vboHandle)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, iboHandle)

glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE,
    3 * sizeof (GLfloat),
    ctypes.c_void_p(0)
)



running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glEnable(GL_PRIMITIVE_RESTART)
    glPrimitiveRestartIndex(99)

    glUseProgram(programRef)
    glBufferData(
        GL_ARRAY_BUFFER, 
        numpy.array(vertices).astype(numpy.float32),
        GL_STATIC_DRAW
    )
    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        numpy.array(indices).astype(numpy.int32),
        GL_STATIC_DRAW
    )

    glDrawElements(
        GL_TRIANGLE_STRIP, len(indices),
        GL_UNSIGNED_INT, ctypes.c_void_p(0)
    )

    pygame.display.flip()