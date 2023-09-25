import pygame

class Sprite_group():

    def __init__(self, dictionary=None, **kwargs):
        self.group = dictionary if isinstance(dictionary, dict) else {}
        self.group.update(kwargs)

    def add(self, dictionary=None, **kwargs):
        if isinstance(dictionary, dict):
            self.group.update(dictionary)
        self.group.update(kwargs)

    def get(self, name):
        return self.group[name]

    def resize(self, screen):
        for s in self.group.values():
            s.resize(screen)
            s.update()

    def update(self):
        for s in self.group.values():
            s.update()

    def draw(self, screen):
        for s in self.group.values():
            screen.blit(s.image, s.rect)

class Sprite_rect():

    def __init__(self, size, anchor, offset, origin, color, width):
        self.size   = size
        self.anchor = anchor
        self.offset = [x for x in offset]
        self.origin = origin
        self.color  = color
        self.width  = width

        if self.anchor in ['topright', 'midright', 'bottomright']:
            self.offset[0] -= self.size[0]
        elif self.anchor in ['midtop', 'center', 'midbottom']:
            self.offset[0] -= self.size[0] / 2
        if self.anchor in ['bottomleft', 'midbottom', 'bottomright']:
            self.offset[1] -= self.size[1]
        elif self.anchor in ['midleft', 'center', 'midright']:
            self.offset[1] -= self.size[1] / 2

    def resize(self, screen):
        self.dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.origin_offset = [0, 0]
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.origin_offset[0] = screen.get_width()
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.origin_offset[0] = screen.get_width() / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.origin_offset[1] = screen.get_height()
        elif self.origin in ['midleft', 'center', 'midright']:
            self.origin_offset[1] = screen.get_height() / 2

    def update(self, **kwargs):
        self.image = pygame.Surface((self.size[0] * self.dim, self.size[1] * self.dim))
        self.rect = pygame.Rect(0, 0, self.size[0] * self.dim, self.size[1] * self.dim)
        pygame.draw.rect(self.image, self.color, self.rect, self.width)
        self.rect.topleft = (self.origin_offset[0] + self.offset[0] * self.dim, self.origin_offset[1] + self.offset[1] * self.dim)

class Sprite_text():

    def __init__(self, text, anchor, offset, origin, color, font_size, font_name=None):
        self.text      = text
        self.anchor    = anchor
        self.offset    = [x for x in offset]
        self.origin    = origin
        self.color     = color
        self.font_size = font_size
        self.font_name = font_name

    def resize(self, screen):
        self.dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.origin_offset = [0, 0]
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.origin_offset[0] = screen.get_width()
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.origin_offset[0] = screen.get_width() / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.origin_offset[1] = screen.get_height()
        elif self.origin in ['midleft', 'center', 'midright']:
            self.origin_offset[1] = screen.get_height() / 2

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'text':
                self.text = v

        self.font = pygame.font.Font(self.font_name, round(.5 * self.font_size * self.dim))
        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect(topleft=(self.origin_offset[0] + self.offset[0] * self.dim, self.origin_offset[1] + self.offset[1] * self.dim))

        if self.anchor in ['topright', 'midright', 'bottomright']:
            self.rect.left -= self.rect.width
        elif self.anchor in ['midtop', 'center', 'midbottom']:
            self.rect.left -= self.rect.width / 2
        if self.anchor in ['bottomleft', 'midbottom', 'bottomright']:
            self.rect.top -= self.rect.height
        elif self.anchor in ['midleft', 'center', 'midright']:
            self.rect.top -= self.rect.height / 2

class Sprite_button():

    def __init__(self, text, size, anchor, offset, origin, rect_color, width, font_color, font_size, font_name=None):
        self.text       = text
        self.size       = size
        self.anchor     = anchor
        self.offset     = [x for x in offset]
        self.origin     = origin
        self.rect_color = rect_color
        self.width      = width
        self.font_color = font_color
        self.font_size  = font_size
        self.font_name  = font_name

        if self.anchor in ['topright', 'midright', 'bottomright']:
            self.offset[0] -= self.size[0]
        elif self.anchor in ['midtop', 'center', 'midbottom']:
            self.offset[0] -= self.size[0] / 2
        if self.anchor in ['bottomleft', 'midbottom', 'bottomright']:
            self.offset[1] -= self.size[1]
        elif self.anchor in ['midleft', 'center', 'midright']:
            self.offset[1] -= self.size[1] / 2

    def resize(self, screen):
        self.dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.origin_offset = [0, 0]
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.origin_offset[0] = screen.get_width()
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.origin_offset[0] = screen.get_width() / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.origin_offset[1] = screen.get_height()
        elif self.origin in ['midleft', 'center', 'midright']:
            self.origin_offset[1] = screen.get_height() / 2

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'text':
                self.text = v

        self.image = pygame.Surface((self.size[0] * self.dim, self.size[1] * self.dim))
        self.rect = pygame.Rect(0, 0, self.size[0] * self.dim, self.size[1] * self.dim)
        pygame.draw.rect(self.image, self.rect_color, self.rect, self.width)

        font = pygame.font.Font(self.font_name, round(.5 * self.font_size * self.dim))
        text_image = font.render(self.text, False, self.font_color)
        text_rect = text_image.get_rect(center=self.rect.center)
        self.image.blit(text_image, text_rect)

        self.rect.topleft = (self.origin_offset[0] + self.offset[0] * self.dim, self.origin_offset[1] + self.offset[1] * self.dim)

