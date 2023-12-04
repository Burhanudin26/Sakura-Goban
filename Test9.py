import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

delta_z = 1
aproximity_adjusted = 0.3

# Set up predefined exact positions
exact_positions = [(0, 0.1), (0.1, -0.1), (-0.1, -0.1)]  # Add more as needed

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
gluPerspective(30, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, 0)
# List to store circles
circles = []

# Function to draw a circle at a specific position
def draw_circle(x, y, z, radius=0.01, segments=100):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(x, y, z)
    for i in range(segments + 1):
        angle = i * (2.0 * math.pi / segments)
        glVertex3f(x + radius * math.cos(angle), y + radius * math.sin(angle), z)
    glEnd()

# Function to find the nearest predefined position
def find_nearest_position(x, y):
    min_distance = float('inf')
    nearest_position = None
    for position in exact_positions:
        distance = math.sqrt((x - position[0]) ** 2 + (y - position[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_position = position
    return nearest_position

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            # Get mouse coordinates
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Convert to OpenGL coordinates
            x = (mouse_x / width) * 2 - 1
            y = -(mouse_y / height) * 2 + 1

            # Adjust coordinates
            x_adjusted = x * (aproximity_adjusted ** delta_z)
            y_adjusted = y * (aproximity_adjusted ** delta_z)

            # Find the nearest predefined position
            nearest_position = find_nearest_position(x_adjusted, y_adjusted)

            # Add a new circle to the list with adjusted coordinates
            circles.append((nearest_position[0], nearest_position[1], -1))
            print(x, x_adjusted, nearest_position, sep=" |")

    # Refresh the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw all circles in the list
    for circle in circles:
        draw_circle(*circle)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
