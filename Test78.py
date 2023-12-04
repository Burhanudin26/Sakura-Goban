import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

BROWN = (0.647, 0.165, 0.165)
BLACK = (0,0,0)
# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
# Set up perspective projection
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# List to store the circles
circles = []

# Function to draw a circle at the specified position
def draw_circle(x, y, radius=30):
    glColor3fv(BLACK)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(x, y, 0)
    for i in range(360):
        angle = i * 2.0 * 3.14159 / 360
        glVertex3f(x + radius * math.cos(angle), y + radius * math.sin(angle), 0)
    glEnd()

# Function to check if a point is inside a circle
def point_inside_circle(point, circle):
    x, y = point
    cx, cy, radius = circle
    distance = math.sqrt((x - cx)**2 + (y - cy)**2)
    return distance <= radius

def screen():
    glBegin(GL_QUADS)
    glColor3fv(BROWN)
    glVertex3f(0, 0, -1)
    glVertex3f(width, 0, -1)
    glVertex3f(width, height, -1)
    glVertex3f(0, height, -1)
    glEnd()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the mouse click is inside any circle
            remove_circles = [circle for circle in circles if point_inside_circle((mouse_x, mouse_y), circle)]

            # If the click is not inside any circle, add a new circle
            if not remove_circles:
                circles.append((mouse_x, mouse_y, 30))
            else:
                # Remove the circles that were clicked inside
                for circle in remove_circles:
                    circles.remove(circle)

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    screen()

    # Draw all the circles
    for circle in circles:
        draw_circle(*circle)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(30)