class Sprite_textfield():

    def __init__(self, size, anchor, offset, origin, rect_color, width, font_color, font_size, font_name=None):
        self.text       = ''
        self.size       = size
        self.anchor     = anchor
        self.offset     = [x for x in offset]
        self.origin     = origin
        self.rect_color = rect_color
        self.width      = width
        self.font_color = font_color
        self.font_size  = font_size
        self.font_name  = font_name
        self.cursor_pos = -1

        if self.anchor in ['topright', 'midright', 'bottomright']:
            self.offset[0] -= self.size[0]
        elif self.anchor in ['midtop', 'center', 'midbottom']:
            self.offset[0] -= self.size[0] / 2
        if self.anchor in ['bottomleft', 'midbottom', 'bottomright']:
            self.offset[1] -= self.size[1]
        elif self.anchor in ['midleft', 'center', 'midright']:
            self.offset[1] -= self.size[1] / 2

    def resize(self, screen):
        self.dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.origin_offset = [0, 0]
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.origin_offset[0] = screen.get_width()
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.origin_offset[0] = screen.get_width() / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.origin_offset[1] = screen.get_height()
        elif self.origin in ['midleft', 'center', 'midright']:
            self.origin_offset[1] = screen.get_height() / 2

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'text':
                self.text = v
            elif k == 'cursor_pos':
                self.cursor_pos = v

        text = self.text
        if self.cursor_pos >= 0:
            text = text[:self.cursor_pos] + '|' + text[self.cursor_pos:]

        self.image = pygame.Surface((self.size[0] * self.dim, self.size[1] * self.dim))
        self.rect = pygame.Rect(0, 0, self.size[0] * self.dim, self.size[1] * self.dim)
        pygame.draw.rect(self.image, self.rect_color, self.rect, self.width)

        font = pygame.font.Font(self.font_name, round(.5 * self.font_size * self.dim))
        text_image = font.render(text, False, self.font_color)
        text_rect = text_image.get_rect(bottomleft=(self.rect.left + .5 * self.dim, self.rect.bottom - .4 * self.dim))
        if text_rect.width > self.rect.width - self.dim and self.cursor_pos > 8:
            text_rect.bottomright = (self.rect.right - .5 * self.dim, self.rect.bottom - .4 * self.dim)
        self.image.blit(text_image, text_rect)

        self.rect.topleft = (self.origin_offset[0] + self.offset[0] * self.dim, self.origin_offset[1] + self.offset[1] * self.dim)

class Sprite_line():

    def __init__(self, length, offset, origin, color, width, orientation):
        self.length      = length
        self.offset      = [x for x in offset]
        self.origin      = origin
        self.color       = color
        self.width       = width
        self.orientation = orientation

    def resize(self, screen):
        self.dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.origin_offset = [0, 0]
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.origin_offset[0] = screen.get_width()
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.origin_offset[0] = screen.get_width() / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.origin_offset[1] = screen.get_height()
        elif self.origin in ['midleft', 'center', 'midright']:
            self.origin_offset[1] = screen.get_height() / 2

    def update(self, **kwargs):
        if self.orientation == 'horizontal':
            self.image = pygame.Surface((self.length * self.dim, self.width))
            self.rect = pygame.Rect(0, 0, self.length * self.dim, self.width)
        elif self.orientation == 'vertical':
            self.image = pygame.Surface((self.width, self.length * self.dim))
            self.rect = pygame.Rect(0, 0, self.width, self.length * self.dim)
        pygame.draw.rect(self.image, self.color, self.rect, self.width)

        self.rect.topleft = (self.origin_offset[0] + self.offset[0] * self.dim, self.origin_offset[1] + self.offset[1] * self.dim)
        if self.orientation == 'horizontal':
            self.rect.top -= self.width / 2
        elif self.orientation == 'vertical':
            self.rect.left -= self.width / 2

class Sprite_circle():

    def __init__(self, radius, offset, origin, color, width, back_color):
        self.radius     = radius
        self.offset     = [x for x in offset]
        self.origin     = origin
        self.color      = color
        self.width      = width
        self.back_color = back_color

    def resize(self, screen):
        self.dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.origin_offset = [0, 0]
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.origin_offset[0] = screen.get_width()
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.origin_offset[0] = screen.get_width() / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.origin_offset[1] = screen.get_height()
        elif self.origin in ['midleft', 'center', 'midright']:
            self.origin_offset[1] = screen.get_height() / 2

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k == 'offset':
                self.offset = [x for x in v]

        self.image = pygame.Surface((self.radius * 2 * self.dim, self.radius * 2 * self.dim))
        self.rect = pygame.Rect(0, 0, self.radius * 2 * self.dim, self.radius * 2 * self.dim)
        pygame.draw.rect(self.image, self.back_color, self.rect, 0)
        pygame.draw.circle(self.image, self.color, (self.radius * self.dim, self.radius * self.dim), self.radius * self.dim, self.width)
        # pygame.draw.circle(self.image, self.color, (int(self.radius * dim), int(self.radius * dim)), int(self.radius * dim), self.width) # TODO: PyInstaller issue

        self.rect.topleft = (self.origin_offset[0] + (self.offset[0] - self.radius) * self.dim, self.origin_offset[1] + (self.offset[1] - self.radius) * self.dim)