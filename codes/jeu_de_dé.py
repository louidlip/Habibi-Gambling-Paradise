import pygame
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Habibi")
clock = pygame.time.Clock()
Logo = pygame.image.load("assets/Logo.png")
pygame.display.set_icon(Logo)
font = pygame.font.Font("font/Daydream.ttf",19)
roll_message = font.render("Appuyer sur ESPACE pour faire tourner le de", True, (255,255,255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    screen.fill((0, 0, 0))
    screen.blit(roll_message,(15,300))
    



    pygame.display.flip()


    clock.tick(60)
