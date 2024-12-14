from OpenGL.GL import *
from OpenGL.GLUT import *

class Line:
    def __init__(self, coord1, coord2):
        self.line = (coord1, coord2)

lines = []
old_lines = []

start_point = None
end_point = None

current_color = (1.0, 1.0, 1.0)


def mouse_click(button, state, x, y):
    global start_point, end_point

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x = 2.0 * x / 1000 - 1.0 
        y = 1.0 - 2.0 * y / 800
        z = 0.0

        if start_point is None:
            start_point = (x, y, z)
        else:
            end_point = (x, y, z)
            lines.append(Line(coord1=start_point, coord2=end_point))
            start_point = None
            end_point = None

        glutPostRedisplay()


def move_lines(dx, dy):
    global lines
    for elem in lines:
        elem.line = ((elem.line[0][0] + dx, elem.line[0][1] + dy, elem.line[0][2]),
                     (elem.line[1][0] + dx, elem.line[1][1] + dy, elem.line[1][2]))


def swap_set(key, x, y):
    global lines
    global old_lines
    global current_color
    if key == b' ':
        old_lines.append(lines)
        lines = [] 
        current_color = (1.0, 1.0, 1.0)

    if key == b'r':
        current_color = (1.0, 0.0, 0.0)
    elif key == b'g':
        current_color = (0.0, 1.0, 0.0)
    elif key == b'b':
        current_color = (0.0, 0.0, 1.0)

    if key == b'z':
        if len(lines) > 0:
                lines = lines[:-1]
    
    if key == b'n':
        lines = []
    glutPostRedisplay()


def change_xyz(key, x, z):
    if key == GLUT_KEY_LEFT:
        move_lines(-0.1, 0.0)
    elif key == GLUT_KEY_RIGHT:
        move_lines(0.1, 0.0)
    elif key == GLUT_KEY_UP:
        move_lines(0.0, 0.1)
    elif key == GLUT_KEY_DOWN:
        move_lines(0.0, -0.1)
    
    glutPostRedisplay()


def draw_line(start, end):
    glBegin(GL_LINES)
    glVertex3fv(start)
    glVertex3fv(end)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for elemelem in old_lines: 
        for elem in elemelem:
            glLineWidth(2.0)
            draw_line(elem.line[0], elem.line[1])

    global current_color
    glColor3fv(current_color)
    
    for elem in lines: 
        glLineWidth(5.0)
        draw_line(elem.line[0], elem.line[1])

    glColor3fv((1.0, 1.0, 1.0))

    glutSwapBuffers()
    
def create_menu():
    menu = glutCreateMenu(menu_handler)
    glutAddMenuEntry("Space - create new set", 1)
    glutAddMenuEntry("R - set color as red", 2)
    glutAddMenuEntry("G - set color as green", 3)
    glutAddMenuEntry("B - set color as blue", 4)
    glutAddMenuEntry("Z - delete last line", 5)
    glutAddMenuEntry("N - delete last set", 6)
    glutAddMenuEntry("Up - actually Up", 7)
    glutAddMenuEntry("Down - actually Down", 8)
    glutAddMenuEntry("Left - actually Left", 9)
    glutAddMenuEntry("Right - actually Right", 10)
    glutAttachMenu(GLUT_RIGHT_BUTTON)
        

def menu_handler(value):
    global lines
    global old_lines
    global current_color

    if value == 1:
        old_lines.append(lines)
        lines = [] 
        current_color = (1.0, 1.0, 1.0)
    elif value == 2:
        current_color = (1.0, 0.0, 0.0)
    elif value == 3:
        current_color = (0.0, 1.0, 0.0)
    elif value == 4:
        current_color = (0.0, 0.0, 1.0)
    elif value == 5:
        if len(lines) > 0:
            lines = lines[:-1]
    elif value == 6:
        lines = []
    elif value == 7:
        move_lines(0.0, 0.1)
    elif value == 8:
        move_lines(0.0, -0.1)
    elif value == 9:
        move_lines(-0.1, 0.0)
    elif value == 10:
        move_lines(0.1, 0.0)


    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1000, 800)
    glutCreateWindow("OpenGL Line Drawing")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glLineWidth(5.0)

    glutMouseFunc(mouse_click)
    glutKeyboardFunc(swap_set)
    glutSpecialFunc(change_xyz)
    glutDisplayFunc(display)

    create_menu()

    glutMainLoop()

if __name__ == "__main__":
    main()