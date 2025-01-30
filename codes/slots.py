import pygame
import random
import os

# Initialisation de pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Chemin de base pour les ressources
BASE_PATH = r"\\0641-SRV-FILES\perso\ELEVES_LYC\1ERE06\KIMPFLERJ\Downloads\Habibi-Gambling-Paradise-main"

# Symboles et leurs paiements
SYMBOLS = {
    "lanterne": (os.path.join(BASE_PATH, "assets", "lanterne.png"), 1000),
    "arabicLight": (os.path.join(BASE_PATH, "assets", "arabicLight.jpg"), 500),
    "kebab": (os.path.join(BASE_PATH, "assets", "kebab.png"), 400),
    "kim": (os.path.join(BASE_PATH, "assets", "kim.png"), 300),
    "bonbons": (os.path.join(BASE_PATH, "assets", "bonbons.png"), 200),
    "pyramid": (os.path.join(BASE_PATH, "assets", "pyramid.jpg"), 100),
    "pixel9": (os.path.join(BASE_PATH, "assets", "pixel-number-9.png"), 50),
    "pixel6": (os.path.join(BASE_PATH, "assets", "pixel-number-6.png"), 10),
}

# Dimensions des rouleaux et des symboles
SYMBOL_SIZE = 100  # Taille des symboles redimensionnés (100x100 pixels)

# Vérification des chemins des fichiers
for symbol, (path, _) in SYMBOLS.items():
    if not os.path.exists(path):
        print(f"Fichier de symbole introuvable : {path}")
        exit()

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slot Machine")

# Charger et redimensionner les symboles
symbol_images = {}
for name, data in SYMBOLS.items():
    image = pygame.image.load(data[0])  # Charger l'image
    symbol_images[name] = pygame.transform.scale(image, (SYMBOL_SIZE, SYMBOL_SIZE))  # Redimensionner

# Variables du jeu
running = True
REEL_COUNT = 3
SYMBOL_LIST = list(SYMBOLS.keys())

# Position des rouleaux centrée sur l'écran
REEL_START_X = SCREEN_WIDTH // 2 - (SYMBOL_SIZE * REEL_COUNT) // 2  # Centrer horizontalement
REEL_START_Y = 150  # Position verticale du haut des rouleaux

# Initialisation des rouleaux avec des symboles aléatoires
reels = [[random.choice(SYMBOL_LIST) for _ in range(REEL_COUNT)] for _ in range(3)]
payout = 0
argent = 1000  # Argent initial du joueur

# Fonction pour vérifier les combinaisons gagnantes
def check_winnings(reels):
    global payout
    payout = 0

    # Lignes gagnantes
    lines = [
        [reels[0][0], reels[0][1], reels[0][2]],  # Ligne du haut
        [reels[1][0], reels[1][1], reels[1][2]],  # Ligne du milieu
        [reels[2][0], reels[2][1], reels[2][2]],  # Ligne du bas
        [reels[0][0], reels[1][1], reels[2][2]],  # Diagonale haut-gauche à bas-droit
        [reels[0][2], reels[1][1], reels[2][0]],  # Diagonale haut-droit à bas-gauche
    ]

    for line in lines:
        if line[0] == line[1] == line[2]:  # Combinaison gagnante
            payout += SYMBOLS[line[0]][1]  # Ajouter le paiement de cette combinaison

# Fonction pour dessiner la machine à sous
def draw_slot_machine():
    # Dessiner les rouleaux (avec les symboles)
    for col_index, reel in enumerate(reels):
        for row_index, symbol in enumerate(reel):
            x = REEL_START_X + col_index * SYMBOL_SIZE  # Position horizontale centrée
            y = REEL_START_Y + row_index * SYMBOL_SIZE  # Ajuster la position verticale pour chaque ligne
            screen.blit(symbol_images[symbol], (x, y))

    # Dessiner les bordures de la machine
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(REEL_START_X - 20, REEL_START_Y - 20, SYMBOL_SIZE * REEL_COUNT + 40, SYMBOL_SIZE * 3 + 40), 5)  # Bordure extérieure

# Boucle principale du jeu
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Lancer les rouleaux
                if argent >= 50:  # Vérifier si le joueur a assez d'argent pour jouer
                    argent -= 50  # Retirer 50 الله
                    reels = [[random.choice(SYMBOL_LIST) for _ in range(REEL_COUNT)] for _ in range(3)]
                    check_winnings(reels)
                    argent += payout  # Ajouter le gain au total

    # Remplir l'écran avec une couleur de fond
    screen.fill((255, 255, 255))  # Fond blanc

    # Dessiner la machine à sous
    draw_slot_machine()

    # Afficher le paiement
    font = pygame.font.Font(None, 36)
    payout_text = f"Paiement : {payout} الله"
    text_surface = font.render(payout_text, True, (0, 0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT - 50))

    # Afficher l'argent total
    argent_text = f"Argent : {argent} الله"
    argent_surface = font.render(argent_text, True, (0, 0, 0))
    screen.blit(argent_surface, (SCREEN_WIDTH // 2 - argent_surface.get_width() // 2, SCREEN_HEIGHT - 100))

    pygame.display.flip()

pygame.quit()
