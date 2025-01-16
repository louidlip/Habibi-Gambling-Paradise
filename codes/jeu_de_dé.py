import pygame
import random
import sys
import time

pygame.init()

# Initialisation de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu de Dé - Habibi")
clock = pygame.time.Clock()

# Chargement des ressources
Logo = pygame.image.load("assets/Logo.png")
pygame.display.set_icon(Logo)
font = pygame.font.Font("font/Daydream.ttf", 32)
small_font = pygame.font.Font("font/Daydream.ttf", 19)

roll_message = small_font.render("Appuyer sur ESPACE pour lancer le de", True, (255, 255, 255))
win_message = font.render("Vous avez gagne !", True, (0, 255, 0))
lose_message = font.render("Vous avez perdu !", True, (255, 0, 0))

# Chargement des images de dés
dice_images = [
    pygame.image.load(f"assets/dice/{i}.png") for i in range(1, 7)
]

# Variables du jeu
dice_result = None  # Résultat du dé
game_outcome = None  # Résultat du jeu: "win", "lose" ou None
rolling = False  # Indique si le dé est en train de rouler
animation_frames = 20  # Nombre de frames pour l'animation

# Fonction pour lancer un dé avec probabilité ajustée
def roll_dice():
    weighted_roll = [1, 2, 3, 4, 5, 6, 6]  # Chances ajustées (6 a plus de chances)
    return random.choice(weighted_roll)

# Fonction pour vérifier les conditions de victoire ou de défaite
def check_game_outcome(dice_result):
    if dice_result in [5, 6]:  # Victoire si le résultat est 5 ou 6
        return "win"
    else:  # Défaite pour les autres résultats
        return "lose"

# Fonction pour jouer l'animation du dé
def dice_animation():
    global dice_result, rolling
    rolling = True
    for i in range(animation_frames):
        # Change l'image du dé aléatoirement
        current_image = random.choice(dice_images)
        screen.fill((0, 0, 0))
        screen.blit(roll_message, (90, 300))
        screen.blit(current_image, (screen_width // 2 - current_image.get_width() // 2, 150))
        pygame.display.flip()
        pygame.time.delay(50 + i * 10)  # Augmente progressivement le délai
    dice_result = roll_dice()
    rolling = False

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not rolling:  # Si ESPACE est pressée et pas d'animation en cours
                dice_animation()
                game_outcome = check_game_outcome(dice_result)

    # Dessin à l'écran
    screen.fill((0, 0, 0))  # Remplit l'écran en noir
    screen.blit(roll_message, (90, 300))  # Affiche le message

    if dice_result is not None and not rolling:
        # Affiche l'image du dé correspondant au résultat final
        dice_image = dice_images[dice_result - 1]
        screen.blit(dice_image, (screen_width // 2 - dice_image.get_width() // 2, 150))

        # Affiche le résultat du jeu
        if game_outcome == "win":
            screen.blit(win_message, (screen_width // 2 - win_message.get_width() // 2, 400))
        elif game_outcome == "lose":
            screen.blit(lose_message, (screen_width // 2 - lose_message.get_width() // 2, 400))

    pygame.display.flip()
    clock.tick(60)
