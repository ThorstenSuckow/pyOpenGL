

## 1. pointmover.py
The pupose of this program is the following:
pygame is used for drawing a single point onto the screen
using OpenGL.
imgui[pygame] is the being used to create an overlay that 
shows two sliders: one for the x-coordinate, one for the
y-coordinate. Moving the sliders will update the point's
position.

## 2. objectinfo.py
The pupose of this program is the following:
Draw a single point on the screen and a triangle
using two different buffers.
Upon clicking one of the elements, the imgui overlay
should provide information about the selected
element, i.e. correctly identify it as the point or 
triangle.

## 3. trianglestripquad.py
Draw a rectangle using the GL_TRIANGLE_STRIP primitive

## 4. duoubletriangleindices.py
Draw two rectangles using an Index Buffer Object.

## 5. primitiverestart.py
Force restarting primitive rendering to break GL_TRIANGLE_STRIP order.


## ToDo:
 - scale object according to screen size, using various options:
   a. scale WITH dimension
   b. regain original dimensions, i.e. expand/collapse the viewable 
      rect
 - select rect and apply matrix transformations using imgui
 - render objectinfo to offscreen framebuffer so it does not impact usual rendering