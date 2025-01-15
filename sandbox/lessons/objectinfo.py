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

    void main() {
        FragColor = vec4(1, 0, 0, 1);
    }
"""


pickingFragmentCode = """
    out vec4 FragColor;
    
    uniform vec4 PickingColor;

    void main() {
        FragColor = PickingColor;
    }
"""

objects = {
    'triangle': 1199424,
    'point': 2142573
}

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
pickingProgramRef = OpenGLUtils.initializeProgram(vertexCode, pickingFragmentCode)
programRef = OpenGLUtils.initializeProgram(vertexCode, fragmentCode)

pickingColorUniformLocation = glGetUniformLocation(program=pickingProgramRef, name="PickingColor"),  
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

screen_width = screen.get_size()[0]
screen_height = screen.get_size()[1]


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            newSize = event.dict['size']
            screen_width = newSize[0]
            screen_height = newSize[1]
        overlay.process_event(event)

    overlay.process_inputs()
  
    point_vertices[0] = x / 100
    point_vertices[1] = y / 100


    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    # imgui should be rendered.
    # in this case we switch between pickingFragment-shader and "normal"
    # fragment shader. we'll utilize imguis mouse event to trigger
    # identifying objects
    if render_imgui:
        mousePos = imgui.get_mouse_pos()    
        
        if imgui.is_mouse_clicked(0):
            wasClicked = mousePos

            glUseProgram(pickingProgramRef)    
        
            # point drawing
            glBindVertexArray(vaoHandles[0])
            uniformColorId(pickingColorUniformLocation, objects['point'])
            glBindBuffer(GL_ARRAY_BUFFER, vboHandles[0])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(point_vertices).astype(numpy.float32), GL_STATIC_DRAW)
            glDrawArrays(GL_POINTS, 0, 1)

            # triangle drawing
            glBindVertexArray(vaoHandles[1])
            uniformColorId(pickingColorUniformLocation, objects['triangle'])
            glBindBuffer(GL_ARRAY_BUFFER, vboHandles[1])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(triangle_vertices).astype(numpy.float32), GL_STATIC_DRAW)
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 3)

            glUseProgram(0)
            glBindVertexArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

            glFlush()
            glFinish()
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            data = glReadPixels(
                wasClicked[0], 
                screen_height - wasClicked[1],
                1,1,
                GL_RGBA, GL_UNSIGNED_BYTE)


    # switch back to regular program
    glUseProgram(programRef)    

    # point drawing
    glBindVertexArray(vaoHandles[0])
    glBindBuffer(GL_ARRAY_BUFFER, vboHandles[0])
    glBufferData(GL_ARRAY_BUFFER, numpy.array(point_vertices).astype(numpy.float32), GL_STATIC_DRAW)
    glDrawArrays(GL_POINTS, 0, 1)

    # triangle drawing
    glBindVertexArray(vaoHandles[1])
    glBindBuffer(GL_ARRAY_BUFFER, vboHandles[1])
    glBufferData(GL_ARRAY_BUFFER, numpy.array(triangle_vertices).astype(numpy.float32), GL_STATIC_DRAW)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 3)

    
    glUseProgram(0)
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


    if render_imgui:
        imgui.new_frame()
        imgui.begin("selecting objects", True)
        imgui.set_window_size(280, 180)
        imgui.begin_child("Child 1", border=False, flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)
    
        normal_x, normal_y = normalize(
            mousePos[0], mousePos[1], 
            screen_width, screen_height
        )

        imgui.text(f"Mouse pos (normalized): {normal_x}, {normal_y}")
    
        imgui.text(f"screen: {screen_width} x {screen_height}")
        
        if wasClicked:
            normal_x, normal_y = normalize(
                wasClicked[0], wasClicked[1], 
                screen_width, screen_height
            )

            imgui.text(f"click x/y: {wasClicked}")
            imgui.text(f"normalized x/y: ({normal_x}, {normal_y})")
            
            id = getIdForColor((data[0], data[1], data[2]))

            sel = '-'

            if id != 0:
                sel = 'triangle' if id == objects['triangle'] else 'point'
                
            imgui.text(f"Selected: {sel} (id: {id})")

        imgui.end_child()
        imgui.end()
        
        imgui.render()
        overlay.render(imgui.get_draw_data())

    pygame.display.flip()
  