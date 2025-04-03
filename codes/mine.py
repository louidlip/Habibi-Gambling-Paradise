import pygame
import random
from argent import get_argent, ajouter_argent, retirer_argent
import subprocess  # Pour lancer le script du lobby

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
    screen.blit(text, (10, 200))
    
    # Ajouter un message pour informer l'utilisateur de l'option "Échap"
    escape_text = font.render("Appuyez sur Échap pour retourner au lobby.", True, RED)
    screen.blit(escape_text, (50, 370))


def display_return_to_lobby():
    font = pygame.font.Font(None, 36)
    text = font.render("Pas assez d'argent ! Appuyez sur Échap pour retourner au lobby.", True, RED)
    screen.blit(text, (150, 250))

running = True
waiting_for_start = True
game_over = False
default_mines = 3
grid = generate_grid(default_mines)
discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
discovered_safe_cells = 0
waiting_for_lobby_response = False  # Pour savoir si on attend une réponse de l'utilisateur

while running:
    screen.fill(WHITE)
    
    font = pygame.font.Font(None, 36)
    money_text = font.render(f"Argent: {get_argent()}€", True, BLACK)
    screen.blit(money_text, (10, 10))
    
    if waiting_for_start:
        if get_argent() >= 10:
            draw_button()
        else:
            display_return_to_lobby()  # Affichage du message de game over ici
    else:
        draw_grid()
        draw_stop_button()
    
    if game_over:
        display_game_over()
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if waiting_for_start:
                if 300 <= x <= 500 and 500 <= y <= 550:
                    if get_argent() >= 10:
                        retirer_argent(10)
                        discovered_safe_cells = 0
                        waiting_for_start = False
                        game_over = False
                        discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                        grid = generate_grid(default_mines)
                    else:
                        print("Pas assez d'argent pour jouer!")
            else:
                if 300 <= x <= 500 and 570 <= y <= 620:
                    if discovered_safe_cells > 0:
                        ajouter_argent(4 * discovered_safe_cells)
                    waiting_for_start = True
                    game_over = False
                    discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    grid = generate_grid(default_mines)
                
                if not game_over:
                    cell = get_cell(event.pos)
                    if cell and not discovered[cell[0]][cell[1]]:
                        discovered[cell[0]][cell[1]] = True
                        if grid[cell[0]][cell[1]]:
                            print("Game Over!")
                            discovered_safe_cells = 0
                            game_over = True
                        else:
                            discovered_safe_cells += 1

        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    waiting_for_start = True
                    game_over = False
                    grid = generate_grid(default_mines)
                    discovered = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            elif event.key == pygame.K_ESCAPE:  # Appuyer sur Échap pour revenir au lobby
                subprocess.Popen(["python", "codes/Lobby.py"])  # Retour au lobby
                pygame.quit()  # Ferme le jeu actuel
                running = False  # Met fin à la boucle principale

pygame.quit()
