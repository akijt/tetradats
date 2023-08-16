import pygame
import time

def state_settings(screen, clock, sql_directory, state, user_info, bindings, handling):

    ### INIT STATE
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
        account_button = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        account_button.bottomright = (screen.get_width() / 2 - 7 * dim, screen.get_height() / 2 - 7 * dim)

        bindings_button = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        bindings_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 7 * dim)

        handling_button = pygame.Rect(0, 0, 12 * dim, 2 * dim)
        handling_button.bottomleft = (screen.get_width() / 2 + 7 * dim, screen.get_height() / 2 - 7 * dim)

        cancel_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        cancel_button.bottomright = (screen.get_width() / 2 - 1 * dim, screen.get_height() / 2 + 11 * dim)

        apply_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        apply_button.bottomleft = (screen.get_width() / 2 + 1 * dim, screen.get_height() / 2 + 11 * dim)

        back_button = pygame.Rect(0, 0, 6 * dim, 2 * dim)
        back_button.bottomleft = (1 * dim, screen.get_height() - 1 * dim)

        interactables = dict()

        if state[1] == 'account':
            user_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            user_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 - 3 * dim)
            interactables['username'] = user_box

            new1_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            new1_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 1 * dim)
            interactables['new_pass1'] = new1_box

            new2_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            new2_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 4 * dim)
            interactables['new_pass2'] = new2_box

            pass_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            pass_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 7 * dim)
            interactables['password'] = pass_box
        
        elif state[1] == 'bindings':
            key_order = (('quit', 'hold', 'rotate_cw', 'rotate_180', 'rotate_ccw'),
                         ('reset', 'move_left', 'move_right', 'soft_drop', 'hard_drop'))
            for c, column in enumerate(key_order):
                for r, action in enumerate(column):
                    key_text = fonts[0].render(pygame.key.name(input_fields[action]), False, 'White')
                    key_rect = key_text.get_rect(bottomleft=(screen.get_width() / 2 + (-6 + c * 15) * dim, screen.get_height() / 2 + (-3 + r * 2) * dim))
                    interactables[action] = key_rect

        elif state[1] == 'handling':
            slider_range = {'DAS': (0, 400), 'ARR': (0, 80), 'SDF': (5, 41)}
            for i, control in enumerate(handling.keys()):
                value = input_fields[control] if control != 'SDF' or input_fields[control] != 0 else slider_range['SDF'][1]
                percentage = (value - slider_range[control][0]) / (slider_range[control][1] - slider_range[control][0])
                start_pos = (screen.get_width() / 2 - 10 * dim, screen.get_height() / 2 + (-3.5 + i * 4) * dim)
                slider_pos = (start_pos[0] + 20 * dim * percentage, start_pos[1])
                interactables[control] = pygame.draw.circle(screen, 'White', slider_pos, dim / 3)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
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
                    cursor_pos = 0
                    error_code = 0
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
                        return
                    elif account_button.collidepoint(pos):
                        if state[1] != 'account':
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
                            cursor_pos = 0
                            error_code = 0
                            state[1] = 'account'
                            state[2] = ''
                    elif bindings_button.collidepoint(pos):
                        if state[1] != 'bindings':
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
                            state[2] = ''
                    elif handling_button.collidepoint(pos):
                        if state[1] != 'handling':
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
                            state[2] = ''
                    elif cancel_button.collidepoint(pos):
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
                        cursor_pos = 0
                        error_code = 0
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
        elif state[1] == 'handling' and state[2]:
            pos = pygame.mouse.get_pos()
            slider_pos = min(max(pos[0], start_pos[0]), end_pos[0])
            percentage = (slider_pos - start_pos[0]) / (end_pos[0] - start_pos[0])
            input_fields[state[2]] = round(slider_range[state[2]][0] + (slider_range[state[2]][1] - slider_range[state[2]][0]) * percentage)

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        pygame.draw.rect(screen, 'White', account_button, border_width + 1 if state[1] != 'account' else 0)
        pygame.draw.rect(screen, 'White', bindings_button, border_width + 1 if state[1] != 'bindings' else 0)
        pygame.draw.rect(screen, 'White', handling_button, border_width + 1 if state[1] != 'handling' else 0)
        pygame.draw.rect(screen, 'White', cancel_button, border_width + 1)
        pygame.draw.rect(screen, 'White', apply_button, border_width + 1)
        pygame.draw.rect(screen, 'White', back_button, border_width + 1)

        ### WRITE TEXT
        state_text = fonts[1].render('SETTINGS', False, 'White')
        state_rect = state_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 - 10 * dim))
        screen.blit(state_text, state_rect)

        account_text = fonts[1].render('account', False, 'White' if state[1] != 'account' else 'Black')
        account_rect = account_text.get_rect(midbottom=account_button.midbottom)
        screen.blit(account_text, account_rect)

        bindings_text = fonts[1].render('bindings', False, 'White' if state[1] != 'bindings' else 'Black')
        bindings_rect = bindings_text.get_rect(midbottom=bindings_button.midbottom)
        screen.blit(bindings_text, bindings_rect)

        handling_text = fonts[1].render('handling', False, 'White' if state[1] != 'handling' else 'Black')
        handling_rect = handling_text.get_rect(midbottom=handling_button.midbottom)
        screen.blit(handling_text, handling_rect)

        cancel_text = fonts[1].render('cancel', False, 'White')
        cancel_rect = cancel_text.get_rect(midbottom=cancel_button.midbottom)
        screen.blit(cancel_text, cancel_rect)

        apply_text = fonts[1].render('apply', False, 'White')
        apply_rect = apply_text.get_rect(midbottom=apply_button.midbottom)
        screen.blit(apply_text, apply_rect)

        back_text = fonts[1].render('back', False, 'White')
        back_rect = back_text.get_rect(midbottom=back_button.midbottom)
        screen.blit(back_text, back_rect)

        if state[1] == 'account':
            ### DRAW TEXTBOXES
            user_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            user_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 - 3 * dim)
            pygame.draw.rect(screen, 'White', user_box, border_width + 1)

            new1_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            new1_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 1 * dim)
            pygame.draw.rect(screen, 'White', new1_box, border_width + 1)

            new2_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            new2_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 4 * dim)
            pygame.draw.rect(screen, 'White', new2_box, border_width + 1)

            pass_box = pygame.Rect(0, 0, 12 * dim, 2 * dim)
            pass_box.midbottom = (screen.get_width() / 2 + 2 * dim, screen.get_height() / 2 + 7 * dim)
            pygame.draw.rect(screen, 'White', pass_box, border_width + 1)

            ### WRITE INPUT TEXT
            user_input_text = fonts[0].render(input_fields['username'][:cursor_pos] + '|' * (state[2] == 'username') + input_fields['username'][cursor_pos:], False, 'White')
            user_input_rect = user_input_text.get_rect(bottomleft=(user_box.left + .5 * dim, user_box.bottom - .4 * dim))
            if user_input_rect.width > user_box.width - dim and cursor_pos > 8:
                user_input_rect.bottomright = (user_box.right - .5 * dim, user_box.bottom - .4 * dim)
            screen.blit(user_input_text, user_input_rect)
            clear_rect = pygame.Rect(0, 0, 4 * dim, 2 * dim)
            clear_rect.bottomright = user_box.bottomleft
            pygame.draw.rect(screen, 'Black', clear_rect)
            clear_rect.bottomleft = user_box.bottomright
            pygame.draw.rect(screen, 'Black', clear_rect)

            new1_input_text = fonts[0].render('*' * len(input_fields['new_pass1'][:cursor_pos]) + '|' * (state[2] == 'new_pass1') + '*' * len(input_fields['new_pass1'][cursor_pos:]), False, 'White')
            new1_input_rect = new1_input_text.get_rect(bottomleft=(new1_box.left + .5 * dim, new1_box.bottom - .4 * dim))
            screen.blit(new1_input_text, new1_input_rect)

            new2_input_text = fonts[0].render('*' * len(input_fields['new_pass2'][:cursor_pos]) + '|' * (state[2] == 'new_pass2') + '*' * len(input_fields['new_pass2'][cursor_pos:]), False, 'White')
            new2_input_rect = new2_input_text.get_rect(bottomleft=(new2_box.left + .5 * dim, new2_box.bottom - .4 * dim))
            screen.blit(new2_input_text, new2_input_rect)

            pass_input_text = fonts[0].render('*' * len(input_fields['password'][:cursor_pos]) + '|' * (state[2] == 'password') + '*' * len(input_fields['password'][cursor_pos:]), False, 'White')
            pass_input_rect = pass_input_text.get_rect(bottomleft=(pass_box.left + .5 * dim, pass_box.bottom - .4 * dim))
            screen.blit(pass_input_text, pass_input_rect)

            ### WRITE TEXT
            user_text = fonts[0].render('username', False, 'White')
            user_rect = user_text.get_rect(bottomright=(user_box.left - 1 * dim, user_box.bottom - .4 * dim))
            screen.blit(user_text, user_rect)

            new1_text = fonts[0].render('new password', False, 'White')
            new1_rect = new1_text.get_rect(bottomright=(new1_box.left - 1 * dim, new1_box.bottom - .4 * dim))
            screen.blit(new1_text, new1_rect)

            new2_text = fonts[0].render('confirm password', False, 'White')
            new2_rect = new2_text.get_rect(bottomright=(new2_box.left - 1 * dim, new2_box.bottom - .4 * dim))
            screen.blit(new2_text, new2_rect)

            pass_text = fonts[0].render('current password', False, 'White')
            pass_rect = pass_text.get_rect(bottomright=(pass_box.left - 1 * dim, pass_box.bottom - .4 * dim))
            screen.blit(pass_text, pass_rect)

            ### ERROR HANDLING
            if input_fields['username'] != user_info['username'] and not sql_directory.username_available(input_fields['username']):
                error_code |= (1 << 0)
                error_text = fonts[0].render('taken', False, 'White')
                error_rect = error_text.get_rect(bottomleft=(user_box.right + 1 * dim, user_box.bottom - .4 * dim))
                screen.blit(error_text, error_rect)
            else:
                error_code &= ~(1 << 0)
            if input_fields['new_pass1'] != input_fields['new_pass2']:
                error_code |= (1 << 1)
                error_text = fonts[0].render('doesn\'t match', False, 'White')
                error_rect = error_text.get_rect(bottomleft=(new2_box.right + 1 * dim, new2_box.bottom - .4 * dim))
                screen.blit(error_text, error_rect)
            else:
                error_code &= ~(1 << 1)
            if error_code & (1 << 2):
                error_text = fonts[0].render('incorrect password', False, 'White')
                error_rect = error_text.get_rect(bottomleft=(pass_box.right + 1 * dim, pass_box.bottom - .4 * dim))
                screen.blit(error_text, error_rect)

        elif state[1] == 'bindings':
            key_order = (('quit', 'hold', 'rotate_cw', 'rotate_180', 'rotate_ccw'),
                         ('reset', 'move_left', 'move_right', 'soft_drop', 'hard_drop'))
            for c, column in enumerate(key_order):
                for r, action in enumerate(column):
                    action_text = fonts[0].render(action.replace('_', ' '), False, 'White')
                    action_rect = action_text.get_rect(bottomleft=(screen.get_width() / 2 + (-13 + c * 15) * dim, screen.get_height() / 2 + (-3 + r * 2) * dim))
                    screen.blit(action_text, action_rect)

                    key_text = fonts[0].render(pygame.key.name(input_fields[action]), False, 'White')
                    key_rect = key_text.get_rect(bottomleft=(screen.get_width() / 2 + (-6 + c * 15) * dim, screen.get_height() / 2 + (-3 + r * 2) * dim))
                    screen.blit(key_text, key_rect)

        elif state[1] == 'handling':
            slider_range = {'DAS': (0, 400), 'ARR': (0, 80), 'SDF': (5, 41)}
            for i, control in enumerate(handling.keys()):
                handling_text = fonts[0].render(control, False, 'White')
                handling_rect = handling_text.get_rect(bottomleft=(screen.get_width() / 2 - 13 * dim, screen.get_height() / 2 + (-3 + i * 4) * dim))
                screen.blit(handling_text, handling_rect)

                value_text = str(input_fields[control]) if not (control == 'SDF' and (input_fields[control] == slider_range['SDF'][1] or input_fields[control] == 0)) else 'inf'
                value_text = fonts[0].render(value_text, False, 'White')
                value_rect = value_text.get_rect(bottomleft=(screen.get_width() / 2 + 11 * dim, screen.get_height() / 2 + (-3 + i * 4) * dim))
                screen.blit(value_text, value_rect)

                start_pos = (screen.get_width() / 2 - 10 * dim, screen.get_height() / 2 + (-3.5 + i * 4) * dim)
                end_pos   = (start_pos[0] + 20 * dim, start_pos[1])
                pygame.draw.line(screen, 'White', start_pos, end_pos, border_width + 1)

                value = input_fields[control] if control != 'SDF' or input_fields[control] != 0 else slider_range['SDF'][1]
                percentage = (value - slider_range[control][0]) / (slider_range[control][1] - slider_range[control][0])
                slider_pos = (start_pos[0] + 20 * dim * percentage, start_pos[1])
                pygame.draw.circle(screen, 'White', slider_pos, dim / 3)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)