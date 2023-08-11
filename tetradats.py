import pygame
from tetris import Tetris
from accounts import Accounts_sql
from records import Records_csv, Records_sql
from animation import Animation
import time # time.time() used over pygame.time.get_ticks() for precision
import datetime
from sys import exit

### INIT PYGAME
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Tetradats')
clock = pygame.time.Clock()

### INIT TETRIS
colors = {'z': 'Red',
          'l': 'Orange',
          'o': 'Yellow',
          's': 'Green',
          'i': 'Cyan',
          'j': 'Blue',
          't': 'Purple'}
game = Tetris()

### INIT DIRECTORY
header = ['username', 'password', 'quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop', 'DAS', 'ARR', 'SDF']
datatype = ['VARCHAR(16)' if h in ['username', 'password'] else
            'INT(4)'      if h in ['DAS', 'ARR', 'SDF'] else
            'INT'         for h in header]
sql_directory = Accounts_sql(header, datatype)

### INIT REGISTRAR
header = ['user', 'datetime', 'timezone'] + game.stat_names
datatype = ['VARCHAR(30)'    if h in ['user', 'mode'] else
            'DATETIME'       if h in ['datetime'] else
            'VARCHAR(5)'     if h in ['timezone'] else
            'DOUBLE(30, 15)' if h in ['time'] else
            'INT'            for h in header]
csv_registrar = Records_csv('records', ['marathon', 'sprint', 'blitz'], header)
sql_registrar = Records_sql('tetris', 'records', header, datatype)
order_by = {'marathon': 'score DESC', 'sprint': 'time ASC', 'blitz': 'score DESC'}

### INIT STATE
animation = Animation(.5, time.time())
input_fields = {'': '', 'user': '', 'pass': ''}
cursor_pos = 0
key_state  = {'Backspace': 0, 'Delete': 0, 'Left': 0, 'Right': 0}
error_code = 0
state = ['login', '', '']

