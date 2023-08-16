import pygame
import time

def state_finish(screen, clock, game, csv_registrar, sql_registrar, order_by, state, bindings, user_info):

    ### INIT STATE
    if not game.lose and user_info['username'] != 'guest':
        row = [user_info['username'], time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime()), time.strftime('%z', time.localtime())] + [game.stats[stat] for stat in game.stat_names]
        position = csv_registrar.save(row, state[1], {'marathon': (5, 'desc'), 'sprint': (4, 'asc'), 'blitz': (5, 'desc')}[state[1]])
        position = sql_registrar.save(row, order_by[state[1]])

    while True:

        ### ADJUST DIM
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        fonts = []
        fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
        fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
        border_width = 1

        ### INIT INTERACTABLES
        retry_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        retry_button.midleft = (screen.get_width() / 2 + 1 * dim, screen.get_height() / 2 + 10 * dim)

        menu_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        menu_button.midright = (screen.get_width() / 2 - 1 * dim, screen.get_height() / 2 + 10 * dim)

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
                    if retry_button.collidepoint(pos):
                        state[0] = 'countdown'
                        return
                    elif menu_button.collidepoint(pos):
                        state[0] = 'menu'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        pygame.draw.rect(screen, 'White', retry_button, border_width + 1)
        pygame.draw.rect(screen, 'White', menu_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('FINISH' if not game.lose else 'LOSE', False, 'White')
        state_rect = state_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 - 10 * dim))
        screen.blit(state_text, state_rect)

        retry_text = fonts[1].render('retry', False, 'White')
        retry_rect = retry_text.get_rect(midbottom=retry_button.midbottom)
        screen.blit(retry_text, retry_rect)

        menu_text = fonts[1].render('menu', False, 'White')
        menu_rect = menu_text.get_rect(midbottom=menu_button.midbottom)
        screen.blit(menu_text, menu_rect)

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
            result_text = fonts[1].render(result_str, False, 'White')
            result_rect = result_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 - 2 * dim))
            screen.blit(result_text, result_rect)

            if position[0] == 1:
                pos_str = 'new best!'
            elif position[0] % 10 == 1 and position[0] // 10 % 100 != 1:
                pos_str = f'{position[0]}st best'
            elif position[0] % 10 == 2 and position[0] // 10 % 100 != 1:
                pos_str = f'{position[0]}nd best'
            elif position[0] % 10 == 3 and position[0] // 10 % 100 != 1:
                pos_str = f'{position[0]}rd best'
            else:
                pos_str = f'{position[0]}th best'
            pos_text = fonts[0].render(pos_str, False, 'White')
            pos_rect = pos_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(pos_text, pos_rect)

            if position[1] == 1:
                pos_str = 'global record!'
            elif position[1] % 10 == 1 and position[1] // 10 % 100 != 1:
                pos_str = f'global {position[1]}st best'
            elif position[1] % 10 == 2 and position[1] // 10 % 100 != 1:
                pos_str = f'global {position[1]}nd best'
            elif position[1] % 10 == 3 and position[1] // 10 % 100 != 1:
                pos_str = f'global {position[1]}rd best'
            else:
                pos_str = f'global {position[1]}th best'
            pos_text = fonts[0].render(pos_str, False, 'White')
            pos_rect = pos_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 + 2 * dim))
            screen.blit(pos_text, pos_rect)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)