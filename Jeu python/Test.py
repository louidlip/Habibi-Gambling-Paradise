import pygame
pygame.init()

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Habibi")
background_image = pygame.image.load("Ecran_titre.png")
clock = pygame.time.Clock()
Logo = pygame.image.load("Logo.png")
pygame.display.set_icon(Logo)
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Background
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0,0))

    
    pygame.display.flip()



    clock.tick(60)