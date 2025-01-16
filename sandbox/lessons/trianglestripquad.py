from OpenGL.GL import *
from core.openGLUtils import OpenGLUtils
import pygame
import numpy


pygame.init()
displayFlags = pygame.OPENGL | pygame.DOUBLEBUF
size = 512, 512
pygame.display.set_mode(size, displayFlags)
pygame.display.set_caption("GL_TRIANGLE_STRIP")
            

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
    -0.5, -0.5, 0,
    -0.5, 0.5, 0,
    0.5, -0.5, 0,
    0.5, 0.5, 0
]


programRef = OpenGLUtils.initializeProgram(vertexShader, fragmentShader);

vbaHandle = glGenVertexArrays(1);
glBindVertexArray(vbaHandle)

vboHandle = glGenBuffers(1);
glBindBuffer(GL_ARRAY_BUFFER, vboHandle)

glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, 
    GL_FLOAT, GL_FALSE, 
    3 * sizeof(GLfloat),
    ctypes.c_void_p(0)
)


runing = True

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

    glClearColor(0, 0 , 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(programRef)
    glBufferData(
        GL_ARRAY_BUFFER,
        numpy.array(vertices).astype(numpy.float32),
        GL_STATIC_DRAW
    )

    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    pygame.display.flip()