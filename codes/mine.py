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
default_mines = 3  # Fixer le nombre de mines à 3

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

def draw_stop_button():
    pygame.draw.rect(screen, RED, (300, 570, 200, 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Arrêter", True, WHITE)
    screen.blit(text, (375, 585))

def display_game_over():
    font = pygame.font.Font(None, 48)
    text = font.render("GAME OVER! Appuyez sur R pour recommencer.", True, RED)
    screen.blit(text, (200, 300))

def display_not_enough_money():
    font = pygame.font.Font(None, 36)
    text = font.render("Pas assez d'argent pour jouer !", True, RED)
    screen.blit(text, (250, 300))

running = True
waiting_for_start = True
game_over = False
grid = generate_grid(default_mines)
discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
safe_cells_count = sum([1 for row in grid for cell in row if not cell])  # Compter le nombre de cases sûres
discovered_safe_cells = 0  # Nombre de cases sûres découvertes par le joueur

while running:
    screen.fill(WHITE)
    
    # Afficher le compteur d'argent en haut à gauche
    font = pygame.font.Font(None, 36)
    money_text = font.render(f"Argent: {money}€", True, BLACK)
    screen.blit(money_text, (10, 10))
    
    if waiting_for_start:
        if money >= 10:  # Vérifier si le joueur a assez d'argent pour jouer
            draw_button()
        else:
            display_not_enough_money()  # Afficher un message d'erreur si l'argent est insuffisant
    else:
        draw_grid()
        draw_stop_button()  # Afficher le bouton "Arrêter"
    
    if game_over:
        display_game_over()
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if waiting_for_start:
                if 300 <= x <= 500 and 500 <= y <= 550:  # Bouton "Jouer"
                    if money >= 10:  # Vérifier si le joueur a assez d'argent pour commencer
                        money -= 10  # Le joueur paie 10€ pour commencer
                        discovered_safe_cells = 0  # Réinitialiser le nombre de cases sûres découvertes
                        waiting_for_start = False
                        game_over = False
                        discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                        grid = generate_grid(default_mines)
                    else:
                        print("Pas assez d'argent pour jouer!")
            else:
                if 300 <= x <= 500 and 570 <= y <= 620:  # Bouton "Arrêter"
                    # Le joueur gagne l'argent seulement lorsqu'il appuie sur "Arrêter"
                    # Le montant gagné est basé sur le nombre de cases sûres découvertes
                    if discovered_safe_cells > 0:
                        money += (4*discovered_safe_cells)  # Gagner de l'argent en fonction des cases sûres découvertes
                    waiting_for_start = True
                    game_over = False
                    discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    grid = generate_grid(default_mines)
                    
                if not game_over:
                    cell = get_cell(event.pos)
                    if cell and not discovered[cell[0]][cell[1]]:
                        discovered[cell[0]][cell[1]] = True
                        if grid[cell[0]][cell[1]]:  # Si c'est une mine
                            print("Game Over!")
                            # Le joueur perd tout l'argent gagné et le jeu se termine
                            discovered_safe_cells = 0
                            game_over = True
                        else:
                            discovered_safe_cells += 1  # Augmenter le nombre de cases sûres découvertes
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                waiting_for_start = True
                game_over = False
                grid = generate_grid(default_mines)
                discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

pygame.quit()
