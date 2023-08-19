import pygame
import time
from utils import Sprite_rect, Sprite_text, Sprite_button

def state_pause(screen, clock, game, state, user_info, bindings):

    ### INIT STATE
    time_elapsed = game.stats['time']
    minutes      = int(time_elapsed // 60)
    seconds      = int(time_elapsed % 60)
    milliseconds = int(time_elapsed % 1 * 1000)

    resume_button = Sprite_button('resume', (8, 2), 'bottomleft', (6, -7), 'center', 'White', 2, 'White', 4, None)
    retry_button  = Sprite_button('retry', (8, 2), 'bottomleft', (6, -4), 'center', 'White', 2, 'White', 4, None)
    menu_button   = Sprite_button('menu', (8, 2), 'bottomright', (-6, -7), 'center', 'White', 2, 'White', 4, None)

    pause_group = pygame.sprite.Group()
    pause_group.add(resume_button)
    pause_group.add(retry_button)
    pause_group.add(menu_button)
    pause_group.add(Sprite_text('time', 'bottomleft', (6, 5), 'center', 'White', 2, None))
    pause_group.add(Sprite_text(f'{minutes}:{seconds:02}.{milliseconds:03}', 'bottomleft', (6, 7), 'center', 'White', 4, None))
    pause_group.add(Sprite_text('score', 'bottomleft', (6, 8), 'center', 'White', 2, None))
    pause_group.add(Sprite_text(f'{game.stats["score"]}', 'bottomleft', (6, 10), 'center', 'White', 4, None))
    pause_group.add(Sprite_text('pieces', 'bottomright', (-6, 2), 'center', 'White', 2, None))
    pause_group.add(Sprite_text(f'{game.stats["pieces"]}', 'bottomright', (-6, 4), 'center', 'White', 4, None))
    pause_group.add(Sprite_text('lines', 'bottomright', (-6, 5), 'center', 'White', 2, None))
    pause_group.add(Sprite_text(f'{game.stats["lines"]}', 'bottomright', (-6, 7), 'center', 'White', 4, None))
    pause_group.add(Sprite_text('level', 'bottomright', (-6, 8), 'center', 'White', 2, None))
    pause_group.add(Sprite_text(f'{game.stats["level"]}', 'bottomright', (-6, 10), 'center', 'White', 4, None))
    pause_group.add(Sprite_text(f'{game.stats["mode"]}', 'midbottom', (0, 12), 'center', 'White', 4, None))

    account_group = pygame.sprite.Group()
    account_group.add(Sprite_rect((8, 2), 'topright', (-1, 1), 'topright', 'White', 2))
    account_group.add(Sprite_rect((1.5, 1.5), 'topleft', (-8.75, 1.25), 'topright', 'White', 1))
    account_group.add(Sprite_text(user_info['username'], 'bottomright', (-1.5, 2.6), 'topright', 'White', 2, None))

    pause_group.update(screen)
    account_group.update(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                pause_group.update(screen)
                account_group.update(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    game.pause(time.time())
                    state[0] = 'play'
                    return
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if resume_button.rect.collidepoint(pos):
                        game.pause(time.time())
                        state[0] = 'play'
                        return
                    elif retry_button.rect.collidepoint(pos):
                        state[0] = 'countdown'
                        return
                    elif menu_button.rect.collidepoint(pos):
                        state[0] = 'menu'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BLANK BOARD
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
        for r in range(20):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                pygame.draw.rect(screen, 'Gray', [left, top, dim + border_width, dim + border_width], border_width)

        ### DRAW SPRITES
        pause_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(None, round(.75 * 2 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, 'White')
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)