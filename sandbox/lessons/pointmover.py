# The pupose of this program is the following:
# pygame is used for drawing a single point onto the screen
# using OpenGL.
# imgui[pygame] is the being used to create an overlay that 
# shows two sliders: one for the x-coordinate, one for the
# y-coordinate. Moving the sliders will update the point's
# position.

import pygame
import imgui
import numpy
from imgui.integrations.pygame import PygameRenderer
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *


vertexCode = """
    in vec3 position;

    void main() {
        gl_Position = vec4(position, 1);
    }
"""

fragmentCode = """
    out vec4 FragColor;

    void main() {
        FragColor = vec4(1, 0, 0, 1);
    }
"""

vertices = [
    0, 0.2, 0
]

# pygame, imgui
pygame.init()
displayFlags = pygame.OPENGL | pygame.RESIZABLE | pygame.DOUBLEBUF
size = 800, 600
pygame.display.set_mode(size, displayFlags)
pygame.display.set_caption("Moving vertice via imgui")

imgui.create_context()
overlay = PygameRenderer()

io = imgui.get_io()
io.display_size = size



# opengl
programRef = OpenGLUtils.initializeProgram(vertexCode, fragmentCode)
vaoHandle = glGenVertexArrays(1)
glBindVertexArray(vaoHandle)

vboHandle = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vboHandle)
#data = numpy.array(vertices).astype(numpy.float32)
#glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE, 
    3 * sizeof(GLfloat), 
    ctypes.c_void_p(0)
)

running = True

glPointSize(10)
    
x = 80
y = 80

render_imgui = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        overlay.process_event(event)
    overlay.process_inputs()
  
    vertices[0] = x / 100
    vertices[1] = y / 100


    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)


    glUseProgram(programRef)    
    glBindVertexArray(vaoHandle)
    glBindBuffer(GL_ARRAY_BUFFER, vboHandle)

    glBufferData(GL_ARRAY_BUFFER, numpy.array(vertices).astype(numpy.float32), GL_STATIC_DRAW)
    
    glDrawArrays(GL_POINTS, 0, 1)

    # reset for imgui
    if not render_imgui:
        pygame.display.flip()
        continue

    glUseProgram(0)
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
  
    imgui.new_frame()
    imgui.begin("x/y!", True)

    imgui.begin_child("Child 1", border=False, flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)

    changedx, x = imgui.slider_float(
        "x", x, min_value = 0, max_value = 100,
        format = "%.0f"
    )
    changedy, y = imgui.slider_float(
        "y", y, min_value = 0, max_value = 100,
        format = "%.0f"
    )

    vertices[0] = x / 100
    vertices[1] = y / 100

    imgui.text(f"changed x: {changedx}, {x / 100}")
    imgui.text(f"changed y: {changedy}, {y / 100}")
    
    imgui.end_child()
    imgui.end()
    
    imgui.render()
    overlay.render(imgui.get_draw_data())

    pygame.display.flip()
  