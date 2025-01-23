import pygame 
import sys
import json
import os

pygame.init()

def load_settings():
    default_settings = {"volume": 0.5, "resolution": (800, 600)}
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    else:
        save_settings(default_settings)
        return default_settings

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

settings = load_settings()
screen_width, screen_height = settings["resolution"]

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Habibi")
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("assets/sol.png"), (screen_width, screen_height))
font = pygame.font.Font("font/Daydream.ttf", 19)
roll_message = font.render("Voulez-vous jouer au jeu de dé ?", True, (255, 255, 255))

x = screen_width * 0.5
y = screen_height * 0.5
dice_machine_x = 50
dice_machine_y = 50
Player_speed = 5
running = True

class Dice_machine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/slot machine.png"), (90, 140))
        self.pos = pygame.math.Vector2(dice_machine_x, dice_machine_y)

    def collision(self, player):
        if player.colliderect(self):
            screen.blit(roll_message, (screen_width * 0.1, screen_height * 0.5))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/sprite perso 1.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.speed = Player_speed

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.velocity_y = -self.speed
            if keys[pygame.K_q] or keys[pygame.K_d]:
                self.velocity_x = 0
                self.velocity_y = 0
        if keys[pygame.K_q]:
            self.velocity_x = -self.speed
            if keys[pygame.K_z] or keys[pygame.K_s]:
                self.velocity_x = 0
                self.velocity_y = 0
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
            if keys[pygame.K_q] or keys[pygame.K_d]:
                self.velocity_x = 0
                self.velocity_y = 0
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
            if keys[pygame.K_z] or keys[pygame.K_s]:
                self.velocity_x = 0
                self.velocity_y = 0

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > screen_width - self.rect.width:
            self.pos.x = screen_width - self.rect.width
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > screen_height - self.rect.height:
            self.pos.y = screen_height - self.rect.height

    def update(self):
        self.user_input()
        self.move()

def display_end_screen():
    end_message = font.render("Merci d'avoir joue !", True, (255, 255, 255))
    screen.fill((0, 0, 0))  # Écran noir
    screen.blit(end_message, (screen_width * 0.4, screen_height * 0.5))
    pygame.display.flip()

player = Player()
dice_machine = Dice_machine()

# Variables pour l'écran principal
in_game = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Vérification du clic sur le bouton "Exit" en haut à droite
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Vérifie si le clic est dans la zone du bouton Exit
            if screen_width - 60 <= mouse_x <= screen_width - 10 and 10 <= mouse_y <= 50:
                in_game = False

    if in_game:
        # Affichage du jeu
        screen.blit(background, (0, 0))
        screen.blit(dice_machine.image, dice_machine.pos)
        screen.blit(player.image, player.pos)
        player.update()

        # Dessiner le bouton Exit (rectangle en haut à droite)
        pygame.draw.rect(screen, (255, 0, 0), (screen_width - 100, 10, 80, 40))  # Bouton rouge
        exit_text = font.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (screen_width - 100, 15))  # Texte blanc

    else:
        # Affichage de l'écran de fin
        display_end_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

