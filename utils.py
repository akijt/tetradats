import pygame

class Sprite_rect(pygame.sprite.Sprite):

    def __init__(self, size, origin, offset, alignment, color, width):
        super().__init__()
        self.size      = size
        self.origin    = origin
        self.offset    = [x for x in offset]
        self.alignment = alignment
        self.color     = color
        self.width     = width
        
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.offset[0] -= self.size[0]
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.offset[0] -= self.size[0] / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.offset[1] -= self.size[1]
        elif self.origin in ['midleft', 'center', 'midright']:
            self.offset[1] -= self.size[1] / 2
    
    def update(self, screen):
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.image = pygame.Surface((self.size[0] * dim, self.size[1] * dim))
        self.rect = pygame.Rect(0, 0, self.size[0] * dim, self.size[1] * dim)
        pygame.draw.rect(self.image, self.color, self.rect, self.width)

        self.rect.topleft = (self.offset[0] * dim, self.offset[1] * dim)
        if self.alignment in ['topright', 'midright', 'bottomright']:
            self.rect.left += screen.get_width()
        elif self.alignment in ['midtop', 'center', 'midbottom']:
            self.rect.left += screen.get_width() / 2
        if self.alignment in ['bottomleft', 'midbottom', 'bottomright']:
            self.rect.top += screen.get_height()
        elif self.alignment in ['midleft', 'center', 'midright']:
            self.rect.top += screen.get_height() / 2

class Sprite_text(pygame.sprite.Sprite): # TODO: text change in update?

    def __init__(self, text, origin, offset, alignment, color, font_size, font_name=None):
        super().__init__()
        self.text      = text
        self.origin    = origin
        self.offset    = [x for x in offset]
        self.alignment = alignment
        self.color     = color
        self.font_size = font_size
        self.font_name = font_name
        
    def update(self, screen):
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        font = pygame.font.Font(self.font_name, round(.75 * self.font_size * dim))
        self.image = font.render(self.text, False, self.color)
        self.rect = self.image.get_rect()

        self.rect.topleft = (self.offset[0] * dim, self.offset[1] * dim)
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.rect.left -= self.rect.width
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.rect.left -= self.rect.width / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.rect.top -= self.rect.height
        elif self.origin in ['midleft', 'center', 'midright']:
            self.rect.top -= self.rect.height / 2

        if self.alignment in ['topright', 'midright', 'bottomright']:
            self.rect.left += screen.get_width()
        elif self.alignment in ['midtop', 'center', 'midbottom']:
            self.rect.left += screen.get_width() / 2
        if self.alignment in ['bottomleft', 'midbottom', 'bottomright']:
            self.rect.top += screen.get_height()
        elif self.alignment in ['midleft', 'center', 'midright']:
            self.rect.top += screen.get_height() / 2

class Sprite_button(pygame.sprite.Sprite): # TODO: text change in update?

    def __init__(self, text, size, origin, offset, alignment, rect_color, width, font_color, font_size, font_name=None):
        super().__init__()
        self.text       = text
        self.size       = size
        self.origin     = origin
        self.offset     = [x for x in offset]
        self.alignment  = alignment
        self.rect_color = rect_color
        self.width      = width
        self.font_color = font_color
        self.font_size  = font_size
        self.font_name  = font_name

        if self.origin in ['topright', 'midright', 'bottomright']:
            self.offset[0] -= self.size[0]
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.offset[0] -= self.size[0] / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.offset[1] -= self.size[1]
        elif self.origin in ['midleft', 'center', 'midright']:
            self.offset[1] -= self.size[1] / 2
    
    def update(self, screen):
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        self.image = pygame.Surface((self.size[0] * dim, self.size[1] * dim))
        self.rect = pygame.Rect(0, 0, self.size[0] * dim, self.size[1] * dim)
        pygame.draw.rect(self.image, self.rect_color, self.rect, self.width)

        font = pygame.font.Font(self.font_name, round(.75 * self.font_size * dim))
        text_image = font.render(self.text, False, self.font_color)
        text_rect = text_image.get_rect(midbottom=self.rect.midbottom)
        self.image.blit(text_image, text_rect)

        self.rect.topleft = (self.offset[0] * dim, self.offset[1] * dim)
        if self.alignment in ['topright', 'midright', 'bottomright']:
            self.rect.left += screen.get_width()
        elif self.alignment in ['midtop', 'center', 'midbottom']:
            self.rect.left += screen.get_width() / 2
        if self.alignment in ['bottomleft', 'midbottom', 'bottomright']:
            self.rect.top += screen.get_height()
        elif self.alignment in ['midleft', 'center', 'midright']:
            self.rect.top += screen.get_height() / 2

class Sprite_textfield(pygame.sprite.Sprite):
    
    def __init__(self, size, origin, offset, alignment, rect_color, width, font_color, font_size, font_name=None):
        super().__init__()
        self.text       = ''
        self.size       = size
        self.origin     = origin
        self.offset     = [x for x in offset]
        self.alignment  = alignment
        self.rect_color = rect_color
        self.width      = width
        self.font_color = font_color
        self.font_size  = font_size
        self.font_name  = font_name

        if self.origin in ['topright', 'midright', 'bottomright']:
            self.offset[0] -= self.size[0]
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.offset[0] -= self.size[0] / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.offset[1] -= self.size[1]
        elif self.origin in ['midleft', 'center', 'midright']:
            self.offset[1] -= self.size[1] / 2
    
    def update(self, screen, text='', cursor_pos=-1):
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio

        if cursor_pos >= 0:
            self.text = text[:cursor_pos] + '|' + text[cursor_pos:]
        else:
            self.text = text

        self.image = pygame.Surface((self.size[0] * dim, self.size[1] * dim))
        self.rect = pygame.Rect(0, 0, self.size[0] * dim, self.size[1] * dim)
        pygame.draw.rect(self.image, self.rect_color, self.rect, self.width)

        font = pygame.font.Font(self.font_name, round(.75 * self.font_size * dim))
        text_image = font.render(self.text, False, self.font_color)
        text_rect = text_image.get_rect(bottomleft=(self.rect.left + .5 * dim, self.rect.bottom - .4 * dim))
        if text_rect.width > self.rect.width - dim and cursor_pos > 8:
            text_rect.bottomright = (self.rect.right - .5 * dim, self.rect.bottom - .4 * dim)
        self.image.blit(text_image, text_rect)

        self.rect.topleft = (self.offset[0] * dim, self.offset[1] * dim)
        if self.alignment in ['topright', 'midright', 'bottomright']:
            self.rect.left += screen.get_width()
        elif self.alignment in ['midtop', 'center', 'midbottom']:
            self.rect.left += screen.get_width() / 2
        if self.alignment in ['bottomleft', 'midbottom', 'bottomright']:
            self.rect.top += screen.get_height()
        elif self.alignment in ['midleft', 'center', 'midright']:
            self.rect.top += screen.get_height() / 2