import pygame
from sys import exit
import time
from utils import Sprite_group, Sprite_text, Sprite_button

def state_finish(screen, clock, game, colors, db_type, registrar, order_by, font_path, state, bindings, user_info):

    ### INIT STATE
    result_str     = ''
    local_pos_str  = ''
    global_pos_str = ''
    if not game.lose:
        if state[1] == 'marathon':
            result_str = f'score: {game.stats["score"]}'
        elif state[1] == 'sprint':
            minutes      = int(game.stats['time'] // 60)
            seconds      = int(game.stats['time'] % 60)
            milliseconds = int(game.stats['time'] % 1 * 1000)
            result_str = f'time: {minutes}:{seconds:02}.{milliseconds:03}'
        elif state[1] == 'blitz':
            result_str = f'score: {game.stats["score"]}'

        if user_info['username'] != 'guest':
            row = [user_info['username'], time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime()), time.strftime('%z', time.localtime())] + [game.stats[stat] for stat in game.stat_names]
            if db_type == 'csv':
                position = registrar.save(row, state[1], order_by[state[1]])
            elif db_type == 'sql' or db_type == 'msa':
                position = registrar.save(row, order_by[state[1]])

            if position[0] == 1:
                local_pos_str = 'new best!'
            elif position[0] % 10 == 1 and position[0] // 10 % 100 != 1:
                local_pos_str = f'{position[0]}st best'
            elif position[0] % 10 == 2 and position[0] // 10 % 100 != 1:
                local_pos_str = f'{position[0]}nd best'
            elif position[0] % 10 == 3 and position[0] // 10 % 100 != 1:
                local_pos_str = f'{position[0]}rd best'
            else:
                local_pos_str = f'{position[0]}th best'

            if position[1] == 1:
                global_pos_str = 'global record!'
            elif position[1] % 10 == 1 and position[1] // 10 % 100 != 1:
                global_pos_str = f'global {position[1]}st'
            elif position[1] % 10 == 2 and position[1] // 10 % 100 != 1:
                global_pos_str = f'global {position[1]}nd'
            elif position[1] % 10 == 3 and position[1] // 10 % 100 != 1:
                global_pos_str = f'global {position[1]}rd'
            else:
                global_pos_str = f'global {position[1]}th'

    finish_group = Sprite_group(
        title_text      = Sprite_text('midbottom', (0, -10), 'center', 'FINISH' if not game.lose else 'LOSE', (255, 255, 255), 4, font_path),
        result_text     = Sprite_text('midbottom', (0, -2), 'center', result_str, (255, 255, 255), 4, font_path),
        local_pos_text  = Sprite_text('midbottom', (0, 0), 'center', local_pos_str, (255, 255, 255), 2, font_path),
        global_pos_text = Sprite_text('midbottom', (0, 2), 'center', global_pos_str, (255, 255, 255), 2, font_path),
        retry_button    = Sprite_button('midleft', (1, 10), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'retry', (255, 255, 255), 4, font_path),
        menu_button     = Sprite_button('midright', (-1, 10), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'menu', (255, 255, 255), 4, font_path)
    )

    finish_group.resize(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                finish_group.resize(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                    return
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if finish_group.get('retry_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        return
                    elif finish_group.get('menu_button').rect.collidepoint(pos):
                        state[0] = 'menu'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, colors['1'], screen.get_rect())

        ### DRAW SPRITES
        finish_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)