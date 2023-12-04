import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


verticies = (
    (2, 0.2, 2),   # 0
    (-2, 0.2, 2),  # 1
    (-2, -0.2, 2),  # 2
    (2, -0.2, 2),  # 3
    (2, 0.2, -2),  # 4
    (-2, 0.2, -2),  # 5
    (-2, -0.2, -2),  # 6
    (2, -0.2, -2),  # 7
)

# Definisi permukaan (surfaces) kubus
surfaces = (
    (0, 1, 2, 3),  # surface 0
    (4, 5, 6, 7),  # surface 1
    (0, 3, 7, 4),  # surface 2
    (1, 2, 6, 5),  # surface 3
    (0, 1, 5, 4),  # surface 4
    (3, 2, 6, 7),  # surface 5
)

# Normal vektor untuk masing-masing permukaan kubus
normals = [
    (0, 0, -1),  # surface 0
    (0, 0, 1),   # surface 1
    (-1, 0, 0),  # surface 2
    (1, 0, 0),   # surface 3
    (0, -1, 0),  # surface 4
    (0, 1, 0)    # surface 5
]

# Koordinat tekstur untuk masing-masing verteks 
coords = [
    (0, 0), #0
    (1, 0), #1
    (1, 1), #2
    (0, 1) #3
]

def draw_grid():
    glLineWidth(3.0)

    glBegin(GL_LINES)
    for i in range(-9, 10):
        # Draw lines along the x-axis
        glVertex3f(i, 0, -9)
        glVertex3f(i, 0, 9)

        # Draw lines along the z-axis
        glVertex3f(-9, 0, i)
        glVertex3f(9, 0, i)
    glEnd()

def draw_board(texture):
    glBindTexture(GL_TEXTURE_2D, texture)                   # mengikat ID tekstur yang akan digunakan saat menggambar kubus dengan tekstur.
    glBegin(GL_QUADS)                                       # Memulai menggambar dengan jenis poligon GL_QUADS
    for i_surface, surface in enumerate(surfaces):          # Loop melalui permukaan (surfaces) kubus
        glNormal3fv(normals[i_surface])                     # Mengatur vektor normal untuk permukaan saat ini
        for vertex in surface:                              # Loop melalui verteks-verteks dalam permukaan saat ini
            glTexCoord2fv(coords[surface.index(vertex)])    # Mengatur koordinat tekstur untuk verteks saat ini
            glVertex3fv(verticies[vertex])                  # Menggambar verteks dalam koordinat 3D
    glEnd()                                                 # Selesai menggambar poligon


def load_texture_board():
    textureSurface = pygame.image.load('board.jpeg')                                                # Memuat gambar tekstur dari file 'texture_mipmap.png'
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)                                          # Mengambil data tekstur sebagai string dengan format RGBA
    # Mendapatkan lebar dan tinggi tekstur
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)                                                                                 # Mengaktifkan penggunaan tekstur dalam mode OpenGL
    textureId = glGenTextures(1)                                                                            # Membuat ID tekstur 
    glBindTexture(GL_TEXTURE_2D, textureId)                                                                 # mengikat ID tekstur yang baru dibuat (textureId) ke target GL_TEXTURE_2D.
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)       # Mengisi data tekstur ke dalam buffer OpenGL

    # Fungsi untuk mengatur filter tekstur menjadi GL_LINEAR
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Pengaturan filter magnifikasi
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Pengaturan filter minifikasi

    return textureId
        
def show_board():  # Receive textureId as an argument
    glPushMatrix()
    glScalef(0.2,0.2,0.2)
    glTranslatef(0,1,0)
    glColor3f(0,0,0)
    draw_grid()
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(1,1,1)
    draw_board(load_texture_board())  # Pass textureId to the draw method
    glPopMatrix()

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 1280, 720
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL | pygame.RESIZABLE)
    pygame.display.set_caption("OpenGL in Pygame")

    glEnable(GL_DEPTH_TEST)  # Mengaktifkan uji kedalaman
    glEnable(GL_BLEND)  # Mengaktifkan blending
    # Set up the perspective projection matrix
    gluPerspective(30, (width / height), 0.1, 50.0)

    # Camera Control
    glTranslatef(0.0, 0.1, -8)
    glRotatef(70, 1,0,0)
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Clear the screen and the depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        show_board()
        # Update the display
        pygame.display.flip()
        pygame.time.wait(10)
main()