while True: # TODO: individual classes/files for each page (merge countdown, play, pause into play)

    ### ADJUST DIM
    dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
    fonts = []
    fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
    fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
    border_width = 1

    ### LOGIN/SIGNUP STATE
    if state[0] == 'login' or state[0] == 'signup':
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
                            user_info, bindings, handling = acct_info
                            state[0] = 'menu'
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
                                user_info, bindings, handling = acct_info
                                state[0] = 'menu'
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
                        user_info, bindings, handling = acct_info
                        state[0] = 'menu'
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
        rect_width  = 12 * dim
        rect_height = 2 * dim

        user_box = pygame.Rect(0, 0, rect_width, rect_height)
        user_box.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)
        pygame.draw.rect(screen, 'White', user_box, border_width + 1)

        pass_box = pygame.Rect(0, 0, rect_width, rect_height)
        pass_box.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 3 * dim)
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
        login_button = pygame.Rect(0, 0, 8 * dim, rect_height)
        login_button.bottomleft = (screen.get_width() / 2 - 1 * dim, screen.get_height() / 2 + 7 * dim)
        pygame.draw.rect(screen, 'White', login_button, border_width + 1)

        signup_button = pygame.Rect(0, 0, 5 * dim, rect_height)
        signup_button.bottomright = (screen.get_width() / 2 - 2 * dim, screen.get_height() / 2 + 7 * dim)
        pygame.draw.rect(screen, 'Black', signup_button)

        guest_button = pygame.Rect(0, 0, 8 * dim, rect_height)
        guest_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 10 * dim)
        pygame.draw.rect(screen, 'Black', guest_button)

        quit_button = pygame.Rect(0, 0, 6 * dim, rect_height)
        quit_button.bottomleft = (1 * dim, screen.get_height() - 1 * dim)
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

    ### MENU STATE
    if state[0] == 'menu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if logout_button.collidepoint(pos):
                        animation = Animation(.5, time.time())
                        input_fields = {'': '', 'user': '', 'pass': ''}
                        cursor_pos = 0
                        key_state  = {'Backspace': 0, 'Delete': 0, 'Left': 0, 'Right': 0}
                        error_code = 0
                        state = ['login', '', '']
                    elif marathon_button.collidepoint(pos):
                        state = ['countdown', 'marathon', '']
                        game.reset(state[1], handling)
                        countdown = time.time()
                    elif sprint_button.collidepoint(pos):
                        state = ['countdown', 'sprint', '']
                        game.reset(state[1], handling)
                        countdown = time.time()
                    elif blitz_button.collidepoint(pos):
                        state = ['countdown', 'blitz', '']
                        game.reset(state[1], handling)
                        countdown = time.time()
                    elif records_button.collidepoint(pos):
                        state = ['records', 'marathon', '']
                        if user_info['username'] == 'guest':
                            state[2] = 'global'
                    elif settings_button.collidepoint(pos):
                        error_code = 0
                        input_fields = {'': ''}
                        for k, v in user_info.items():
                            input_fields[k] = v
                        for k, v in bindings.items():
                            input_fields[k] = v
                        for k, v in handling.items():
                            input_fields[k] = v
                        input_fields['password'] = ''
                        input_fields['new_pass1'] = ''
                        input_fields['new_pass2'] = ''
                        state = ['settings', 'account', '']

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        rect_width  = 14 * dim
        rect_height = 2 * dim

        marathon_button = pygame.Rect(0, 0, rect_width, rect_height)
        marathon_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 4 * dim)
        pygame.draw.rect(screen, 'White', marathon_button, border_width + 1)

        sprint_button = pygame.Rect(0, 0, rect_width, rect_height)
        sprint_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 1 * dim)
        pygame.draw.rect(screen, 'White', sprint_button, border_width + 1)

        blitz_button = pygame.Rect(0, 0, rect_width, rect_height)
        blitz_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 2 * dim)
        pygame.draw.rect(screen, 'White', blitz_button, border_width + 1)

        records_button = pygame.Rect(0, 0, rect_width, rect_height)
        records_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 5 * dim)
        pygame.draw.rect(screen, 'White', records_button, border_width + 1)

        settings_button = pygame.Rect(0, 0, rect_width, rect_height)
        settings_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 8 * dim)
        pygame.draw.rect(screen, 'White', settings_button, border_width + 1)

        logout_button = pygame.Rect(0, 0, 8 * dim, rect_height)
        logout_button.bottomleft = (1 * dim, screen.get_height() - 1 * dim)
        pygame.draw.rect(screen, 'White', logout_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('TETRADATS', False, 'White')
        state_rect = state_text.get_rect()
        state_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 10 * dim)
        screen.blit(state_text, state_rect)

        marathon_text = fonts[1].render('marathon', False, 'White')
        marathon_rect = marathon_text.get_rect()
        marathon_rect.midbottom = marathon_button.midbottom
        screen.blit(marathon_text, marathon_rect)

        sprint_text = fonts[1].render('sprint', False, 'White')
        sprint_rect = sprint_text.get_rect()
        sprint_rect.midbottom = sprint_button.midbottom
        screen.blit(sprint_text, sprint_rect)

        blitz_text = fonts[1].render('blitz', False, 'White')
        blitz_rect = blitz_text.get_rect()
        blitz_rect.midbottom = blitz_button.midbottom
        screen.blit(blitz_text, blitz_rect)

        records_text = fonts[1].render('records', False, 'White')
        records_rect = records_text.get_rect()
        records_rect.midbottom = records_button.midbottom
        screen.blit(records_text, records_rect)

        settings_text = fonts[1].render('settings', False, 'White')
        settings_rect = settings_text.get_rect()
        settings_rect.midbottom = settings_button.midbottom
        screen.blit(settings_text, settings_rect)

        logout_text = fonts[1].render('logout', False, 'White')
        logout_rect = logout_text.get_rect()
        logout_rect.midbottom = logout_button.midbottom
        screen.blit(logout_text, logout_rect)

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

    ### COUNTDOWN STATE
    elif state[0] == 'countdown':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                elif event.key == bindings['reset']:
                    game.reset(state[1], handling)
                    countdown = time.time()
                elif event.key == bindings['move_left']:
                    game.move_press(-1, time.time())
                elif event.key == bindings['move_right']:
                    game.move_press(1, time.time())
                elif event.key == bindings['soft_drop']:
                    game.soft_drop()
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
                    if menu_button.collidepoint(pos):
                        state[0] = 'menu'

        if time.time() - countdown > 3:
            game.start(time.time())
            state[0] = 'play'

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW EMPTY BOARD
        for r in range(20):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                pygame.draw.rect(screen, 'Gray', [left, top, dim + border_width, dim + border_width], border_width)

        ### DRAW NEXT PIECES
        next_num = 3
        for p in range(next_num):
            for dr, dc in game.minos[game.queue[p]][0]:
                left = screen.get_width() / 2 + (6 + dc) * dim
                top = screen.get_height() / 2 + (-7 - dr + p * 4) * dim
                pygame.draw.rect(screen, colors[game.queue[p]], [left, top, dim + border_width, dim + border_width])

        ### WRITE TEXT
        time_label_text = fonts[0].render('time', False, 'White')
        time_label_rect = time_label_text.get_rect()
        time_label_rect.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 + 5 * dim)
        screen.blit(time_label_text, time_label_rect)

        time_value_text = fonts[1].render(f'0:00.000', False, 'White')
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

        mode_text = fonts[1].render(f'{game.stats["mode"]}', False, 'White')
        mode_rect = mode_text.get_rect()
        mode_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 12 * dim)
        screen.blit(mode_text, mode_rect)

        ### DRAW RECT
        int_panel = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        int_panel.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)
        pygame.draw.rect(screen, 'White', int_panel)

        ### WRITE TEXT
        int_text = fonts[1].render(f'{3 - int(time.time() - countdown)}', False, 'Black')
        int_rect = int_text.get_rect()
        int_rect.midbottom = int_panel.midbottom
        screen.blit(int_text, int_rect)

        ### DRAW BUTTON
        menu_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        menu_button.topleft = (1 * dim, 1 * dim)
        pygame.draw.rect(screen, 'White', menu_button, border_width + 1)

        ### WRITE TEXT
        menu_text = fonts[1].render('menu', False, 'White')
        menu_rect = menu_text.get_rect()
        menu_rect.midbottom = menu_button.midbottom
        screen.blit(menu_text, menu_rect)

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

    ### PLAY STATE
    elif state[0] == 'play':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'pause'
                elif event.key == bindings['reset']:
                    countdown = time.time()
                    state[0] = 'countdown'
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
                        state[0] = 'pause'

        ### FRAME UPDATE
        game.frame_update(time.time())

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
        pause_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        pause_button.topleft = (1 * dim, 1 * dim)
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

        ### STATE TRANSITION
        game.finished(time.time())
        if game.finish:
            if game.lose:
                state[0] = 'lose'
            else:
                if user_info['username'] != 'guest':
                    row = [user_info['username'], time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime()), time.strftime('%z', time.localtime())] + [game.stats[stat] for stat in game.stat_names]
                    position = csv_registrar.save(row, state[1], {'marathon': (5, 'desc'), 'sprint': (4, 'asc'), 'blitz': (5, 'desc')}[state[1]])
                    position = sql_registrar.save(row, order_by[state[1]])
                else:
                    position = (0, 0)
                state[0] = 'finish'
        if state[0] == 'pause':
            game.pause(time.time())
        elif state[0] == 'countdown':
            game.reset(state[1], handling)

    ### PAUSE STATE
    elif state[0] == 'pause':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'play'
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if resume_button.collidepoint(pos):
                        state[0] = 'play'
                    elif retry_button.collidepoint(pos):
                        state[0] = 'countdown'
                    elif menu_button.collidepoint(pos):
                        state[0] = 'menu'

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

        mode_text = fonts[1].render(f'{game.stats["mode"]}', False, 'White')
        mode_rect = mode_text.get_rect()
        mode_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 12 * dim)
        screen.blit(mode_text, mode_rect)

        ### DRAW BUTTONS
        rect_width  = 8 * dim
        rect_height = 2 * dim

        resume_button = pygame.Rect(0, 0, rect_width, rect_height)
        resume_button.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', resume_button, border_width + 1)

        retry_button = pygame.Rect(0, 0, rect_width, rect_height)
        retry_button.bottomleft = (screen.get_width() / 2 + 6 * dim, screen.get_height() / 2 - 4 * dim)
        pygame.draw.rect(screen, 'White', retry_button, border_width + 1)

        menu_button = pygame.Rect(0, 0, rect_width, rect_height)
        menu_button.bottomright = (screen.get_width() / 2 - 6 * dim, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', menu_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('PAUSE', False, 'White')
        state_rect = state_text.get_rect()
        state_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 10 * dim)
        screen.blit(state_text, state_rect)

        resume_text = fonts[1].render('resume', False, 'White')
        resume_rect = resume_text.get_rect()
        resume_rect.midbottom = resume_button.midbottom
        screen.blit(resume_text, resume_rect)

        retry_text = fonts[1].render('retry', False, 'White')
        retry_rect = retry_text.get_rect()
        retry_rect.midbottom = retry_button.midbottom
        screen.blit(retry_text, retry_rect)

        menu_text = fonts[1].render('menu', False, 'White')
        menu_rect = menu_text.get_rect()
        menu_rect.midbottom = menu_button.midbottom
        screen.blit(menu_text, menu_rect)

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

        ### STATE TRANSITION
        if state[0] == 'play':
            game.pause(time.time())
        elif state[0] == 'countdown':
            game.reset(state[1], handling)
            countdown = time.time()

    ### LOSE STATE
    elif state[0] == 'lose':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                elif event.key == bindings['reset']:
                    game.reset(state[1], handling)
                    countdown = time.time()
                    state[0] = 'countdown'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if retry_button.collidepoint(pos):
                        game.reset(state[1], handling)
                        countdown = time.time()
                        state[0] = 'countdown'
                    elif menu_button.collidepoint(pos):
                        state[0] = 'menu'

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        rect_width  = 8 * dim
        rect_height = 2 * dim

        retry_button = pygame.Rect(0, 0, rect_width, rect_height)
        retry_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)
        pygame.draw.rect(screen, 'White', retry_button, border_width + 1)

        menu_button = pygame.Rect(0, 0, rect_width, rect_height)
        menu_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 2 * dim)
        pygame.draw.rect(screen, 'White', menu_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('LOSE', False, 'White')
        state_rect = state_text.get_rect()
        state_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 10 * dim)
        screen.blit(state_text, state_rect)

        retry_text = fonts[1].render('retry', False, 'White')
        retry_rect = retry_text.get_rect()
        retry_rect.midbottom = retry_button.midbottom
        screen.blit(retry_text, retry_rect)

        menu_text = fonts[1].render('menu', False, 'White')
        menu_rect = menu_text.get_rect()
        menu_rect.midbottom = menu_button.midbottom
        screen.blit(menu_text, menu_rect)

    ### FINISH STATE
    elif state[0] == 'finish':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
                    game.reset(state[1], handling)
                    countdown = time.time()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if retry_button.collidepoint(pos):
                        state[0] = 'countdown'
                        game.reset(state[1], handling)
                        countdown = time.time()
                    elif menu_button.collidepoint(pos):
                        state[0] = 'menu'

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        rect_width  = 8 * dim
        rect_height = 2 * dim

        retry_button = pygame.Rect(0, 0, rect_width, rect_height)
        retry_button.midleft = (screen.get_width() / 2 + 1 * dim, screen.get_height() / 2 + 10 * dim)
        pygame.draw.rect(screen, 'White', retry_button, border_width + 1)

        menu_button = pygame.Rect(0, 0, rect_width, rect_height)
        menu_button.midright = (screen.get_width() / 2 - 1 * dim, screen.get_height() / 2 + 10 * dim)
        pygame.draw.rect(screen, 'White', menu_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('FINISH', False, 'White')
        state_rect = state_text.get_rect()
        state_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 10 * dim)
        screen.blit(state_text, state_rect)

        retry_text = fonts[1].render('retry', False, 'White')
        retry_rect = retry_text.get_rect()
        retry_rect.midbottom = retry_button.midbottom
        screen.blit(retry_text, retry_rect)

        menu_text = fonts[1].render('menu', False, 'White')
        menu_rect = menu_text.get_rect()
        menu_rect.midbottom = menu_button.midbottom
        screen.blit(menu_text, menu_rect)

        if state[1] == 'marathon':
            score_text = fonts[1].render(f'score: {game.stats["score"]}', False, 'White')
            score_rect = score_text.get_rect()
            score_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)
            screen.blit(score_text, score_rect)
        elif state[1] == 'sprint':
            minutes      = int(game.stats['time'] // 60)
            seconds      = int(game.stats['time'] % 60)
            milliseconds = int(game.stats['time'] % 1 * 1000)
            time_text = fonts[1].render(f'time: {minutes}:{seconds:02}.{milliseconds:03}', False, 'White')
            time_rect = time_text.get_rect()
            time_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)
            screen.blit(time_text, time_rect)
        elif state[1] == 'blitz':
            score_text = fonts[1].render(f'score: {game.stats["score"]}', False, 'White')
            score_rect = score_text.get_rect()
            score_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)
            screen.blit(score_text, score_rect)

        if position[0] == 0:
            pos_str = ''
        elif position[0] == 1:
            pos_str = 'new best!'
        elif position[0] % 10 == 1 and position[0] // 10 % 100 != 1:
            pos_str = f'{position[0]}st best'
        elif position[0] % 10 == 2 and position[0] // 10 % 100 != 1:
            pos_str = f'{position[0]}nd best'
        elif position[0] % 10 == 3 and position[0] // 10 % 100 != 1:
            pos_str = f'{position[0]}rd best'
        else:
            pos_str = f'{position[0]}th best'
        pos_text = fonts[0].render(pos_str, False, 'White')
        pos_rect = pos_text.get_rect()
        pos_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2)
        screen.blit(pos_text, pos_rect)

        if position[1] == 0:
            pos_str = ''
        elif position[1] == 1:
            pos_str = 'global record!'
        elif position[1] % 10 == 1 and position[1] // 10 % 100 != 1:
            pos_str = f'global {position[1]}st best'
        elif position[1] % 10 == 2 and position[1] // 10 % 100 != 1:
            pos_str = f'global {position[1]}nd best'
        elif position[1] % 10 == 3 and position[1] // 10 % 100 != 1:
            pos_str = f'global {position[1]}rd best'
        else:
            pos_str = f'global {position[1]}th best'
        pos_text = fonts[0].render(pos_str, False, 'White')
        pos_rect = pos_text.get_rect()
        pos_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 2 * dim)
        screen.blit(pos_text, pos_rect)

    ### RECORDS STATE
    elif state[0] == 'records':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if back_button.collidepoint(pos):
                        state[0] = 'menu'
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
        rect_width  = 12 * dim
        rect_height = 2 * dim

        marathon_button = pygame.Rect(0, 0, rect_width, rect_height)
        marathon_button.bottomright = (screen.get_width() / 2 - 7 * dim, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', marathon_button, border_width + 1 if state[1] != 'marathon' else 0)

        sprint_button = pygame.Rect(0, 0, rect_width, rect_height)
        sprint_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', sprint_button, border_width + 1 if state[1] != 'sprint' else 0)

        blitz_button = pygame.Rect(0, 0, rect_width, rect_height)
        blitz_button.bottomleft = (screen.get_width() / 2 + 7 * dim, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', blitz_button, border_width + 1 if state[1] != 'blitz' else 0)

        back_button = pygame.Rect(0, 0, 6 * dim, rect_height)
        back_button.bottomleft = (1 * dim, screen.get_height() - 1 * dim)
        pygame.draw.rect(screen, 'White', back_button, border_width + 1)

        global_button = pygame.Rect(0, 0, 8 * dim, rect_height)
        global_button.bottomright = (screen.get_width() - 1 * dim, screen.get_height() - 1 * dim)
        pygame.draw.rect(screen, 'White', global_button, border_width + 1 if state[2] == '' else 0)

        ### WRITE TEXT
        state_text = fonts[1].render('RECORDS', False, 'White')
        state_rect = state_text.get_rect()
        state_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 10 * dim)
        screen.blit(state_text, state_rect)

        marathon_text = fonts[1].render('marathon', False, 'White' if state[1] != 'marathon' else 'Black')
        marathon_rect = marathon_text.get_rect()
        marathon_rect.midbottom = marathon_button.midbottom
        screen.blit(marathon_text, marathon_rect)

        sprint_text = fonts[1].render('sprint', False, 'White' if state[1] != 'sprint' else 'Black')
        sprint_rect = sprint_text.get_rect()
        sprint_rect.midbottom = sprint_button.midbottom
        screen.blit(sprint_text, sprint_rect)

        blitz_text = fonts[1].render('blitz', False, 'White' if state[1] != 'blitz' else 'Black')
        blitz_rect = blitz_text.get_rect()
        blitz_rect.midbottom = blitz_button.midbottom
        screen.blit(blitz_text, blitz_rect)

        back_text = fonts[1].render('back', False, 'White')
        back_rect = back_text.get_rect()
        back_rect.midbottom = back_button.midbottom
        screen.blit(back_text, back_rect)

        global_text = fonts[1].render('global', False, 'White' if state[2] == '' else 'Black')
        global_rect = global_text.get_rect()
        global_rect.midbottom = global_button.midbottom
        screen.blit(global_text, global_rect)

        # records_query = sql_registrar.load('' if state[2] == 'global' else user_info['username'], state[1], 10)
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
            int_rect = int_text.get_rect()
            int_rect.midbottom = (screen.get_width() / 2 - 13 * dim, screen.get_height() / 2 + (-4.5 + r * 1.5) * dim)
            screen.blit(int_text, int_rect)
            for c in range(1, len(top_n[r])):
                stat_text = fonts[0].render(top_n[r][c], False, 'White')
                stat_rect = stat_text.get_rect()
                stat_rect.bottomleft = (screen.get_width() / 2 + (-15 + c * 5) * dim, screen.get_height() / 2 + (-4.5 + r * 1.5) * dim)
                screen.blit(stat_text, stat_rect)

    ### SETTINGS STATE
    elif state[0] == 'settings':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    error_code = 0
                    input_fields = {'': ''}
                    for k, v in user_info.items():
                        input_fields[k] = v
                    for k, v in bindings.items():
                        input_fields[k] = v
                    for k, v in handling.items():
                        input_fields[k] = v
                    input_fields['password'] = ''
                    input_fields['new_pass1'] = ''
                    input_fields['new_pass2'] = ''
                elif event.key == pygame.K_RETURN:
                    if state[1] == 'account':
                        if user_info['username'] != 'guest':
                            if not (error_code & (1 << 0)) and user_info['username'] != input_fields['username']:
                                sql_directory.settings(user_info['username'], '', {'username': input_fields['username']})
                                user_info['username'] = input_fields['username']
                            if not (error_code & (1 << 1)) and len(input_fields['new_pass1']) > 0:
                                if sql_directory.settings(user_info['username'], input_fields['password'], {'password': input_fields['new_pass1']}):
                                    pass
                                else:
                                    error_code |= (1 << 2)
                        input_fields['username'] = user_info['username']
                        input_fields['password'] = ''
                        input_fields['new_pass1'] = ''
                        input_fields['new_pass2'] = ''
                    elif state[1] == 'bindings':
                        changes = {k: input_fields[k] for k, v in bindings.items() if input_fields[k] != v}
                        if changes:
                            if user_info['username'] != 'guest':
                                sql_directory.settings(user_info['username'], '', changes)
                            for k, v in changes.items():
                                bindings[k] = v
                    elif state[1] == 'handling':
                        changes = {k: input_fields[k] for k, v in handling.items() if input_fields[k] != v}
                        if changes:
                            if user_info['username'] != 'guest':
                                sql_directory.settings(user_info['username'], '', changes)
                            for k, v in changes.items():
                                handling[k] = v
                elif state[1] == 'account':
                    if event.key == pygame.K_TAB:
                        state_transition = ['password', 'new_pass2', 'new_pass1', 'username', '']
                        state[2] = state_transition[state_transition.index(state[2]) - 1]
                        cursor_pos = len(input_fields[state[2]])
                    elif event.key == pygame.K_BACKSPACE:
                        key_state['Backspace'] = time.time() - .05 + .3 # (- ARR + DAS)
                        key_state['Delete'] = 0
                        input_fields[state[2]] = input_fields[state[2]][:max(cursor_pos - 1, 0)] + input_fields[state[2]][cursor_pos:]
                        cursor_pos = max(cursor_pos - 1, 0)
                    elif event.key == pygame.K_DELETE:
                        key_state['Delete'] = time.time() - .05 + .3 # (- ARR + DAS)
                        key_state['Backspace'] = 0
                        input_fields[state[2]] = input_fields[state[2]][:cursor_pos] + input_fields[state[2]][cursor_pos + 1:]
                    elif event.key == pygame.K_LEFT:
                        key_state['Left'] = time.time() - .05 + .3 # (- ARR + DAS)
                        key_state['Right'] = 0
                        cursor_pos = max(cursor_pos - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        key_state['Right'] = time.time() - .05 + .3 # (- ARR + DAS)
                        key_state['Left'] = 0
                        cursor_pos = min(cursor_pos + 1, len(input_fields[state[2]]))
                    elif len(event.unicode) == 1 and len(input_fields[state[2]]) < 16:
                        alphanumeric = (48 <= ord(event.unicode) <= 57 or 65 <= ord(event.unicode) <= 90 or 97 <= ord(event.unicode) <= 122)
                        if state[2] == 'username' and alphanumeric or state[2] == 'password' or state[2] == 'new_pass1' or state[2] == 'new_pass2':
                            input_fields[state[2]] = input_fields[state[2]][:cursor_pos] + event.unicode + input_fields[state[2]][cursor_pos:]
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
                    if back_button.collidepoint(pos):
                        state[0] = 'menu'
                    elif account_button.collidepoint(pos):
                        if state[1] != 'account':
                            error_code = 0
                            input_fields = {'': ''}
                            for k, v in user_info.items():
                                input_fields[k] = v
                            for k, v in bindings.items():
                                input_fields[k] = v
                            for k, v in handling.items():
                                input_fields[k] = v
                            input_fields['password'] = ''
                            input_fields['new_pass1'] = ''
                            input_fields['new_pass2'] = ''
                            state[1] = 'account'
                    elif bindings_button.collidepoint(pos):
                        if state[1] != 'bindings':
                            error_code = 0
                            input_fields = {'': ''}
                            for k, v in user_info.items():
                                input_fields[k] = v
                            for k, v in bindings.items():
                                input_fields[k] = v
                            for k, v in handling.items():
                                input_fields[k] = v
                            input_fields['password'] = ''
                            input_fields['new_pass1'] = ''
                            input_fields['new_pass2'] = ''
                            state[1] = 'bindings'
                    elif handling_button.collidepoint(pos):
                        if state[1] != 'handling':
                            error_code = 0
                            input_fields = {'': ''}
                            for k, v in user_info.items():
                                input_fields[k] = v
                            for k, v in bindings.items():
                                input_fields[k] = v
                            for k, v in handling.items():
                                input_fields[k] = v
                            input_fields['password'] = ''
                            input_fields['new_pass1'] = ''
                            input_fields['new_pass2'] = ''
                            state[1] = 'handling'
                    elif cancel_button.collidepoint(pos):
                        error_code = 0
                        input_fields = {'': ''}
                        for k, v in user_info.items():
                            input_fields[k] = v
                        for k, v in bindings.items():
                            input_fields[k] = v
                        for k, v in handling.items():
                            input_fields[k] = v
                        input_fields['password'] = ''
                        input_fields['new_pass1'] = ''
                        input_fields['new_pass2'] = ''
                    elif apply_button.collidepoint(pos):
                        if state[1] == 'account':
                            if user_info['username'] != 'guest':
                                if not (error_code & (1 << 0)) and user_info['username'] != input_fields['username'] and len(input_fields['username']) > 0:
                                    sql_directory.settings(user_info['username'], '', {'username': input_fields['username']})
                                    user_info['username'] = input_fields['username']
                                if not (error_code & (1 << 1)) and len(input_fields['new_pass1']) > 0:
                                    if sql_directory.settings(user_info['username'], input_fields['password'], {'password': input_fields['new_pass1']}):
                                        pass
                                    else:
                                        error_code |= (1 << 2)
                            input_fields['username'] = user_info['username']
                            input_fields['password'] = ''
                            input_fields['new_pass1'] = ''
                            input_fields['new_pass2'] = ''
                        elif state[1] == 'bindings':
                            changes = {k: input_fields[k] for k, v in bindings.items() if input_fields[k] != v}
                            if changes:
                                if user_info['username'] != 'guest':
                                    sql_directory.settings(user_info['username'], '', changes)
                                for k, v in changes.items():
                                    bindings[k] = v
                        elif state[1] == 'handling':
                            changes = {k: input_fields[k] for k, v in handling.items() if input_fields[k] != v}
                            if changes:
                                if user_info['username'] != 'guest':
                                    sql_directory.settings(user_info['username'], '', changes)
                                for k, v in changes.items():
                                    handling[k] = v
                    elif state[1] == 'account':
                        for k in ['username', 'new_pass1', 'new_pass2', 'password']:
                            if interactables[k].collidepoint(pos):
                                state[2] = k
                                cursor_pos = len(input_fields[state[2]])
                                break
                        else:
                            state[2] = ''
                    elif state[1] == 'bindings':
                        for k in bindings.keys():
                            if interactables[k].collidepoint(pos):
                                pygame.draw.rect(screen, 'Black', interactables[k])
                                pygame.draw.rect(screen, 'White', interactables[k], border_width + 1)
                                pygame.display.update()
                                while True:
                                    event = pygame.event.wait()
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    elif event.type == pygame.KEYDOWN:
                                        for k2 in bindings.keys():
                                            if input_fields[k2] == event.key:
                                                input_fields[k2] = input_fields[k]
                                        input_fields[k] = event.key
                                        break
                                break
                    elif state[1] == 'handling':
                        for k in handling.keys():
                            if interactables[k].collidepoint(pos):
                                state[2] = k
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if state[1] == 'handling':
                        if state[2] == 'SDF' and input_fields['SDF'] == slider_range['SDF'][1]:
                            input_fields['SDF'] = 0
                        state[2] = ''

        ### AUTOREPEAT FOR KEYBOARD
        if state[1] == 'account':
            if key_state['Backspace']:
                remove_timer = time.time() - key_state['Backspace']
                if remove_timer > .05:
                    distance = int(remove_timer // .05)
                    key_state['Backspace'] += distance * .05
                    input_fields[state[2]] = input_fields[state[2]][:max(cursor_pos - distance, 0)] + input_fields[state[2]][cursor_pos:]
                    cursor_pos = max(cursor_pos - distance, 0)
            elif key_state['Delete']:
                remove_timer = time.time() - key_state['Delete']
                if remove_timer > .05:
                    distance = int(remove_timer // .05)
                    key_state['Delete'] += distance * .05
                    input_fields[state[2]] = input_fields[state[2]][:cursor_pos] + input_fields[state[2]][cursor_pos + distance:]
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
                    cursor_pos = min(cursor_pos + distance, len(input_fields[state[2]]))

        ### SLIDER MOVEMENT
        if state[1] == 'handling' and state[2]:
            pos = pygame.mouse.get_pos()
            slider_pos = min(max(pos[0], start_pos[0]), end_pos[0])
            percentage = (slider_pos - start_pos[0]) / (end_pos[0] - start_pos[0])
            input_fields[state[2]] = round(slider_range[state[2]][0] + (slider_range[state[2]][1] - slider_range[state[2]][0]) * percentage)

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### COLLECT INTERACTABLES
        interactables = {k: None for k, v in bindings.items()}
        interactables['new_pass1'] = None
        interactables['new_pass2'] = None

        ### DRAW BUTTONS
        rect_width  = 12 * dim
        rect_height = 2 * dim

        account_button = pygame.Rect(0, 0, rect_width, rect_height)
        account_button.bottomright = (screen.get_width() / 2 - 7 * dim, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', account_button, border_width + 1 if state[1] != 'account' else 0)

        bindings_button = pygame.Rect(0, 0, rect_width, rect_height)
        bindings_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', bindings_button, border_width + 1 if state[1] != 'bindings' else 0)

        handling_button = pygame.Rect(0, 0, rect_width, rect_height)
        handling_button.bottomleft = (screen.get_width() / 2 + 7 * dim, screen.get_height() / 2 - 7 * dim)
        pygame.draw.rect(screen, 'White', handling_button, border_width + 1 if state[1] != 'handling' else 0)

        cancel_button = pygame.Rect(0, 0, 8 * dim, rect_height)
        cancel_button.bottomright = (screen.get_width() / 2 - 1 * dim, screen.get_height() / 2 + 11 * dim)
        pygame.draw.rect(screen, 'White', cancel_button, border_width + 1)

        apply_button = pygame.Rect(0, 0, 8 * dim, rect_height)
        apply_button.bottomleft = (screen.get_width() / 2 + 1 * dim, screen.get_height() / 2 + 11 * dim)
        pygame.draw.rect(screen, 'White', apply_button, border_width + 1)

        back_button = pygame.Rect(0, 0, 6 * dim, rect_height)
        back_button.bottomleft = (1 * dim, screen.get_height() - 1 * dim)
        pygame.draw.rect(screen, 'White', back_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('SETTINGS', False, 'White')
        state_rect = state_text.get_rect()
        state_rect.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 10 * dim)
        screen.blit(state_text, state_rect)

        account_text = fonts[1].render('account', False, 'White' if state[1] != 'account' else 'Black')
        account_rect = account_text.get_rect()
        account_rect.midbottom = account_button.midbottom
        screen.blit(account_text, account_rect)

        bindings_text = fonts[1].render('bindings', False, 'White' if state[1] != 'bindings' else 'Black')
        bindings_rect = bindings_text.get_rect()
        bindings_rect.midbottom = bindings_button.midbottom
        screen.blit(bindings_text, bindings_rect)

        handling_text = fonts[1].render('handling', False, 'White' if state[1] != 'handling' else 'Black')
        handling_rect = handling_text.get_rect()
        handling_rect.midbottom = handling_button.midbottom
        screen.blit(handling_text, handling_rect)

        cancel_text = fonts[1].render('cancel', False, 'White')
        cancel_rect = cancel_text.get_rect()
        cancel_rect.midbottom = cancel_button.midbottom
        screen.blit(cancel_text, cancel_rect)

        apply_text = fonts[1].render('apply', False, 'White')
        apply_rect = apply_text.get_rect()
        apply_rect.midbottom = apply_button.midbottom
        screen.blit(apply_text, apply_rect)

        back_text = fonts[1].render('back', False, 'White')
        back_rect = back_text.get_rect()
        back_rect.midbottom = back_button.midbottom
        screen.blit(back_text, back_rect)

        if state[1] == 'account':
            ### DRAW TEXTBOXES
            rect_width  = 12 * dim
            rect_height = 2 * dim

            user_box = pygame.Rect(0, 0, rect_width, rect_height)
            user_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 - 3 * dim)
            pygame.draw.rect(screen, 'White', user_box, border_width + 1)
            interactables['username'] = user_box

            new1_box = pygame.Rect(0, 0, rect_width, rect_height)
            new1_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 1 * dim)
            pygame.draw.rect(screen, 'White', new1_box, border_width + 1)
            interactables['new_pass1'] = new1_box

            new2_box = pygame.Rect(0, 0, rect_width, rect_height)
            new2_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 4 * dim)
            pygame.draw.rect(screen, 'White', new2_box, border_width + 1)
            interactables['new_pass2'] = new2_box

            pass_box = pygame.Rect(0, 0, rect_width, rect_height)
            pass_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 7 * dim)
            pygame.draw.rect(screen, 'White', pass_box, border_width + 1)
            interactables['password'] = pass_box

            ### WRITE INPUT TEXT
            user_input_text = fonts[0].render(input_fields['username'][:cursor_pos] + '|' * (state[2] == 'username') + input_fields['username'][cursor_pos:], False, 'White')
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

            new1_input_text = fonts[0].render('*' * len(input_fields['new_pass1'][:cursor_pos]) + '|' * (state[2] == 'new_pass1') + '*' * len(input_fields['new_pass1'][cursor_pos:]), False, 'White')
            new1_input_rect = new1_input_text.get_rect()
            new1_input_rect.bottomleft = (new1_box.left + .5 * dim, new1_box.bottom - .4 * dim)
            screen.blit(new1_input_text, new1_input_rect)

            new2_input_text = fonts[0].render('*' * len(input_fields['new_pass2'][:cursor_pos]) + '|' * (state[2] == 'new_pass2') + '*' * len(input_fields['new_pass2'][cursor_pos:]), False, 'White')
            new2_input_rect = new2_input_text.get_rect()
            new2_input_rect.bottomleft = (new2_box.left + .5 * dim, new2_box.bottom - .4 * dim)
            screen.blit(new2_input_text, new2_input_rect)

            pass_input_text = fonts[0].render('*' * len(input_fields['password'][:cursor_pos]) + '|' * (state[2] == 'password') + '*' * len(input_fields['password'][cursor_pos:]), False, 'White')
            pass_input_rect = pass_input_text.get_rect()
            pass_input_rect.bottomleft = (pass_box.left + .5 * dim, pass_box.bottom - .4 * dim)
            screen.blit(pass_input_text, pass_input_rect)

            ### WRITE TEXT
            user_text = fonts[0].render('username', False, 'White')
            user_rect = user_text.get_rect()
            user_rect.bottomright = (user_box.left - 1 * dim, user_box.bottom - .4 * dim)
            screen.blit(user_text, user_rect)

            new1_text = fonts[0].render('new password', False, 'White')
            new1_rect = new1_text.get_rect()
            new1_rect.bottomright = (new1_box.left - 1 * dim, new1_box.bottom - .4 * dim)
            screen.blit(new1_text, new1_rect)

            new2_text = fonts[0].render('confirm password', False, 'White')
            new2_rect = new2_text.get_rect()
            new2_rect.bottomright = (new2_box.left - 1 * dim, new2_box.bottom - .4 * dim)
            screen.blit(new2_text, new2_rect)

            pass_text = fonts[0].render('current password', False, 'White')
            pass_rect = pass_text.get_rect()
            pass_rect.bottomright = (pass_box.left - 1 * dim, pass_box.bottom - .4 * dim)
            screen.blit(pass_text, pass_rect)

            if input_fields['username'] != user_info['username'] and not sql_directory.username_available(input_fields['username']):
                error_code |= (1 << 0)
                error_text = fonts[0].render('taken', False, 'White')
                error_rect = error_text.get_rect()
                error_rect.bottomleft = (user_box.right + 1 * dim, user_box.bottom - .4 * dim)
                screen.blit(error_text, error_rect)
            else:
                error_code &= ~(1 << 0)
            if input_fields['new_pass1'] != input_fields['new_pass2']:
                error_code |= (1 << 1)
                error_text = fonts[0].render('doesn\'t match', False, 'White')
                error_rect = error_text.get_rect()
                error_rect.bottomleft = (new2_box.right + 1 * dim, new2_box.bottom - .4 * dim)
                screen.blit(error_text, error_rect)
            else:
                error_code &= ~(1 << 1)
            if error_code & (1 << 2):
                error_text = fonts[0].render('incorrect password', False, 'White')
                error_rect = error_text.get_rect()
                error_rect.bottomleft = (pass_box.right + 1 * dim, pass_box.bottom - .4 * dim)
                screen.blit(error_text, error_rect)

        elif state[1] == 'bindings':
            key_order = (('quit', 'hold', 'rotate_cw', 'rotate_180', 'rotate_ccw'),
                         ('reset', 'move_left', 'move_right', 'soft_drop', 'hard_drop'))
            for c, column in enumerate(key_order):
                for r, action in enumerate(column):
                    action_text = fonts[0].render(action.replace('_', ' '), False, 'White')
                    action_rect = action_text.get_rect()
                    action_rect.bottomleft = (screen.get_width() / 2 + (-13 + c * 15) * dim, screen.get_height() / 2 + (-3 + r * 2) * dim)
                    screen.blit(action_text, action_rect)

                    key_text = fonts[0].render(pygame.key.name(input_fields[action]), False, 'White')
                    key_rect = key_text.get_rect()
                    key_rect.bottomleft = (screen.get_width() / 2 + (-6 + c * 15) * dim, screen.get_height() / 2 + (-3 + r * 2) * dim)
                    screen.blit(key_text, key_rect)
                    interactables[action] = key_rect

        elif state[1] == 'handling':
            slider_range = {'DAS': (0, 400), 'ARR': (0, 80), 'SDF': (5, 41)}
            for i, control in enumerate(handling.keys()):
                handling_text = fonts[0].render(control, False, 'White')
                handling_rect = handling_text.get_rect()
                handling_rect.bottomleft = (screen.get_width() / 2 - 13 * dim, screen.get_height() / 2 + (-3 + i * 4) * dim)
                screen.blit(handling_text, handling_rect)

                value_text = str(input_fields[control]) if not (control == 'SDF' and (input_fields[control] == slider_range['SDF'][1] or input_fields[control] == 0)) else 'inf'
                value_text = fonts[0].render(value_text, False, 'White')
                value_rect = value_text.get_rect()
                value_rect.bottomleft = (screen.get_width() / 2 + 11 * dim, screen.get_height() / 2 + (-3 + i * 4) * dim)
                screen.blit(value_text, value_rect)

                start_pos = (screen.get_width() / 2 - 10 * dim, screen.get_height() / 2 + (-3.5 + i * 4) * dim)
                end_pos   = (start_pos[0] + 20 * dim, start_pos[1])
                pygame.draw.line(screen, 'White', start_pos, end_pos, border_width + 1)

                value = input_fields[control] if control != 'SDF' or input_fields[control] != 0 else slider_range['SDF'][1]
                percentage = (value - slider_range[control][0]) / (slider_range[control][1] - slider_range[control][0])
                slider_pos = (start_pos[0] + 20 * dim * percentage, start_pos[1])
                interactables[control] = pygame.draw.circle(screen, 'White', slider_pos, dim / 3)

    pygame.display.update()
    clock.tick(60)