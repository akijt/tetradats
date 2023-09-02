import pygame
from sys import exit
import time
from animation import Animation
from utils import Sprite_rect, Sprite_text, Sprite_button, Sprite_textfield

def state_login(screen, clock, dir_type, directory, font_path, state):

    ### INIT STATE
    animation = Animation(.5, time.time())
    input_fields = {'': '', 'user': '', 'pass': ''}
    cursor_pos = 0
    error_code = 0
    key_state  = {'Backspace': 0, 'Delete': 0, 'Left': 0, 'Right': 0}

    title_text    = Sprite_text('LOGIN', 'midbottom', (0, -6), 'center', (255, 255, 255), 4, font_path)
    user_box      = Sprite_textfield((12, 2), 'midbottom', (0, -2), 'center', (255, 255, 255), 2, (255, 255, 255), 2, font_path)
    pass_box      = Sprite_textfield((12, 2), 'midbottom', (0, 3), 'center', (255, 255, 255), 2, (255, 255, 255), 2, font_path)
    login_button  = Sprite_button('login', (8, 2), 'bottomleft', (-1, 7), 'center', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    signup_button = Sprite_button('sign up', (5, 2), 'bottomright', (-2, 7), 'center', (0, 0, 0), 0, (255, 255, 255), 2, font_path)
    guest_button  = Sprite_button('play as guest', (8, 2), 'midbottom', (0, 10), 'center', (0, 0, 0), 0, (255, 255, 255), 2, font_path)
    quit_button   = Sprite_button('quit', (6, 2), 'bottomleft', (1, -1), 'bottomleft', (255, 255, 255), 2, (255, 255, 255), 4, font_path)

    login_group = pygame.sprite.Group()
    login_group.add(title_text)
    login_group.add(Sprite_rect((16, 14), 'midbottom', (0, 8), 'center', (255, 255, 255), 2))
    login_group.add(Sprite_text('username', 'bottomleft', (-6, -4), 'center', (255, 255, 255), 2, font_path))
    login_group.add(Sprite_text('password', 'bottomleft', (-6, 1), 'center', (255, 255, 255), 2, font_path))
    login_group.add(user_box)
    login_group.add(pass_box)
    login_group.add(login_button)
    login_group.add(signup_button)
    login_group.add(guest_button)
    login_group.add(quit_button)

    error1_text = Sprite_text('', 'topright', (6, -2), 'center', (255, 255, 255), 2, font_path)
    error2_text = Sprite_text('', 'topright', (6, 3), 'center', (255, 255, 255), 2, font_path)
    error_group = pygame.sprite.Group()
    error_group.add(error1_text)
    error_group.add(error2_text)

    login_group.update(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                login_group.update(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not (input_fields['user'] and input_fields['pass']):
                        error_code = (not input_fields['user']) + (not input_fields['pass']) * 2
                    else:
                        if state[0] == 'login':
                            if dir_type == 'csv':
                                acct_info = directory.login(input_fields['user'])
                            elif dir_type == 'sql' or dir_type == 'msa':
                                acct_info = directory.login(input_fields['user'], input_fields['pass'])
                        elif state[0] == 'signup':
                            if dir_type == 'csv':
                                acct_info = directory.sign_up(input_fields['user'])
                            elif dir_type == 'sql' or dir_type == 'msa':
                                acct_info = directory.sign_up(input_fields['user'], input_fields['pass'], time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime()), time.strftime('%z', time.localtime()))
                        if acct_info:
                            state[0] = 'menu'
                            return acct_info
                        elif state[0] == 'login':
                            error_code = 4
                elif event.key == pygame.K_TAB:
                    state_transition = ['pass', 'user', '']
                    state[1] = state_transition[state_transition.index(state[1]) - 1]
                    cursor_pos = len(input_fields[state[1]])
                elif event.key == pygame.K_BACKSPACE:
                    key_state['Backspace'] = time.time() - .05 + .3 # (- ARR + DAS)
                    key_state['Delete'] = 0
                    input_fields[state[1]] = input_fields[state[1]][:max(cursor_pos - 1, 0)] + input_fields[state[1]][cursor_pos:]
                    cursor_pos = max(cursor_pos - 1, 0)
                elif event.key == pygame.K_DELETE:
                    key_state['Delete'] = time.time() - .05 + .3 # (- ARR + DAS)
                    key_state['Backspace'] = 0
                    input_fields[state[1]] = input_fields[state[1]][:cursor_pos] + input_fields[state[1]][cursor_pos + 1:]
                elif event.key == pygame.K_LEFT:
                    key_state['Left'] = time.time() - .05 + .3 # (- ARR + DAS)
                    key_state['Right'] = 0
                    cursor_pos = max(cursor_pos - 1, 0)
                elif event.key == pygame.K_RIGHT:
                    key_state['Right'] = time.time() - .05 + .3 # (- ARR + DAS)
                    key_state['Left'] = 0
                    cursor_pos = min(cursor_pos + 1, len(input_fields[state[1]]))
                elif len(event.unicode) == 1 and len(input_fields[state[1]]) < 16:
                    alphanumeric = (48 <= ord(event.unicode) <= 57 or 65 <= ord(event.unicode) <= 90 or 97 <= ord(event.unicode) <= 122)
                    if state[1] == 'user' and alphanumeric or state[1] == 'pass' and not event.unicode.isspace():
                        input_fields[state[1]] = input_fields[state[1]][:cursor_pos] + event.unicode + input_fields[state[1]][cursor_pos:]
                        cursor_pos += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    key_state['Backspace'] = 0
                elif event.key == pygame.K_DELETE:
                    key_state['Delete'] = 0
                elif event.key == pygame.K_LEFT:
                    key_state['Left'] = 0
                elif event.key == pygame.K_RIGHT:
                    key_state['Right'] = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if quit_button.rect.collidepoint(pos):
                        pygame.quit()
                        exit()
                    elif user_box.rect.collidepoint(pos):
                        state[1] = 'user'
                        cursor_pos = len(input_fields[state[1]])
                    elif pass_box.rect.collidepoint(pos):
                        state[1] = 'pass'
                        cursor_pos = len(input_fields[state[1]])
                    elif login_button.rect.collidepoint(pos):
                        if not (input_fields['user'] and input_fields['pass']):
                            error_code = (not input_fields['user']) + (not input_fields['pass']) * 2
                        else:
                            if state[0] == 'login':
                                if dir_type == 'csv':
                                    acct_info = directory.login(input_fields['user'])
                                elif dir_type == 'sql' or dir_type == 'msa':
                                    acct_info = directory.login(input_fields['user'], input_fields['pass'])
                            elif state[0] == 'signup':
                                if dir_type == 'csv':
                                    acct_info = directory.sign_up(input_fields['user'])
                                elif dir_type == 'sql' or dir_type == 'msa':
                                    acct_info = directory.sign_up(input_fields['user'], input_fields['pass'], time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime()), time.strftime('%z', time.localtime()))
                            if acct_info:
                                state[0] = 'menu'
                                return acct_info
                            elif state[0] == 'login':
                                error_code = 4
                    elif signup_button.rect.collidepoint(pos):
                        error_code = 0
                        input_fields = {'': '', 'user': '', 'pass': ''}
                        state_transition = ['signup', 'login']
                        signup_button.update(screen, text=state[0])
                        state[0] = state_transition[state_transition.index(state[0]) - 1]
                        title_text.update(screen, text=state[0].upper())
                        login_button.update(screen, text=state[0].upper())
                        state[1] = ''
                    elif guest_button.rect.collidepoint(pos):
                        input_fields['user'] = 'guest'
                        input_fields['pass'] = ''
                        if dir_type == 'csv':
                            acct_info = directory.login(input_fields['user'])
                        elif dir_type == 'sql' or dir_type == 'msa':
                            acct_info = directory.login(input_fields['user'], input_fields['pass'])
                        state[0] = 'menu'
                        return acct_info
                    else:
                        state[1] = ''

        ### AUTOREPEAT FOR KEYBOARD
        if key_state['Backspace']:
            remove_timer = time.time() - key_state['Backspace']
            if remove_timer > .05:
                distance = int(remove_timer // .05)
                key_state['Backspace'] += distance * .05
                input_fields[state[1]] = input_fields[state[1]][:max(cursor_pos - distance, 0)] + input_fields[state[1]][cursor_pos:]
                cursor_pos = max(cursor_pos - distance, 0)
        elif key_state['Delete']:
            remove_timer = time.time() - key_state['Delete']
            if remove_timer > .05:
                distance = int(remove_timer // .05)
                key_state['Delete'] += distance * .05
                input_fields[state[1]] = input_fields[state[1]][:cursor_pos] + input_fields[state[1]][cursor_pos + distance:]
        if key_state['Left']:
            move_timer = time.time() - key_state['Left']
            if move_timer > .05:
                distance = int(move_timer // .05)
                key_state['Left'] += distance * .05
                cursor_pos = max(cursor_pos - distance, 0)
        elif key_state['Right']:
            move_timer = time.time() - key_state['Right']
            if move_timer > .05:
                distance = int(move_timer // .05)
                key_state['Right'] += distance * .05
                cursor_pos = min(cursor_pos + distance, len(input_fields[state[1]]))

        ### ERROR HANDLING
        if state[0] == 'signup' and not directory.username_available(input_fields['user']):
            error1_text.update(screen, text='username taken')
        elif error_code & (1 << 0):
            error1_text.update(screen, text='enter username')
        else:
            error1_text.update(screen, text='')
        if error_code & (1 << 1):
            error2_text.update(screen, text='enter password')
        elif error_code & (1 << 2):
            error2_text.update(screen, text='incorrect password')
        else:
            error2_text.update(screen, text='')

        ### CLEAR SCREEN
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())

        ### DRAW ANIMATION
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
        blocks, shade = animation.get(time.time())
        for i in blocks:
            pygame.draw.rect(screen, shade, [screen.get_width() / 2 + (i[0] - 2) * dim, screen.get_height() / 2 + (-11 - i[1]) * dim, dim + border_width, dim + border_width])
            # pygame.draw.rect(screen, (255, 255, 255), [screen.get_width() / 2 + (i[0] - 2) * dim, screen.get_height() / 2 + (-11 - i[1]) * dim, dim + border_width, dim + border_width], border_width)

        ### DRAW SPRITES
        user_box.update(screen, text=input_fields['user'], cursor_pos=cursor_pos if state[1] == 'user' else -1)
        pass_box.update(screen, text='*' * len(input_fields['pass']), cursor_pos=cursor_pos if state[1] == 'pass' else -1)
        login_group.draw(screen)
        error_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.75 * 2 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)