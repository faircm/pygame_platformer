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
        self.surf.fill((139, 69, 19))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30))
        )
        self.moving = True
        self.speed = random.randint(-3, 3)
        self.point_value = abs(self.speed)

    def check_collision(self, groupies):
        if pygame.sprite.spritecollideany(self, groupies):
            return True
        else:
            for entity in groupies:
                if entity == self:
                    continue
                if (abs(self.rect.top - entity.rect.bottom) < 50) and (
                    abs(self.rect.bottom - entity.rect.top) < 50
                ):
                    if abs(self.rect.left - entity.rect.right) < 50 or (
                        abs(self.rect.right - entity.rect.left) < 50
                    ):
                        return True
        C = False
        return False

    def move(self):
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.right > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.left < 0:
                self.rect.left = WIDTH
