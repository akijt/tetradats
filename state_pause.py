import pygame
from sys import exit
import time
from utils import Sprite_group, Sprite_rect, Sprite_text, Sprite_button

def state_pause(screen, clock, game, colors, font_path, state, user_info, bindings):

    ### INIT STATE
    time_elapsed = game.stats['time']
    minutes      = int(time_elapsed // 60)
    seconds      = int(time_elapsed % 60)
    milliseconds = int(time_elapsed % 1 * 1000)

    pause_group = Sprite_group(
        resume_button = Sprite_button('bottomleft', (6, -7), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'resume', (255, 255, 255), 4, font_path),
        retry_button  = Sprite_button('bottomleft', (6, -4), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'retry', (255, 255, 255), 4, font_path),
        menu_button   = Sprite_button('bottomright', (-6, -7), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'menu', (255, 255, 255), 4, font_path),
        time_label    = Sprite_text('bottomleft', (6, 5), 'center', 'time', (255, 255, 255), 2, font_path),
        time_value    = Sprite_text('bottomleft', (6, 7), 'center', f'{minutes}:{seconds:02}.{milliseconds:03}', (255, 255, 255), 4, font_path),
        score_label   = Sprite_text('bottomleft', (6, 8), 'center', 'score', (255, 255, 255), 2, font_path),
        score_value   = Sprite_text('bottomleft', (6, 10), 'center', f'{game.stats["score"]}', (255, 255, 255), 4, font_path),
        pieces_label  = Sprite_text('bottomright', (-6, 2), 'center', 'pieces', (255, 255, 255), 2, font_path),
        pieces_value  = Sprite_text('bottomright', (-6, 4), 'center', f'{game.stats["pieces"]}', (255, 255, 255), 4, font_path),
        lines_label   = Sprite_text('bottomright', (-6, 5), 'center', 'lines', (255, 255, 255), 2, font_path),
        lines_value   = Sprite_text('bottomright', (-6, 7), 'center', f'{game.stats["lines"]}', (255, 255, 255), 4, font_path),
        level_label   = Sprite_text('bottomright', (-6, 8), 'center', 'level', (255, 255, 255), 2, font_path),
        level_value   = Sprite_text('bottomright', (-6, 10), 'center', f'{game.stats["level"]}', (255, 255, 255), 4, font_path),
        mode_text     = Sprite_text('midbottom', (0, 12), 'center', f'{game.stats["mode"]}', (255, 255, 255), 4, font_path)
    )

    account_group = Sprite_group(
        tab_rect  = Sprite_rect('topright', (-1, 1), 'topright', (8, 2), (0, 0, 0), (255, 255, 255), 2),
        pfp_rect  = Sprite_rect('topleft', (-8.75, 1.25), 'topright', (1.5, 1.5), (0, 0, 0), (255, 255, 255), 1),
        user_text = Sprite_text('bottomright', (-1.5, 2.6), 'topright', user_info['username'], (255, 255, 255), 2, font_path)
    )

    pause_group.resize(screen)
    account_group.resize(screen)

    while True:

        current_time = time.time()

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                pause_group.resize(screen)
                account_group.resize(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    game.pause(current_time)
                    state[0] = 'play'
                    return
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pause_group.get('resume_button').rect.collidepoint(pos):
                        game.pause(current_time)
                        state[0] = 'play'
                        return
                    elif pause_group.get('retry_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        return
                    elif pause_group.get('menu_button').rect.collidepoint(pos):
                        state[0] = 'menu'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, colors['1'], screen.get_rect())

        ### DRAW BLANK BOARD
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
        pygame.draw.rect(screen, (0, 0, 0), [screen.get_width() / 2 - 5 * dim, screen.get_height() / 2 - 10 * dim, 10 * dim + border_width, 20 * dim + border_width])
        for r in range(20):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                pygame.draw.rect(screen, (127, 127, 127), [left, top, dim + border_width, dim + border_width], border_width)

        ### DRAW SPRITES
        pause_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)