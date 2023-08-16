import pygame
import time

def state_pause(screen, clock, game, state, user_info, bindings):

    ### INIT STATE
    pass # pause() is called in same frame

    while True:

        ### ADJUST DIM
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        fonts = []
        fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
        fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
        border_width = 1

        ### INIT INTERACTABLES
        resume_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        resume_button.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 - 7 * dim)

        retry_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        retry_button.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 - 4 * dim)

        menu_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        menu_button.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 7 * dim)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                    if resume_button.collidepoint(pos):
                        game.pause(time.time())
                        state[0] = 'play'
                        return
                    elif retry_button.collidepoint(pos):
                        state[0] = 'countdown'
                        return
                    elif menu_button.collidepoint(pos):
                        state[0] = 'menu'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BLANK BOARD
        for r in range(20):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                pygame.draw.rect(screen, 'Gray', [left, top, dim + border_width, dim + border_width], border_width)

        ### WRITE TEXT
        time_elapsed = game.stats['time']
        minutes      = int(time_elapsed // 60)
        seconds      = int(time_elapsed % 60)
        milliseconds = int(time_elapsed % 1 * 1000)

        time_label_text = fonts[0].render('time', False, 'White')
        time_label_rect = time_label_text.get_rect(bottomleft=(screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 5 * dim))
        screen.blit(time_label_text, time_label_rect)

        time_value_text = fonts[1].render(f'{minutes}:{seconds:02}.{milliseconds:03}', False, 'White')
        time_value_rect = time_value_text.get_rect(bottomleft=(screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 7 * dim))
        screen.blit(time_value_text, time_value_rect)

        score_label_text = fonts[0].render('score', False, 'White')
        score_label_rect = time_label_text.get_rect(bottomleft=(screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 8 * dim))
        screen.blit(score_label_text, score_label_rect)

        score_value_text = fonts[1].render(f'{game.stats["score"]}', False, 'White')
        score_value_rect = score_value_text.get_rect(bottomleft=(screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 10 * dim))
        screen.blit(score_value_text, score_value_rect)

        pieces_label_text = fonts[0].render('pieces', False, 'White')
        pieces_label_rect = pieces_label_text.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 2 * dim))
        screen.blit(pieces_label_text, pieces_label_rect)

        pieces_value_text = fonts[1].render(f'{game.stats["pieces"]}', False, 'White')
        pieces_value_rect = pieces_value_text.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 4 * dim))
        screen.blit(pieces_value_text, pieces_value_rect)

        lines_label_text = fonts[0].render('lines', False, 'White')
        lines_label_rect = lines_label_text.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 5 * dim))
        screen.blit(lines_label_text, lines_label_rect)

        lines_value_text = fonts[1].render(f'{game.stats["lines"]}', False, 'White')
        lines_value_rect = lines_value_text.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 7 * dim))
        screen.blit(lines_value_text, lines_value_rect)

        level_label_text = fonts[0].render('level', False, 'White')
        level_label_rect = level_label_text.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 8 * dim))
        screen.blit(level_label_text, level_label_rect)

        level_value_text = fonts[1].render(f'{game.stats["level"]}', False, 'White')
        level_value_rect = level_value_text.get_rect(bottomright=(screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 10 * dim))
        screen.blit(level_value_text, level_value_rect)

        mode_text = fonts[1].render(f'{game.stats["mode"]}', False, 'White')
        mode_rect = mode_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 + 12 * dim))
        screen.blit(mode_text, mode_rect)

        ### DRAW BUTTONS
        pygame.draw.rect(screen, 'White', resume_button, border_width + 1)
        pygame.draw.rect(screen, 'White', retry_button, border_width + 1)
        pygame.draw.rect(screen, 'White', menu_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('PAUSE', False, 'White')
        state_rect = state_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 - 10 * dim))
        screen.blit(state_text, state_rect)

        resume_text = fonts[1].render('resume', False, 'White')
        resume_rect = resume_text.get_rect(midbottom=resume_button.midbottom)
        screen.blit(resume_text, resume_rect)

        retry_text = fonts[1].render('retry', False, 'White')
        retry_rect = retry_text.get_rect(midbottom=retry_button.midbottom)
        screen.blit(retry_text, retry_rect)

        menu_text = fonts[1].render('menu', False, 'White')
        menu_rect = menu_text.get_rect(midbottom=menu_button.midbottom)
        screen.blit(menu_text, menu_rect)

        ### ACCOUNT TAB
        account_tab = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        account_tab.topright = (screen.get_width() - 1 * dim, 1 * dim)
        pygame.draw.rect(screen, 'White', account_tab, border_width + 1)

        account_text = fonts[0].render(user_info['username'], False, 'White')
        account_rect = account_text.get_rect(bottomright=(account_tab.right - .5 * dim, account_tab.bottom - .4 * dim))
        screen.blit(account_text, account_rect)

        pfp_tab = pygame.Rect(0, 0, 1.5 * dim, 1.5 * dim)
        pfp_tab.bottomleft = (account_tab.left + .25 * dim, account_tab.bottom - .25 * dim)
        pygame.draw.rect(screen, 'White', pfp_tab, border_width)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)