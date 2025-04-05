import random
import pygame
import pygame.locals

# Two dimensional vector
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30))
        )
