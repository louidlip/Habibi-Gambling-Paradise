import pygame
import sys

pygame.init()

# Définir la résolution par défaut
screen_width, screen_height = 800, 600

# Initialisation de la fenêtre Pygame avec la résolution fixe
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Habibi")
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("assets/sol.png"), (screen_width, screen_height))
font = pygame.font.Font("font/Daydream.ttf", 19)
roll_message = font.render("Voulez-vous jouer au jeu de dé ?", True, (255, 255, 255))

x = screen_width * 0.5
y = screen_height * 0.5
dice_machine_x = 390
dice_machine_y = 30
Player_speed = 5
running = True

class Dice_machine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/slot machine.png"), (90, 140))
        self.pos = pygame.math.Vector2(dice_machine_x, dice_machine_y)
        self.rect = self.image.get_rect(center=(dice_machine_x, dice_machine_y))

    def collision(self, player):
        if self.rect.colliderect(player.rect):
            screen.blit(roll_message,(x,y))
    
    def update(self, player):
        self.collision(player)

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
        self.rect.topleft = (self.pos.x,self.pos.y)



player = Player()
dice_machine = Dice_machine()

in_game = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if screen_width - 60 <= mouse_x <= screen_width - 10 and 10 <= mouse_y <= 50:
                in_game = False
    if in_game:
        screen.blit(background, (0, 0))
        screen.blit(dice_machine.image, dice_machine.pos)
        screen.blit(player.image, player.pos)
        player.update()
        dice_machine.update(player)
        pygame.draw.rect(screen, (255, 0, 0), (screen_width - 100, 10, 80, 40))  
        exit_text = font.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (screen_width - 100, 15))
    else:
        display_end_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

