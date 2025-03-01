import pygame
import os
import sys
import subprocess

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Habibi")

background_image = pygame.image.load("assets/Ecran_titre.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
Logo = pygame.image.load("assets/Logo.png")
pygame.display.set_icon(Logo)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 36)
button_width = 200
button_height = 50
button_x = (screen_width - button_width) // 2
button_y_play = screen_height // 2
button_y_settings = button_y_play + button_height + 20
button_y_quit = button_y_settings + button_height + 20

button_play_text = font.render("Jouer", True, WHITE)
button_settings_text = font.render("Paramètres", True, WHITE)
button_quit_text = font.render("Quitter", True, WHITE)

pygame.mixer.init()
pygame.mixer.music.load("assets/background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

current_volume = 0.5

def draw_button(x, y, width, height, text, screen, bg_color=BLUE):
    pygame.draw.rect(screen, bg_color, (x, y, width, height))
    text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text, text_rect)

def show_settings():
    global current_volume
    settings_running = True
    slider_x = (screen_width - 200) // 2
    slider_y = 350
    slider_width = 200
    slider_height = 10
    handle_radius = 10

    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if slider_x <= mouse_x <= slider_x + slider_width and slider_y - handle_radius <= mouse_y <= slider_y + handle_radius:
                    current_volume = (mouse_x - slider_x) / slider_width
                    pygame.mixer.music.set_volume(current_volume)
            elif event.type == pygame.MOUSEWHEEL:
                current_volume += event.y * 0.05
                current_volume = max(0.0, min(1.0, current_volume))
                pygame.mixer.music.set_volume(current_volume)

        screen.fill(GRAY)
        settings_text = font.render("Paramètres - Échap pour revenir", True, BLACK)
        volume_text = font.render(f"Volume : {int(current_volume * 100)}%", True, BLACK)

        screen.blit(settings_text, (screen_width // 2 - settings_text.get_width() // 2, 200))
        screen.blit(volume_text, (screen_width // 2 - volume_text.get_width() // 2, slider_y - 40))

        pygame.draw.rect(screen, WHITE, (slider_x, slider_y, slider_width, slider_height))
        handle_x = slider_x + int(current_volume * slider_width)
        pygame.draw.circle(screen, GREEN, (handle_x, slider_y + slider_height // 2), handle_radius)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if button_x <= mouse_x <= button_x + button_width and button_y_play <= mouse_y <= button_y_play + button_height:
                running = False
                subprocess.Popen(["python", "codes/Lobby.py"])
            elif button_x <= mouse_x <= button_x + button_width and button_y_settings <= mouse_y <= button_y_settings + button_height:
                show_settings()
            elif button_x <= mouse_x <= button_x + button_width and button_y_quit <= mouse_y <= button_y_quit + button_height:
                pygame.quit()
                sys.exit()

    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))
    draw_button(button_x, button_y_play, button_width, button_height, button_play_text, screen)
    draw_button(button_x, button_y_settings, button_width, button_height, button_settings_text, screen)
    draw_button(button_x, button_y_quit, button_width, button_height, button_quit_text, screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
