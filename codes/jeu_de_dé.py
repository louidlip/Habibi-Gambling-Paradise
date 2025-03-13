import pygame
import random
import sys
import subprocess

pygame.init()

# Paramètres d'affichage
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu de Craps")
clock = pygame.time.Clock()

# Chargement des ressources
logo = pygame.image.load("assets/Logo.png")
pygame.display.set_icon(logo)
font = pygame.font.Font("font/Daydream.ttf", 32)
small_font = pygame.font.Font("font/Daydream.ttf", 19)
ecran_noir = pygame.image.load("assets/surface noire.jpg")

# Messages
roll_message = small_font.render("Appuyez sur ESPACE pour lancer les dés", True, (255, 255, 255))
win_message = font.render("Vous avez gagne !", True, (0, 255, 0))
lose_message = font.render("Vous avez perdu !", True, (255, 0, 0))
esc_message = small_font.render("Appuyez sur 'E' pour retourner au Lobby", True, (255, 255, 255))

# Images des dés
dice_images = [
    pygame.image.load(f"assets/dice/{i}.png") for i in range(1, 7)
]

# Image de fond
background_image = pygame.image.load("assets/arriere-plan.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Variables de jeu
dice_results = [None, None]
game_outcome = None
rolling = False
animation_frames = 20
score = 0
point = None  # Le point est le nombre que le joueur doit obtenir après le premier lancer
score_flash = False  # Pour l'animation de score

def roll_dice():
    # Lancer deux dés
    return random.randint(1, 6), random.randint(1, 6)

def check_game_outcome(dice_results):
    global score, point, score_flash
    total = sum(dice_results)
    
    if point is None:  # Premier lancer (Come Out Roll)
        if total in [7, 11]:  # Le joueur gagne immédiatement
            score += 50
            score_flash = True
            return "win"
        elif total in [2, 3, 12]:  # Le joueur perd immédiatement
            score -= 5
            score_flash = True
            return "lose"
        else:  # Le joueur établit un point
            point = total
            return "point"
    else:  # Point Roll
        if total == point:  # Le joueur fait son point et gagne
            score += 30
            score_flash = True
            point = None  # Réinitialiser le point
            return "win"
        elif total == 7:  # Le joueur perd
            score -= 5
            score_flash = True
            point = None  # Réinitialiser le point
            return "lose"
        else:
            return "point"

def dice_animation():
    global dice_results, rolling
    rolling = True
    for i in range(animation_frames):
        # Pour chaque frame, on génère deux dés avec des valeurs aléatoires
        current_image1 = dice_images[random.randint(0, 5)]
        current_image2 = dice_images[random.randint(0, 5)]
        
        # Placer les dés à des positions différentes pour qu'ils soient visibles
        screen.blit(background_image, (0, 0))
        screen.blit(roll_message, (90, 300))
        
        # Positionner les dés
        screen.blit(current_image1, (screen_width // 2 - 150, 150))  # Premier dé à gauche
        screen.blit(current_image2, (screen_width // 2 + 50, 150))   # Deuxième dé à droite
        
        pygame.display.flip()
        pygame.time.delay(50 + i * 10)
        
    dice_results = roll_dice()  # Lancer les dés après l'animation
    rolling = False

def exit_possibility():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        subprocess.Popen(["python", "codes/Lobby.py"])
        pygame.quit()
        sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not rolling:
                dice_animation()
                game_outcome = check_game_outcome(dice_results)

    exit_possibility()
    screen.blit(background_image, (0, 0))
    screen.blit(roll_message, (90, 300))
    
    if dice_results[0] is not None and not rolling:
        # Afficher les résultats des dés après l'animation
        dice_image1 = dice_images[dice_results[0] - 1]
        dice_image2 = dice_images[dice_results[1] - 1]
        
        # Afficher les dés à la position finale
        screen.blit(dice_image1, (screen_width // 2 - 150, 150))
        screen.blit(dice_image2, (screen_width // 2 + 50, 150))
        
        # Afficher le résultat du jeu
        if game_outcome == "win":
            screen.blit(win_message, (screen_width // 2 - win_message.get_width() // 2, 400))
        elif game_outcome == "lose":
            screen.blit(lose_message, (screen_width // 2 - lose_message.get_width() // 2, 400))
        elif game_outcome == "point":
            screen.blit(font.render(f"Point a obtenir: {point}", True, (255, 255, 255)), (screen_width // 2 - 120, 400))

    # Animation du score
    if score_flash:
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))  # Score en jaune quand il change
    else:
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Score normal
    
    # Réinitialiser l'animation du score après une courte durée
    if score_flash:
        pygame.time.delay(500)
        score_flash = False
    
    screen.blit(score_text, (screen_width - score_text.get_width() - 20, 20))
    screen.blit(esc_message, (75, 550))
    pygame.display.flip()
    clock.tick(60)
