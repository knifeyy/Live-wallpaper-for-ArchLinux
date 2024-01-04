import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Set the width and height of the screen (width, height).
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(size, pygame.NOFRAME)

# Set the title of the window.
pygame.display.set_caption("Wallpaper")

# Define colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Base velocity for autonomous movement
        self.base_vx = random.uniform(-1, 1)
        self.base_vy = random.uniform(-1, 1)
        # Current velocity
        self.vx = self.base_vx
        self.vy = self.base_vy

    def update(self, mouse_pos):
        # Calculate the distance to the cursor
        distance_to_cursor = math.sqrt((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)

        # If the cursor is close, increase the velocity
        if distance_to_cursor < 100:
            angle = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)
            # Increase velocity by 60%
            self.vx += math.cos(angle) * self.base_vx * 0.6
            self.vy += math.sin(angle) * self.base_vy * 0.6
        else:
            # Apply damping to gradually reduce velocity back to base velocity
            self.vx = self.vx * 0.95 + self.base_vx * 0.05
            self.vy = self.vy * 0.95 + self.base_vy * 0.05

        # Update the node's position based on its velocity
        self.x += self.vx
        self.y += self.vy

        # Bounce off the edges with a little damping to reduce velocity
        if self.x <= 0 or self.x >= size[0]:
            self.base_vx = -self.base_vx  # Reflect the base velocity
            self.vx = -self.vx * 0.9  # Reflect the current velocity with damping
            self.x = max(min(self.x, size[0]), 0)
        if self.y <= 0 or self.y >= size[1]:
            self.base_vy = -self.base_vy  # Reflect the base velocity
            self.vy = -self.vy * 0.9  # Reflect the current velocity with damping
            self.y = max(min(self.y, size[1]), 0)


# Create a bunch of nodes
nodes = [Node(random.uniform(0, size[0]), random.uniform(0, size[1])) for _ in range(250)]

# Enhanced range for connections
connection_range = 120

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Update nodes
    for node in nodes:
        node.update(mouse_pos)

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw lines between close nodes
    for i, node in enumerate(nodes):
        for other in nodes[i+1:]:
            distance = math.sqrt((node.x - other.x)**2 + (node.y - other.y)**2)
            if distance < connection_range:  # Only draw line if nodes are close
                # Check if cursor is close to either node
                if (math.sqrt((node.x - mouse_pos[0])**2 + (node.y - mouse_pos[1])**2) < 100 or
                    math.sqrt((other.x - mouse_pos[0])**2 + (other.y - mouse_pos[1])**2) < 100):
                    color = WHITE  # Cursor is influencing the connection
                else:
                    color = GRAY  # Normal connection
                pygame.draw.line(screen, color, (node.x, node.y), (other.x, other.y), 1)

    # Draw the nodes
    for node in nodes:
        pygame.draw.circle(screen, GRAY, (int(node.x), int(node.y)), 3)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
