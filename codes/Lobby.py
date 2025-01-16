import pygame
import sys
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Habibi")
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load("assets/sol.png"),(screen_width,screen_height))
font = pygame.font.Font("font/Daydream.ttf",19)
roll_message = font.render("Voulez vous jouer au jeu de dé ?", True, (255,255,255))
x = screen_width*0.5
y = screen_height*0.5
dice_machine_x = 50
dice_machine_y = 50
Player_speed = 5
running = True

class Dice_machine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/slot machine.png"),(90,140))
        self.pos = pygame.math.Vector2(dice_machine_x,dice_machine_y)
    def collision(self,player):
        if player.colliderect(self):
            screen.blit(roll_message,(15,300))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/sprite perso 1.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x,y)
        self.speed = Player_speed

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.velocity_y = -self.speed
            if keys[pygame.K_q] or keys[pygame.K_d]:
                self.velocity_x=0
                self.velocity_y=0
        if keys[pygame.K_q]:
            self.velocity_x = -self.speed
            if keys[pygame.K_z] or keys[pygame.K_s]:
                self.velocity_x=0
                self.velocity_y=0
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
            if keys[pygame.K_q] or keys[pygame.K_d]:
                self.velocity_x=0
                self.velocity_y=0
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
            if keys[pygame.K_z] or keys[pygame.K_s]:
                self.velocity_x=0
                self.velocity_y=0
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


player = Player()
dice_machine = Dice_machine()
while running:
    keys = pygame.key.get_pressed
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background,(0,0))
    screen.blit(dice_machine.image, dice_machine.pos)
    screen.blit(player.image, player.pos)
    player.update()
        
    pygame.display.flip()
    


    clock.tick(60)
pygame.quit()
sys.exit()
