import pygame
import sys
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Habibi")
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load("assets/sol.png"),(screen_width,screen_height))
x = screen_width*0.5
y = screen_height*0.5
Player_speed = 5
running = True

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
while running:
    keys = pygame.key.get_pressed
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background,(0,0))
    screen.blit(player.image, player.pos)
    player.update()
        
    pygame.display.flip()
    


    clock.tick(60)
pygame.quit()
sys.exit()
