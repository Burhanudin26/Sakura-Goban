import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

## Definisi verteks-verteks untuk membuat kubus 3D
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

class Board:
    def __init__(self):
        self.vertices = verticies
        self.surfaces = surfaces
        self.coords = coords  # Add this line for texture coordinates
        self.normals = normals

    def draw(self, texture):
        glBindTexture(GL_TEXTURE_2D, texture)                   # mengikat ID tekstur yang akan digunakan saat menggambar kubus dengan tekstur.
        glBegin(GL_QUADS)                                       # Memulai menggambar dengan jenis poligon GL_QUADS
        for i_surface, surface in enumerate(surfaces):          # Loop melalui permukaan (surfaces) kubus
            glNormal3fv(normals[i_surface])                     # Mengatur vektor normal untuk permukaan saat ini
            for vertex in surface:                              # Loop melalui verteks-verteks dalam permukaan saat ini
                glTexCoord2fv(coords[surface.index(vertex)])    # Mengatur koordinat tekstur untuk verteks saat ini
                glVertex3fv(verticies[vertex])                  # Menggambar verteks dalam koordinat 3D
        glEnd()                                                 # Selesai menggambar poligon


    def load_texture(self):
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
        
    def show(self):  # Receive textureId as an argument
        glPushMatrix()
        self.draw(self.load_texture())  # Pass textureId to the draw method
        glPopMatrix()
        

class App:
    def __init__(self):
        material_ambient = (0.1, 0.1, 0.1, 1.0)  # Sifat ambient material
        material_diffuse = (0.7, 0.7, 0.7, 1.0)  # Sifat diffuse material
        material_specular = (0.5, 0.5, 0.5, 1)  # Sifat specular material
        
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)  # Mengaktifkan uji kedalaman
        glEnable(GL_COLOR_MATERIAL)  # Mengaktifkan bahan warna
        glEnable(GL_LIGHTING)  # Mengaktifkan pencahayaan
        glEnable(GL_LIGHT0)  # Mengaktifkan cahaya 0
        glEnable(GL_BLEND)  # Mengaktifkan blending

        # Mengatur properti material
        glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)

        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Mengatur perspektif
        glTranslatef(0.0, 0.2, -5.0)  # Menggeser objek dalam sumbu Z negatif
        glRotatef(180, 0, 0, 1)  # Memutar objek 180 derajat sekitar sumbu Z
        glRotatef(-60, 1, 0, 0) 
        glRotatef(0, 0, 1, 0) 
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 0, 0))  # Mengatur posisi cahaya

        self.board = Board()
        self.frame_rate = 0  # Initialize frame rate
        
    def run(self):
        clock = pygame.time.Clock()  # Create a clock object for tracking time
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.board.show()
            pygame.display.flip()

            # Calculate and set frame rate in window title
            self.frame_rate = int(clock.get_fps())
            pygame.display.set_caption(f"3D board | Frame Rate: {self.frame_rate}")

            clock.tick(60)  # Set the frame rate to 60 frames per second

if __name__ == "__main__":
    app = App()
    app.run()