import pygame
import time
from utils import Sprite_text, Sprite_button

def state_finish(screen, clock, game, csv_registrar, sql_registrar, order_by, state, bindings, user_info):

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
            position = csv_registrar.save(row, state[1], {'marathon': (5, 'desc'), 'sprint': (4, 'asc'), 'blitz': (5, 'desc')}[state[1]])
            position = sql_registrar.save(row, order_by[state[1]])

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
                global_pos_str = f'global {position[1]}st best'
            elif position[1] % 10 == 2 and position[1] // 10 % 100 != 1:
                global_pos_str = f'global {position[1]}nd best'
            elif position[1] % 10 == 3 and position[1] // 10 % 100 != 1:
                global_pos_str = f'global {position[1]}rd best'
            else:
                global_pos_str = f'global {position[1]}th best'

    retry_button = Sprite_button('retry', (8, 2), 'midleft', (1, 10), 'center', 'White', 2, 'White', 4, None)
    menu_button  = Sprite_button('menu', (8, 2), 'midright', (-1, 10), 'center', 'White', 2, 'White', 4, None)

    finish_group = pygame.sprite.Group()
    finish_group.add(Sprite_text('FINISH' if not game.lose else 'LOSE', 'midbottom', (0, -10), 'center', 'White', 4, None))
    finish_group.add(Sprite_text(result_str, 'midbottom', (0, -2), 'center', 'White', 4, None))
    finish_group.add(Sprite_text(local_pos_str, 'midbottom', (0, 0), 'center', 'White', 2, None))
    finish_group.add(Sprite_text(global_pos_str, 'midbottom', (0, 2), 'center', 'White', 2, None))
    finish_group.add(retry_button)
    finish_group.add(menu_button)

    while True:

        ### UPDATE SPRITES
        finish_group.update(screen)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                    if retry_button.rect.collidepoint(pos):
                        state[0] = 'countdown'
                        return
                    elif menu_button.rect.collidepoint(pos):
                        state[0] = 'menu'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW SPRITES
        finish_group.draw(screen)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)