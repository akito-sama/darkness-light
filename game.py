import pygame
from player import Player
from monster import Monster
from fonts import Fonts
from itertools import cycle
from buttons import Button
from map import Parser


class Game:

    def __init__(self, screen):
        self.running = True
        self.screen = screen
        self.state = "title screen"
        self.score = 0
        self.cycle_alpha = cycle([*range(0, 256, 2)] + [*range(0, 256, 2)][::-1])
        self.player = Player(self)
        self.clock = pygame.time.Clock()
        self.banner = pygame.transform.scale2x(pygame.image.load("assets/banner.png"))
        self.all_monsters = pygame.sprite.Group()
        self.SpawnMonsterEvent = pygame.USEREVENT + 1
        self.play_button = Button("assets/playbutton.png", (300, 280))
        self.title_background = pygame.image.load("assets/background.png").convert()
        self.play_button.image = pygame.transform.scale2x(self.play_button.image).convert_alpha()
        self.read_lvl(1)
        self.lvl_background = self.map.screen.convert()
        self.background = self.title_background

    def event(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and self.state == "in game":
                    self.player.shoot()
            elif event.type == self.SpawnMonsterEvent and self.state == "in game":
                self.all_monsters.add(Monster(self))
                pygame.time.set_timer(self.SpawnMonsterEvent, 3000, True)
            elif event.type == pygame.KEYDOWN and self.state == "game over":
                self.state = "title screen"
            elif event.type == pygame.MOUSEBUTTONDOWN  and self.state == "title screen":
                print(event.pos)
                if self.play_button.rect.collidepoint(event.pos):
                    self.state = "in game"
                    self.background = self.lvl_background
                    self.reset_timer()

    def update(self):
        if self.state == "in game":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT]:
                self.player.weapon.rotate(-1)
            elif pressed[pygame.K_LEFT]:
                self.player.weapon.rotate(1)
            if pressed[pygame.K_z]:
                self.player.move_y(True)
            elif pressed[pygame.K_s]:
                self.player.move_y(False)
            if pressed[pygame.K_d]:
                self.player.move_x(True)
            elif pressed[pygame.K_q]:
                self.player.move_x(False)
            if pressed[pygame.K_UP]:
                self.player.weapon.charging()
            for plasma in self.player.all_plasma:
                plasma.move()
        pygame.display.flip()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.state == "in game":
            Fonts.render(self.screen, str(self.score), (0, 0))
            self.player.draw()
            for plasma in self.player.all_plasma:
                plasma.draw()
            for monster_ in self.all_monsters:
                monster_.move()
                if not monster_.is_dead:
                    monster_.draw_rects()
            self.all_monsters.draw(self.screen)
        elif self.state == "game over":
            width, height = self.screen.get_size()
            self.screen.blit(Fonts.game_over, (width//2 - Fonts.game_over.get_width() // 2, height // 2 - Fonts.game_over.get_height() // 2))
            self.screen.blit(Fonts.help_screen, (width//2 - Fonts.help_screen.get_width() // 2, height // 2 - Fonts.help_screen.get_height() // 2 + 40))
            Fonts.help_screen.set_alpha(next(self.cycle_alpha))
        if self.state == "title screen":
            self.screen.blit(self.banner, (260, 115))
            self.play_button.draw(self.screen)

    def reset_timer(self):
        pygame.time.set_timer(self.SpawnMonsterEvent, 200, True)

    def game_over(self):
        self.state = "game over"
        self.all_monsters = pygame.sprite.Group()
        self.score = 0
        self.background = self.title_background

    def read_lvl(self, index):
        with open(f'maps/lvl{index}.dmap', 'r') as lvl:
            self.map = Parser(lvl.read())
