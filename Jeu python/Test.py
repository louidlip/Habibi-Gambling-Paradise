import pygame
import os
import sys

pygame.init()

# Configuration de l'écran
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Habibi")
background_image = pygame.image.load("Jeu python/Ecran_titre.png")
clock = pygame.time.Clock()
Logo = pygame.image.load("Jeu python/Logo.png")
pygame.display.set_icon(Logo)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Définir le bouton "Jouer"
button_width = 200
button_height = 50
button_x = (screen_width - button_width) // 2
button_y = screen_height // 2

# Police pour le texte du bouton
font = pygame.font.Font(None, 36)
button_text = font.render("Jouer", True, WHITE)

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_x, mouse_y = event.pos
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    # Lancer 'Lobby.py'
                    os.system("python Lobby.py")
                    pygame.quit()
                    sys.exit()

    # Dessiner l'arrière-plan
    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))

    # Dessiner le bouton
    pygame.draw.rect(screen, (0, 0, 255), (button_x, button_y, button_width, button_height))
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, text_rect)

    pygame.display.flip()
    clock.tick(60)
