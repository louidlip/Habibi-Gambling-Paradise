import pygame
import random
import time
import subprocess  # Permet d'exécuter un autre fichier Python

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Machine à sous")

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Police de texte
font = pygame.font.Font(None, 36)

# Chargement des images des symboles
symbols = ["assets/slots/siete.png", "assets/slots/tsinelas.png", "assets/slots/banyal.png"]
images = [pygame.image.load(img) for img in symbols]
image_width, image_height = images[0].get_size()

def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_reels(reels):
    x_offset = 50
    for reel in reels:
        for i, image in enumerate(reel):
            screen.blit(image, (x_offset, 100 + i * image_height))
        x_offset += image_width + 10

def spin_reels():
    reels = [random.sample(images, 3) for _ in range(3)]
    spin_duration = 1.5
    start_time = time.time()
    
    while time.time() - start_time < spin_duration:
        temp_reels = [[random.choice(images) for _ in range(3)] for _ in range(3)]
        draw_reels(temp_reels)
        pygame.display.flip()
        pygame.time.wait(50)
    
    return [random.sample(images, 3) for _ in range(3)]

def check_win(reels):
    for i in range(3):
        if reels[0][i] == reels[1][i] == reels[2][i]:
            return True
    return False

def draw_exit_button():
    exit_button_rect = pygame.Rect(WIDTH - 100, 10, 90, 40)
    pygame.draw.rect(screen, RED, exit_button_rect)
    draw_text("EXIT", WIDTH - 90, 20, WHITE)
    return exit_button_rect

def run_game():
    running = True
    credits = 100
    bet = 1
    reels = [random.sample(images, 3) for _ in range(3)]
    win_amount = 0
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    bet *= 2
                elif event.key == pygame.K_x and bet > 1:
                    bet //= 2
        
        draw_text(f"Crédits: {credits}", 10, 10)
        draw_text(f"Mise: {bet}", 10, 50)
        
        if win_amount > 0:
            draw_text(f"Gagné: {win_amount}", 250, 50, GREEN)
        elif win_amount < 0:
            draw_text(f"Perdu: {-win_amount}", 250, 50, RED)
        
        draw_reels(reels)
        
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 75, HEIGHT - 100, 150, 50))
        draw_text("SPIN", WIDTH // 2 - 40, HEIGHT - 85, WHITE)
        
        exit_button_rect = draw_exit_button()
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if WIDTH // 2 - 75 < mouse_pos[0] < WIDTH // 2 + 75 and HEIGHT - 100 < mouse_pos[1] < HEIGHT - 50:
            if mouse_click[0] == 1 and credits >= bet:
                credits -= bet
                reels = spin_reels()
                if check_win(reels):
                    win_amount = bet * 10
                    credits += win_amount
                else:
                    win_amount = -bet
                time.sleep(1)
        
        if exit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
            running = False
            subprocess.run(['python', 'codes/Lobby.py'])
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

run_game()
