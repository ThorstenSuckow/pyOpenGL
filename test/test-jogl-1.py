import pygame
import sys
from core.openGLUtils import OpenGLUtils
import numpy
from OpenGL.GL import *
import ctypes

pygame.init()
displayFlags = pygame.DOUBLEBUF | pygame.OPENGL
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

screen = pygame.display.set_mode([512, 512], displayFlags)
pygame.display.set_caption("Graphics Window")

running = True
clock = pygame.time.Clock()
time = 0 


vertexShader = """
    in vec3 position;
    in vec3 col;

    out vec3 color;
    void main() {
        gl_Position = vec4(position, 1.0);
        color = col;
    }
"""

fragmentShader = """
    in vec3 color;
    out vec4 FragColor;

    void main() {
        FragColor = vec4(color, 1);
    }

"""


programRef = OpenGLUtils.initializeProgram(vertexShader, fragmentShader)

vertices = [
    -0.5, 0.0, 0.0, #pos
    1.0, 1.5, 0.4, #col
    0.5, 0, 0.0, #pos
    .0, 1.0, 1.0, #col
    0., 0.5, 0.0, #pos
    1.0, 0.0, 0.0 #col
]

vaoHandle = glGenVertexArrays(1)
glBindVertexArray(vaoHandle)

vboHandle = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vboHandle)

data = numpy.array(vertices).astype(numpy.float32)
glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*sizeof(GLfloat),  ctypes.c_void_p(0))


glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, False, 6*sizeof(GLfloat),  ctypes.c_void_p(3 * sizeof(GLfloat)))


#glClearColor(0, 0, 0, 1)



while running:

    deltaTime = clock.get_time() / 1000
    time += deltaTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Screen clear

    glLineWidth(4)
    glPointSize(5)    
    glUseProgram(programRef)
    glDrawArrays(GL_POINTS, 0, 3)
      
    pygame.display.flip()
    
    clock.tick(60.0)

pygame.quit()
sys.exit()


