import pygame
import time
from animation import Animation

def state_login(screen, clock, sql_directory, state):

    ### INIT STATE
    animation = Animation(.5, time.time())
    input_fields = {'': '', 'user': '', 'pass': ''}
    cursor_pos = 0
    error_code = 0
    key_state  = {'Backspace': 0, 'Delete': 0, 'Left': 0, 'Right': 0}

    while True:

        ### ADJUST DIM
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        fonts = []
        fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
        fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
        border_width = 1

        ### INIT INTERACTABLES
        user_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        user_box.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)

        pass_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        pass_box.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 3 * dim)

        login_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        login_button.bottomleft = (screen.get_width() / 2 - 1 * dim, screen.get_height() / 2 + 7 * dim)

        signup_button = pygame.Rect(0, 0, 5 * dim, 2 * dim)
        signup_button.bottomright = (screen.get_width() / 2 - 2 * dim, screen.get_height() / 2 + 7 * dim)

        guest_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        guest_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 10 * dim)

        quit_button = pygame.Rect(0, 0, 6 * dim, 2 * dim)
        quit_button.bottomleft = (1 * dim, screen.get_height() - 1 * dim)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not (input_fields['user'] and input_fields['pass']):
                        error_code = (not input_fields['user']) + (not input_fields['pass']) * 2
                    else:
                        if state[0] == 'login':
                            acct_info = sql_directory.login(input_fields['user'], input_fields['pass'])
                        elif state[0] == 'signup':
                            acct_info = sql_directory.sign_up(input_fields['user'], input_fields['pass'])
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
                    if state[1] == 'user' and alphanumeric or state[1] == 'pass':
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
                    if quit_button.collidepoint(pos):
                        pygame.quit()
                        exit()
                    elif user_box.collidepoint(pos):
                        state[1] = 'user'
                        cursor_pos = len(input_fields[state[1]])
                    elif pass_box.collidepoint(pos):
                        state[1] = 'pass'
                        cursor_pos = len(input_fields[state[1]])
                    elif login_button.collidepoint(pos):
                        if not (input_fields['user'] and input_fields['pass']):
                            error_code = (not input_fields['user']) + (not input_fields['pass']) * 2
                        else:
                            if state[0] == 'login':
                                acct_info = sql_directory.login(input_fields['user'], input_fields['pass'])
                            elif state[0] == 'signup':
                                acct_info = sql_directory.sign_up(input_fields['user'], input_fields['pass'])
                            if acct_info:
                                state[0] = 'menu'
                                return acct_info
                            elif state[0] == 'login':
                                error_code = 4
                    elif signup_button.collidepoint(pos):
                        error_code = 0
                        input_fields = {'': '', 'user': '', 'pass': ''}
                        state_transition = ['signup', 'login']
                        state[0] = state_transition[state_transition.index(state[0]) - 1]
                    elif guest_button.collidepoint(pos):
                        input_fields['user'] = 'guest'
                        input_fields['pass'] = ''
                        acct_info = sql_directory.login(input_fields['user'], input_fields['pass'])
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

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW ANIMATION
        blocks, shade = animation.get(time.time())
        for i in blocks:
            pygame.draw.rect(screen, shade, [screen.get_width() / 2 + (i[0] - 2) * dim, screen.get_height() / 2 + (-11 - i[1]) * dim, dim + border_width, dim + border_width])
            # pygame.draw.rect(screen, 'White', [screen.get_width() / 2 + (i[0] - 2) * dim, screen.get_height() / 2 + (-11 - i[1]) * dim, dim + border_width, dim + border_width], border_width)

        ### DRAW TEXTBOXES
        pygame.draw.rect(screen, 'White', user_box, border_width + 1)
        pygame.draw.rect(screen, 'White', pass_box, border_width + 1)

        ### WRITE INPUT TEXT
        user_input_text = fonts[0].render(input_fields['user'][:cursor_pos] + '|' * (state[1] == 'user') + input_fields['user'][cursor_pos:], False, 'White')
        user_input_rect = user_input_text.get_rect()
        if user_input_rect.width < user_box.width - dim or cursor_pos < 8:
            user_input_rect.bottomleft = (user_box.left + .5 * dim, user_box.bottom - .4 * dim)
        else:
            user_input_rect.bottomright = (user_box.right - .5 * dim, user_box.bottom - .4 * dim)
        screen.blit(user_input_text, user_input_rect)
        clear_rect = pygame.Rect(0, 0, 4 * dim, 2 * dim)
        clear_rect.bottomright = user_box.bottomleft
        pygame.draw.rect(screen, 'Black', clear_rect)
        clear_rect.bottomleft = user_box.bottomright
        pygame.draw.rect(screen, 'Black', clear_rect)

        pass_input_text = fonts[0].render('*' * len(input_fields['pass'][:cursor_pos]) + '|' * (state[1] == 'pass') + '*' * len(input_fields['pass'][cursor_pos:]), False, 'White')
        pass_input_rect = pass_input_text.get_rect()
        pass_input_rect.bottomleft = (pass_box.left + .5 * dim, pass_box.bottom - .4 * dim)
        screen.blit(pass_input_text, pass_input_rect)

        ### DRAW RECT
        area_rect = pygame.Rect(0, 0, 16 * dim, 14 * dim)
        area_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 8 * dim)
        pygame.draw.rect(screen, 'White', area_rect, border_width + 1)

        ### DRAW BUTTONS
        pygame.draw.rect(screen, 'White', login_button, border_width + 1)
        pygame.draw.rect(screen, 'Black', signup_button)
        pygame.draw.rect(screen, 'Black', guest_button)
        pygame.draw.rect(screen, 'White', quit_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('LOGIN' if state[0] == 'login' else 'SIGN UP', False, 'White')
        state_rect = state_text.get_rect()
        state_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 6 * dim)
        screen.blit(state_text, state_rect)

        user_text = fonts[0].render('username', False, 'White')
        user_rect = user_text.get_rect()
        user_rect.bottomleft = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 4 * dim)
        screen.blit(user_text, user_rect)

        pass_text = fonts[0].render('password', False, 'White')
        pass_rect = pass_text.get_rect()
        pass_rect.bottomleft = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 + 1 * dim)
        screen.blit(pass_text, pass_rect)

        login_text = fonts[1].render('login' if state[0] == 'login' else 'sign up', False, 'White')
        login_rect = login_text.get_rect()
        login_rect.midbottom = login_button.midbottom
        screen.blit(login_text, login_rect)

        signup_text = fonts[0].render('sign up' if state[0] == 'login' else 'login', False, 'White')
        signup_rect = signup_text.get_rect()
        signup_rect.center = signup_button.center
        screen.blit(signup_text, signup_rect)

        guest_text = fonts[0].render('play as guest', False, 'White')
        guest_rect = guest_text.get_rect()
        guest_rect.center = guest_button.center
        screen.blit(guest_text, guest_rect)

        quit_text = fonts[1].render('quit', False, 'White')
        quit_rect = quit_text.get_rect()
        quit_rect.midbottom = quit_button.midbottom
        screen.blit(quit_text, quit_rect)

        ### ERROR HANDLING
        if state[0] == 'signup' and not sql_directory.username_available(input_fields['user']):
            error_text = fonts[0].render('username taken', False, 'White')
            error_rect = error_text.get_rect()
            error_rect.topright = user_box.bottomright
            screen.blit(error_text, error_rect)
        elif error_code & (1 << 0):
            error_text = fonts[0].render('enter username', False, 'White')
            error_rect = error_text.get_rect()
            error_rect.topright = user_box.bottomright
            screen.blit(error_text, error_rect)
        if error_code & (1 << 1):
            error_text = fonts[0].render('enter password', False, 'White')
            error_rect = error_text.get_rect()
            error_rect.topright = pass_box.bottomright
            screen.blit(error_text, error_rect)
        elif error_code & (1 << 2):
            error_text = fonts[0].render('incorrect password', False, 'White')
            error_rect = error_text.get_rect()
            error_rect.topright = pass_box.bottomright
            screen.blit(error_text, error_rect)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)