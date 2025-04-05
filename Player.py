import pygame
import pygame.locals as local

# Two dimensional vector
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center=(10, 420))

        self.pos = vec((10, 430))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.jumping = False

    def move(self):
        self.acc = vec(0, 0.5)

        keys = pygame.key.get_pressed()

        if keys[pygame.locals.K_LEFT]:
            self.acc.x = -ACC
        if keys[pygame.locals.K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Screen warp
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3
            self.jumping = False

    def update(self, platforms):
        self.check_y_collisions(platforms)
        self.check_x_collisions(platforms)

    def check_y_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def check_x_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.x > 0:
            if hits:
                if self.pos.x < hits[0].rect.left:
                    self.pos.x = hits[0].rect.left - 1
                    self.vel.x = 0
                if self.pos.x > hits[0].rect.right:
                    self.pos.x = hits[0].rect.right + 1
                    self.vel.x = 0
