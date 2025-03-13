import pygame
import random
import sys
import ctypes
import os

# Paramètres du jeu
WIDTH, HEIGHT = 1600, 1000
FPS = 120
BG_IMAGE_PATH = "assets/bg.png"  # Changer le chemin pour être relatif
GRID_IMAGE_PATH = "assets/gridline.png"  # Changer le chemin pour être relatif
SYM_PATH = "assets/symbols"
TEXT_COLOR = 'White'
UI_FONT = "assets/font/kidspace.ttf"  # Changer le chemin pour être relatif
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110
DEFAULT_IMAGE_SIZE = (300, 300)
GAME_INDICES = [1, 2, 3]

# Initialisation pygame
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

# Définition des symboles
symbols = {
    'diamond': f"{SYM_PATH}/0_diamond.png", 
    'floppy': f"{SYM_PATH}/0_floppy.png",
    'hourglass': f"{SYM_PATH}/0_hourglass.png",
    'telephone': f"{SYM_PATH}/0_telephone.png"
}

class Player():
    def __init__(self):
        self.balance = 1000.00
        self.bet_size = 10.00
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00

    def get_data(self):
        player_data = {
            'balance': "{:.2f}".format(self.balance),
            'bet_size': "{:.2f}".format(self.bet_size),
            'last_payout': "{:.2f}".format(self.last_payout) if self.last_payout else "N/A",
            'total_won': "{:.2f}".format(self.total_won),
            'total_wager': "{:.2f}".format(self.total_wager)
        }
        return player_data

    def place_bet(self):
        bet = self.bet_size
        self.balance -= bet
        self.total_wager += bet

class Reel(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5]  # Limité à 5 symboles

        self.reel_is_spinning = False
        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            # Animation des rouleaux
            if self.delay_time <= 0:
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100
                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                        symbol.kill()
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -300), symbol.idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        spin_symbols = [self.symbol_list.sprites()[i].sym_type for i in GAME_INDICES]
        return spin_symbols[::-1]

class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()
        self.sym_type = pathToFile.split('/')[3].split('.')[0]
        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(pathToFile).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        if self.fade_in and self.size_x < 320:
            self.size_x += 1
            self.size_y += 1
            self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        elif not self.fade_in and self.fade_out and self.alpha > 115:
            self.alpha -= 7
            self.image.set_alpha(self.alpha)

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.win_animation_ongoing = False
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

    def spawn_reels(self):
        x_topleft, y_topleft = 10, -300
        for reel_index in range(5):
            self.reel_list[reel_index] = Reel((x_topleft + reel_index * 320, y_topleft))

    def cooldowns(self):
        for reel in self.reel_list.values():
            if reel.reel_is_spinning:
                self.can_toggle = False
                self.spinning = True
        if not self.can_toggle and all(not reel.reel_is_spinning for reel in self.reel_list.values()):
            self.can_toggle = True
            self.spin_result = self.get_result()
            if self.check_wins(self.spin_result):
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size

    def toggle_spinning(self):
        if self.can_toggle:
            self.spinning = not self.spinning
            self.can_toggle = False
            for reel in self.reel_list.values():
                reel.start_spin(200)

    def get_result(self):
        for reel_index, reel in self.reel_list.items():
            self.spin_result[reel_index] = reel.reel_spin_result()
        return self.spin_result

    def check_wins(self, result):
        hits = {}
        for row in result:
            for symbol in row:
                if row.count(symbol) > 2:
                    hits[symbol] = row
        return hits

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        for reel in self.reel_list.values():
            reel.animate(delta_time)
        self.ui.update()

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        self.win_text_angle = random.randint(-4, 4)

    def display_info(self):
        player_data = self.player.get_data()
        balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR)
        bet_surf = self.font.render("Wager: $" + player_data['bet_size'], True, TEXT_COLOR)
        self.display_surface.blit(balance_surf, (20, HEIGHT - 30))
        self.display_surface.blit(bet_surf, (WIDTH - 20 - bet_surf.get_width(), HEIGHT - 30))

        if self.player.last_payout:
            win_surf = self.win_font.render("WIN! $" + player_data['last_payout'], True, TEXT_COLOR)
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            self.display_surface.blit(win_surf, (WIDTH // 2 - win_surf.get_width() // 2, HEIGHT // 2))

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Slot Machine Demo')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()  # Utilisation du chemin relatif
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()  # Utilisation du chemin relatif
        self.machine = Machine()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(0)
            self.screen.blit(self.grid_image, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
