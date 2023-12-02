import pygame
import sys

# Initialize pygame
pygame.init()

# Set up some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 20
GRID_LINE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 255)

# Create a screen surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Draw the grid
for x in range(200, 600, GRID_SIZE):
    for y in range(200, 600, GRID_SIZE):
        pygame.draw.rect(screen, BACKGROUND_COLOR, (x, y, GRID_SIZE, GRID_SIZE), 1)

# Draw the lines
for x in range(200, 600, GRID_SIZE):
    pygame.draw.line(screen, GRID_LINE_COLOR, (x, 200), (x, 600))
    pygame.draw.line(screen, GRID_LINE_COLOR, (200, x), (600, x))

# Update the display
pygame.display.flip()

# Wait for the user to quit
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()