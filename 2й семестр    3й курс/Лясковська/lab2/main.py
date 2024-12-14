import sys
import math
import random
from OpenGL.GL import *
from numpy import arctan
from OpenGL.GLUT import *
from math import cos, pi, sin, sqrt


from PIL import Image
def TexFromPNG(link):
    texture_image = Image.open(link)
    texture_data = texture_image.tobytes()
    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_image.width, texture_image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    
    return texture_id


textures = []
active_object = None
objects = []
current_color = [0.0, 0.0, 0.0]

start_point = None
end_point = None
grid = 0
grid_size = 10
mixer = 0
only_border = 0


def draw_pentagon(color, radius, x, y, angle, texture):

    if mixer != 0:
        glEnable(GL_COLOR_LOGIC_OP)
        if mixer == 1:
            glLogicOp(GL_AND) 
        else:
            glLogicOp(GL_NAND)
    else:
        glDisable(GL_COLOR_LOGIC_OP)

    if only_border:
        glBegin(GL_LINE_LOOP)
        for i in range(5):
            theta = pi + angle + 2.0 * pi * i / 5
            x_pos = x + radius * cos(theta)
            y_pos = y + radius * sin(theta)
            glVertex2f(x_pos, y_pos)
        glEnd()
    else:
        if texture != None:
            glEnable(GL_TEXTURE_2D)
            glColor3fv(color)
            glBindTexture(GL_TEXTURE_2D, texture)
            glBegin(GL_POLYGON)
        
            for i in range(5):
                theta = pi + angle + 2.0 * pi * i / 5

                xt = 0.5 + 0.5 * cos(theta)
                yt = 0.5 + 0.5 * sin(theta)
                glTexCoord2f(xt, yt)

                x_pos = x + radius * cos(theta)
                y_pos = y + radius * sin(theta)
                glVertex2f(x_pos, y_pos)

            glEnd()
            glDisable(GL_TEXTURE_2D)
        else:
            glBegin(GL_POLYGON)
            glColor3fv(color)
            for i in range(5):
                theta = pi + angle + 2.0 * pi * i / 5
                x_pos = x + radius * cos(theta)
                y_pos = y + radius * sin(theta)
                glVertex2f(x_pos, y_pos)
            glEnd()

    
def draw_grid(size):
    glColor3f(0.5, 0.5, 0.5) 
    glLineWidth(1.0)
    glBegin(GL_LINES)
    for i in range(-size, size + 1):
        glVertex2f(i / size, -1)
        glVertex2f(i / size, 1)
        glVertex2f(-1, i / size)
        glVertex2f(1, i / size)
    glEnd()
    

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for object in objects:    
        draw_pentagon(object[0], object[1], object[2], object[3], object[4], object[5])

    if grid:
        draw_grid(grid_size)

    glutSwapBuffers()


def mouse_click(button, state, x, y):
    global current_color, start_point, end_point
    global objects, active_object
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x = 2.0 * x / glutGet(GLUT_WINDOW_WIDTH) - 1.0
        y = 1.0 - 2.0 * y / glutGet(GLUT_WINDOW_HEIGHT)
        check = False

        if start_point == None:
            for i in range(len(objects)):
                dist = sqrt((objects[i][2] - x)**2 + (objects[i][3] - y)**2)
                if dist < objects[i][1]:
                    active_object = i
                    check = True
        
        if not check or not objects:
            if start_point is None:
                start_point = (x, y)
            else:
                end_point = (x, y)
                objects.append([current_color, sqrt((start_point[0] - x)**2 + (start_point[1] - y)**2),
                            start_point[0], start_point[1], 
                            math.atan2(start_point[1] - y, start_point[0] - x ), None])
                active_object = len(objects) - 1
                start_point = None
                end_point = None
        glutPostRedisplay()


def rotate_object(da):
    global objects
    objects[active_object][4] += da


def scale_object(dr):
    global objects
    objects[active_object][1] += dr


