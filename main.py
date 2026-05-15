import pygame
import random

pygame.init()
pygame.mixer.init()

# SCREEN
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()

# IMAGES
background = pygame.image.load("background.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_img = pygame.image.load("bullet.jpeg")
player_img = pygame.transform.scale(player_img, (80, 80))

enemy_img = pygame.image.load("enemy.jpeg")
enemy_img = pygame.transform.scale(enemy_img, (80, 80))

bullet_img = pygame.Surface((8, 20))
bullet_img.fill((255, 255, 0))

# SOUNDS
fire_sound = pygame.mixer.Sound("firempeg.mpeg")
explosion_sound = pygame.mixer.Sound("explosion.mpeg")

# PLAYER
player_x = WIDTH // 2
player_y = HEIGHT - 120
player_speed = 7

# BULLET
bullet_x = 0
bullet_y = player_y
bullet_speed = 10
bullet_state = "ready"

# ENEMY
enemy_x = random.randint(0, WIDTH - 80)
enemy_y = 50
enemy_speed = 4

# SCORE
score = 0
font = pygame.font.SysFont(None, 40)

# PLAYER FUNCTION
def player(x, y):
    screen.blit(player_img, (x, y))

# ENEMY FUNCTION
def enemy(x, y):
    screen.blit(enemy_img, (x, y))

# FIRE BULLET
def fire_bullet(x, y):
    global bullet_state

    bullet_state = "fire"

    fire_sound.play()

    screen.blit(bullet_img, (x + 35, y))

# COLLISION
def collision(enemy_x, enemy_y, bullet_x, bullet_y):

    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5

    if distance < 50:
        return True

    return False

# GAME LOOP
running = True

while running:

    clock.tick(60)

    # BACKGROUND
    screen.blit(background, (0, 0))

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # KEYS
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # LIMITS
    if player_x < 0:
        player_x = 0

    if player_x > WIDTH - 80:
        player_x = WIDTH - 80

    # SHOOT
    if keys[pygame.K_SPACE]:

        if bullet_state == "ready":

            bullet_x = player_x
            bullet_y = player_y

            fire_bullet(bullet_x, bullet_y)

    # BULLET MOVEMENT
    if bullet_state == "fire":

        screen.blit(bullet_img, (bullet_x + 35, bullet_y))

        bullet_y -= bullet_speed

        if bullet_y < 0:
            bullet_state = "ready"

    # ENEMY MOVEMENT
    enemy_y += enemy_speed

    if enemy_y > HEIGHT:

        enemy_x = random.randint(0, WIDTH - 80)
        enemy_y = 50

    # COLLISION CHECK
    hit = collision(enemy_x, enemy_y, bullet_x, bullet_y)

    if hit:

        explosion_sound.play()

        score += 1

        bullet_state = "ready"
        bullet_y = player_y

        enemy_x = random.randint(0, WIDTH - 80)
        enemy_y = 50

    # DRAW
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)

    # SCORE
    score_text = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
