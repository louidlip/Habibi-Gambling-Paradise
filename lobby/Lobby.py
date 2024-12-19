import pygame
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Habibi")
clock = pygame.time.Clock()
sprite_perso = pygame.image.load("sprites/sprite perso 1.png")
def add_character_at_location(x,y):
        screen.blit(sprite_perso, (x,y))
x = screen_width*0.5
y = screen_height*0.5
add_character_at_location(x,y)
character_move_speed = 10
y_change = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y_change = -character_move_speed
            elif event.key == pygame.K_DOWN:
                y_change = character_move_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y = 0
    y+= y_change

    
    pygame.display.update()
    pygame.display.flip()


    clock.tick(60)