def key_click(key, x, y):
    global objects, grid_size, grid, mixer, only_border
    if key == b'c':
        if active_object != None:
            objects[active_object][0] = [random.random(), random.random(), random.random()]
    elif key == b'r':
        rotate_object(-pi/18.0)
    elif key == b'l':
        rotate_object(+pi/18.0)
    elif key == b'=':
        scale_object(+0.1)
    elif key == b'-':
        scale_object(-0.1)
    elif key == b'_':
        if grid_size > 10:
            grid_size -= 10
    elif key == b'+':
        grid_size += 10
    elif key == b'g':
        if grid == 0:
            grid_size = 10
        grid = not grid
    elif key == b'0':
        mixer = 0
    elif key == b'1':
        mixer = 1
    elif key == b'2':
        mixer = 2
    elif key == b'f':
        only_border = not only_border
    elif key == b't':
        if objects[active_object][5] == None:
            objects[active_object][5] = textures[0]
        else:
            objects[active_object][5] = None
        
    glutPostRedisplay()


def move_object(dx, dy):
    global objects
    objects[active_object][2] += dx
    objects[active_object][3] += dy


def move_active_object(key, x, z):
    if key == GLUT_KEY_LEFT:
        move_object(-0.1, 0.0)
    elif key == GLUT_KEY_RIGHT:
        move_object(0.1, 0.0)
    elif key == GLUT_KEY_UP:
        move_object(0.0, 0.1)
    elif key == GLUT_KEY_DOWN:
        move_object(0.0, -0.1)
    
    glutPostRedisplay()


def menu_handler(value, x = None, y = None):
    global current_color
    match value:
        case 0:
            key_click(b'c', x, y)
        case 1:
            key_click(b't', x, y)
        case 2:
            key_click(b'f', x, y)
        case 3:
            key_click(b'=', x, y)
        case 4:
            key_click(b'-', x, y)
        case 5:
            key_click(b'l', x, y)
        case 6:
            key_click(b'r', x, y)
        case 7:
            move_active_object(GLUT_KEY_UP, x, y)
        case 8:
            move_active_object(GLUT_KEY_DOWN, x, y)
        case 9:
            move_active_object(GLUT_KEY_LEFT, x, y)
        case 10:
            move_active_object(GLUT_KEY_RIGHT, x, y)
        case 11:
            key_click(b'g', x, y)
        case 12:
            key_click(b'+', x, y)
        case 13:
            key_click(b'_', x, y)
        case 14:
            key_click(b'0', x, y)
        case 15:
            key_click(b'1', x, y)
        case 16:
            key_click(b'2', x, y)

    glutPostRedisplay()


def create_menu():
    menu = glutCreateMenu(menu_handler)
    glutAddMenuEntry("c - change color", 0)
    glutAddMenuEntry("t - texture on active object", 1)
    glutAddMenuEntry("f - fill active object", 2)

    glutAddMenuEntry("= - scale object Up", 3)
    glutAddMenuEntry("- - scale object Down", 4)
    glutAddMenuEntry("l - rotate Left", 5)
    glutAddMenuEntry("r - rotate Right", 6)

    glutAddMenuEntry("Up - actually Up", 7)
    glutAddMenuEntry("Down - actually Down", 8)
    glutAddMenuEntry("Left - actually Left", 9)
    glutAddMenuEntry("Right - actually Right", 10)

    glutAddMenuEntry("g - enable/disable grid", 11)
    glutAddMenuEntry("+ - scale grid Up", 12)
    glutAddMenuEntry("_ - scale grid Down", 13)

    glutAddMenuEntry("0 - no color mix", 14)
    glutAddMenuEntry("1 - AND color mix", 15)
    glutAddMenuEntry("2 - NAND color mix", 16)

    glutAttachMenu(GLUT_RIGHT_BUTTON)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1000, 800)
    glutCreateWindow("OpenGL Mouse Click Example")

    global textures
    textures.append(TexFromPNG("Лясковська/lab2/images/image.jpg"))
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glOrtho(-1, 1, -1, 1, -1, 1)
    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(key_click)
    glutSpecialFunc(move_active_object)

    create_menu()
    glutMainLoop()


if __name__ == "__main__":
    main()