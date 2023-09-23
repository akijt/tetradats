import pygame
from sys import exit
import time
from utils import Sprite_rect, Sprite_text, Sprite_button

def state_play(screen, clock, game, colors, font_path, state, user_info, bindings):

    ### INIT STATE
    pause_button = Sprite_button('pause', (8, 2), 'topleft', (1, 1), 'topleft', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    time_text    = Sprite_text('0:00.000', 'bottomleft', (6, 7), 'center', (255, 255, 255), 4, font_path)
    score_text   = Sprite_text('0', 'bottomleft', (6, 10), 'center', (255, 255, 255), 4, font_path)
    pieces_text  = Sprite_text('0', 'bottomright', (-6, 4), 'center', (255, 255, 255), 4, font_path)
    lines_text   = Sprite_text('0', 'bottomright', (-6, 7), 'center', (255, 255, 255), 4, font_path)
    level_text   = Sprite_text('1', 'bottomright', (-6, 10), 'center', (255, 255, 255), 4, font_path)
    last_text    = Sprite_text('', 'bottomright', (-6, -4), 'center', (255, 255, 255), 2, font_path)
    b2b_text     = Sprite_text('', 'bottomright', (-6, -3), 'center', (255, 255, 255), 2, font_path)
    combo_text   = Sprite_text('', 'bottomright', (-6, -2), 'center', (255, 255, 255), 2, font_path)

    play_group = pygame.sprite.Group()
    play_group.add(pause_button)
    play_group.add(Sprite_text('time', 'bottomleft', (6, 5), 'center', (255, 255, 255), 2, font_path))
    play_group.add(time_text)
    play_group.add(Sprite_text('score', 'bottomleft', (6, 8), 'center', (255, 255, 255), 2, font_path))
    play_group.add(score_text)
    play_group.add(Sprite_text('pieces', 'bottomright', (-6, 2), 'center', (255, 255, 255), 2, font_path))
    play_group.add(pieces_text)
    play_group.add(Sprite_text('lines', 'bottomright', (-6, 5), 'center', (255, 255, 255), 2, font_path))
    play_group.add(lines_text)
    play_group.add(Sprite_text('level', 'bottomright', (-6, 8), 'center', (255, 255, 255), 2, font_path))
    play_group.add(level_text)
    play_group.add(last_text)
    play_group.add(b2b_text)
    play_group.add(combo_text)
    play_group.add(Sprite_text(f'{game.stats["mode"]}', 'midbottom', (0, 12), 'center', (255, 255, 255), 4, font_path))

    account_group = pygame.sprite.Group()
    account_group.add(Sprite_rect((8, 2), 'topright', (-1, 1), 'topright', (255, 255, 255), 2))
    account_group.add(Sprite_rect((1.5, 1.5), 'topleft', (-8.75, 1.25), 'topright', (255, 255, 255), 1))
    account_group.add(Sprite_text(user_info['username'], 'bottomright', (-1.5, 2.6), 'topright', (255, 255, 255), 2, font_path))

    play_group.update(screen)
    account_group.update(screen)

    game.start(time.time())

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                play_group.update(screen)
                account_group.update(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    game.pause(time.time())
                    state[0] = 'pause'
                    return
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
                    return
                elif event.key == bindings['hold']:
                    game.hold(time.time())
                elif event.key == bindings['move_left']:
                    game.move(-1, time.time())
                    game.move_press(-1, time.time())
                elif event.key == bindings['move_right']:
                    game.move(1, time.time())
                    game.move_press(1, time.time())
                elif event.key == bindings['rotate_cw']:
                    game.rotate(1, time.time())
                elif event.key == bindings['rotate_180']:
                    game.rotate(2, time.time())
                elif event.key == bindings['rotate_ccw']:
                    game.rotate(3, time.time())
                elif event.key == bindings['soft_drop']:
                    game.soft_drop(time.time())
                elif event.key == bindings['hard_drop']:
                    game.hard_drop(time.time())
            elif event.type == pygame.KEYUP:
                if event.key == bindings['soft_drop']:
                    game.soft_drop(time.time(), down=False)
                elif event.key == bindings['move_left']:
                    game.move_press(-1, time.time(), down=False)
                elif event.key == bindings['move_right']:
                    game.move_press(1, time.time(), down=False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pause_button.rect.collidepoint(pos):
                        game.pause(time.time())
                        state[0] = 'pause'
                        return

        ### FRAME UPDATE
        game.frame_update(time.time())
        if game.finish:
            state[0] = 'finish'
            return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())

        ### DRAW BOARD
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
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
        time_elapsed = time.time() - game.stats['time']
        minutes      = int(time_elapsed // 60)
        seconds      = int(time_elapsed % 60)
        milliseconds = int(time_elapsed % 1 * 1000)

        time_text.update(screen, text=f'{minutes}:{seconds:02}.{milliseconds:03}')
        score_text.update(screen, text=f'{game.stats["score"]}')
        pieces_text.update(screen, text=f'{game.stats["pieces"]}')
        lines_text.update(screen, text=f'{game.stats["lines"]}')
        level_text.update(screen, text=f'{game.stats["level"]}')
        last_text.update(screen, text=f'{game.last_clear}')
        b2b_text.update(screen, text=f'{game.b2b} B2B' if game.b2b > 0 else '')
        combo_text.update(screen, text=f'{game.combo} combo' if game.combo > 0 else '')
        play_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.75 * 2 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)