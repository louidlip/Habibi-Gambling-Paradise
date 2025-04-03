import pygame
import random
import time

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Machine à sous")

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Police de texte
font = pygame.font.Font(None, 36)

# Chargement des images des symboles (remplacer par vos propres images)
symbols = ["assets/slots/siete.png", "assets/slots/tsinelas.png", "assets/slots/banyal.png"]  # Remplacez par les chemins de vos images
images = [pygame.image.load(img) for img in symbols]
image_width, image_height = images[0].get_size()

# Fonction pour afficher le texte
def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Fonction pour afficher les rouleaux
def draw_reels(reels):
    x_offset = 50
    for reel in reels:
        for i, image in enumerate(reel):
            screen.blit(image, (x_offset, 100 + i * image_height))
        x_offset += image_width + 10  # Espace entre les rouleaux

# Fonction pour faire tourner les rouleaux (avec animation)
def spin_reels():
    reels = [random.sample(images, 3) for _ in range(3)]  # Initialisation des rouleaux
    spin_duration = 1.5  # Durée de l'animation en secondes
    start_time = time.time()
    spin_result = [random.sample(images, 3) for _ in range(3)]  # Résultat final des rouleaux

    # Animation des rouleaux
    while time.time() - start_time < spin_duration:
        temp_reels = []
        for reel in range(3):
            temp_reels.append([random.choice(images) for _ in range(3)])
        draw_reels(temp_reels)
        pygame.display.flip()
        pygame.time.wait(50)  # Pause pour l'animation
    return spin_result

# Fonction pour vérifier si le joueur a gagné
def check_win(reels):
    # Vérifier si tous les symboles sont identiques sur une ligne
    for i in range(3):
        if reels[0][i] == reels[1][i] == reels[2][i]:
            return True
    return False

# Fonction principale pour le jeu
def run_game():
    running = True
    credits = 100  # Crédits du joueur
    reels = [random.sample(images, 3) for _ in range(3)]  # Initialisation des rouleaux avec des images aléatoires
    win_amount = 0  # Gain de la partie

    while running:
        screen.fill(WHITE)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Affichage des crédits
        draw_text(f"Crédits: {credits}", 10, 10)

        # Affichage du gain de la partie (si applicable)
        if win_amount > 0:
            draw_text(f"Gagné: {win_amount}", 250, 50, GREEN)
        elif win_amount < 0:
            draw_text(f"Perdu: {-win_amount}", 250, 50, (255, 0, 0))  # Perte en rouge

        # Affichage des rouleaux
        draw_reels(reels)

        # Affichage du bouton de spin
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 75, HEIGHT - 100, 150, 50))
        draw_text("SPIN", WIDTH // 2 - 40, HEIGHT - 85, WHITE)

        # Gestion de l'interaction (clic sur le bouton de spin)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if WIDTH // 2 - 75 < mouse_pos[0] < WIDTH // 2 + 75 and HEIGHT - 100 < mouse_pos[1] < HEIGHT - 50:
            if mouse_click[0] == 1 and credits > 0:  # Si le joueur a cliqué sur le bouton "Spin" et a des crédits
                credits -= 1  # Déduction d'un crédit
                reels = spin_reels()  # Spin des rouleaux
                if check_win(reels):  # Vérifier si le joueur a gagné
                    win_amount = 10  # Par exemple, gagner 10 crédits si trois symboles identiques sont alignés
                    credits += win_amount
                else:
                    win_amount = -1  # Perte d'un crédit
                time.sleep(1)  # Pause pour simuler le temps de spin
        
        # Actualisation de l'écran
        pygame.display.flip()

        # Limiter la fréquence de mise à jour de l'écran (60 FPS)
        pygame.time.Clock().tick(60)

    pygame.quit()

# Lancer le jeu
run_game()
