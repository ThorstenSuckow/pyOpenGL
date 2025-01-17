import numpy
import pygame
from OpenGL.GL import *
from core.openGLUtils import OpenGLUtils

pygame.init()
pygame.display.set_mode((512, 512), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("instanced rendering")

vertexShader = """
    in vec3 position;

    float rand(vec2 co){
        return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
    }
    
    void main() {
        int id = gl_InstanceID;

        gl_Position = vec4(
            position.x + id * 0.1, 
            position.y + id * 0.1, 
            0, 
            1
        );
    }
"""

fragmentShader = """
    out vec4 FragColor;

    void main() {
        FragColor = vec4(1, 0, 0, 1);
    }
"""

vertices = [
    -1, -1, 0
]

programRef = OpenGLUtils.initializeProgram(
    vertexShader, fragmentShader
)

vaoHandle = glGenVertexArrays(1)
vboHandle = glGenBuffers(1)

glBindVertexArray(vaoHandle)
glBindBuffer(GL_ARRAY_BUFFER, vboHandle)

glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE,
    3*sizeof(GLfloat),
    ctypes.c_void_p(0)
)

glPointSize(10)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(programRef)
    glBufferData(
        GL_ARRAY_BUFFER,
        numpy.array(vertices).astype(numpy.float32),
        GL_STATIC_DRAW    
    )

    glDrawArraysInstanced(GL_POINTS, 0, 1, 20)

    pygame.display.flip()