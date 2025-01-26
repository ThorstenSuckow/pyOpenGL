import numpy
import pygame
from OpenGL.GL import *
from core.openGLUtils import OpenGLUtils
from core.matrix import Matrix
import imgui
from imgui.integrations.pygame import PygameRenderer
from core.util import Util

vertexShader = """
    in vec3 position;
    uniform mat4 modelMatrix;

    void main() {
        gl_Position = modelMatrix * vec4(position, 1);
    }
"""

axisVertexShader = """
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 axisColor;
    uniform mat4 modelMatrix;
    out vec3 axis_color;
    void main() {
        axis_color = axisColor;
        gl_Position = modelMatrix * vec4(position, 1);
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


pickingFragmentCode = """
    out vec4 FragColor;
    
    uniform vec4 PickingColor;

    void main() {
        FragColor = PickingColor;
    }
"""

pygame.init()
size = 800, 600
pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

imgui.create_context()
overlay = PygameRenderer()

io = imgui.get_io()
io.display_size = size


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

modelMatrix = Matrix.makeIdentity()

'''
Rectangle
'''
programRef = OpenGLUtils.initializeProgram(vertexShader, fragmentShader)
vaoHandle = glGenVertexArrays(1)
vboHandle = glGenBuffers(1)
glBindVertexArray(vaoHandle)
glUseProgram(programRef)
modelMatrixUniformLocation = glGetUniformLocation(programRef, "modelMatrix")  
    
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

'''
Picking rectangle
'''
pickingProgramRef = OpenGLUtils.initializeProgram(vertexShader, pickingFragmentCode)
pickingVaoHandle = glGenVertexArrays(1) 
pickingVboHandle = glGenBuffers(1)
glUseProgram(pickingProgramRef)
glBindVertexArray(pickingVaoHandle)
pickingColorUniformLocation = glGetUniformLocation(pickingProgramRef, "PickingColor")
glBindBuffer(GL_ARRAY_BUFFER, pickingVboHandle)
glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0, 3, GL_FLOAT, GL_FALSE, 
    3 * sizeof(GLfloat), 
    ctypes.c_void_p(0)
)

'''
Vectors / Axis
'''
axisProgramRef = OpenGLUtils.initializeProgram(axisVertexShader, axisFragmentShader)
vaoHandleAxis = glGenVertexArrays(1)
vboAxisHandle = glGenBuffers(1)
glBindVertexArray(vaoHandleAxis)
pickingModelMatrixLocation = glGetUniformLocation(axisProgramRef, "modelMatrix")
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
wasClicked = False
selectedObject = None
posx = 0
posy = 0

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

    if devMode: 
        mousePos = imgui.get_mouse_pos()    
        if  ((imgui.is_any_item_hovered() == False and imgui.is_window_hovered(imgui.HOVERED_ANY_WINDOW) == False)
            and imgui.is_mouse_clicked(0)):
            wasClicked = mousePos

            '''
                draw color id
            '''
            glUseProgram(pickingProgramRef)
            glBindVertexArray(pickingVaoHandle)
            pickingColor = Util.intToRgb(2145525151)
            glUniformMatrix4fv(modelMatrixUniformLocation, 1, GL_TRUE, modelMatrix)
            glUniform4f(pickingColorUniformLocation, pickingColor[0]/255, 
                        pickingColor[1]/255, pickingColor[2]/255, 1.0)
            glBindBuffer(GL_ARRAY_BUFFER, pickingVboHandle)
            glBufferData(GL_ARRAY_BUFFER, numpy.array(vertices).astype(numpy.float32), GL_STATIC_DRAW)

            
            glDrawArrays(GL_TRIANGLE_STRIP, 0, len(vertices) // 3)
            glFlush()
            glFinish()
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            data = glReadPixels(
                wasClicked[0],  screen_height - wasClicked[1], 1,1, GL_RGBA, GL_UNSIGNED_BYTE)

    glUseProgram(programRef)
    glBindVertexArray(vaoHandle)
    glUniformMatrix4fv(modelMatrixUniformLocation, 1, GL_TRUE, modelMatrix)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, len(vertices) // 3)
    

    if devMode:
        glBindVertexArray(vaoHandleAxis)
        glUseProgram(axisProgramRef)
        glUniformMatrix4fv(pickingModelMatrixLocation, 1, GL_TRUE, modelMatrix)
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
        
        if wasClicked:
   
            normal_x, normal_y = Util.toClipCoordinates(
                wasClicked[0], wasClicked[1], 
                screen_width, screen_height
            )

            imgui.text(f"click x/y: {wasClicked}")
            imgui.text(f"normalized x/y: ({normal_x}, {normal_y})")
            
            id = Util.rgbToInt((data[0], data[1], data[2]))
            
            imgui.text(f"Selected id: {id}")


            if id != 0:
                selectedObject = "rectangle"
                imgui.text(f"Selected object: {selectedObject}")
    

                changed, values = imgui.core.slider_float2(
                    "move", 
                    posx, 
                    posy, 
                    -1, 
                    1, 
                    format='%.3f', 
                )
                if changed:
                    posx, posy = values
                    modelMatrix = Matrix.makeTranslation(posx, posy, 0)
        imgui.end_child()
        imgui.end()
        
        imgui.render()
        overlay.render(imgui.get_draw_data())    

    pygame.display.flip()