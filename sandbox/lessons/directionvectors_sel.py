import numpy
import pygame
from OpenGL.GL import *
from core.openGLUtils import OpenGLUtils
import imgui
from imgui.integrations.pygame import PygameRenderer
from core.util import Util

vertexShader = """
    in vec3 position;

    void main() {
        gl_Position = vec4(position, 1);
    }
"""


pickingFragmentCode = """
    out vec4 FragColor;
    
    uniform vec4 PickingColor;

    void main() {
        FragColor = PickingColor;
    }
"""

axisVertexShader = """
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 axisColor;
    out vec3 axis_color;
    void main() {
        axis_color = axisColor;
        gl_Position = vec4(position, 1);
    }
"""

axisFragmentShader = """
    in vec3 axis_color;
    out vec4 FracColor;
    void main() {
        FracColor = vec4(axis_color, 1);
    }

"""

fragmentShader = """
    out vec4 FragColor;

    void main() {
        FragColor = vec4(1, 1, 1, 0.5);
    } 
"""

pygame.init()
size = 800, 600
pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

imgui.create_context()
overlay = PygameRenderer()

io = imgui.get_io()
io.display_size = size

pickingProgramRef = OpenGLUtils.initializeProgram(vertexShader, pickingFragmentCode)
programRef = OpenGLUtils.initializeProgram(vertexShader, fragmentShader)
axisProgramRef = OpenGLUtils.initializeProgram(axisVertexShader, axisFragmentShader)

vertices = [
    #  x      y   z
    -0.25,    0,  0,
    -0.25,  0.5,  0,
     0.25,    0,  0,
     0.25,  0.5,  0
]

axis = [
    0, 0.25, 0,
    1, 0, 0, 
    0.5, 0.25, 0, 
    1, 0, 0,
    0, 0.25, 0,
    0, 1, 0,
    0, 0.75, 0,
    0, 1, 0
]

vaoHandle = glGenVertexArrays(1)
vboHandle = glGenBuffers(1)
glBindVertexArray(vaoHandle)
glBindBuffer(GL_ARRAY_BUFFER, vboHandle)
glBufferData(
    GL_ARRAY_BUFFER,
    numpy.array(vertices).astype(numpy.float32),
    GL_STATIC_DRAW     
)
glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE, 
    3 * sizeof(GLfloat), 
    ctypes.c_void_p(0)
)

vaoHandleAxis = glGenVertexArrays(1)
vboAxisHandle = glGenBuffers(1)
glBindVertexArray(vaoHandleAxis)
glBindBuffer(GL_ARRAY_BUFFER, vboAxisHandle)
glBufferData(
    GL_ARRAY_BUFFER,
    numpy.array(axis).astype(numpy.float32),
    GL_STATIC_DRAW     
)
glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE, 
    6 * sizeof(GLfloat), 
    ctypes.c_void_p(0)
)
glEnableVertexAttribArray(1)
glVertexAttribPointer(
    1, 3, GL_FLOAT, GL_FALSE, 
    6 * sizeof(GLfloat), 
    ctypes.c_void_p(3 * sizeof(GLfloat))
)


glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


running = True
devMode = False
screen_width, screen_height = size

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            devMode = True
        elif event.type == pygame.VIDEORESIZE:
                newSize = event.dict['size']
                screen_width = newSize[0]
                screen_height = newSize[1]
        overlay.process_event(event)

    

    overlay.process_inputs()
  
    glClearColor(0, 0 , 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(vaoHandle)
    glUseProgram(programRef)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, len(vertices) // 3)
    

    if devMode: 
        mousePos = imgui.get_mouse_pos()    

        glBindVertexArray(vaoHandleAxis)
        glUseProgram(axisProgramRef)
        glDrawArrays(GL_LINES, 0, len(axis) // 3)

        glUseProgram(0)
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        imgui.new_frame()
        imgui.begin("selecting objects", True)
        imgui.set_window_size(280, 180)
        imgui.begin_child("Child 1", border=False, flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)
    
        normal_x, normal_y = Util.toClipCoordinates(
            mousePos[0], mousePos[1], 
            screen_width, screen_height
        )

        imgui.text(f"Mouse pos (normalized): {normal_x}, {normal_y}")    
        imgui.text(f"screen: {screen_width} x {screen_height}")
        
        imgui.end_child()
        imgui.end()
        
        imgui.render()
        overlay.render(imgui.get_draw_data())    

    pygame.display.flip()