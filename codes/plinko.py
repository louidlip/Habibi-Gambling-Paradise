import os
import pygame
import pymunk
import random
from collections import defaultdict
pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko Gambler")
space = pymunk.Space()
space.gravity = (0, 500)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)
GRAY = (100, 100, 100)

FONT_SMALL = pygame.font.Font(None, 24)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_LARGE = pygame.font.Font(None, 48)
PIN_RADIUS = 3
BALL_RADIUS = 10
BUCKET_WIDTH = WIDTH // 8
BUCKET_HEIGHT = 100
ball_colors = defaultdict(lambda: BLUE)

LEVELS = {
    "Easy": {
        "multipliers": [0, 0.5, 1, 1.5, 2, 1.5, 1, 0.5],
        "ball_cost": 10,
        "rows": 10
    },
    "Medium": {
        "multipliers": [-0.5, 0, 1, 2, 3, 2, 1, 0],
        "ball_cost": 20,
        "rows": 12
    },
    "Hard": {
        "multipliers": [-1, -0.5, 0, 2, 5, 2, 0, -0.5],
        "ball_cost": 30,
        "rows": 14
    }
}

current_level = None
initial_money = 0
current_money = 0
profit = 0
balls_dropped = 0
balls_in_play = 0
streak_counter = 0
jackpot = 100 


def create_pins(rows):
    pins = []
    for row in range(rows):
        pins_in_row = row + 1
        row_width = pins_in_row * 60
        start_x = (WIDTH - row_width) // 2 + 30
        y = 100 + row * 50
        for col in range(pins_in_row):
            x = start_x + col * 60
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = x, y
            shape = pymunk.Circle(body, PIN_RADIUS)
            shape.elasticity = 0.3
            shape.friction = 0.5
            space.add(body, shape)
            pins.append(shape)
    return pins


def create_walls():
    walls = [
        pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5),
        pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5),
    ]
    for wall in walls:
        wall.elasticity = 0.9
        wall.friction = 0.5
        space.add(wall)
    return walls


def create_buckets():
    buckets = []
    for i in range(8):
        x = i * BUCKET_WIDTH
        bucket = pymunk.Segment(space.static_body, (x, HEIGHT - BUCKET_HEIGHT),
                                (x + BUCKET_WIDTH, HEIGHT - BUCKET_HEIGHT), 5)
        bucket.sensor = True
        bucket.collision_type = i + 1
        space.add(bucket)
        buckets.append(bucket)
    return buckets


def create_ball(position):
    body = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, BALL_RADIUS))
    body.position = position
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.elasticity = 0.3
    shape.friction = 0.5
    shape.collision_type = 0
    space.add(body, shape)
    ball_colors[shape] = BLUE
    return shape


def collision_handler(arbiter, space, data):
    global profit, current_money, balls_dropped, balls_in_play, streak_counter, jackpot
    ball_shape, bucket_shape = arbiter.shapes
    bucket_index = bucket_shape.collision_type - 1
    multiplier = LEVELS[current_level]["multipliers"][bucket_index]

    score_change = LEVELS[current_level]["ball_cost"] * multiplier
    profit += score_change
    current_money += score_change
    balls_dropped += 1
    balls_in_play -= 1

    if score_change > 0:
        streak_counter += 1
    else:
        streak_counter = 0

    if streak_counter >= 3 and score_change > 0:
        bonus = LEVELS[current_level]["ball_cost"] * 0.5
        current_money += bonus
        profit += bonus
        print(f"Streak bonus! ${bonus:.2f} added to your money!")

    if bucket_index == 4:
        current_money += jackpot
        profit += jackpot
        print(f"Jackpot won! ${jackpot} added to your money!")
        jackpot = 100 
    else:
        jackpot += int(LEVELS[current_level]["ball_cost"] * 0.1)

    space.remove(ball_shape, ball_shape.body)
    del ball_colors[ball_shape]
    return True


def setup_collision_handlers():
    for i in range(1, 9):
        handler = space.add_collision_handler(0, i)
        handler.begin = collision_handler


