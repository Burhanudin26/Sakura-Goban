import pygame
import sys

# Constants
GRID_SIZE = 9
CELL_SIZE = 40
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
WHITE, BLACK, EMPTY = (255, 255, 255), (0, 0, 0), (200, 200, 200)

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Go Game")

# Create a 2D list to represent the Go board
board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, EMPTY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2, 0)
    pygame.display.flip()

def draw_stone(row, col, color):
    pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2, 0)
    pygame.display.flip()

def main():
    turn = 'B'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE

                if board[row][col] == ' ':
                    board[row][col] = turn
                    draw_stone(row, col, BLACK if turn == 'B' else WHITE)
                    turn = 'W' if turn == 'B' else 'B'

        pygame.display.flip()

if __name__ == "__main__":
    draw_board()
    main()
