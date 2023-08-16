import pygame
import datetime

def state_records(screen, clock, csv_registrar, sql_registrar, order_by, state, user_info, bindings):

    ### INIT STATE
    pass

    while True:

        ### ADJUST DIM
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        fonts = []
        fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
        fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
        border_width = 1

        ### INIT INTERACTABLES
        marathon_button = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        marathon_button.bottomright = (screen.get_width() / 2 - 7 * dim, screen.get_height() / 2 - 7 * dim)

        sprint_button = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        sprint_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 7 * dim)

        blitz_button = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        blitz_button.bottomleft = (screen.get_width() / 2 + 7 * dim, screen.get_height() / 2 - 7 * dim)

        back_button = pygame.Rect(0, 0, 6 * dim, 2 * dim)
        back_button.bottomleft = (1 * dim, screen.get_height() - 1 * dim)

        global_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        global_button.bottomright = (screen.get_width() - 1 * dim, screen.get_height() - 1 * dim)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.collidepoint(pos):
                        state[0] = 'menu'
                        return
                    elif marathon_button.collidepoint(pos):
                        state[1] = 'marathon'
                    elif sprint_button.collidepoint(pos):
                        state[1] = 'sprint'
                    elif blitz_button.collidepoint(pos):
                        state[1] = 'blitz'
                    elif global_button.collidepoint(pos):
                        if state[2] == '':
                            state[2] = 'global'
                        elif user_info['username'] != 'guest':
                            state[2] = ''

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        pygame.draw.rect(screen, 'White', marathon_button, border_width + 1 if state[1] != 'marathon' else 0)
        pygame.draw.rect(screen, 'White', sprint_button, border_width + 1 if state[1] != 'sprint' else 0)
        pygame.draw.rect(screen, 'White', blitz_button, border_width + 1 if state[1] != 'blitz' else 0)
        pygame.draw.rect(screen, 'White', back_button, border_width + 1)
        pygame.draw.rect(screen, 'White', global_button, border_width + 1 if state[2] == '' else 0)

        ### WRITE TEXT
        state_text = fonts[1].render('RECORDS', False, 'White')
        state_rect = state_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 - 10 * dim))
        screen.blit(state_text, state_rect)

        marathon_text = fonts[1].render('marathon', False, 'White' if state[1] != 'marathon' else 'Black')
        marathon_rect = marathon_text.get_rect(midbottom=marathon_button.midbottom)
        screen.blit(marathon_text, marathon_rect)

        sprint_text = fonts[1].render('sprint', False, 'White' if state[1] != 'sprint' else 'Black')
        sprint_rect = sprint_text.get_rect(midbottom=sprint_button.midbottom)
        screen.blit(sprint_text, sprint_rect)

        blitz_text = fonts[1].render('blitz', False, 'White' if state[1] != 'blitz' else 'Black')
        blitz_rect = blitz_text.get_rect(midbottom=blitz_button.midbottom)
        screen.blit(blitz_text, blitz_rect)

        back_text = fonts[1].render('back', False, 'White')
        back_rect = back_text.get_rect(midbottom=back_button.midbottom)
        screen.blit(back_text, back_rect)

        global_text = fonts[1].render('global', False, 'White' if state[2] == '' else 'Black')
        global_rect = global_text.get_rect(midbottom=global_button.midbottom)
        screen.blit(global_text, global_rect)

        # records_query = csv_registrar.load('' if state[2] == 'global' else user_info['username'], state[1], 10)
        # for r in range(len(records_query)):
        #     records_query[r] = [str(r) if r != 0 else ''] + records_query[r]
        #     if r != 0:
        #         records_query[r][2] = datetime.datetime.strptime(records_query[r][2], '%Y/%m/%d %H:%M:%S')
        records_query = sql_registrar.load('' if state[2] == 'global' else user_info['username'], state[1], order_by[state[1]], 10)
        top_n = []
        for r in range(len(records_query)):
            top_n.append([str(records_query[r][0])])
            if state[2] == 'global':
                top_n[r].append(records_query[r][1])
            if state[1] == 'marathon':
                top_n[r].append(str(records_query[r][6]))
            elif state[1] == 'sprint':
                top_n[r].append(records_query[r][5])
                if r != 0:
                    top_n[r][-1] = float(top_n[r][-1])
                    minutes      = int(top_n[r][-1] // 60)
                    seconds      = int(top_n[r][-1] % 60)
                    milliseconds = int(top_n[r][-1] % 1 * 1000)
                    top_n[r][-1] = f'{minutes}:{seconds:02}.{milliseconds:03}'
            elif state[1] == 'blitz':
                top_n[r].append(str(records_query[r][6]))
            top_n[r].append(records_query[r][2])
            if r != 0:
                if state[2] == '':
                    neg          = -1 if records_query[r][3][0] == '-' else 1
                    hours        = int(records_query[r][3][-4:-2])
                    minutes      = int(records_query[r][3][-2:])
                    top_n[r][-1] += datetime.timedelta(hours=hours, minutes=minutes) * neg
                top_n[r][-1] = top_n[r][-1].strftime('%m/%d/%Y, %H:%M:%S')
            
        for r in range(len(top_n)):
            int_text = fonts[0].render(top_n[r][0], False, 'White')
            int_rect = int_text.get_rect(midbottom=(screen.get_width() / 2 - 13 * dim, screen.get_height() / 2 + (-4.5 + r * 1.5) * dim))
            screen.blit(int_text, int_rect)
            for c in range(1, len(top_n[r])):
                stat_text = fonts[0].render(top_n[r][c], False, 'White')
                stat_rect = stat_text.get_rect(bottomleft=(screen.get_width() / 2 + (-15 + c * 5) * dim, screen.get_height() / 2 + (-4.5 + r * 1.5) * dim))
                screen.blit(stat_text, stat_rect)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)