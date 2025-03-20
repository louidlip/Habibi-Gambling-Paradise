#pas encore fonctionel, probleme de chemin pour trouver les fichiers
import pygame
import random
import sys
import ctypes
import os


# Display settings
DEFAULT_IMAGE_SIZE = (300, 300)
FPS = 120
HEIGHT = 1000
WIDTH = 1600
START_X, START_Y = 0, -300
X_OFFSET, Y_OFFSET = 20, 0

# Images
BG_IMAGE_PATH = "assets/bg.png"
GRID_IMAGE_PATH = "assets/gridline.png"
GAME_INDICES = [1, 2, 3]  # 0 and 4 are outside of play area
SYM_PATH = "assets/symbols"

# Text
TEXT_COLOR = 'White'
UI_FONT = "assets/kidspace.ttf"
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# Symbols
symbols = {
    'diamond': f"{SYM_PATH}/0_diamond.png", 
    'floppy': f"{SYM_PATH}/0_floppy.png",
    'hourglass': f"{SYM_PATH}/0_hourglass.png",
    'hourglass2': f"{SYM_PATH}/0_hourglass.png",
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
        player_data = {}
        player_data['balance'] = "{:.2f}".format(self.balance)
        player_data['bet_size'] = "{:.2f}".format(self.bet_size)
        player_data['last_payout'] = "{:.2f}".format(self.last_payout) if self.last_payout else "N/A"
        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        return player_data

    def place_bet(self):
        bet = self.bet_size
        self.balance -= bet
        self.total_wager += bet

class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()
        self.sym_type = pathToFile.split('/')[-1].split('.')[0]
        self.pos = pos
        self.idx = idx
        try:
            self.image = pygame.image.load(pathToFile).convert_alpha()
        except FileNotFoundError:
            print(f"File not found: {pathToFile}")
            self.image = pygame.Surface(DEFAULT_IMAGE_SIZE)
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)

class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5]
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
            if self.delay_time <= 0:
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100
                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                        symbol_idx = symbol.idx
                        symbol.kill()
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -300), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1]

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

    def cooldowns(self):
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True
        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()
            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft))
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False
            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                self.win_animation_ongoing = False

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
                    if len(longest_seq(possible_win)) > 2:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits

    def pay_player(self, win_data, curr_player):
        multiplier = 0
        spin_payout = 0
        for v in win_data.values():
            multiplier += len(v[1])
        spin_payout = (multiplier * curr_player.bet_size)
        curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        try:
            self.font, self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except FileNotFoundError:
            print("Error loading font!")
            print(f"Currently, the UI_FONT variable is set to {UI_FONT}")
            print("Does the file exist?")
            try:
                self.font, self.bet_font = pygame.font.SysFont(None, UI_FONT_SIZE), pygame.font.SysFont(None, UI_FONT_SIZE)
                self.win_font = pygame.font.SysFont(None, WIN_FONT_SIZE)
            except Exception as e:
                print(f"Unable to load fallback font: {e}")
                pygame.quit()
                sys.exit()
        self.win_text_angle = random.randint(-4, 4)

    def display_info(self):
        player_data = self.player.get_data()
        balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR, None)
        x, y = 20, self.display_surface.get_size()[1] - 30
        balance_rect = balance_surf.get_rect(bottomleft = (x, y))
        bet_surf = self.bet_font.render("Wager: $" + player_data['bet_size'], True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 20
        bet_rect = bet_surf.get_rect(bottomright = (x, y))
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! $" + last_payout, True, TEXT_COLOR, None)
            x1 = 800
            y1 = self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center = (x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()

def flip_horizontal(result):
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
    rows, cols = len(horizontal_values), len(horizontal_values[0])
    hvals2 = [[""] * rows for _ in range(cols)]
    for x in range(rows):
        for y in range(cols):
            hvals2[y][rows - x - 1] = horizontal_values[x][y]
    hvals3 = [item[::-1] for item in hvals2]
    return hvals3

def longest_seq(hit):
    subSeqLength, longest = 1, 1
    start, end = 0, 0
    for i in range(len(hit) - 1):
        if hit[i] == hit[i + 1] - 1:
            subSeqLength += 1
            if subSeqLength > longest:
                longest = subSeqLength
                start = i + 2 - subSeqLength
                end = i + 2
        else:
            subSeqLength = 1
    return hit[start:end]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Slot Machine Demo')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        self.machine = Machine()
        self.delta_time = 0

    def run(self):
        self.start_time = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(self.delta_time)
            self.screen.blit(self.grid_image, (0, 0))
            self.clock.tick(FPS)

