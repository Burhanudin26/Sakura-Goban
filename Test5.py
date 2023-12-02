import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
BOARD_SIZE = 19
SQUARE_SIZE = 50
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the clock
clock = pygame.time.Clock()

def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            if (row + col) % 2 == 0:
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(screen, color, rect)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_board(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()