import pygame
import sys
import subprocess
from argent import get_argent, ajouter_argent, retirer_argent

pygame.init()

# Définir la résolution par défaut
screen_width, screen_height = 800, 600

# Initialisation de la fenêtre Pygame avec la résolution fixe
Logo = pygame.image.load("assets/Logo.png")
pygame.display.set_icon(Logo)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Habibi")
clock = pygame.time.Clock()
ecran_noir = pygame.image.load("assets/surface noire.jpg")
ecran_noir.set_alpha(100)
background = pygame.transform.scale(pygame.image.load("assets/sol.png"), (screen_width, screen_height))
font = pygame.font.Font("font/Daydream.ttf", 18)
roll_message = font.render("Voulez-vous jouer au jeu de de ? (appuyez sur 'E')", True, (255, 255, 255))
roll_message2 = font.render("Voulez-vous jouer au Plinko ? (appuyez sur 'E')", True, (255, 255, 255))
roll_message3 = font.render("Voulez-vous jouer a la machine a sous ? (appuyez sur 'E')", True, (255, 255, 255))
roll_message4 = font.render("Voulez-vous jouer aux mines ? (appuyez sur 'E')", True, (255, 255, 255))

x = screen_width * 0.5 - 45
y = screen_height * 0.5 - 80
Player_speed = 5
running = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/Sprite arrière.png"),(150,150))
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.speed = Player_speed

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.image = pygame.transform.scale(pygame.image.load("assets/Sprite arrière.png"),(150,150))
            self.velocity_y = -self.speed
            if keys[pygame.K_q] or keys[pygame.K_d]:
                self.velocity_x = 0
                self.velocity_y = 0
        if keys[pygame.K_q]:
            self.image = pygame.transform.scale(pygame.image.load("assets/Sprite gauche.png"),(150,150))
            self.velocity_x = -self.speed
            if keys[pygame.K_z] or keys[pygame.K_s]:
                self.velocity_x = 0
                self.velocity_y = 0
        if keys[pygame.K_s]:
            self.image = pygame.transform.scale(pygame.image.load("assets/Sprite avant.png"),(150,150))
            self.velocity_y = self.speed
            if keys[pygame.K_q] or keys[pygame.K_d]:
                self.velocity_x = 0
                self.velocity_y = 0
        if keys[pygame.K_d]:
            self.image = pygame.transform.scale(pygame.image.load("assets/Sprite droite.png"),(150,150))
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
        self.rect.topleft = (self.pos.x,self.pos.y)

class Dice_machine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/dicelogo.jpg"), (140, 140))
        self.pos = pygame.math.Vector2(350, 30)
        self.rect = self.image.get_rect(center=(350, 30))
        self.rect = pygame.Rect(350, 30, 100, 100)
    def collision(self, player):
        keys = pygame.key.get_pressed()
        if self.rect.colliderect(player.rect):
            screen.blit(ecran_noir,(0,0))
            screen.blit(roll_message,(5,250))
            if keys[pygame.K_e]:
                subprocess.Popen(["python", "codes/jeu_de_dé.py"])
                pygame.quit()
                sys.exit()
    
    def update(self, player):
        self.collision(player)

class Plinko_machine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/plinkologo.jpg"), (140, 140))
        self.pos = pygame.math.Vector2(25, 210)
        self.rect = pygame.Rect(25, 210, 100, 100)

    def collision(self, player):
        keys = pygame.key.get_pressed()
        if self.rect.colliderect(player.rect):
            screen.blit(ecran_noir,(0,0))
            screen.blit(roll_message2,(5,250))
            if keys[pygame.K_e]:
                subprocess.Popen(["python", "codes/plinko.py"])
                pygame.quit()
                sys.exit()
    
    def update(self, player):
        self.collision(player)

class Slots_machine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/slotslogo.png"), (140, 140))
        self.pos = pygame.math.Vector2(640, 210)
        self.rect = pygame.Rect(640, 210, 100, 100)
    def collision(self, player):
        keys = pygame.key.get_pressed()
        if self.rect.colliderect(player.rect):
            screen.blit(ecran_noir,(0,0))
            screen.blit(roll_message3,(5,250))
            if keys[pygame.K_e]:
                subprocess.Popen(["python", "codes/slots.py"])
                pygame.quit()
                sys.exit()
    
    def update(self, player):
        self.collision(player)

class Mines_machine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/minelogo.png"), (140, 140))
        self.pos = pygame.math.Vector2(350, 450)
        self.rect = pygame.Rect(350, 450, 100, 100)
    
    def collision(self, player):
        keys = pygame.key.get_pressed()
        if self.rect.colliderect(player.rect):
            screen.blit(ecran_noir,(0,0))
            screen.blit(roll_message4,(5, 250))
            if keys[pygame.K_e]:
                subprocess.Popen(["python", "codes/mine.py"])
                pygame.quit()
                sys.exit()
    
    def update(self, player):
        self.collision(player)

def display_end_screen():
    keys = pygame.key.get_pressed()
    end_message = font.render("Merci d'avoir joue !", True, (255, 255, 255))
    end_message_2 = font.render("Appuyez sur 'ESC' pour retourner a l'Ecran titre", True, (255, 255, 255))
    screen.fill((0, 0, 0))  
    screen.blit(end_message, (screen_width * 0.3, screen_height * 0.5))
    screen.blit(end_message_2, (5, screen_height * 0.6))
    pygame.display.flip()
    if keys[pygame.K_ESCAPE]:
        subprocess.Popen(["python", "codes/test.py"])
        pygame.quit()
        sys.exit()


player = Player()
dice_machine = Dice_machine()
plinko_machine = Plinko_machine()
slots_machine = Slots_machine()
mines_machine = Mines_machine()
argent_text = font.render(f"Argent: {get_argent()}$", True, (255, 255, 0))
in_game = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if screen_width - 60 <= mouse_x <= screen_width - 10 and 10 <= mouse_y <= 50:
                in_game = False
    if in_game:
        screen.blit(background, (0, 0))
        screen.blit(dice_machine.image, dice_machine.pos)
        screen.blit(plinko_machine.image, plinko_machine.pos)
        screen.blit(slots_machine.image, slots_machine.pos)
        screen.blit(mines_machine.image, mines_machine.pos)
        screen.blit(player.image, player.pos)
        player.update()
        dice_machine.update(player)
        plinko_machine.update(player)
        slots_machine.update(player)
        mines_machine.update(player)
        pygame.draw.rect(screen, (255, 0, 0), (screen_width - 100, 10, 80, 40))  
        exit_text = font.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (screen_width - 100, 15))
        screen.blit(argent_text, (10, 20))
    else:
        display_end_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
