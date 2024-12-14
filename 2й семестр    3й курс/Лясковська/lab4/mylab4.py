from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL._null import NULL
from math import cos, sin, pi

CHANGE_LIGHT = 1
SHOW_FIGURES = 2

floor_coordinates = [
    [-30.0, 0.0, 30.0],
    [30.0, 0.0, 30.0],
    [30.0, 0.0, -30.0],
    [-30.0, 0.0, -30.0],
]

width = 1000
height = 800
ableFloor = False
stencilReflection = 1
stencilShadow = 1
offsetShadow = 1
renderShadow = 1
renderFigure = 1
renderReflection = 1
reportSpeed = 0
animation = 0
lightSwitch = False
lightAngle = 0.0
lightHeight = 20
angle = -160
angle2 = 40
moving, startx, starty = ..., ..., ...
lightMoving = 0
lightStartX = 5
lightStartY = 5
lightPosition = [-5, -5, -5, -5]
lightColor = [0.8, 1.0, 0.8, 1.0]

coords = []
sizes = []
colors = []
figuretype = []
floorPlane = []
floorShadow = [[-1 for i in range(4)] for j in range(4)]

def chunk_iterable(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def read_coordinates(path):
    with open(path, "r") as file:
        for line in chunk_iterable(file.readlines(), 4):
            figtype, size, cords, color = map(lambda x: x.strip(), line)
            coords.append(list(map(float, cords.split())))
            sizes.append(int(size))
            colors.append(list(map(float, color.split())))
            figuretype.append(figtype)


def calculate_shadow_matrix(shadowMat, groundplane, lightpos):
    dot = groundplane[0] * lightpos[0] + groundplane[1] * lightpos[1] + groundplane[2] * lightpos[2] + groundplane[3] * lightpos[3]

    shadowMat[0][0] = dot - lightpos[0] * groundplane[0]
    shadowMat[1][0] = 0 - lightpos[0] * groundplane[1]
    shadowMat[2][0] = 0 - lightpos[0] * groundplane[2]
    shadowMat[3][0] = 0 - lightpos[0] * groundplane[3]

    shadowMat[0][1] = 0 - lightpos[1] * groundplane[0]
    shadowMat[1][1] = dot - lightpos[1] * groundplane[1]
    shadowMat[2][1] = 0 - lightpos[1] * groundplane[2]
    shadowMat[3][1] = 0 - lightpos[1] * groundplane[3]

    shadowMat[0][2] = 0 - lightpos[2] * groundplane[0]
    shadowMat[1][2] = 0 - lightpos[2] * groundplane[1]
    shadowMat[2][2] = dot - lightpos[2] * groundplane[2]
    shadowMat[3][2] = 0 - lightpos[2] * groundplane[3]

    shadowMat[0][3] = 0 - lightpos[3] * groundplane[0]
    shadowMat[1][3] = 0 - lightpos[3] * groundplane[1]
    shadowMat[2][3] = 0 - lightpos[3] * groundplane[2]
    shadowMat[3][3] = dot - lightpos[3] * groundplane[3]

def calculate_plane_from_points(v0, v1, v2):
    vec0 = [v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]]
    vec1 = [v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]]
    plane = [-1, -1, -1, -1]
    plane[0] = vec0[1] * vec1[2] - vec0[2] * vec1[1]
    plane[1] = -(vec0[0] * vec1[2] - vec0[2] * vec1[0])
    plane[2] = vec0[0] * vec1[1] - vec0[1] * vec1[0]
    plane[3] = -(plane[0] * v0[0] + plane[1] * v0[1] + plane[2] * v0[2])
    return plane

def displayFigures():
    for i in range(len(colors)):
        color = colors[i]
        glPushMatrix()
        glTranslatef(*coords[i])
        glScalef(sizes[i], sizes[i], sizes[i])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        
        glEnable(GL_NORMALIZE)
        if figuretype[i] == "Sphere":
            glutSolidSphere(sizes[i] * 0.1, 50, 50)
        elif figuretype[i] == "Piramid":
            glutSolidTetrahedron()

        glDisable(GL_NORMALIZE)
        glPopMatrix()


def displayFloor():
    glDisable(GL_LIGHTING)
    glBegin(GL_QUADS)
    glVertex3fv(floor_coordinates[0])
    glVertex3fv(floor_coordinates[1])
    glVertex3fv(floor_coordinates[2])
    glVertex3fv(floor_coordinates[3])
    glEnd()
    glEnable(GL_LIGHTING)


