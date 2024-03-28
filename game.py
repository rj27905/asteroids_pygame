import random
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_q, K_e

from objects import Rocket, Asteroid, Bullet, Explosion

### SETUP *********************************************************************
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Asteroids')

gunshot_sound = pygame.mixer.Sound("Asteroids_music_laser.wav")
explosion_sound = pygame.mixer.Sound("Asteroids_music_explosion.mp3")

font = pygame.font.Font('freesansbold.ttf', 32)

### Objects & Events **********************************************************
ADDAST1 = pygame.USEREVENT + 1
ADDAST2 = pygame.USEREVENT + 2
ADDAST3 = pygame.USEREVENT + 3
ADDAST4 = pygame.USEREVENT + 4
ADDAST5 = pygame.USEREVENT + 5
pygame.time.set_timer(ADDAST1, 2000)
pygame.time.set_timer(ADDAST2, 6000)
pygame.time.set_timer(ADDAST3, 10000)
pygame.time.set_timer(ADDAST4, 15000)
pygame.time.set_timer(ADDAST5, 20000)

rocket = Rocket(SIZE)

asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(rocket)

backgrounds = [f'assets/background/bg{i}s.png' for i in range(1,5)]
bg = pygame.image.load(random.choice(backgrounds))

startbg = pygame.image.load('start.jpg')

start_font = pygame.font.Font('freesansbold.ttf', 64)
start_text = start_font.render('Press SPACE to Start', True, (255, 255, 255))

score_font = pygame.font.Font('freesansbold.ttf', 24)

game_started = False
music_started = False
score = 0

### Game **********************************************************************
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        if not game_started:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_started = True
                    music_started = False

        elif game_started:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == K_SPACE:
                    pos = rocket.rect[:2]
                    bullet = Bullet(pos, rocket.dir, SIZE)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    gunshot_sound.play()
                if event.key == K_q:
                    rocket.rotate_left()
                if event.key == K_e:
                    rocket.rotate_right()

                elif event.type == ADDAST1:
                    ast = Asteroid(1, SIZE)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ADDAST2:
                    ast = Asteroid(2, SIZE)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ADDAST3:
                    ast = Asteroid(3, SIZE)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ADDAST4:
                    ast = Asteroid(4, SIZE)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ADDAST5:
                    ast = Asteroid(5, SIZE)
                    asteroids.add(ast)
                    all_sprites.add(ast)

    pressed_keys = pygame.key.get_pressed()
    rocket.update(pressed_keys)

    asteroids.update()
    bullets.update()
    explosions.update()

    win.blit(bg, (0, 0))

    if not game_started:
        win.blit(startbg, (0, 0))
        win.blit(start_text, (50, 400))
    else:
        for sprite in all_sprites:
            win.blit(sprite.surf, sprite.rect)
        win.blit(rocket.surf, rocket.rect)

        explosions.draw(win)

        for bullet in bullets:
            collision = pygame.sprite.spritecollide(bullet, asteroids, True)
            if collision:
                pos = bullet.rect[:2]
                explosion = Explosion(pos)
                explosions.add(explosion)
                score += 1
                explosion_sound.play()

                bullet.kill()
                bullets.remove(bullet)

        if pygame.sprite.spritecollideany(rocket, asteroids):
            rocket.kill()
            score = 0
            for sprite in all_sprites:
                sprite.kill()
            all_sprites.empty()
            rocket = Rocket(SIZE)
            all_sprites.add(rocket)
            game_started = False
            music_started = False

        score_text = score_font.render('Score: ' + str(score), True, (255, 255, 255))
        win.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

