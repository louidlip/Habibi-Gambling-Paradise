import pygame
import random

# Initialisation de pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Charger les ressources
BACKGROUND_IMAGE = "Habibi-Gambling-Paradise/assets/slut machine.png"
SYMBOLS = {
    "lanterne": ("Habibi-Gambling-Paradise/assets/lanterne.png", 1000),
    "arabicLight": ("Habibi-Gambling-Paradise/assets/arabicLight.jpg", 500),
    "kebab": ("Habibi-Gambling-Paradise/assets/kebab.png", 400),
    "kim": ("Habibi-Gambling-Paradise/assets/kim.png", 300),
    "bonbons": ("Habibi-Gambling-Paradise/assets/bonbons.png", 200),
    "pyramid": ("Habibi-Gambling-Paradise/assets/pyramid.jpg", 100),
    "pixel9": ("Habibi-Gambling-Paradise/assets/pixel-number-9.png", 50),
    "pixel6": ("Habibi-Gambling-Paradise/assets/pixel-number-6.png", 10),
}

# Liste des symboles pour la sélection aléatoire
SYMBOL_LIST = list(SYMBOLS.keys())

# Dimensions des rouleaux
REEL_COUNT = 3
SYMBOL_SIZE = 100
# Positions des rouleaux ajustées pour correspondre au design de la machine
REEL_POSITIONS = [
    (175, 150),  # Ligne du haut
    (175, 250),  # Ligne du milieu
    (175, 350),  # Ligne du bas
]

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slot Machine")

# Charger l'image de fond
background = pygame.image.load(BACKGROUND_IMAGE)

# Charger les symboles
symbol_images = {
    name: pygame.image.load(data[0]) for name, data in SYMBOLS.items()
}

# Variables du jeu
running = True
reels = [[random.choice(SYMBOL_LIST) for _ in range(REEL_COUNT)] for _ in range(3)]
payout = 0

# Fonction pour vérifier les combinaisons gagnantes
def check_winnings(reels):
    global payout
    payout = 0

    # Lignes gagnantes
    lines = [
        reels[1],  # Ligne du milieu
        reels[0],  # Ligne du haut
        reels[2],  # Ligne du bas
        [reels[0][0], reels[1][1], reels[2][2]],  # Diagonale haut-gauche à bas-droit
        [reels[0][2], reels[1][1], reels[2][0]],  # Diagonale haut-droit à bas-gauche
    ]

    for line in lines:
        if line[0] == line[1] == line[2]:
            payout += SYMBOLS[line[0]][1]

# Fonction pour dessiner les rouleaux
def draw_reels():
    for row_index, row in enumerate(reels):
        for col_index, symbol in enumerate(row):
            x = 325 + col_index * SYMBOL_SIZE  # Ajustement horizontal pour les colonnes
            y = REEL_POSITIONS[row_index][1]  # Utiliser les positions verticales ajustées
            screen.blit(symbol_images[symbol], (x, y))

# Boucle principale du jeu
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Lancer les rouleaux
                reels = [[random.choice(SYMBOL_LIST) for _ in range(REEL_COUNT)] for _ in range(3)]
                check_winnings(reels)

    # Dessiner l'arrière-plan
    screen.blit(background, (0, 0))

    # Dessiner les rouleaux
    draw_reels()

    # Afficher le paiement
    font = pygame.font.Font(None, 36)
    text = font.render(f"Payout: {payout}", True, (255, 255, 255))
    screen.blit(text, (50, 50))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter pygame
pygame.quit()
