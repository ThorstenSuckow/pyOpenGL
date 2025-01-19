import numpy
import pygame
from OpenGL.GL import *
from core.openGLUtils import OpenGLUtils


vertexShader = """
    in vec3 position;

    void main() {
        gl_Position = vec4(position, 1);
    }
"""

fragmentShader = """
    out vec4 FragColor;

    void main() {
        FragColor = vec4(1, 1, 1, 0.5);
    } 
"""

pygame.init()
size = 512, 512
pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)

programRef = OpenGLUtils.initializeProgram(vertexShader, fragmentShader)

vertices = [
    -0.25, 0, 0,
    -0.25, 0.5, 0,
    0.25, 0, 0,
    0.25, 0.5, 0
]

vaoHandle = glGenVertexArrays(1)
vboHandle = glGenBuffers(1)

glBindVertexArray(vaoHandle)
glBindBuffer(GL_ARRAY_BUFFER, vboHandle)

glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE, 
    3 * sizeof(GLfloat), 
    ctypes.c_void_p(0)
)

glBufferData(
    GL_ARRAY_BUFFER,
    numpy.array(vertices).astype(numpy.float32),
    GL_STATIC_DRAW     
)

glUseProgram(programRef)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    glClearColor(0, 0 , 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)


    glDrawArrays(GL_TRIANGLE_STRIP, 0, len(vertices) // 3)

    pygame.display.flip()