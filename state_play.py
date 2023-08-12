import pygame
import time

def state_play(screen, clock, game, colors, state, user_info, bindings):

    ### INIT STATE
    pass # comes from 'countdown' or 'pause'

    while True:

        ### ADJUST DIM
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        fonts = []
        fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
        fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
        border_width = 1

        ### INIT INTERACTABLES
        pause_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        pause_button.topleft = (1 * dim, 1 * dim)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                    game.soft_drop() 
                elif event.key == bindings['hard_drop']:
                    game.hard_drop(time.time())
            elif event.type == pygame.KEYUP:
                if event.key == bindings['soft_drop']:
                    game.soft_drop(down=False)
                elif event.key == bindings['move_left']:
                    game.move_press(-1, time.time(), down=False)
                elif event.key == bindings['move_right']:
                    game.move_press(1, time.time(), down=False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pause_button.collidepoint(pos):
                        game.pause(time.time())
                        state[0] = 'pause'
                        return

        ### FRAME UPDATE
        game.frame_update(time.time())
        game.finished(time.time())
        if game.finish:
            state[0] = 'finish'
            return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BOARD
        for r in range(20):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                if game.board[r][c] != None:
                    pygame.draw.rect(screen, colors[game.board[r][c]], [left, top, dim + border_width, dim + border_width])
                else:
                    pygame.draw.rect(screen, 'Gray', [left, top, dim + border_width, dim + border_width], border_width)

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
                pygame.draw.rect(screen, colors[game.held], [left, top, dim + border_width, dim + border_width])

        ### DRAW NEXT PIECES
        next_num = 3
        for p in range(next_num):
            for dr, dc in game.minos[game.queue[p]][0]:
                left = screen.get_width() / 2 + (6 + dc) * dim
                top = screen.get_height() / 2 + (-7 - dr + p * 4) * dim
                pygame.draw.rect(screen, colors[game.queue[p]], [left, top, dim + border_width, dim + border_width])

        ### WRITE TEXT
        time_elapsed = time.time() - game.stats['time']
        minutes      = int(time_elapsed // 60)
        seconds      = int(time_elapsed % 60)
        milliseconds = int(time_elapsed % 1 * 1000)

        time_label_text = fonts[0].render('time', False, 'White')
        time_label_rect = time_label_text.get_rect()
        time_label_rect.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 5 * dim)
        screen.blit(time_label_text, time_label_rect)

        time_value_text = fonts[1].render(f'{minutes}:{seconds:02}.{milliseconds:03}', False, 'White')
        time_value_rect = time_value_text.get_rect()
        time_value_rect.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 7 * dim)
        screen.blit(time_value_text, time_value_rect)

        score_label_text = fonts[0].render('score', False, 'White')
        score_label_rect = time_label_text.get_rect()
        score_label_rect.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 8 * dim)
        screen.blit(score_label_text, score_label_rect)

        score_value_text = fonts[1].render(f'{game.stats["score"]}', False, 'White')
        score_value_rect = score_value_text.get_rect()
        score_value_rect.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 10 * dim)
        screen.blit(score_value_text, score_value_rect)

        pieces_label_text = fonts[0].render('pieces', False, 'White')
        pieces_label_rect = pieces_label_text.get_rect()
        pieces_label_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 2 * dim)
        screen.blit(pieces_label_text, pieces_label_rect)

        pieces_value_text = fonts[1].render(f'{game.stats["pieces"]}', False, 'White')
        pieces_value_rect = pieces_value_text.get_rect()
        pieces_value_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 4 * dim)
        screen.blit(pieces_value_text, pieces_value_rect)

        lines_label_text = fonts[0].render('lines', False, 'White')
        lines_label_rect = lines_label_text.get_rect()
        lines_label_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 5 * dim)
        screen.blit(lines_label_text, lines_label_rect)

        lines_value_text = fonts[1].render(f'{game.stats["lines"]}', False, 'White')
        lines_value_rect = lines_value_text.get_rect()
        lines_value_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 7 * dim)
        screen.blit(lines_value_text, lines_value_rect)

        level_label_text = fonts[0].render('level', False, 'White')
        level_label_rect = level_label_text.get_rect()
        level_label_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 8 * dim)
        screen.blit(level_label_text, level_label_rect)

        level_value_text = fonts[1].render(f'{game.stats["level"]}', False, 'White')
        level_value_rect = level_value_text.get_rect()
        level_value_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 10 * dim)
        screen.blit(level_value_text, level_value_rect)

        last_text = fonts[0].render(f'{game.last_clear}', False, 'White')
        last_rect = last_text.get_rect()
        last_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 4 * dim)
        screen.blit(last_text, last_rect)

        b2b_text = fonts[0].render(f'{game.b2b} B2B' if game.b2b > 0 else '', False, 'White')
        b2b_rect = b2b_text.get_rect()
        b2b_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 3 * dim)
        screen.blit(b2b_text, b2b_rect)

        combo_text = fonts[0].render(f'{game.combo} combo' if game.combo > 0 else '', False, 'White')
        combo_rect = combo_text.get_rect()
        combo_rect.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 2 * dim)
        screen.blit(combo_text, combo_rect)

        mode_text = fonts[1].render(f'{game.stats["mode"]}', False, 'White')
        mode_rect = mode_text.get_rect()
        mode_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 12 * dim)
        screen.blit(mode_text, mode_rect)

        ### DRAW BUTTON
        pygame.draw.rect(screen, 'White', pause_button, border_width + 1)

        ### WRITE TEXT
        pause_text = fonts[1].render('pause', False, 'White')
        pause_rect = pause_text.get_rect()
        pause_rect.midbottom = pause_button.midbottom
        screen.blit(pause_text, pause_rect)

        ### ACCOUNT TAB
        account_tab = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        account_tab.topright = (screen.get_width() - 1 * dim, 1 * dim)
        pygame.draw.rect(screen, 'White', account_tab, border_width + 1)

        account_text = fonts[0].render(user_info['username'], False, 'White')
        account_rect = account_text.get_rect()
        account_rect.bottomright = (account_tab.right - .5 * dim, account_tab.bottom - .4 * dim)
        screen.blit(account_text, account_rect)

        pfp_tab = pygame.Rect(0, 0, 1.5 * dim, 1.5 * dim)
        pfp_tab.bottomleft = (account_tab.left + .25 * dim, account_tab.bottom - .25 * dim)
        pygame.draw.rect(screen, 'White', pfp_tab, border_width)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)