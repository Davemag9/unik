from OpenGL.GL import *
from OpenGL.GLUT import *

triangles = []
old_triangles = []
v1 = None
v2 = None
v3 = None 

current_color = (1.0, 1.0, 1.0)

def draw_triangle(a, b, c):
    glBegin(GL_TRIANGLES)
    glVertex3f(*a)
    glVertex3f(*b)
    glVertex3f(*c)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    global triangles, old_triangles

    for elemelem in old_triangles: 
        for elem in elemelem:
            glLineWidth(2.0)
            glColor3fv((0.5, 0.5, 0.5))
            draw_triangle(a=elem[0], b=elem[1], c=elem[2])

    global current_color
    glColor3fv(current_color)

    for elem in triangles:
        draw_triangle(a=elem[0], b=elem[1], c=elem[2])
    
    # glColor3fv((1.0, 1.0, 1.0))
    
    glutSwapBuffers()


def mouse_click(button, state, x, y):
    global v1, v2, v3, triangles

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x = 2.0 * x / 1000 - 1.0 
        y = 1.0 - 2.0 * y / 800
        z = 0.0

        if v1 is not None and v2 is not None:
            v3 = (x, y, z)
            triangles.append([v1, v2, v3])
            v1 = None
            v2 = None
            v3 = None

        elif v1 is not None and v3 is None:
            v2 = (x, y, z)
        else:
            v1 = (x, y, z)


        glutPostRedisplay()

def keyboard_click(key, x, y):
    global triangles, old_triangles, current_color

    if key == b' ':
        old_triangles.append(triangles)
        triangles = [] 
        current_color = (1.0, 1.0, 1.0)

    if key == b'r':
        current_color = (1.0, 0.0, 0.0)
    elif key == b'g':
        current_color = (0.0, 1.0, 0.0)
    elif key == b'b':
        current_color = (0.0, 0.0, 1.0)

    if key == b'z':
        if len(triangles) > 0:
                triangles = triangles[:-1]
    if key == b'n':
        triangles = []
        
    glutPostRedisplay()

 

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1000, 800)
    glutCreateWindow("OpenGL Line Drawing")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glLineWidth(5.0)

    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard_click)
    glutDisplayFunc(display)

    glutMainLoop()

if __name__ == "__main__":
    main()
