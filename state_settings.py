import pygame
import time
from utils import Sprite_text, Sprite_button, Sprite_textfield, Sprite_line, Sprite_circle

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
    interactables = dict()

    account_button  = Sprite_button('account', (12, 2), 'bottomright', (-7, -7), 'center', 'White', 2 if state[1] != 'account' else 0, 'White' if state[1] != 'account' else 'Black', 4, None)
    bindings_button = Sprite_button('bindings', (12, 2), 'midbottom', (0, -7), 'center', 'White', 2 if state[1] != 'bindings' else 0, 'White' if state[1] != 'bindings' else 'Black', 4, None)
    handling_button = Sprite_button('handling', (12, 2), 'bottomleft', (7, -7), 'center', 'White', 2 if state[1] != 'handling' else 0, 'White' if state[1] != 'handling' else 'Black', 4, None)
    cancel_button   = Sprite_button('cancel', (8, 2), 'bottomright', (-1, 11), 'center', 'White', 2, 'White', 4, None)
    apply_button    = Sprite_button('apply', (8, 2), 'bottomleft', (1, 11), 'center', 'White', 2, 'White', 4, None)
    back_button     = Sprite_button('back', (6, 2), 'bottomleft', (1, -1), 'bottomleft', 'White', 2, 'White', 4, None)

    settings_group = pygame.sprite.Group()
    settings_group.add(Sprite_text('SETTINGS', 'midbottom', (0, -10), 'center', 'White', 4, None))
    settings_group.add(account_button)
    settings_group.add(bindings_button)
    settings_group.add(handling_button)
    settings_group.add(cancel_button)
    settings_group.add(apply_button)
    settings_group.add(back_button)

    if state[1] == 'account':
        user_box = Sprite_textfield((12, 2), 'midbottom', (2, -3), 'center', 'White', 2, 'White', 2, None)
        new1_box = Sprite_textfield((12, 2), 'midbottom', (2, 1), 'center', 'White', 2, 'White', 2, None)
        new2_box = Sprite_textfield((12, 2), 'midbottom', (2, 4), 'center', 'White', 2, 'White', 2, None)
        pass_box = Sprite_textfield((12, 2), 'midbottom', (2, 7), 'center', 'White', 2, 'White', 2, None)

        settings_group.add(Sprite_text('username', 'bottomright', (-5, -3.4), 'center', 'White', 2, None))
        settings_group.add(Sprite_text('new password', 'bottomright', (-5, 0.6), 'center', 'White', 2, None))
        settings_group.add(Sprite_text('confirm password', 'bottomright', (-5, 3.6), 'center', 'White', 2, None))
        settings_group.add(Sprite_text('current password', 'bottomright', (-5, 6.6), 'center', 'White', 2, None))
        settings_group.add(user_box)
        settings_group.add(new1_box)
        settings_group.add(new2_box)
        settings_group.add(pass_box)
        
        interactables['username'] = user_box
        interactables['new_pass1'] = new1_box
        interactables['new_pass2'] = new2_box
        interactables['password'] = pass_box

        error1_text = Sprite_text('', 'bottomleft', (9, -3.4), 'center', 'White', 2, None)
        error2_text = Sprite_text('', 'bottomleft', (9, 3.6), 'center', 'White', 2, None)
        error3_text = Sprite_text('', 'bottomleft', (9, 6.6), 'center', 'White', 2, None)
        error_group = pygame.sprite.Group()
        error_group.add(error1_text)
        error_group.add(error2_text)
        error_group.add(error3_text)
    
    elif state[1] == 'bindings':
        key_order = (('quit', 'hold', 'rotate_cw', 'rotate_180', 'rotate_ccw'),
                        ('reset', 'move_left', 'move_right', 'soft_drop', 'hard_drop'))
        for c, column in enumerate(key_order):
            for r, action in enumerate(column):
                settings_group.add(Sprite_text(action.replace('_', ' '), 'bottomleft', (-13 + c * 15, -3 + r * 2), 'center', 'White', 2, None))

                key_text = Sprite_text(pygame.key.name(input_fields[action]), 'bottomleft', (-6 + c * 15, -3 + r * 2), 'center', 'White', 2, None)
                settings_group.add(key_text)
                interactables[action] = key_text

    elif state[1] == 'handling':
        slider_range = {'DAS': (0, 400), 'ARR': (0, 80), 'SDF': (5, 41)}
        for i, control in enumerate(handling.keys()):
            value_text = str(input_fields[control]) if not (control == 'SDF' and (input_fields[control] == slider_range['SDF'][1] or input_fields[control] == 0)) else 'inf'
            value_text = Sprite_text(value_text, 'bottomleft', (11, -3 + i * 4), 'center', 'White', 2, None)
            slider = Sprite_circle(0.4, (-10, -3.5 + i * 4), 'center', 'White', 0, 'Black')

            settings_group.add(Sprite_text(control, 'bottomleft', (-13, -3 + i * 4), 'center', 'White', 2, None))
            settings_group.add(value_text)
            settings_group.add(Sprite_line(20, (-10, -3.5 + i * 4), 'center', 'White', 3, 'horizontal'))
            settings_group.add(slider)

            interactables[control] = (slider, value_text)

    settings_group.update(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                settings_group.update(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[2] = ''
                    return
                elif event.key == pygame.K_RETURN:
                    if state[1] == 'account':
                        if user_info['username'] != 'guest':
                            if not (error_code & (1 << 0)) and user_info['username'] != input_fields['username']:
                                sql_directory.settings(user_info['username'], '', {'username': input_fields['username']})
                                user_info['username'] = input_fields['username']
                            if not (error_code & (1 << 1)) and len(input_fields['new_pass1']) > 0:
                                if not sql_directory.settings(user_info['username'], input_fields['password'], {'password': input_fields['new_pass1']}):
                                    error_code |= (1 << 2)
                        input_fields['username'] = user_info['username']
                        input_fields['password'] = ''
                        input_fields['new_pass1'] = ''
                        input_fields['new_pass2'] = ''
                        state[2] = ''
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
                    if back_button.rect.collidepoint(pos):
                        state[0] = 'menu'
                        state[1] = ''
                        state[2] = ''
                        return
                    elif account_button.rect.collidepoint(pos):
                        if state[1] != 'account':
                            state[1] = 'account'
                            state[2] = ''
                            return
                    elif bindings_button.rect.collidepoint(pos):
                        if state[1] != 'bindings':
                            state[1] = 'bindings'
                            state[2] = ''
                            return
                    elif handling_button.rect.collidepoint(pos):
                        if state[1] != 'handling':
                            state[1] = 'handling'
                            state[2] = ''
                            return
                    elif cancel_button.rect.collidepoint(pos):
                        state[2] = ''
                        return
                    elif apply_button.rect.collidepoint(pos):
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
                            state[2] = ''
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
                            if interactables[k].rect.collidepoint(pos):
                                state[2] = k
                                cursor_pos = len(input_fields[state[2]])
                                break
                        else:
                            state[2] = ''
                    elif state[1] == 'bindings':
                        for k in bindings.keys():
                            if interactables[k].rect.collidepoint(pos):
                                pygame.draw.rect(screen, 'Black', interactables[k].rect)
                                pygame.draw.rect(screen, 'White', interactables[k].rect, 2)
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
                                                interactables[k2].update(screen, text=interactables[k].text)
                                        input_fields[k] = event.key
                                        interactables[k].update(screen, text=pygame.key.name(event.key))
                                        break
                                break
                    elif state[1] == 'handling':
                        for k in handling.keys():
                            if interactables[k][0].rect.collidepoint(pos):
                                state[2] = k
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if state[1] == 'handling':
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
            dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
            pos = pygame.mouse.get_pos()[0]
            start_pos = screen.get_width() / 2 - 10 * dim
            end_pos   = start_pos + 20 * dim
            pos = min(max(pos, start_pos), end_pos)
            percentage = (pos - start_pos) / (end_pos - start_pos)
            input_fields[state[2]] = round(slider_range[state[2]][0] + (slider_range[state[2]][1] - slider_range[state[2]][0]) * percentage)
            if state[2] == 'SDF' and input_fields['SDF'] == slider_range['SDF'][1]:
                input_fields['SDF'] = 0
                interactables['SDF'][1].update(screen, text='inf')
            else:
                interactables[state[2]][1].update(screen, text=str(input_fields[state[2]]))

        ### ERROR HANDLING
        if state[1] == 'account':
            if input_fields['username'] != user_info['username'] and not sql_directory.username_available(input_fields['username']):
                error1_text.update(screen, text='taken')
                error_code |= (1 << 0)
            else:
                error1_text.update(screen, text='')
                error_code &= ~(1 << 0)
            if input_fields['new_pass1'] != input_fields['new_pass2']:
                error2_text.update(screen, text='doesn\'t match')
                error_code |= (1 << 1)
            else:
                error2_text.update(screen, text='')
                error_code &= ~(1 << 1)
            if error_code & (1 << 2):
                error3_text.update(screen, text='incorrect password')
            else:
                error3_text.update(screen, text='')

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW SPRITES
        if state[1] == 'account':
            user_box.update(screen, text=input_fields['username'], cursor_pos=cursor_pos if state[2] == 'username' else -1)
            new1_box.update(screen, text='*' * len(input_fields['new_pass1']), cursor_pos=cursor_pos if state[2] == 'new_pass1' else -1)
            new2_box.update(screen, text='*' * len(input_fields['new_pass2']), cursor_pos=cursor_pos if state[2] == 'new_pass2' else -1)
            pass_box.update(screen, text='*' * len(input_fields['password']), cursor_pos=cursor_pos if state[2] == 'password' else -1)
            error_group.draw(screen)
        elif state[1] == 'handling':
            slider_range = {'DAS': (0, 400), 'ARR': (0, 80), 'SDF': (5, 41)}
            for i, control in enumerate(handling.keys()):
                value = input_fields[control] if control != 'SDF' or input_fields[control] != 0 else slider_range['SDF'][1]
                percentage = (value - slider_range[control][0]) / (slider_range[control][1] - slider_range[control][0])
                interactables[control][0].update(screen, offset=(-10 + 20 * percentage, interactables[control][0].offset[1]))
        settings_group.draw(screen)
        
        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(None, round(.75 * 2 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, 'White')
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)