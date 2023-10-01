import pygame
from sys import exit
import time
from utils import Sprite_group, Sprite_rect, Sprite_text, Sprite_button

def state_play(screen, clock, game, colors, font_path, state, user_info, bindings):

    ### INIT STATE
    play_group = Sprite_group(
        pause_button = Sprite_button('topleft', (1, 1), 'topleft', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'pause', (255, 255, 255), 4, font_path),
        time_label   = Sprite_text('bottomleft', (6, 5), 'center', 'time', (255, 255, 255), 2, font_path),
        time_value   = Sprite_text('bottomleft', (6, 7), 'center', '0:00.000', (255, 255, 255), 4, font_path),
        score_label  = Sprite_text('bottomleft', (6, 8), 'center', 'score', (255, 255, 255), 2, font_path),
        score_value  = Sprite_text('bottomleft', (6, 10), 'center', '0', (255, 255, 255), 4, font_path),
        pieces_label = Sprite_text('bottomright', (-6, 2), 'center', 'pieces', (255, 255, 255), 2, font_path),
        pieces_value = Sprite_text('bottomright', (-6, 4), 'center', '0', (255, 255, 255), 4, font_path),
        lines_label  = Sprite_text('bottomright', (-6, 5), 'center', 'lines', (255, 255, 255), 2, font_path),
        lines_value  = Sprite_text('bottomright', (-6, 7), 'center', '0', (255, 255, 255), 4, font_path),
        level_label  = Sprite_text('bottomright', (-6, 8), 'center', 'level', (255, 255, 255), 2, font_path),
        level_value  = Sprite_text('bottomright', (-6, 10), 'center', '1', (255, 255, 255), 4, font_path),
        last_text    = Sprite_text('bottomright', (-6, -4), 'center', '', (255, 255, 255), 2, font_path),
        b2b_text     = Sprite_text('bottomright', (-6, -3), 'center', '', (255, 255, 255), 2, font_path),
        combo_text   = Sprite_text('bottomright', (-6, -2), 'center', '', (255, 255, 255), 2, font_path),
        mode_text    = Sprite_text('midbottom', (0, 12), 'center', f'{game.stats["mode"]}', (255, 255, 255), 4, font_path)
    )

    account_group = Sprite_group(
        tab_rect  = Sprite_rect('topright', (-1, 1), 'topright', (8, 2), (0, 0, 0), (255, 255, 255), 2),
        pfp_rect  = Sprite_rect('topleft', (-8.75, 1.25), 'topright', (1.5, 1.5), (0, 0, 0), (255, 255, 255), 1),
        user_text = Sprite_text('bottomright', (-1.5, 2.6), 'topright', user_info['username'], (255, 255, 255), 2, font_path)
    )

    play_group.resize(screen)
    account_group.resize(screen)

    game.start(time.time())

    while True:

        current_time = time.time()

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                play_group.resize(screen)
                account_group.resize(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    game.pause(current_time)
                    state[0] = 'pause'
                    return
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
                    return
                elif event.key == bindings['hold']:
                    game.hold(current_time)
                elif event.key == bindings['move_left']:
                    game.move(-1, current_time)
                    game.move_press(-1, current_time)
                elif event.key == bindings['move_right']:
                    game.move(1, current_time)
                    game.move_press(1, current_time)
                elif event.key == bindings['rotate_cw']:
                    game.rotate(1, current_time)
                elif event.key == bindings['rotate_180']:
                    game.rotate(2, current_time)
                elif event.key == bindings['rotate_ccw']:
                    game.rotate(3, current_time)
                elif event.key == bindings['soft_drop']:
                    game.soft_drop(current_time)
                elif event.key == bindings['hard_drop']:
                    game.hard_drop(current_time)
            elif event.type == pygame.KEYUP:
                if event.key == bindings['soft_drop']:
                    game.soft_drop(current_time, down=False)
                elif event.key == bindings['move_left']:
                    game.move_press(-1, current_time, down=False)
                elif event.key == bindings['move_right']:
                    game.move_press(1, current_time, down=False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if play_group.get('pause_button').rect.collidepoint(pos):
                        game.pause(current_time)
                        state[0] = 'pause'
                        return

        ### FRAME UPDATE
        game.frame_update(current_time)
        if game.finish:
            state[0] = 'finish'
            return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, colors['1'], screen.get_rect())

        ### DRAW BOARD
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
        pygame.draw.rect(screen, (0, 0, 0), [screen.get_width() / 2 - 5 * dim, screen.get_height() / 2 - 10 * dim, 10 * dim + border_width, 20 * dim + border_width])
        for r in range(20):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                if game.board[r][c] != None:
                    pygame.draw.rect(screen, colors[game.board[r][c]], [left, top, dim + border_width, dim + border_width])
                else:
                    pygame.draw.rect(screen, (128, 128, 128), [left, top, dim + border_width, dim + border_width], border_width)

        ### DRAW CURRENT PIECE
        for dr, dc in game.minos[game.piece][game.rotation]:
            left = screen.get_width() / 2 + (-5 + game.position[1] + dc) * dim
            top = screen.get_height() / 2 + (9 - game.position[0] - dr) * dim
            pygame.draw.rect(screen, colors[game.piece], [left, top, dim + border_width, dim + border_width])

        ### DRAW GHOST PIECE
        for dr, dc in game.minos[game.piece][game.rotation]:
            left = screen.get_width() / 2 + (-5 + game.position[1] + dc) * dim
            top = screen.get_height() / 2 + (9 - game.position[0] - dr + game.height) * dim
            pygame.draw.rect(screen, colors[game.piece], [left, top, dim + border_width, dim + border_width], border_width + 1)

        ### DRAW HELD PIECE
        if game.held != None:
            for dr, dc in game.minos[game.held][0]:
                left = screen.get_width() / 2 + (-10 + dc) * dim
                top = screen.get_height() / 2 + (-7 - dr) * dim
                if game.hold_used:
                    pygame.draw.rect(screen, (128, 128, 128), [left, top, dim + border_width, dim + border_width])
                else:
                    pygame.draw.rect(screen, colors[game.held], [left, top, dim + border_width, dim + border_width])

        ### DRAW NEXT PIECES
        next_num = 3
        for p in range(next_num):
            for dr, dc in game.minos[game.queue[p]][0]:
                left = screen.get_width() / 2 + (6 + dc) * dim
                top = screen.get_height() / 2 + (-7 - dr + p * 4) * dim
                pygame.draw.rect(screen, colors[game.queue[p]], [left, top, dim + border_width, dim + border_width])

        ### DRAW SPRITES
        time_elapsed = current_time - game.stats['time']
        minutes      = int(time_elapsed // 60)
        seconds      = int(time_elapsed % 60)
        milliseconds = int(time_elapsed % 1 * 1000)

        # fonts = []
        # fonts.append(pygame.font.Font(font_path, round(.5 * 2 * dim)))
        # fonts.append(pygame.font.Font(font_path, round(.5 * 4 * dim)))

        # time_value = play_group.get('time_value')
        # time_value.text = f'{minutes}:{seconds:02}.{milliseconds:03}'
        # time_value.image = fonts[1].render(time_value.text, False, time_value.color)
        # time_value.rect = time_value.image.get_rect(bottomleft=(screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 7 * dim))

        # score_value = play_group.get('score_value')
        # score_value.text = f'{game.stats["score"]}'
        # score_value.image = fonts[1].render(score_value.text, False, score_value.color)
        # score_value.rect = score_value.image.get_rect(bottomleft=(screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 10 * dim))

        # pieces_value = play_group.get('pieces_value')
        # pieces_value.text = f'{game.stats["pieces"]}'
        # pieces_value.image = fonts[1].render(pieces_value.text, False, pieces_value.color)
        # pieces_value.rect = pieces_value.image.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 4 * dim))

        # lines_value = play_group.get('lines_value')
        # lines_value.text = f'{game.stats["lines"]}'
        # lines_value.image = fonts[1].render(lines_value.text, False, lines_value.color)
        # lines_value.rect = lines_value.image.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 7 * dim))

        # level_value = play_group.get('level_value')
        # level_value.text = f'{game.stats["level"]}'
        # level_value.image = fonts[1].render(level_value.text, False, level_value.color)
        # level_value.rect = level_value.image.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 10 * dim))

        # last_text = play_group.get('last_text')
        # last_text.text = f'{game.last_clear}'
        # last_text.image = fonts[0].render(last_text.text, False, last_text.color)
        # last_text.rect = last_text.image.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 4 * dim))

        # b2b_text = play_group.get('b2b_text')
        # b2b_text.text = f'{game.b2b} B2B' if game.b2b > 0 else ''
        # b2b_text.image = fonts[0].render(b2b_text.text, False, b2b_text.color)
        # b2b_text.rect = b2b_text.image.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 3 * dim))

        # combo_text = play_group.get('combo_text')
        # combo_text.text = f'{game.combo} combo' if game.combo > 0 else ''
        # combo_text.image = fonts[0].render(combo_text.text, False, combo_text.color)
        # combo_text.rect = combo_text.image.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 2 * dim))

        play_group.get('time_value').update(text=f'{minutes}:{seconds:02}.{milliseconds:03}')
        play_group.get('score_value').update(text=f'{game.stats["score"]}')
        play_group.get('pieces_value').update(text=f'{game.stats["pieces"]}')
        play_group.get('lines_value').update(text=f'{game.stats["lines"]}')
        play_group.get('level_value').update(text=f'{game.stats["level"]}')
        play_group.get('last_text').update(text=f'{game.last_clear}')
        play_group.get('b2b_text').update(text=f'{game.b2b} B2B' if game.b2b > 0 else '')
        play_group.get('combo_text').update(text=f'{game.combo} combo' if game.combo > 0 else '')
        play_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)