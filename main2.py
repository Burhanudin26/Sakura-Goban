import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

BACKGROUND = 'ramin2.jpg'  # Nama file gambar latar belakang
BOARD_SIZE = (820, 820)  # Ukuran papan
WHITE = (255, 255, 255)  # Warna putih
BLACK = (0, 0, 0)  # Warna hitam

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

surfaces = (
    (0, 1, 2, 3),  # surface 0
    (4, 5, 6, 7),  # surface 1
    (0, 3, 7, 4),  # surface 2
    (1, 2, 6, 5),  # surface 3
    (0, 1, 5, 4),  # surface 4
    (3, 2, 6, 7),  # surface 5
)

normals = [
    (0, 0, -1),  # surface 0
    (0, 0, 1),   # surface 1
    (-1, 0, 0),  # surface 2
    (1, 0, 0),   # surface 3
    (0, -1, 0),  # surface 4
    (0, 1, 0)    # surface 5
]

coords = [
    (0, 0),  # 0
    (1, 0),  # 1
    (1, 1),  # 2
    (0, 1)   # 3
]


class Stone(object):
    def __init__(self, board, point, color):
        self.board = board
        self.point = point
        self.color = color
        self.group = self.find_group()
        self.coords = (5 + self.point[0] * 40, 5 + self.point[1] * 40)
        self.draw()

    def draw(self):
        pygame.draw.circle(screen, self.color, self.coords, 20, 0)
        pygame.display.update()

    def remove(self):
        blit_coords = (self.coords[0] - 20, self.coords[1] - 20)
        area_rect = pygame.Rect(blit_coords, (40, 40))
        screen.blit(background, blit_coords, area_rect)
        pygame.display.update()
        self.group.stones.remove(self)
        del self

    @property
    def neighbors(self):
        neighboring = [(self.point[0] - 1, self.point[1]),
                       (self.point[0] + 1, self.point[1]),
                       (self.point[0], self.point[1] - 1),
                       (self.point[0], self.point[1] + 1)]
        neighboring = [point for point in neighboring if 0 < point[0] < 20 and 0 < point[1] < 20]
        return neighboring

    @property
    def liberties(self):
        liberties = self.neighbors
        stones = self.board.search(points=self.neighbors)
        for stone in stones:
            liberties.remove(stone.point)
        return liberties

    def find_group(self):
        groups = []
        stones = self.board.search(points=self.neighbors)
        for stone in stones:
            if stone.color == self.color and stone.group not in groups:
                groups.append(stone.group)
        if not groups:
            group = Group(self.board, self)
            return group
        else:
            if len(groups) > 1:
                for group in groups[1:]:
                    groups[0].merge(group)
            groups[0].stones.append(self)
            return groups[0]

    def __str__(self):
        return 'ABCDEFGHJKLMNOPQRST'[self.point[0]-1] + str(20-(self.point[1]))


class Group(object):
    def __init__(self, board, stone):
        self.board = board
        self.board.groups.append(self)
        self.stones = [stone]
        self.liberties = None

    def merge(self, group):
        for stone in group.stones:
            stone.group = self
            self.stones.append(stone)
        self.board.groups.remove(group)
        del group

    def remove(self):
        while self.stones:
            self.stones[0].remove()
        self.board.groups.remove(self)
        del self

    def update_liberties(self):
        liberties = []
        for stone in self.stones:
            for liberty in stone.liberties:
                liberties.append(liberty)
        self.liberties = set(liberties)
        if len(self.liberties) == 0:
            self.remove()

    def __str__(self):
        return str([str(stone) for stone in self.stones])


class Board:
    def __init__(self):
        self.vertices = verticies
        self.surfaces = surfaces
        self.coords = coords
        self.normals = normals
        self.groups = []
        self.next = BLACK
        self.outline = pygame.Rect(45, 45, 720, 720)
        self.draw()

    def search(self, point=None, points=[]):
        stones = []
        for group in self.groups:
            for stone in group.stones:
                if stone.point == point and not points:
                    return stone
                if stone.point in points:
                    stones.append(stone)
        return stones

    def turn(self):
        if self.next == BLACK:
            self.next = WHITE
            return BLACK
        else:
            self.next = BLACK
            return WHITE

    def draw(self):
        pygame.draw.rect(background, BLACK, self.outline, 3)
        self.outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pygame.Rect(45 + (40 * i), 45 + (40 * j), 40, 40)
                pygame.draw.rect(background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                coords = (165 + (240 * i), 165 + (240 * j))
                pygame.draw.circle(background, BLACK, coords, 5, 0)

        glBindTexture(GL_TEXTURE_2D, self.load_texture())
        glBegin(GL_QUADS)
        for i_surface, surface in enumerate(self.surfaces):
            glNormal3fv(self.normals[i_surface])
            for vertex in surface:
                glTexCoord2fv(self.coords[surface.index(vertex)])
                glVertex3fv(self.vertices[vertex])
        glEnd()

        screen.blit(background, (0, 0))

    def update_liberties(self, added_stone=None):
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()

    def load_texture(self):
        texture_surface = pygame.image.load('board.jpeg')
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)

        width = texture_surface.get_width()
        height = texture_surface.get_height()

        glEnable(GL_TEXTURE_2D)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return texture_id

    def show(self):
        glPushMatrix()
        self.draw()
        glPopMatrix()


class App:
    def __init__(self):
        material_ambient = (0.1, 0.1, 0.1, 1.0)
        material_diffuse = (0.7, 0.7, 0.7, 1.0)
        material_specular = (0.5, 0.5, 0.5, 1)

        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL | OPENGLBLIT)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_BLEND)

        glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)

        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.2, -5.0)
        glRotatef(180, 0, 0, 1)
        glRotatef(-60, 1, 0, 0)
        glRotatef(0, 0, 1, 0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 0, 0))

        self.board = Board()
        self.frame_rate = 0

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.board.outline.collidepoint(event.pos):
                        x = int(round(((event.pos[0] - 5) / 40.0), 0))
                        y = int(round(((event.pos[1] - 5) / 40.0), 0))
                        stone = self.board.search(point=(x, y))
                        if stone:
                            stone.remove()
                        else:
                            added_stone = Stone(self.board, (x, y), self.board.turn())
                        self.board.update_liberties(added_stone)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.board.show()
            pygame.display.flip()

            self.frame_rate = int(clock.get_fps())
            pygame.display.set_caption(f"3D board | Frame Rate: {self.frame_rate}")

            clock.tick(60)

if __name__ == "__main__":
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load(BACKGROUND).convert()
    app = App()
    app.run()
