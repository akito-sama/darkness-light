import pygame


class Parser:

    def __init__(self, text):
        self.text = text
        self.screen = pygame.Surface((720, 480))
        self.index = 0
        self.up_rects = []
        self.down_rects = []
        self.right_rects = []
        self.left_rects = []
        self.dico = self.get_images()
        self.arrays = self.text[self.index:]
        self.creat_image()
        self.all_rects = self.up_rects + self.down_rects + self.right_rects + self.left_rects
        if __name__ == '__main__':
            self.draw_rects()

    @property
    def current_char(self):
        return self.text[self.index]

    def advance(self):
        self.index += 1

    def get_images(self):
        current_word = ""
        word = ""
        dico = {}
        current_key = None
        while current_word != "/*start*/":
            if self.current_char == '"':
                self.advance()
                while self.current_char != '"':
                    word += self.current_char
                    self.advance()
                dico[current_key] = pygame.image.load(word)
                word = ""
            elif self.current_char == ":":
                current_key = current_word.strip()
                current_word = ""
            elif self.current_char not in ('', '\n', ' '):
                current_word += self.current_char
            self.advance()
        return dico

    def creat_image(self):
        self.arrays = self.arrays.strip('\n').split('\n')
        for j in range(len(self.arrays)):
            images_keys = self.arrays[j].split(', ')
            for i in range(len(images_keys)):
                hint = images_keys[i]
                image = self.dico[hint.split('-')[0] if  '-' in hint else hint]
                self.screen.blit(image, (i * 60, j * 60))
                hint = hint[hint.find('-'):]
                if len(hint) > 1:
                    up, right, down, left = hint.split(".")
                    up = up.replace('-', '')
                    if up == "T":
                        self.up_rects.append(pygame.Rect((i * 60 + 5, j * 60), (50, 10)))
                    if down == "T":
                        self.down_rects.append(pygame.Rect((i * 60 + 5, j * 60 + 55), (50, 10)))
                    if right == "T":
                        self.right_rects.append(pygame.Rect((i * 60 + 55, j * 60 + 5), (10, 50)))
                    if left == "T":
                        self.left_rects.append(pygame.Rect((i * 60, j * 60 + 5), (10, 50)))

    def draw_rects(self):
        for i in self.all_rects:
            pygame.draw.rect(self.screen, 'red', i, 1)

    def check_collision(self, rect: pygame.Rect):
        for i in self.all_rects:
            if rect.colliderect(i):
                return True
        return False


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("test")
    with open("maps/lvl1.dmap", 'r') as text:
        parser = Parser(text.read())
    running = True
    screen.blit(parser.screen, (0, 0))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
