import pygame, random, sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
W, H = screen.get_width(), screen.get_height()
pygame.display.set_caption("Tung Sahour")
clock = pygame.time.Clock()
font = pygame.font.Font(None, max(36, H // 12))

S = max(1.0, H / 480)


def new_stick():
    return {'x': random.randint(100, max(101, W - 100)),
            'y': random.randint(150, max(151, H - 150))}


def new_game():
    p = {'x': W // 2, 'y': H // 2, 'speed': 9 * S}
    en = [{'x': random.randint(0, W), 'y': random.randint(0, H),
           'dx': random.choice([-2, 2]) * S, 'dy': random.choice([-2, 2]) * S}
          for _ in range(4)]
    return p, new_stick(), en


player, stick, enemies = new_game()
touch_pos = None
score = 0
game_over = False


def draw_tung():
    x, y = player['x'], player['y']
    pygame.draw.rect(screen, (139, 90, 43), (x, y, 50 * S, 60 * S), border_radius=10)
    pygame.draw.circle(screen, (222, 184, 135), (x + 25 * S, y - 10 * S), 25 * S)
    pygame.draw.circle(screen, (0, 0, 0), (x + 18 * S, y - 15 * S), 5 * S)
    pygame.draw.circle(screen, (0, 0, 0), (x + 32 * S, y - 15 * S), 5 * S)
    pygame.draw.arc(screen, (0, 0, 0), (x + 15 * S, y - 10 * S, 20 * S, 10 * S), 3.14, 6.28, 3)
    pygame.draw.rect(screen, (101, 67, 33), (x + 10 * S, y + 60 * S, 10 * S, 15 * S))
    pygame.draw.rect(screen, (101, 67, 33), (x + 30 * S, y + 60 * S, 10 * S, 15 * S))


def draw_stick(s):
    pygame.draw.line(screen, (255, 215, 0), (s['x'] - 20 * S, s['y']), (s['x'] + 20 * S, s['y']), int(8 * S))
    pygame.draw.circle(screen, (255, 255, 0), (s['x'], s['y']), 12 * S)
    pygame.draw.circle(screen, (255, 255, 255), (s['x'] - 3 * S, s['y'] - 3 * S), 3 * S)


def draw_chair(e):
    pygame.draw.rect(screen, (200, 0, 0), (e['x'], e['y'], 40 * S, 40 * S), border_radius=5)
    pygame.draw.rect(screen, (150, 0, 0), (e['x'] + 5 * S, e['y'] + 5 * S, 30 * S, 30 * S))


def center(txt, y, color):
    t = font.render(txt, True, color)
    screen.blit(t, (W // 2 - t.get_width() // 2, y))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION):
            touch_pos = (event.x * W, event.y * H)
            if event.type == pygame.FINGERDOWN and game_over:
                player, stick, enemies = new_game()
                score = 0
                game_over = False
        elif event.type == pygame.FINGERUP:
            touch_pos = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            touch_pos = event.pos
            if game_over:
                player, stick, enemies = new_game()
                score = 0
                game_over = False
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            touch_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            touch_pos = None

    if touch_pos and not game_over:
        dx = touch_pos[0] - (player['x'] + 25 * S)
        dy = touch_pos[1] - (player['y'] + 25 * S)
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist > 5:
            player['x'] += dx / dist * player['speed']
            player['y'] += dy / dist * player['speed']

    player['x'] = max(0, min(W - 50 * S, player['x']))
    player['y'] = max(25 * S, min(H - 75 * S, player['y']))

    screen.fill((210, 180, 140))

    if not game_over:
        for e in enemies:
            e['x'] += e['dx']
            e['y'] += e['dy']
            if e['x'] < 0 or e['x'] > W - 40 * S:
                e['dx'] *= -1
            if e['y'] < 0 or e['y'] > H - 40 * S:
                e['dy'] *= -1
            draw_chair(e)
            if abs(e['x'] - player['x']) < 45 * S and abs(e['y'] - player['y']) < 45 * S:
                game_over = True

        draw_stick(stick)
        if abs(stick['x'] - player['x']) < 35 * S and abs(stick['y'] - player['y']) < 35 * S:
            score += 10
            stick = new_stick()

        draw_tung()
        screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (20, 20))
        center("Lhaq el 3asa!", 20, (101, 67, 33))
    else:
        center("Mesek el kursi!", H // 2 - 70, (255, 0, 0))
        center(f"Score: {score}", H // 2 - 15, (0, 0, 0))
        center("Touch to restart", H // 2 + 40, (0, 0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
