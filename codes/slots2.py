import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 100
GRID_SIZE = 3  # 3x3 grid for the slot machine

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, '..', 'assets')

# Symbols Paths
SYMBOLS_PATHS = [
    os.path.join(ASSETS_DIR, 'symbols', '0_diamond.png'),
    os.path.join(ASSETS_DIR, 'symbols', '0_floppy.png'),
    os.path.join(ASSETS_DIR, 'symbols', '0_hourglass.png'),
    os.path.join(ASSETS_DIR, 'symbols', '0_telephone.png')
]

# Load symbols
symbols_images = [pygame.image.load(path) for path in SYMBOLS_PATHS]

# Resize symbols
symbols_images = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in symbols_images]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Slot Machine")

# Function to draw grid
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)

# Function to draw symbols
def draw_symbols():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            symbol = random.choice(symbols_images)
            screen.blit(symbol, (x * CELL_SIZE, y * CELL_SIZE))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen.fill(WHITE)
                draw_symbols()

    # Draw grid
    draw_grid()

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