def input_money():
    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    color_inactive = GRAY
    color_active = WHITE
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key != pygame.K_RETURN:
                        text += event.unicode
                if event.key == pygame.K_RETURN:
                    try:
                        amount = float(text)
                        if amount > 0:
                            return amount
                    except ValueError:
                        pass

        screen.fill(BLACK)
        txt_surface = FONT_MEDIUM.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        prompt_text = FONT_LARGE.render("Enter your starting money:", True, WHITE)
        screen.blit(prompt_text, (WIDTH // 4, HEIGHT // 2 - 100))

        instruction_text = FONT_SMALL.render("Press ENTER to continue", True, GRAY)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()


def select_level():
    levels = list(LEVELS.keys())
    selected = 0
    while True:
        screen.fill(BLACK)
        title = FONT_LARGE.render("Select Difficulty", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for i, level in enumerate(levels):
            color = GREEN if i == selected else WHITE
            text = FONT_MEDIUM.render(level, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    return levels[selected]


def main_game():
    global current_money, profit, balls_dropped, balls_in_play, streak_counter, jackpot

    pins = create_pins(LEVELS[current_level]["rows"])
    walls = create_walls()
    buckets = create_buckets()
    setup_collision_handlers()

    running = True
    clock = pygame.time.Clock()
    can_drop_balls = True

    while running and (balls_in_play > 0 or can_drop_balls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and can_drop_balls and current_money >= LEVELS[current_level]["ball_cost"]:
                    ball = create_ball((event.pos[0], 50))
                    current_money -= LEVELS[current_level]["ball_cost"]
                    profit -= LEVELS[current_level]["ball_cost"]
                    balls_in_play += 1
                elif event.button == 1 and can_drop_balls:
                    can_drop_balls = False

        space.step(1 / 60.0)

        screen.fill(BLACK)

        for pin in pins:
            pygame.draw.circle(screen, WHITE, (int(pin.body.position.x), int(pin.body.position.y)), PIN_RADIUS)

        for wall in walls:
            pygame.draw.line(screen, WHITE, wall.a, wall.b, 5)

        for i, bucket in enumerate(buckets):
            pygame.draw.line(screen, WHITE, bucket.a, bucket.b, 5)
            multiplier = LEVELS[current_level]['multipliers'][i]
            color = GREEN if multiplier > 0 else RED if multiplier < 0 else YELLOW
            multiplier_text = FONT_SMALL.render(f"x{multiplier:.2f}", True, color)
            screen.blit(multiplier_text, (i * BUCKET_WIDTH + BUCKET_WIDTH // 2 - 15, HEIGHT - BUCKET_HEIGHT + 10))

        for ball in space.shapes:
            if isinstance(ball, pymunk.Circle) and ball.body.mass != 0:
                pygame.draw.circle(screen, ball_colors[ball], (int(ball.body.position.x), int(ball.body.position.y)),
                                   int(ball.radius))

        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 100))

        profit_color = GREEN if profit >= 0 else RED
        profit_text = FONT_MEDIUM.render(f"Profit: ${profit:.2f}", True, profit_color)
        screen.blit(profit_text, (20, 20))

        money_text = FONT_MEDIUM.render(f"Money: ${current_money:.2f}", True, GREEN)
        screen.blit(money_text, (WIDTH - 250, 20))

        balls_text = FONT_SMALL.render(f"Balls Dropped: {balls_dropped}", True, WHITE)
        screen.blit(balls_text, (20, 60))

        level_text = FONT_SMALL.render(f"Level: {current_level}", True, YELLOW)
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 20))

        cost_text = FONT_SMALL.render(f"Ball Cost: ${LEVELS[current_level]['ball_cost']}", True, WHITE)
        screen.blit(cost_text, (WIDTH // 2 - cost_text.get_width() // 2, 50))

        streak_text = FONT_SMALL.render(f"Streak: {streak_counter}", True, YELLOW)
        screen.blit(streak_text, (WIDTH - 250, 60))

        jackpot_text = FONT_SMALL.render(f"Jackpot: ${jackpot}", True, GREEN)
        screen.blit(jackpot_text, (WIDTH // 2 - jackpot_text.get_width() // 2, 80))

        if not can_drop_balls:
            end_text = FONT_MEDIUM.render("Waiting for balls to settle...", True, RED)
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

    screen.fill(BLACK)
    game_over_text = FONT_LARGE.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))

    final_profit_color = GREEN if profit >= 0 else RED
    final_profit_text = FONT_MEDIUM.render(f"Final Profit: ${profit:.2f}", True, final_profit_color)
    screen.blit(final_profit_text, (WIDTH // 2 - final_profit_text.get_width() // 2, HEIGHT // 2 - 50))

    final_money_text = FONT_MEDIUM.render(f"Final Money: ${current_money:.2f}", True, GREEN)
    screen.blit(final_money_text, (WIDTH // 2 - final_money_text.get_width() // 2, HEIGHT // 2 + 0))

    balls_dropped_text = FONT_MEDIUM.render(f"Balls Dropped: {balls_dropped}", True, WHITE)
    screen.blit(balls_dropped_text, (WIDTH // 2 - balls_dropped_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def main():
    global current_level, initial_money, current_money, profit, balls_dropped, balls_in_play, streak_counter, jackpot

    while True:
        current_level = select_level()
        if current_level is None:
            break

        initial_money = input_money()
        if initial_money is None:
            break

        current_money = initial_money
        profit = 0
        balls_dropped = 0
        balls_in_play = 0
        streak_counter = 0
        jackpot = 100

        main_game()

        # Ask if the player wants to play again
        play_again = False
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        play_again = True
                        waiting = False
                    elif event.key == pygame.K_n:
                        waiting = False
            screen.fill(BLACK)
            again_text = FONT_MEDIUM.render("Do you want to play again? (Y/N)", True, WHITE)
            screen.blit(again_text, (WIDTH // 2 - again_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()

        if not play_again:
            break

    print("Thanks for playing Plinko Gambler!")
    pygame.quit()


if __name__ == "__main__":
    main()
