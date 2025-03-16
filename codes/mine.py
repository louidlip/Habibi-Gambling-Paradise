import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 5
CELL_SIZE = 80
BOARD_X, BOARD_Y = 150, 100

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
RED = (200, 50, 50)

mine_img = pygame.image.load("assets/mine.jpg")
mine_img = pygame.transform.scale(mine_img, (CELL_SIZE, CELL_SIZE))
safe_img = pygame.image.load("assets/money.jpg")
safe_img = pygame.transform.scale(safe_img, (CELL_SIZE, CELL_SIZE))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu des Mines")

money = 100
default_mines = 5

def generate_grid(num_mines):
    grid = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines_positions = random.sample([(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)], num_mines)
    for x, y in mines_positions:
        grid[x][y] = True
    return grid

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(BOARD_X + x * CELL_SIZE, BOARD_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
            if discovered[x][y]:
                if grid[x][y]:
                    screen.blit(mine_img, (BOARD_X + x * CELL_SIZE, BOARD_Y + y * CELL_SIZE))
                else:
                    screen.blit(safe_img, (BOARD_X + x * CELL_SIZE, BOARD_Y + y * CELL_SIZE))

def get_cell(pos):
    x, y = (pos[0] - BOARD_X) // CELL_SIZE, (pos[1] - BOARD_Y) // CELL_SIZE
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        return x, y
    return None

def draw_button():
    pygame.draw.rect(screen, GREEN, (300, 500, 200, 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Jouer", True, WHITE)
    screen.blit(text, (375, 515))

def draw_mine_controls():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Mines: {default_mines}", True, BLACK)
    screen.blit(text, (50, 500))
    
    pygame.draw.rect(screen, GREEN, (50, 540, 30, 30))
    plus_text = font.render("+", True, WHITE)
    screen.blit(plus_text, (60, 545))
    
    pygame.draw.rect(screen, RED, (90, 540, 30, 30))
    minus_text = font.render("-", True, WHITE)
    screen.blit(minus_text, (100, 545))

running = True
waiting_for_start = True
game_over = False
grid = generate_grid(default_mines)
discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

while running:
    screen.fill(WHITE)
    
    if waiting_for_start:
        draw_button()
        draw_mine_controls()
    else:
        draw_grid()
        font = pygame.font.Font(None, 36)
        money_text = font.render(f"Argent: {money}€", True, BLACK)
        screen.blit(money_text, (10, 10))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if waiting_for_start:
                if 300 <= x <= 500 and 500 <= y <= 550:  # Bouton "Jouer"
                    waiting_for_start = False
                    game_over = False
                    discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    grid = generate_grid(default_mines)
                elif 50 <= x <= 80 and 540 <= y <= 570:  # Augmenter mines
                    default_mines = min(default_mines + 1, GRID_SIZE * GRID_SIZE - 1)
                elif 90 <= x <= 120 and 540 <= y <= 570:  # Diminuer mines
                    default_mines = max(default_mines - 1, 1)
            else:
                cell = get_cell(event.pos)
                if cell and not discovered[cell[0]][cell[1]]:
                    discovered[cell[0]][cell[1]] = True
                    if grid[cell[0]][cell[1]]:
                        print("Game Over!")
                        money -= 10
                        game_over = True
                    else:
                        money += 5
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                waiting_for_start = True
                game_over = False

pygame.quit()
