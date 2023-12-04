import pygame
from sys import exit
import sys
BACKGROUND = 'ramin2.jpg'  # Nama file gambar latar belakang
MENU_BACK = 'Sakura.jpg'
BOARD_SIZE = (820, 820)# Ukuran papan
MENU_SIZE = (820,820)
WHITE = (255, 255, 255)  # Warna putih
BLACK = (0, 0, 0)  # Warna hitam

class Stone(object):
    def __init__(self, board, point, color):
        """Create, initialize, and draw a stone."""
        self.board = board
        self.point = point
        self.color = color
        self.group = self.find_group()
        self.coords = (5 + self.point[0] * 40, 5 + self.point[1] * 40)
        self.draw()

    def draw(self):
        """Draw the stone as a circle."""
        pygame.draw.circle(screen, self.color, self.coords, 20, 0)
        pygame.display.update()

    def remove(self):
        """Remove the stone from the board."""
        blit_coords = (self.coords[0] - 20, self.coords[1] - 20)
        area_rect = pygame.Rect(blit_coords, (40, 40))
        screen.blit(background, blit_coords, area_rect)
        pygame.display.update()
        self.group.stones.remove(self)
        del self

    @property
    def neighbors(self):
        """Return a list of neighboring points."""
        neighboring = [(self.point[0] - 1, self.point[1]),
                       (self.point[0] + 1, self.point[1]),
                       (self.point[0], self.point[1] - 1),
                       (self.point[0], self.point[1] + 1)]
        for point in neighboring:
            if not 0 < point[0] < 20 or not 0 < point[1] < 20:
                neighboring.remove(point)
        return neighboring

    @property
    def liberties(self):
        """Find and return the liberties of the stone."""
        liberties = self.neighbors
        stones = self.board.search(points=self.neighbors)
        for stone in stones:
            liberties.remove(stone.point)
        return liberties

    def find_group(self):
        """Find or create a group for the stone."""
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
        """Return the location of the stone, e.g., 'D17'."""
        return 'ABCDEFGHJKLMNOPQRST'[self.point[0]-1] + str(20-(self.point[1]))

class Group(object):
    def __init__(self, board, stone):
        """Create and initialize a new group."""
        self.board = board
        self.board.groups.append(self)
        self.stones = [stone]
        self.liberties = None

    def merge(self, group):
        """Merge two groups."""
        for stone in group.stones:
            stone.group = self
            self.stones.append(stone)
        self.board.groups.remove(group)
        del group

    def remove(self):
        """Remove the entire group."""
        while self.stones:
            self.stones[0].remove()
        self.board.groups.remove(self)
        del self

    def update_liberties(self):
        """Update the group's liberties."""
        liberties = []
        for stone in self.stones:
            for liberty in stone.liberties:
                liberties.append(liberty)
        self.liberties = set(liberties)
        if len(self.liberties) == 0:
            self.remove()

    def __str__(self):
        """Return a list of the group's stones as a string."""
        return str([str(stone) for stone in self.stones])

class Board(object):
    def __init__(self):
        """Create, initialize, and draw an empty board."""
        self.groups = []
        self.next = BLACK
        self.outline = pygame.Rect(45, 45, 720, 720)
        self.draw()

    def search(self, point=None, points=[]):
        """Search the board for a stone."""
        stones = []
        for group in self.groups:
            for stone in group.stones:
                if stone.point == point and not points:
                    return stone
                if stone.point in points:
                    stones.append(stone)
        return stones

    def turn(self):
        """Keep track of the turn by flipping between BLACK and WHITE."""
        if self.next == BLACK:
            self.next = WHITE
            return BLACK
        else:
            self.next = BLACK
            return WHITE

    def draw(self):
        """Draw the board to the background and blit it to the screen."""
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
        screen.blit(background, (0, 0))
        pygame.display.update()

    def update_liberties(self, added_stone=None):
        """Updates the liberties of the entire board, group by group."""
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()
            
def get_font(size):
    return pygame.font.Font("font.ttf", size)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)



class GameScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
        self.background = pygame.image.load(BACKGROUND).convert()
        self.board = Board()

    def update(self):
        while True:
            pygame.time.wait(10)
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

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.board.draw()
        pygame.display.update()

class MainMenuScreen:
    def __init__(self):
        self.screen = pygame.display.set_mode(MENU_SIZE, 0, 32)
        self.background = pygame.image.load(MENU_BACK).convert()
        # Initialize the mixer
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load("Sakura_music.mp3")
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    
    def start_game(self):
        game_screen = GameScreen()
        game_screen.update()
        game_screen.draw()
            
    def update(self):
        pygame.time.wait(250)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        Title = get_font(70).render("SAKURA GOBAN", True, (255,45,255))
        MENU_RECT = Title.get_rect(center=(410, 210))

        start_button = Button(image=pygame.image.load("play_button.png"), pos=(420, 350),
                              text_input="", font=get_font(70), base_color="#d7fcd4", hovering_color="white")
        exit_button = Button(image=pygame.image.load("quit_button.png"), pos=(420, 550),
                             text_input="", font=get_font(70), base_color="#d7fcd4", hovering_color="white")
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(Title, MENU_RECT)

        for button in [start_button, exit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkForInput(MENU_MOUSE_POS):
                    self.start_game()
                elif exit_button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Go Game Board')
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load(BACKGROUND).convert()
    main_menu_screen = MainMenuScreen()
    while True:
        main_menu_screen.update()
        pygame.display.update()