#Autodesk Example of using function table

# Import the module
import maya.OpenMayaRender as OpenMayaRender

# Get a renderer, then a function table
glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()

# Query the maximum texture size
def printMaxTextureSize():
    maxTxtSize = glFT.maxTextureSize()
    print maxTxtSize

# Draw an axis
def drawAxis():
    glFT.glDisable(OpenMayaRender.MGL_LIGHTING)
    glFT.glBegin(OpenMayaRender.MGL_LINES)
    
    glFT.glColor3f( 1.0, 0.0, 0.0 )
    glFT.glVertex3f( 0.0, 0.0, 0.0 )
    glFT.glVertex3f( 3.0, 0.0, 0.0 )
    
    glFT.glColor3f( 0.0, 1.0, 0.0 )
    glFT.glVertex3f( 0.0, 0.0, 0.0 )
    glFT.glVertex3f( 0.0, 3.0, 0.0 )
    
    glFT.glColor3f( 0.0, 0.0, 1.0 )
    glFT.glVertex3f( 0.0, 0.0, 0.0 )
    glFT.glVertex3f( 0.0, 0.0, 3.0 )
    
    glFT.glEnd()
    glFT.glEnable(OpenMayaRender.MGL_LIGHTING)
