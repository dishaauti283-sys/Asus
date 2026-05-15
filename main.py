
import pygame
import random
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
FPS = 60

# Load assets (fallback if missing)
def load_image(name, size, color):
    try:
        return pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)), size)
    except:
        surf = pygame.Surface(size)
        surf.fill(color)
        return surf

player_img = load_image("player.jpeg", (60, 50), (0,255,0))
enemy_img = load_image("enemy.jpeg", (50, 40), (255,0,0))
bullet_img = load_image("bullet .jpeg", (6, 15), (255,255,255))
bg_img = load_image("background.jpeg", (WIDTH, HEIGHT), (0,0,20))

# Sounds (optional)
def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), name))
    except:
        return None

shoot_sound = load_sound("firempeg.mpeg")
explosion_sound = load_sound("explosion.mpeg")

font_big = pygame.font.SysFont(None, 64)
font_small = pygame.font.SysFont(None, 32)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.speed = 4
        self.lives = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        if shoot_sound:
            shoot_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-50)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2,6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.respawn()

    def respawn(self):
        self.rect.x = random.randint(0, WIDTH-50)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(2,6)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x,y))
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

def draw_text(text, font, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH//2, y))
    screen.blit(surface, rect)

def show_menu():
    while True:
        screen.blit(bg_img, (0,0))
        draw_text("Space Shooter", font_big, (255,255,255), 200)
        draw_text("Press ENTER to Start", font_small, (200,200,200), 300)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

def show_game_over(score):
    while True:
        screen.blit(bg_img, (0,0))
        draw_text("GAME OVER", font_big, (255,0,0), 200)
        draw_text(f"Score: {score}", font_small, (255,255,255), 300)
        draw_text("Press R to Restart or Q to Quit", font_small, (200,200,200), 350)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

def game_loop():
    global all_sprites, enemies, bullets

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)

    score = 0

    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    except:
        pass

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            #Request to remove explosion sound 
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)

        player_hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in player_hits:
            player.lives -= 1
            if explosion_sound:
                explosion_sound.play()
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)
            if player.lives <= 0:
                return score

        screen.blit(bg_img, (0,0))
        all_sprites.draw(screen)

        draw_text(f"Score: {score}", font_small, (255,255,255), 20)
        draw_text(f"Lives: {player.lives}", font_small, (255,255,255), 50)

        pygame.display.flip()

while True:
    if not show_menu():
        break
    score = game_loop()
    if not show_game_over(score):
        break

pygame.quit()
