import pygame

class Sprite_rect(pygame.sprite.Sprite):

    def __init__(self, size, origin, offset, alignment, color):
        super().__init__()
        self.size      = size
        self.origin    = origin
        self.offset    = [x for x in offset]
        self.alignment = alignment
        self.color     = color
        
        if self.origin in ['topright', 'midright', 'bottomright']:
            self.offset[0] -= self.size[0]
        elif self.origin in ['midtop', 'center', 'midbottom']:
            self.offset[0] -= self.size[0] / 2
        if self.origin in ['bottomleft', 'midbottom', 'bottomright']:
            self.offset[1] -= self.size[1]
        elif self.origin in ['midleft', 'center', 'midright']:
            self.offset[1] -= self.size[1] / 2
    
    def update(self, screen_size, dim, width):
        self.image = pygame.Surface((self.size[0] * dim, self.size[1] * dim))
        self.rect = pygame.Rect(0, 0, self.size[0] * dim, self.size[1] * dim)
        pygame.draw.rect(self.image, self.color, self.rect, width)

        self.rect.topleft = (self.offset[0] * dim, self.offset[1] * dim)
        if self.alignment in ['topright', 'midright', 'bottomright']:
            self.rect.left += screen_size[0]
        elif self.alignment in ['midtop', 'center', 'midbottom']:
            self.rect.left += screen_size[0] / 2
        if self.alignment in ['bottomleft', 'midbottom', 'bottomright']:
            self.rect.top += screen_size[1]
        elif self.alignment in ['midleft', 'center', 'midright']:
            self.rect.top += screen_size[1] / 2

class Sprite_text(pygame.sprite.Sprite):
    pass

class Sprite_button(pygame.sprite.Sprite):
    pass

class Sprite_textfield(pygame.sprite.Sprite):
    pass