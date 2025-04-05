import sys
import random
import pygame
from pygame.locals import *
import Player
import Platform

pygame.init()

# Two dimensional vector
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

frames_per_sec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Create sprite groups
platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Create player sprite and bottom platform
player_1 = Player.Player()

bottom = Platform.Platform()
bottom.surf = pygame.Surface((WIDTH, 20))
bottom.surf.fill((255, 0, 0))
bottom.rect = bottom.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

all_sprites.add(player_1)
all_sprites.add(bottom)
platforms.add(bottom)


def generate_platforms():
    if not platforms:
        while len(platforms) < 7:
            width = random.randrange(50, 75)
            pl = Platform.Platform()
            pl.rect.center = (
                random.randrange(0, WIDTH - width),
                random.randrange(-50, 0),
            )
            platforms.add(pl)
            all_sprites.add(pl)

    else:
        # Find highest platform (smallest y val) to prevent new platforms from generating below old platforms
        highest_platform = platforms.sprites()[0]
        for platform in platforms:
            if platform.rect.y < highest_platform.rect.y:
                highest_platform = platform
        while len(platforms) < 7:
            width = random.randrange(50, 100)
            pl = Platform.Platform()
            pl.rect.center = (
                random.randrange(0, WIDTH - width),
                random.randrange(-50, highest_platform.rect.y + 15),
            )
            platforms.add(pl)
            all_sprites.add(pl)


# Initial platform generation
generate_platforms()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1.jump(platforms)

    display_surface.fill((0, 0, 0))

    # Generate new platforms only if the player has moved up
    if player_1.rect.top <= HEIGHT / 3:
        player_1.pos.y += abs(player_1.vel.y)
        for platform in platforms:
            platform.rect.y += abs(player_1.vel.y)
            if platform.rect.top >= HEIGHT:
                platform.kill()
        generate_platforms()

    for sprite in all_sprites:
        display_surface.blit(sprite.surf, sprite.rect)

    player_1.move()
    player_1.update(platforms)
    pygame.display.update()
    frames_per_sec.tick(FPS)
