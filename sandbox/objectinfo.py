# The pupose of this program is the following:
# Draw a single point on the screen and a rect
# using two different buffers.
# Upon clicking one of the elements, the imgui overlay
# should provide information about the selected
# element, i.e. correctly identify it as the point or 
# rectangular.

import pygame
import imgui
import numpy
from imgui.integrations.pygame import PygameRenderer
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *

def normalize (x, y, width, height):
    
    mid_w = width / 2
    mid_h = height / 2
  
    normal_x = (x - mid_w) / mid_w
    normal_y = (mid_h - y) / mid_h

    return round(normal_x, 2), round(normal_y, 2)    

vertexCode = """
    in vec3 position;

    void main() {
        gl_Position = vec4(position, 1);
    }
"""

fragmentCode = """
    out vec4 FragColor;

    
    uniform vec4 PickingColor2;
    uniform vec4 PickingColor;

    void main() {
        FragColor = PickingColor;
    }
"""

point_vertices = [
    -0.1, -0.1, 0    
]

triangle_vertices = [
    0, 0.0, 0,
    0.5, 0.0, 0,
    0.25, 0.5, 0,
]

def getColorForId(id):
    return(
         (id & 0x000000FF) >>  0,
         (id & 0x0000FF00) >>  8,
         (id & 0x00FF0000) >> 16
    )

def getIdForColor(rgb):
    r, g, b = rgb 
    return(r + g * 256 + b * 256**2)


def uniformColorId(attributLocation, objectId):
    pickingColor = getColorForId(objectId)
    glUniform4f(attributLocation,
                pickingColor[0]/255, 
                pickingColor[1]/255, 
                pickingColor[2]/255,
                1.0)




# pygame, imgui
pygame.init()
displayFlags = pygame.OPENGL | pygame.RESIZABLE | pygame.DOUBLEBUF
size = 800, 600
screen = pygame.display.set_mode(size, displayFlags)
pygame.display.set_caption("Selecting elements via imgui")

imgui.create_context()
overlay = PygameRenderer()

io = imgui.get_io()
io.display_size = size


# opengl
programRef = OpenGLUtils.initializeProgram(vertexCode, fragmentCode)
pickingColorUniformLocation = glGetUniformLocation(program=programRef, name="PickingColor"),  
pickingColorUniformLocation = pickingColorUniformLocation[0] 


vaoHandles = glGenVertexArrays(2)
vboHandles = glGenBuffers(2)

glBindVertexArray(vaoHandles[0])
glBindBuffer(GL_ARRAY_BUFFER, vboHandles[0])
glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE, 
    3 * sizeof(GLfloat), 
    ctypes.c_void_p(0)
)

glBindVertexArray(vaoHandles[1])
glBindBuffer(GL_ARRAY_BUFFER, vboHandles[1])
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
wasClicked = False


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        overlay.process_event(event)
    overlay.process_inputs()
  
    point_vertices[0] = x / 100
    point_vertices[1] = y / 100


    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)


    glUseProgram(programRef)    
    
    # point drawing
    glBindVertexArray(vaoHandles[0])
    uniformColorId(pickingColorUniformLocation, 1324125)
    glBindBuffer(GL_ARRAY_BUFFER, vboHandles[0])
    glBufferData(GL_ARRAY_BUFFER, numpy.array(point_vertices).astype(numpy.float32), GL_STATIC_DRAW)
    glDrawArrays(GL_POINTS, 0, 1)

    # triangle drawing
    glBindVertexArray(vaoHandles[1])
    uniformColorId(pickingColorUniformLocation, 1214111)
    glBindBuffer(GL_ARRAY_BUFFER, vboHandles[1])
    glBufferData(GL_ARRAY_BUFFER, numpy.array(triangle_vertices).astype(numpy.float32), GL_STATIC_DRAW)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 3)

    # reset for imgui
    if not render_imgui:
        pygame.display.flip()
        continue

    glUseProgram(0)
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    
    imgui.new_frame()
    imgui.begin("selecting objects", True)
    imgui.set_window_size(280, 180)
    imgui.begin_child("Child 1", border=False, flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)

    
    mousePos = imgui.get_mouse_pos()    
    screen_width = screen.get_size()[0]
    screen_height = screen.get_size()[1]

    normal_x, normal_y = normalize(
        mousePos[0], mousePos[1], 
        screen_width, screen_height
    )

    imgui.text(f"Mouse pos (normalized): {normal_x}, {normal_y}")

    if imgui.is_mouse_clicked(0):
        wasClicked = mousePos

    
    
    imgui.text(f"screen: {screen_width} x {screen_height}")
            
    if wasClicked:
    
        glFlush()
        glFinish()
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        data = glReadPixels(
            wasClicked[0], 
            screen_height - wasClicked[1],
            1,1,
              GL_RGBA, GL_UNSIGNED_BYTE)

        normal_x, normal_y = normalize(
            wasClicked[0], wasClicked[1], 
            screen_width, screen_height
        )

        imgui.text(f"click x/y: {wasClicked}")
        imgui.text(f"normalized x/y: ({normal_x}, {normal_y})")
        
        imgui.text(f"Selected: {getIdForColor((data[0], data[1], data[2]))}")# r{data[0]/255} g{data[1]/255} b{data[2]/255} a{data[3]/255}")

    imgui.end_child()
    imgui.end()
    
    
    imgui.render()
    overlay.render(imgui.get_draw_data())

    pygame.display.flip()
  