import pygame
import sys
import json

def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config["screen_width"], config["screen_height"]

pygame.init()

screen_width, screen_height = load_config()

screen = pygame.display.set_mode((screen_width, screen_height))

game_over_image = pygame.image.load("ecran-fin.png")

game_over_image = pygame.transform.scale(game_over_image, (screen_width, screen_height))

def game_over_screen():
    screen.blit(game_over_image, (0, 0))  # Afficher l'image de fin à l'écran
    pygame.display.flip()  # Mettre à jour l'affichage

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_input = False
                return
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.wait(3000)

        game_over_screen()

if __name__ == "__main__":
    main()
