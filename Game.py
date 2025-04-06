import sys
import random
import time
import pygame
import pygame.locals
import Player
import Platform

pygame.init()
game_over = False

# Two dimensional vector
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

lg_text = pygame.font.Font(None, 72)
md_text = pygame.font.Font(None, 24)
sm_text = pygame.font.Font(None, 20)

frames_per_sec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Create sprite groups
platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def generate_assets():
    global player_1
    global bottom
    # Create player sprite and bottom platform
    player_sprite = pygame.image.load("./assets/player_sprite.gif")
    player_1 = Player.Player()
    player_1.surf = player_sprite
    player_1.rect = player_1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 30))

    bottom = Platform.Platform()
    bottom.surf = pygame.Surface((WIDTH, 40))
    bottom_sprite = pygame.image.load("./assets/bottom_sprite.gif")
    bottom.surf = bottom_sprite
    bottom.rect = bottom.surf.get_rect(center=(WIDTH / 2, HEIGHT - 20))
    bottom.moving = False

    all_sprites.add(player_1)
    all_sprites.add(bottom)
    platforms.add(bottom)


def generate_platforms():
    new_platforms = []
    if not platforms:
        while len(platforms) + len(new_platforms) < 7:
            width = random.randrange(50, 75)
            C = True
            while C:
                pl = Platform.Platform()
                pl.rect.center = (
                    random.randrange(0, WIDTH - width),
                    random.randrange(-50, 0),
                )
                C = pl.check_collision(list(platforms) + new_platforms)
            new_platforms.append(pl)

    else:
        # Find highest platform (smallest y val) to prevent new platforms from generating below old platforms
        highest_platform = platforms.sprites()[0]
        for platform in platforms:
            if platform.rect.y < highest_platform.rect.y:
                highest_platform = platform
        while len(platforms) + len(new_platforms) < 7:
            width = random.randrange(50, 100)
            C = True
            while C:
                pl = Platform.Platform()
                pl.rect.center = (
                    random.randrange(0, WIDTH - width),
                    random.randrange(-50, highest_platform.rect.y + 15),
                )
                C = pl.check_collision(list(platforms) + new_platforms)
            new_platforms.append(pl)
    for platform in new_platforms:
        platforms.add(platform)
        all_sprites.add(platform)


# Initial player + ground generation
generate_assets()
# Initial platform generation
generate_platforms()

while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1.jump(platforms)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_1.cancel_jump()
            if event.key == pygame.K_ESCAPE and game_over:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                generate_assets()
                generate_platforms()
    if not game_over:
        display_surface.fill((135, 206, 250))
        score_text = md_text.render("Score: " + str(player_1.score), True, (0, 0, 0))
        display_surface.blit(score_text, (10, 10))
        for platform in platforms:
            platform.move()

        # Generate new platforms as player moves up
        if player_1.rect.top <= HEIGHT / 3:
            player_1.pos.y += abs(player_1.vel.y)
            for platform in platforms:
                platform.rect.y += abs(player_1.vel.y)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
            generate_platforms()
        for sprite in all_sprites:
            display_surface.blit(sprite.surf, sprite.rect)

        instruction_text = sm_text.render(
            "CONTROLS: Left and Right Arrows to move",
            True,
            (255, 255, 255),
        )
        instruction_text_2 = sm_text.render(
            "Up arrow to jump (hold to jump higher!)",
            True,
            (255, 255, 255),
        )
        display_surface.blit(
            instruction_text,
            (
                WIDTH / 2 - instruction_text.get_width() / 2,
                HEIGHT - 35,
            ),
        )
        display_surface.blit(
            instruction_text_2,
            (
                WIDTH / 2 - instruction_text_2.get_width() / 2,
                HEIGHT - 20,
            ),
        )

        if player_1.rect.top > HEIGHT:
            game_over = True
        player_1.move()
        player_1.update(platforms)
        pygame.display.update()
        frames_per_sec.tick(FPS)

    else:
        for entity in all_sprites:
            entity.kill()
            display_surface.fill((0, 0, 0))
            game_over_text = lg_text.render("Game Over", True, (255, 255, 255))
            retry_text = md_text.render(
                "Press 'Enter' to try again, or 'Esc' to quit",
                True,
                (255, 255, 255),
            )
            display_surface.blit(
                game_over_text,
                (
                    WIDTH / 2 - game_over_text.get_width() / 2,
                    HEIGHT / 2 - game_over_text.get_height() / 2,
                ),
            )
            display_surface.blit(
                retry_text,
                (
                    WIDTH / 2 - retry_text.get_width() / 2,
                    HEIGHT - 20 - retry_text.get_height() - 20,
                ),
            )
            pygame.display.update()