def updateScene():
    if (stencilReflection and renderReflection) or (stencilShadow and renderShadow):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
    else:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    lightPosition[0] = 12 * cos(lightAngle)
    lightPosition[1] = lightHeight
    lightPosition[2] = 12 * sin(lightAngle)
    lightPosition[3] = 1.0

    calculate_shadow_matrix(floorShadow, floorPlane, lightPosition)

    glPushMatrix()
    glRotatef(angle2, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

    if renderReflection:
        if stencilReflection:
            glDisable(GL_DEPTH_TEST)
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
            glEnable(GL_STENCIL_TEST)
            glStencilOp(GL_REPLACE, GL_REPLACE, GL_REPLACE)
            glStencilFunc(GL_ALWAYS, 1, 0xffffffff)
            displayFloor()

            glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
            glEnable(GL_DEPTH_TEST)

            glStencilFunc(GL_EQUAL, 1, 0xffffffff)
            glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)

        glPushMatrix()

        glScalef(1.0, -1.0, 1.0)

        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

        glEnable(GL_NORMALIZE)
        glCullFace(GL_FRONT)

        displayFigures()

        glDisable(GL_NORMALIZE)
        glCullFace(GL_BACK)

        glPopMatrix()

        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

        if stencilReflection:
            glDisable(GL_STENCIL_TEST)

    glFrontFace(GL_CW)
    glColor4f(0.1, 0.1, 0.7, 1.0)
    displayFloor()
    glFrontFace(GL_CCW)

    if renderShadow:
        if stencilShadow:
            glEnable(GL_STENCIL_TEST)
            glStencilFunc(GL_ALWAYS, 3, 0xffffffff)
            glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.7, 0.0, 0.0, 0.3)
    glColor4f(1.0, 1.0, 1.0, 0.3)
    displayFloor()
    glDisable(GL_BLEND)

    if renderFigure:
        displayFigures()

    if renderShadow:
        if stencilShadow:
            glStencilFunc(GL_LESS, 2, 0xffffffff)
            glStencilOp(GL_REPLACE, GL_REPLACE, GL_REPLACE)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_LIGHTING)
        glColor4f(0.0, 0.0, 0.0, 0.5)

        glPushMatrix()
        glMultMatrixf(floorShadow)
        displayFigures()
        glPopMatrix()

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

    if stencilShadow:
        glDisable(GL_STENCIL_TEST)

    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 0.0)

    glEnable(GL_LIGHTING)
    glPopMatrix()

    glPopMatrix()

    if reportSpeed:
        glFinish()
    glutSwapBuffers()


def handleMouseMotion(button: int, state: int, x: int, y: int):
    global moving, startx, starty, lightMoving, lightStartY, lightStartX
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            moving = 1
            startx = x
            starty = y
        if state == GLUT_UP:
            moving = 0


def handleMotion(x: int, y: int):
    global lightAngle, lightHeight, angle, startx, starty, lightStartX, lightStartY, angle2
    if moving:
        angle = angle + (x - startx)
        angle2 = angle2 + (y - starty)
        startx = x
        starty = y
    if lightMoving:
        lightAngle += (x - lightStartX) / 40.0
        lightHeight += (lightStartY - y) / 20.0
        lightStartX = x
        lightStartY = y
        
    glutPostRedisplay()

def handleAnimation():
    global lightAngle
    if not lightMoving:
        lightAngle += 0.01
    glutPostRedisplay()


def handleLightControl(value: int):
    global renderFigure, animation, lightSwitch, useTexture, renderShadow, renderReflection, renderFigure, \
        reportSpeed
    if value == CHANGE_LIGHT:
        animation = 1 - animation
        if animation:
            glutIdleFunc(handleAnimation)
        else:
            glutIdleFunc(None)
    elif value == SHOW_FIGURES:
        renderFigure = 1 - renderFigure
        renderShadow = 1 - renderShadow
        renderReflection = 1 - renderReflection
    glutPostRedisplay()
    return value


def handleVisibility(vis: int):
    if vis == GLUT_VISIBLE:
        if animation:
            glutIdleFunc(handleAnimation)
    else:
        if not animation:
            glutIdleFunc(NULL)


def handleKeyCommands(key, x, y):
    global renderFigure, animation, lightSwitch, useTexture, renderShadow, renderReflection, renderFigure, \
        reportSpeed, ableFloor, lightMoving
    if key == b'1':
        animation = 1 - animation
        if animation:
            glutIdleFunc(handleAnimation)
        else:
            glutIdleFunc(None)
    elif key == b'2':
        lightSwitch = not lightSwitch
        if lightSwitch:
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)
    elif key == GLUT_KEY_F5:
        renderReflection = 1 - renderReflection
    elif key == b'3':
        renderFigure = 1 - renderFigure
        renderShadow = 1 - renderShadow
        renderReflection = 1 - renderReflection
    elif key == b'4':
        ableFloor = not ableFloor
        if ableFloor:
            glEnable(GL_CULL_FACE)
        else:
            glDisable(GL_CULL_FACE) 
    glutPostRedisplay()

glutInit()
glutInitWindowSize(width, height)
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL | GLUT_MULTISAMPLE)

read_coordinates("Лясковська/lab4/data2.txt")

glutCreateWindow("OpenGL Test project")

glutDisplayFunc(updateScene)
glutMouseFunc(handleMouseMotion)
glutMotionFunc(handleMotion)
glutVisibilityFunc(handleVisibility)
glutKeyboardFunc(handleKeyCommands)
glutSpecialFunc(handleKeyCommands)
glLineWidth(3.0)

glMatrixMode(GL_PROJECTION)
gluPerspective(40.0, 1.0, 20.0, 100.0)
glMatrixMode(GL_MODELVIEW)
gluLookAt(0.0, 16.0, 60.0, 0.0, 8.0, 0.0, 0.0, 1.0, 0.)

glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, 1)
glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)

floorPlane = calculate_plane_from_points( floor_coordinates[1], floor_coordinates[2], floor_coordinates[3])
glutMainLoop()