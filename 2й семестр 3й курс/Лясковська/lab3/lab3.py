from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import numpy as np

all_gran = []
triangle1 = []
triangle2 = []
size = 1.5
angles = [0., 0., 0.]
delta = 5

ALEG = False
frame = False
render_normals = False
texture = None
texure_on = False

SHADOW_WIDTH = 1000
SHADOW_HEIGHT = 800
light_pos = (-2.0, -2.0, -2.0, 1.0)
depth_map_fbo = None
depth_map = None

def TexFromPNG():
    texture_image = Image.open("Лясковська/lab3/sand.jpg")
    texture_data = texture_image.tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_image.width, texture_image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    
    return texture_id

def read_vertices_from_file(path):
    with open(path, 'r') as file:
        triangle = [list(map(float, line.split())) for line in file]
    return triangle

def inputt(key, x, y):
    global angles, ALEG, frame, render_normals, texure_on
    if key == b'1':
        angles[1] += delta
    elif key == b'2':
        angles[1] -= delta
    elif key == b'3':
        angles[0] += delta
    elif key == b'4':
        angles[0] -= delta
    elif key == b'5':
        angles[2] += delta
    elif key == b'6':
        angles[2] -= delta
    elif key == b'p':
        ALEG = not ALEG
    elif key == b'f':
        frame = not frame
    elif key == b'n':
        render_normals = not render_normals
    elif key == b't':
        texure_on = not texure_on

    glutPostRedisplay()


def calculate_normal(vertices):
        v0 = np.array(vertices[0])
        v1 = np.array(vertices[1])
        v2 = np.array(vertices[2])
        normal = np.cross(v1 - v0, v2 - v0)
        normalized_normal = normal / np.linalg.norm(normal)
        return normalized_normal
    
def draw_normal(vertices, normal, multiplier):
    glBegin(GL_LINES)
    centroid = np.mean(vertices, axis=0)
    vertex = centroid * multiplier
    glVertex3fv(vertex)
    glVertex3fv(normal)
    glEnd()

def display():
    render()
    glViewport(0, 0, 1000, 800)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if ALEG:
        gluPerspective(90, 1000 / 800, 0.1, 100)
    elif not ALEG:
        glOrtho(-10, 10, -10, 10, 1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -10) 
    
    glRotatef(angles[0], 1, 0, 0)
    glRotatef(angles[1], 0, 1, 0)
    glRotatef(angles[2], 0, 0, 1)

    if texure_on:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)

        for item in all_gran:
            normal = list(calculate_normal(item))
            if render_normals:
                draw_normal(item, normal, 2)
        
            glBegin(GL_POLYGON)
            for i in range(len(item)):
                if i == 0:
                    glTexCoord2f(0.0, 0.0)
                elif i == 1:
                    glTexCoord2f(1.0, 0.0)
                elif i == 2:
                    glTexCoord2f(1.0, 1.0)
                elif i == 3:
                    glTexCoord2f(0.0, 1.0)
                
                glVertex3fv(item[i])
            glEnd()
    else:
        if frame:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            for item in all_gran:
                normal = list(calculate_normal(item))
                if render_normals:
                    draw_normal(item, normal, 2)

                glBegin(GL_LINE_LOOP)
                for i in range(len(item)):
                    glVertex3fv(item[i])
                glEnd()
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            for item in all_gran:
                normal = list(calculate_normal(item))
                if render_normals:
                    draw_normal(item, normal, 2)
                glBegin(GL_POLYGON)
                for i in range(len(item)):
                    glVertex3fv(item[i])
                glEnd()
    
    glDisable(GL_TEXTURE_2D)

    glutSwapBuffers()


def render():
    glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
    glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10, 10, -10, 10, 1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(light_pos[0], light_pos[1], light_pos[2], 0, 0, 0, 0, 1, 0)
    for item in all_gran:
        glBegin(GL_POLYGON)
        for i in range(len(item)):
            glVertex3fv(item[i])
        glEnd()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)


def setup():
    global light_pos
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [25.0] )

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)  

def init():
    global depth_map_fbo, depth_map
    depth_map_fbo = glGenFramebuffers(1)
    depth_map = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, depth_map)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1.0, 1.0, 1.0, 1.0])
    glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)
    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

def main():
    global all_gran, triangle1, triangle2, texture

    triangle1 = read_vertices_from_file('Лясковська/lab3/test_vertices')
    triangle2 = read_vertices_from_file('Лясковська/lab3/test_vertices')
    for elem in triangle1:
        elem.append(-size)

    for elem in triangle2:
        elem.append(size)
    for i in range(3):
        tmp = []
        tmp.append(triangle1[i])
        tmp.append(triangle2[i])
        tmp.append(triangle2[(i + 1)%3])
        tmp.append(triangle1[(i + 1)%3])
        all_gran.append(tmp)
    all_gran.append(triangle1)
    all_gran.append(triangle2)

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(1000, 800)

    glutInit(sys.argv)
    glutCreateWindow(b"1234567890")
    texture = TexFromPNG() 
    glutDisplayFunc(display)
    glutKeyboardFunc(inputt)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glDepthFunc(GL_LESS)
    setup()
    init()

    glutMainLoop()

if __name__ == '__main__':
    main()