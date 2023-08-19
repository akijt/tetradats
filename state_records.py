import pygame
import datetime
from utils import Sprite_text, Sprite_button

def state_records(screen, clock, csv_registrar, sql_registrar, order_by, state, user_info, bindings):

    ### INIT STATE
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

    marathon_button = Sprite_button('marathon', (12, 2), 'bottomright', (-7, -7), 'center', 'White', 2 if state[1] != 'marathon' else 0, 'White' if state[1] != 'marathon' else 'Black', 4, None)
    sprint_button   = Sprite_button('sprint', (12, 2), 'midbottom', (0, -7), 'center', 'White', 2 if state[1] != 'sprint' else 0, 'White' if state[1] != 'sprint' else 'Black', 4, None)
    blitz_button    = Sprite_button('blitz', (12, 2), 'bottomleft', (7, -7), 'center', 'White', 2 if state[1] != 'blitz' else 0, 'White' if state[1] != 'blitz' else 'Black', 4, None)
    back_button     = Sprite_button('back', (6, 2), 'bottomleft', (1, -1), 'bottomleft', 'White', 2, 'White', 4, None)
    global_button   = Sprite_button('global', (8, 2), 'bottomright', (-1, -1), 'bottomright', 'White', 2 if state[2] != 'global' else 0, 'White' if state[2] != 'global' else 'Black', 4, None)

    records_group = pygame.sprite.Group()
    records_group.add(Sprite_text('RECORDS', 'midbottom', (0, -10), 'center', 'White', 4, None))
    records_group.add(marathon_button)
    records_group.add(sprint_button)
    records_group.add(blitz_button)
    records_group.add(back_button)
    records_group.add(global_button)
    for r in range(len(top_n)):
        records_group.add(Sprite_text(top_n[r][0], 'midbottom', (-13, -4.5 + r * 1.5), 'center', 'White', 2, None))
        for c in range(1, len(top_n[r])):
            records_group.add(Sprite_text(top_n[r][c], 'bottomleft', (-15 + c * 5, -4.5 + r * 1.5), 'center', 'White', 2, None))

    records_group.update(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                records_group.update(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.rect.collidepoint(pos):
                        state[0] = 'menu'
                        return
                    elif marathon_button.rect.collidepoint(pos):
                        state[1] = 'marathon'
                        return
                    elif sprint_button.rect.collidepoint(pos):
                        state[1] = 'sprint'
                        return
                    elif blitz_button.rect.collidepoint(pos):
                        state[1] = 'blitz'
                        return
                    elif global_button.rect.collidepoint(pos):
                        if state[2] == '':
                            state[2] = 'global'
                        elif user_info['username'] != 'guest':
                            state[2] = ''
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW SPRITES
        records_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(None, round(.75 * 2 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, 'White')
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)