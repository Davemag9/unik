from OpenGL.GL import *
from OpenGL.GLUT import *

def draw_grid(size=10, step=1):
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)

    for i in range(-size, size + step, step):
        # Lines along X-axis
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)

        # Lines along Z-axis
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)

    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_grid()

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Grid")

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()

if __name__ == "__main__":
    main()
