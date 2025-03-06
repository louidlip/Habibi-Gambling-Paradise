import pygame
import random
import sys
import time
import subprocess

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu de Dé Amélioré")
clock = pygame.time.Clock()

logo = pygame.image.load("assets/Logo.png")
pygame.display.set_icon(logo)
font = pygame.font.Font("font/Daydream.ttf", 32)
small_font = pygame.font.Font("font/Daydream.ttf", 19)
ecran_noir = pygame.image.load("assets/surface noire.jpg")

roll_message = small_font.render("Appuyez sur ESPACE pour lancer le dé", True, (255, 255, 255))
win_message = font.render("Vous avez gagné !", True, (0, 255, 0))
lose_message = font.render("Vous avez perdu !", True, (255, 0, 0))
esc_message = small_font.render("Appuyez sur 'E' pour retourner au Lobby", True, (255, 255, 255))
dice_images = [
    pygame.image.load(f"assets/dice/{i}.png") for i in range(1, 7)
]

background_image = pygame.image.load("assets/arriere-plan.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

dice_result = None
game_outcome = None
rolling = False
animation_frames = 20
score = 0

def roll_dice():
    weighted_roll = [1, 2, 3, 4, 5, 6, 6]
    return random.choice(weighted_roll)

def check_game_outcome(dice_result):
    global score
    if dice_result in [5, 6]:
        score += 10
        return "win"
    else:
        score -= 5
        return "lose"

def dice_animation():
    global dice_result, rolling
    rolling = True
    for i in range(animation_frames):
        current_image = random.choice(dice_images)
        screen.blit(background_image, (0, 0))
        screen.blit(roll_message, (90, 300))
        screen.blit(current_image, (screen_width // 2 - current_image.get_width() // 2, 150))
        pygame.display.flip()
        pygame.time.delay(50 + i * 10)
    dice_result = roll_dice()
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
                game_outcome = check_game_outcome(dice_result)
    exit_possibility()
    screen.blit(background_image, (0, 0))
    screen.blit(roll_message, (90, 300))
    if dice_result is not None and not rolling:
        dice_image = dice_images[dice_result - 1]
        screen.blit(dice_image, (screen_width // 2 - dice_image.get_width() // 2, 150))
        if game_outcome == "win":
            screen.blit(win_message, (screen_width // 2 - win_message.get_width() // 2, 400))
        elif game_outcome == "lose":
            screen.blit(lose_message, (screen_width // 2 - lose_message.get_width() // 2, 400))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width - score_text.get_width() - 20, 20))
    screen.blit(esc_message, (75, 550))
    pygame.display.flip()
    clock.tick(60)
