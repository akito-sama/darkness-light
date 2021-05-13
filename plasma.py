import pygame
import math

image = pygame.image.load("assets/projectile.png")
coef = 1.8
image = pygame.transform.scale(image, tuple(map(round, (image.get_width() * coef,image.get_height() * coef))))


class Plasma(pygame.sprite.Sprite):
    def __init__(self, weapon):
        super().__init__()
        self.weapon = weapon
        self.damage = self.weapon.damage * self.weapon.charge
        self.center = self.weapon.center
        self.rect = list(weapon.position)
        self.velocity = 4
        weap_w, weap_h = self.weapon.image.get_size()
        self.radiant = math.atan2(
            self.center[1] - self.rect[1] - weap_h / 2,
            self.center[0] - self.rect[0] - weap_w / 2
        )
        degree = self.radiant * 180 / math.pi
        self.image = pygame.transform.rotate(image, -degree).convert_alpha()
        self.cosinus = math.cos(self.radiant) * self.velocity
        self.sinus = math.sin(self.radiant) * self.velocity
        self.update_rect()

    def move(self):
        width, height = self.weapon.game.screen.get_size()
        self.rect[0] -= self.cosinus
        self.rect[1] -= self.sinus
        if (not 0 - self.image.get_width() < self.rect[1] < height or
            not 0 - self.image.get_height() < self.rect[0] < width or
            self.weapon.game.map.check_collision(self.rectangle)):
            self.kill()
        # print(repr(self))

    def __repr__(self):
        return f"x : {self.rectangle.x}, y : {self.rectangle.y},\n\
        cos : {self.cosinus}, sin : {self.sinus}"

    def draw(self):
        self.update_rect()
        self.weapon.game.screen.blit(self.image, self.rectangle)

    def update_rect(self):
        self.rectangle = self.image.get_rect(x=self.rect[0], y=self.rect[1])
