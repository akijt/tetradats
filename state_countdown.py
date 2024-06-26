import pygame
from sys import exit
import time
from utils import Sprite_group, Sprite_rect, Sprite_text, Sprite_button

def state_countdown(screen, clock, game, colors, font_path, state, user_info, bindings, handling):

    ### INIT STATE
    game.reset(state[1], state[2], handling)
    countdown = time.time()

    countdown_group = Sprite_group(
        menu_button  = Sprite_button('topleft', (1, 1), 'topleft', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'menu', (255, 255, 255), 4, font_path),
        int_rect     = Sprite_button('midbottom', (0, -2), 'center', (8, 2), (255, 255, 255), (255, 255, 255), 0, '3', (0, 0, 0), 4, font_path),
        time_label   = Sprite_text('bottomleft', (6, 5), 'center', 'time', (255, 255, 255), 2, font_path),
        time_value   = Sprite_text('bottomleft', (6, 7), 'center', '0:00.000', (255, 255, 255), 4, font_path),
        score_label  = Sprite_text('bottomleft', (6, 8), 'center', 'score', (255, 255, 255), 2, font_path),
        score_value  = Sprite_text('bottomleft', (6, 10), 'center', '0', (255, 255, 255), 4, font_path),
        pieces_label = Sprite_text('bottomright', (-6, 2), 'center', 'pieces', (255, 255, 255), 2, font_path),
        pieces_value = Sprite_text('bottomright', (-6, 4), 'center', '0', (255, 255, 255), 4, font_path),
        lines_label  = Sprite_text('bottomright', (-6, 5), 'center', 'lines', (255, 255, 255), 2, font_path),
        lines_value  = Sprite_text('bottomright', (-6, 7), 'center', '0', (255, 255, 255), 4, font_path),
        level_label  = Sprite_text('bottomright', (-6, 8), 'center', 'level', (255, 255, 255), 2, font_path),
        level_value  = Sprite_text('bottomright', (-6, 10), 'center', f'{state[2]}', (255, 255, 255), 4, font_path),
        mode_text    = Sprite_text('midbottom', (0, 12), 'center', f'{game.stats["mode"]}', (255, 255, 255), 4, font_path)
    )

    account_group = Sprite_group(
        tab_rect  = Sprite_rect('topright', (-1, 1), 'topright', (8, 2), (0, 0, 0), (255, 255, 255), 2),
        pfp_rect  = Sprite_rect('topleft', (-8.75, 1.25), 'topright', (1.5, 1.5), (0, 0, 0), (255, 255, 255), 1),
        user_text = Sprite_text('bottomright', (-1.5, 2.6), 'topright', user_info['username'], (255, 255, 255), 2, font_path)
    )

    countdown_group.resize(screen)
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
                countdown_group.resize(screen)
                account_group.resize(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                    return
                elif event.key == bindings['reset']:
                    game.reset(state[1], state[2], handling)
                    countdown = current_time
                elif event.key == bindings['move_left']:
                    game.move_press('move_left', 'move_right', current_time)
                elif event.key == bindings['move_right']:
                    game.move_press('move_right', 'move_left', current_time)
                elif event.key == bindings['soft_drop']:
                    game.soft_drop(current_time)
                elif event.key == bindings['rotate_cw'] and game.stats['mode'] == 'classic':
                    state[2] = min(state[2] + 1, 20)
                    game.reset(state[1], state[2], handling)
                    countdown = current_time
                    countdown_group.get('level_value').update(text=f'{game.stats["level"]}')
                elif event.key == bindings['rotate_ccw'] and game.stats['mode'] == 'classic':
                    state[2] = max(state[2] - 1, 1)
                    game.reset(state[1], state[2], handling)
                    countdown = current_time
                    countdown_group.get('level_value').update(text=f'{game.stats["level"]}')
            elif event.type == pygame.KEYUP:
                if event.key == bindings['soft_drop']:
                    game.unsoft_drop()
                elif event.key == bindings['move_left']:
                    game.move_unpress('move_left', 'move_right', current_time)
                elif event.key == bindings['move_right']:
                    game.move_unpress('move_right', 'move_left', current_time)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if countdown_group.get('menu_button').rect.collidepoint(pos):
                        state[0] = 'menu'
                        return

        if current_time - countdown > 3:
            game.start(time.time())
            state[0] = 'play'
            return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, colors['b'], screen.get_rect())

        ### DRAW BOARD
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
        pygame.draw.rect(screen, (0, 0, 0), [screen.get_width() / 2 - 5 * dim, screen.get_height() / 2 - 10 * dim, 10 * dim + border_width, 20 * dim + border_width])
        for r in range(40):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                if game.board[r][c] != None:
                    pygame.draw.rect(screen, colors[game.board[r][c]], [left, top, dim + border_width, dim + border_width])
                elif r < 20:
                    pygame.draw.rect(screen, (127, 127, 127), [left, top, dim + border_width, dim + border_width], border_width)

        ### DRAW NEXT PIECES
        for p in range(game.next_num):
            for dr, dc in game.minos[game.queue[p]][0]:
                left = screen.get_width() / 2 + (6 + dc) * dim
                top = screen.get_height() / 2 + (-7 - dr + p * 4) * dim
                pygame.draw.rect(screen, colors[game.queue[p]], [left, top, dim + border_width, dim + border_width])

        ### DRAW SPRITES
        countdown_group.get('int_rect').update(text=f'{3 - int(current_time - countdown)}')
        countdown_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)