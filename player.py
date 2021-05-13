import pygame
from weapon import Weapon
from plasma import Plasma
from sounds import Sounds


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.max_health = 300
        self.health = self.max_health
        self.game = game
        self.image = pygame.image.load("assets/player2.png").convert_alpha()
        self.image_right = pygame.transform.flip(self.image, True, False).convert_alpha()
        self.image_left = self.image.copy().convert_alpha()
        self.rect = self.image.get_rect(
            x=game.screen.get_width() // 2 - 100, y=game.screen.get_height() // 2
        )
        self.velocity = 3
        self.weapon = Weapon(self, game)
        self.all_plasma = pygame.sprite.Group()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        prop_health = self.health / self.max_health * 100
        prop_charge = self.weapon.charge / self.weapon.max_charge * 100
        rect = pygame.Rect(self.rect.left - self.image.get_width() + 5, self.rect.top - 30, prop_health, 3)
        max_rect = pygame.Rect(self.rect.left - self.image.get_width() + 5, self.rect.top - 30, 100, 3)
        charge_rect = pygame.Rect(self.rect.left - self.image.get_width() + 5, self.rect.top - 25, prop_charge, 3)
        charge_max_rect = pygame.Rect(self.rect.left - self.image.get_width() + 5, self.rect.top - 25, 100, 3)
        pygame.draw.rect(self.game.screen, "#0e0e0e", max_rect)
        pygame.draw.rect(self.game.screen, "#e6d16a", rect)
        if self.weapon.charge != 1:
            pygame.draw.rect(self.game.screen, "#0e0e0e", charge_max_rect)
            pygame.draw.rect(self.game.screen, "#00ccff", charge_rect)
        self.weapon.draw()

    def move_y(self, direction):
        can_move = True
        if direction and self.rect.y > 0:
            for rect in self.game.map.down_rects:
                if rect.colliderect(self.rect):
                    can_move = False
            if can_move:
                self.rect.y -= self.velocity
        elif (
            not direction
            and self.rect.y < self.game.screen.get_height() - self.image.get_height()
        ):
            for rect in self.game.map.up_rects:
                if rect.colliderect(self.rect):
                    can_move = False
            if can_move:
                self.rect.y += self.velocity

    def move_x(self, direction):
        can_move = True
        if not direction and self.rect.x > 0:
            for rect in self.game.map.right_rects:
                if rect.colliderect(self.rect):
                    can_move = False
            if can_move:
                self.rect.x -= self.velocity
                self.image = self.image_left
        elif (
            direction
            and self.rect.x < self.game.screen.get_width() - self.image.get_width()
        ):
            for rect in self.game.map.left_rects:
                if rect.colliderect(self.rect):
                    can_move = False
            if can_move:
                self.rect.x += self.velocity
                self.image = self.image_right

    def shoot(self):
        self.all_plasma.add(Plasma(self.weapon))
        Sounds.lazer.play()
        self.weapon.reset()

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.dead()
            self.game.game_over()

    def dead(self):
        self.health = self.max_health
        self.rect = self.image.get_rect(
            x=self.game.screen.get_width() // 2 - 100, y=self.game.screen.get_height() // 2
        )
        self.all_plasma = pygame.sprite.Group()
        self.weapon.charge = 0
