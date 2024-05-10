import pygame
from sys import exit
import time
from animation import Animation
from utils import Sprite_group, Sprite_rect, Sprite_text, Sprite_button, Sprite_textfield

def state_login(screen, clock, colors, db_type, directory, font_path, state):

    ### INIT STATE
    animation = Animation(.5, time.time())
    input_fields = {'user': '', 'pass': ''}
    cursor_pos = 0
    key_state  = {'Backspace': 0, 'Delete': 0, 'Left': 0, 'Right': 0}
    if db_type == 'csv':
        state_transition = ['user', '']
    else:
        state_transition = ['pass', 'user', '']

    login_group = Sprite_group(
        title_text    = Sprite_text('midbottom', (0, -6), 'center', 'LOGIN', (255, 255, 255), 4, font_path),
        menu_rect     = Sprite_rect('midbottom', (0, 8), 'center', (16, 14), (0, 0, 0), (255, 255, 255), 2),
        user_label    = Sprite_text('bottomleft', (-6, -4), 'center', 'username', (255, 255, 255), 2, font_path),
        pass_label    = Sprite_text('bottomleft', (-6, 1), 'center', 'password', (255, 255, 255), 2, font_path),
        user_box      = Sprite_textfield('midbottom', (0, -2), 'center', (12, 2), (0, 0, 0), (255, 255, 255), 2, (255, 255, 255), 2, font_path),
        pass_box      = Sprite_textfield('midbottom', (0, 3), 'center', (12, 2), (0, 0, 0), (255, 255, 255), 2, (255, 255, 255), 2, font_path),
        login_button  = Sprite_button('bottomleft', (-1, 7), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'login', (255, 255, 255), 4, font_path),
        signup_button = Sprite_button('bottomright', (-2, 7), 'center', (5, 2), (0, 0, 0), (0, 0, 0), 0, 'sign up', (255, 255, 255), 2, font_path),
        guest_button  = Sprite_button('midbottom', (0, 10), 'center', (8, 2), colors['b'], colors['b'], 0, 'play as guest', (255, 255, 255), 2, font_path),
        quit_button   = Sprite_button('bottomleft', (1, -1), 'bottomleft', (6, 2), (0, 0, 0), (255, 255, 255), 2, 'quit', (255, 255, 255), 4, font_path)
    )

    if db_type == 'csv': # hide password features and reorganize
        login_group.get('pass_label').offset = [50, 50]
        login_group.get('pass_box').offset = [50, 50]
        login_group.get('guest_button').offset = [50, 50]
        login_group.get('user_label').offset[1] += 2
        login_group.get('user_box').offset[1] += 2
        login_group.get('login_button').offset[1] -= 1
        login_group.get('signup_button').offset[1] -= 1

    error_group = Sprite_group(
        error1_text = Sprite_text('topright', (6, -2), 'center', '', (255, 255, 255), 2, font_path),
        error2_text = Sprite_text('topright', (6, 3), 'center', '', (255, 255, 255), 2, font_path)
    )

    if db_type == 'csv':
        error_group.get('error1_text').offset[1] += 2

    login_group.resize(screen)
    error_group.resize(screen)

    while True:

        current_time = time.time()

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                login_group.resize(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    acct_info = input_submit(db_type, directory, state, input_fields, error_group)
                    if acct_info:
                        return acct_info
                elif event.key == pygame.K_TAB:
                    state[1] = state_transition[state_transition.index(state[1]) - 1]
                    if state[1]:
                        cursor_pos = len(input_fields[state[1]])
                if state[1]:
                    if event.key == pygame.K_BACKSPACE:
                        key_state['Backspace'] = current_time - .05 + .3 # (- ARR + DAS)
                        key_state['Delete'] = 0
                        input_fields[state[1]] = input_fields[state[1]][:max(cursor_pos - 1, 0)] + input_fields[state[1]][cursor_pos:]
                        cursor_pos = max(cursor_pos - 1, 0)
                        input_subtract(directory, state, input_fields, error_group)
                    elif event.key == pygame.K_DELETE:
                        key_state['Delete'] = current_time - .05 + .3 # (- ARR + DAS)
                        key_state['Backspace'] = 0
                        input_fields[state[1]] = input_fields[state[1]][:cursor_pos] + input_fields[state[1]][cursor_pos + 1:]
                        input_subtract(directory, state, input_fields, error_group)
                    elif event.key == pygame.K_LEFT:
                        key_state['Left'] = current_time - .05 + .3 # (- ARR + DAS)
                        key_state['Right'] = 0
                        cursor_pos = max(cursor_pos - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        key_state['Right'] = current_time - .05 + .3 # (- ARR + DAS)
                        key_state['Left'] = 0
                        cursor_pos = min(cursor_pos + 1, len(input_fields[state[1]]))
                    elif len(event.unicode) == 1 and len(input_fields[state[1]]) < 16:
                        alphanumeric = (48 <= ord(event.unicode) <= 57 or 65 <= ord(event.unicode) <= 90 or 97 <= ord(event.unicode) <= 122)
                        if state[1] == 'user' and alphanumeric or state[1] == 'pass' and not event.unicode.isspace():
                            input_fields[state[1]] = input_fields[state[1]][:cursor_pos] + event.unicode + input_fields[state[1]][cursor_pos:]
                            cursor_pos += 1
                            input_add(directory, state, input_fields, error_group)
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
                    if login_group.get('quit_button').rect.collidepoint(pos):
                        pygame.quit()
                        exit()
                    elif login_group.get('user_box').rect.collidepoint(pos):
                        state[1] = 'user'
                        cursor_pos = len(input_fields['user'])
                    elif login_group.get('pass_box').rect.collidepoint(pos):
                        state[1] = 'pass'
                        cursor_pos = len(input_fields['pass'])
                    elif login_group.get('login_button').rect.collidepoint(pos):
                        acct_info = input_submit(db_type, directory, state, input_fields, error_group)
                        if acct_info:
                            return acct_info
                    elif login_group.get('signup_button').rect.collidepoint(pos):
                        input_fields = {'user': '', 'pass': ''}
                        login_group.get('signup_button').update(text=state[0])
                        state0_transition = ['signup', 'login']
                        state[0] = state0_transition[state0_transition.index(state[0]) - 1]
                        state[1] = ''
                        login_group.get('title_text').update(text=state[0].upper())
                        login_group.get('login_button').update(text=state[0])
                        error_group.get('error1_text').update(text='')
                        error_group.get('error2_text').update(text='')
                    elif login_group.get('guest_button').rect.collidepoint(pos):
                        input_fields['user'] = 'guest'
                        input_fields['pass'] = ''
                        if db_type == 'csv':
                            acct_info = directory.login(input_fields['user'])
                        elif db_type == 'sql' or db_type == 'msa':
                            acct_info = directory.login(input_fields['user'], input_fields['pass'])
                        state[0] = 'menu'
                        return acct_info
                    else:
                        state[1] = ''

        ### AUTOREPEAT FOR KEYBOARD
        if state[1]:
            if key_state['Backspace']:
                remove_timer = current_time - key_state['Backspace']
                if remove_timer > .05:
                    distance = int(remove_timer // .05)
                    key_state['Backspace'] += distance * .05
                    input_fields[state[1]] = input_fields[state[1]][:max(cursor_pos - distance, 0)] + input_fields[state[1]][cursor_pos:]
                    cursor_pos = max(cursor_pos - distance, 0)
                    input_subtract(directory, state, input_fields, error_group)
            elif key_state['Delete']:
                remove_timer = current_time - key_state['Delete']
                if remove_timer > .05:
                    distance = int(remove_timer // .05)
                    key_state['Delete'] += distance * .05
                    input_fields[state[1]] = input_fields[state[1]][:cursor_pos] + input_fields[state[1]][cursor_pos + distance:]
                    input_subtract(directory, state, input_fields, error_group)
            if key_state['Left']:
                move_timer = current_time - key_state['Left']
                if move_timer > .05:
                    distance = int(move_timer // .05)
                    key_state['Left'] += distance * .05
                    cursor_pos = max(cursor_pos - distance, 0)
            elif key_state['Right']:
                move_timer = current_time - key_state['Right']
                if move_timer > .05:
                    distance = int(move_timer // .05)
                    key_state['Right'] += distance * .05
                    cursor_pos = min(cursor_pos + distance, len(input_fields[state[1]]))

        ### CLEAR SCREEN
        pygame.draw.rect(screen, colors['b'], screen.get_rect())

        ### DRAW ANIMATION
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
        blocks, shade = animation.get(current_time)
        for i in blocks:
            pygame.draw.rect(screen, shade, [screen.get_width() / 2 + (i[0] - 2) * dim, screen.get_height() / 2 + (-11 - i[1]) * dim, dim + border_width, dim + border_width])
            # pygame.draw.rect(screen, (255, 255, 255), [screen.get_width() / 2 + (i[0] - 2) * dim, screen.get_height() / 2 + (-11 - i[1]) * dim, dim + border_width, dim + border_width], border_width)

        ### DRAW SPRITES
        login_group.get('user_box').update(text=input_fields['user'], cursor_pos=cursor_pos if state[1] == 'user' else -1)
        login_group.get('pass_box').update(text='*' * len(input_fields['pass']), cursor_pos=cursor_pos if state[1] == 'pass' else -1)
        login_group.draw(screen)
        error_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)

### INPUT FUNCTIONS AND ERROR HANDLING

def input_add(directory, state, input_fields, error_group):
    if state[1] == 'user':
        if state[0] == 'signup' and not directory.username_available(input_fields['user']):
            error_group.get('error1_text').update(text='username taken')
        elif error_group.get('error1_text').text == 'enter username' or error_group.get('error1_text').text == 'username taken':
            error_group.get('error1_text').update(text='')
    if state[1] == 'pass' and error_group.get('error2_text').text == 'enter password':
        error_group.get('error2_text').update(text='')

def input_subtract(directory, state, input_fields, error_group):
    if state[0] == 'signup' and state[1] == 'user':
        if not directory.username_available(input_fields['user']):
            error_group.get('error1_text').update(text='username taken')
        else:
            error_group.get('error1_text').update(text='')

def input_submit(db_type, directory, state, input_fields, error_group):
    if not input_fields['user']:
        error_group.get('error1_text').update(text='enter username')
    if not input_fields['pass'] and db_type != 'csv':
        error_group.get('error2_text').update(text='enter password')
    if input_fields['user'] and (input_fields['pass'] or db_type == 'csv'):
        if state[0] == 'login':
            if db_type == 'csv':
                acct_info = directory.login(input_fields['user'])
            elif db_type == 'sql' or db_type == 'msa':
                acct_info = directory.login(input_fields['user'], input_fields['pass'])
        elif state[0] == 'signup':
            if db_type == 'csv':
                acct_info = directory.sign_up(input_fields['user'])
            elif db_type == 'sql' or db_type == 'msa':
                acct_info = directory.sign_up(input_fields['user'], input_fields['pass'], time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime()), time.strftime('%z', time.localtime()))
        if acct_info:
            state[0] = 'menu'
            return acct_info
        elif state[0] == 'login':
            if db_type == 'csv':
                error_group.get('error1_text').update(text='void account')
            elif db_type == 'sql' or db_type == 'msa':
                error_group.get('error2_text').update(text='incorrect password')