import pygame
from sys import exit
import time
from utils import Sprite_group, Sprite_text, Sprite_button, Sprite_textfield, Sprite_line, Sprite_circle

def state_settings(screen, clock, colors, db_type, directory, registrar, font_path, state, user_info, bindings, handling):

    ### INIT STATE
    if state[1] == 'account':
        input_fields = {k: v for k, v in user_info.items()}
        input_fields['password'] = ''
        input_fields['new_pass1'] = ''
        input_fields['new_pass2'] = ''
        input_to_sprite = {'username': 'user_box', 'password': 'pass_box', 'new_pass1': 'new1_box', 'new_pass2': 'new2_box'}
        cursor_pos = 0
        key_state  = {'Backspace': 0, 'Delete': 0, 'Left': 0, 'Right': 0}
        state_transition = ['password', 'new_pass2', 'new_pass1', 'username', '']
    elif state[1] == 'bindings':
        input_fields = {k: v for k, v in bindings.items()}
        input_to_sprite = {k: f'{k}_value' for k in bindings.keys()}
    elif state[1] == 'handling':
        input_fields = {k: v for k, v in handling.items()}
        input_to_sprite = {k: (f'{k}_circle', f'{k}_value') for k in handling.keys()}

    settings_group = Sprite_group(
        title_text      = Sprite_text('midbottom', (0, -10), 'center', 'SETTINGS', (255, 255, 255), 4, font_path),
        account_button  = Sprite_button('bottomright', (-7, -7), 'center', (12, 2), (0, 0, 0) if state[1] != 'account' else (255, 255, 255), (255, 255, 255), 2, 'account', (255, 255, 255) if state[1] != 'account' else (0, 0, 0), 4, font_path),
        bindings_button = Sprite_button('midbottom', (0, -7), 'center', (12, 2), (0, 0, 0) if state[1] != 'bindings' else (255, 255, 255), (255, 255, 255), 2, 'bindings', (255, 255, 255) if state[1] != 'bindings' else (0, 0, 0), 4, font_path),
        handling_button = Sprite_button('bottomleft', (7, -7), 'center', (12, 2), (0, 0, 0) if state[1] != 'handling' else (255, 255, 255), (255, 255, 255), 2, 'handling', (255, 255, 255) if state[1] != 'handling' else (0, 0, 0), 4, font_path),
        cancel_button   = Sprite_button('bottomright', (-1, 11), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'cancel', (255, 255, 255), 4, font_path),
        apply_button    = Sprite_button('bottomleft', (1, 11), 'center', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'apply', (255, 255, 255), 4, font_path),
        back_button     = Sprite_button('bottomleft', (1, -1), 'bottomleft', (6, 2), (0, 0, 0), (255, 255, 255), 2, 'back', (255, 255, 255), 4, font_path)
    )

    if state[1] == 'account':
        settings_group.add(
            user_label = Sprite_text('bottomright', (-5, -3.4), 'center', 'username', (255, 255, 255), 2, font_path),
            new1_label = Sprite_text('bottomright', (-5, 0.6), 'center', 'new password', (255, 255, 255), 2, font_path),
            new2_label = Sprite_text('bottomright', (-5, 3.6), 'center', 'confirm password', (255, 255, 255), 2, font_path),
            pass_label = Sprite_text('bottomright', (-5, 6.6), 'center', 'current password', (255, 255, 255), 2, font_path),
            user_box = Sprite_textfield('midbottom', (2, -3), 'center', (12, 2), (0, 0, 0), (255, 255, 255), 2, (255, 255, 255), 2, font_path),
            new1_box = Sprite_textfield('midbottom', (2, 1), 'center', (12, 2), (0, 0, 0), (255, 255, 255), 2, (255, 255, 255), 2, font_path),
            new2_box = Sprite_textfield('midbottom', (2, 4), 'center', (12, 2), (0, 0, 0), (255, 255, 255), 2, (255, 255, 255), 2, font_path),
            pass_box = Sprite_textfield('midbottom', (2, 7), 'center', (12, 2), (0, 0, 0), (255, 255, 255), 2, (255, 255, 255), 2, font_path)
        )

        error_group = Sprite_group(
            error1_text = Sprite_text('bottomleft', (9, -3.4), 'center', '', (255, 255, 255), 2, font_path),
            error2_text = Sprite_text('bottomleft', (9, 3.6), 'center', '', (255, 255, 255), 2, font_path),
            error3_text = Sprite_text('bottomleft', (9, 6.6), 'center', '', (255, 255, 255), 2, font_path)
        )

        error_group.resize(screen)

    elif state[1] == 'bindings':
        key_order = (('quit', 'hold', 'rotate_cw', 'rotate_180', 'rotate_ccw'),
                     ('reset', 'move_left', 'move_right', 'soft_drop', 'hard_drop'))
        settings_group.add({f'{action}_label' : Sprite_text('bottomleft', (-13 + c * 15, -3 + r * 2), 'center', action.replace('_', ' '), (255, 255, 255), 2, font_path) for c, column in enumerate(key_order) for r, action in enumerate(column)})
        settings_group.add({f'{action}_value' : Sprite_text('bottomleft', (-6 + c * 15, -3 + r * 2), 'center', pygame.key.name(input_fields[action]), (255, 255, 255), 2, font_path) for c, column in enumerate(key_order) for r, action in enumerate(column)})

    elif state[1] == 'handling': # TODO: DAS, ARR, and SDF descriptions when hovering
        slider_range = {'DAS': (0, 400), 'ARR': (0, 80), 'SDF': (5, 41)}
        for i, control in enumerate(handling.keys()):
            value_text = str(input_fields[control]) if not (control == 'SDF' and (input_fields[control] == slider_range['SDF'][1] or input_fields[control] == 0)) else 'inf'

            settings_group.add({
                f'{control}_label' : Sprite_text('bottomleft', (-13, -3 + i * 4), 'center', control, (255, 255, 255), 2, font_path),
                f'{control}_value' : Sprite_text('bottomleft', (11, -3 + i * 4), 'center', value_text, (255, 255, 255), 2, font_path),
                f'{control}_line'   : Sprite_line((-10, -3.5 + i * 4), 'center', 20, (255, 255, 255), 3, 'horizontal'),
                f'{control}_circle' : Sprite_circle((-10, -3.5 + i * 4), 'center', colors['b'], 0.4, (255, 255, 255))
            })

    settings_group.resize(screen)

    while True:

        current_time = time.time()

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                settings_group.resize(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[2] = ''
                    return
                elif event.key == pygame.K_RETURN:
                    if state[1] == 'account':
                        input_submit(db_type, directory, registrar, user_info, input_fields, error_group)
                        state[2] = ''
                    elif state[1] == 'bindings':
                        changes = {k: input_fields[k] for k, v in bindings.items() if input_fields[k] != v}
                        if changes:
                            if user_info['username'] != 'guest':
                                directory.settings(user_info['username'], changes)
                            for k, v in changes.items():
                                bindings[k] = v
                    elif state[1] == 'handling':
                        changes = {k: input_fields[k] for k, v in handling.items() if input_fields[k] != v}
                        if changes:
                            if user_info['username'] != 'guest':
                                directory.settings(user_info['username'], changes)
                            for k, v in changes.items():
                                handling[k] = v
                elif state[1] == 'account':
                    if event.key == pygame.K_TAB:
                        state[2] = state_transition[state_transition.index(state[2]) - 1]
                        if state[2]:
                            cursor_pos = len(input_fields[state[2]])
                    if state[2] and not (db_type != 'csv' and user_info['username'] == 'guest') and not (db_type == 'csv' and state[2] != 'username'):
                        if event.key == pygame.K_BACKSPACE:
                            key_state['Backspace'] = current_time - .05 + .3 # (- ARR + DAS)
                            key_state['Delete'] = 0
                            input_fields[state[2]] = input_fields[state[2]][:max(cursor_pos - 1, 0)] + input_fields[state[2]][cursor_pos:]
                            cursor_pos = max(cursor_pos - 1, 0)
                            input_edit(directory, state, user_info, input_fields, error_group)
                        elif event.key == pygame.K_DELETE:
                            key_state['Delete'] = current_time - .05 + .3 # (- ARR + DAS)
                            key_state['Backspace'] = 0
                            input_fields[state[2]] = input_fields[state[2]][:cursor_pos] + input_fields[state[2]][cursor_pos + 1:]
                            input_edit(directory, state, user_info, input_fields, error_group)
                        elif event.key == pygame.K_LEFT:
                            key_state['Left'] = current_time - .05 + .3 # (- ARR + DAS)
                            key_state['Right'] = 0
                            cursor_pos = max(cursor_pos - 1, 0)
                        elif event.key == pygame.K_RIGHT:
                            key_state['Right'] = current_time - .05 + .3 # (- ARR + DAS)
                            key_state['Left'] = 0
                            cursor_pos = min(cursor_pos + 1, len(input_fields[state[2]]))
                        elif len(event.unicode) == 1 and len(input_fields[state[2]]) < 16:
                            alphanumeric = (48 <= ord(event.unicode) <= 57 or 65 <= ord(event.unicode) <= 90 or 97 <= ord(event.unicode) <= 122)
                            if state[2] == 'username' and alphanumeric or state[2] == 'password' or state[2] == 'new_pass1' or state[2] == 'new_pass2':
                                input_fields[state[2]] = input_fields[state[2]][:cursor_pos] + event.unicode + input_fields[state[2]][cursor_pos:]
                                cursor_pos += 1
                                input_edit(directory, state, user_info, input_fields, error_group)
            elif event.type == pygame.KEYUP:
                if state[1] == 'account':
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
                    if settings_group.get('back_button').rect.collidepoint(pos):
                        state[0] = 'menu'
                        state[1] = ''
                        state[2] = ''
                        return
                    elif settings_group.get('account_button').rect.collidepoint(pos):
                        if state[1] != 'account':
                            state[1] = 'account'
                            state[2] = ''
                            return
                    elif settings_group.get('bindings_button').rect.collidepoint(pos):
                        if state[1] != 'bindings':
                            state[1] = 'bindings'
                            state[2] = ''
                            return
                    elif settings_group.get('handling_button').rect.collidepoint(pos):
                        if state[1] != 'handling':
                            state[1] = 'handling'
                            state[2] = ''
                            return
                    elif settings_group.get('cancel_button').rect.collidepoint(pos):
                        state[2] = ''
                        return
                    elif settings_group.get('apply_button').rect.collidepoint(pos):
                        if state[1] == 'account':
                            input_submit(db_type, directory, registrar, user_info, input_fields, error_group)
                            state[2] = ''
                        elif state[1] == 'bindings':
                            changes = {k: input_fields[k] for k, v in bindings.items() if input_fields[k] != v}
                            if changes:
                                if user_info['username'] != 'guest':
                                    directory.settings(user_info['username'], changes)
                                for k, v in changes.items():
                                    bindings[k] = v
                        elif state[1] == 'handling':
                            changes = {k: input_fields[k] for k, v in handling.items() if input_fields[k] != v}
                            if changes:
                                if user_info['username'] != 'guest':
                                    directory.settings(user_info['username'], changes)
                                for k, v in changes.items():
                                    handling[k] = v
                    elif state[1] == 'account':
                        for k in ['username', 'new_pass1', 'new_pass2', 'password']:
                            if settings_group.get(input_to_sprite[k]).rect.collidepoint(pos):
                                state[2] = k
                                cursor_pos = len(input_fields[k])
                                break
                        else:
                            state[2] = ''
                    elif state[1] == 'bindings':
                        for k in bindings.keys():
                            key_rect = settings_group.get(input_to_sprite[k]).rect
                            if key_rect.width < key_rect.height:
                                key_rect.width = key_rect.height
                            if key_rect.collidepoint(pos):
                                pygame.draw.rect(screen, (0, 0, 0), key_rect)
                                pygame.draw.rect(screen, (255, 255, 255), key_rect, 2)
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
                                                settings_group.get(input_to_sprite[k2]).update(text=pygame.key.name(input_fields[k2]))
                                                break
                                        input_fields[k] = event.key
                                        settings_group.get(input_to_sprite[k]).update(text=pygame.key.name(input_fields[k]))
                                        break
                                break
                    elif state[1] == 'handling':
                        for k in handling.keys():
                            if settings_group.get(input_to_sprite[k][0]).rect.collidepoint(pos):
                                state[2] = k
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if state[1] == 'handling':
                        state[2] = ''

        ### AUTOREPEAT FOR KEYBOARD
        if state[1] == 'account' and state[2]:
            if key_state['Backspace']:
                remove_timer = current_time - key_state['Backspace']
                if remove_timer > .05:
                    distance = int(remove_timer // .05)
                    key_state['Backspace'] += distance * .05
                    input_fields[state[2]] = input_fields[state[2]][:max(cursor_pos - distance, 0)] + input_fields[state[2]][cursor_pos:]
                    cursor_pos = max(cursor_pos - distance, 0)
                    input_edit(directory, state, user_info, input_fields, error_group)
            elif key_state['Delete']:
                remove_timer = current_time - key_state['Delete']
                if remove_timer > .05:
                    distance = int(remove_timer // .05)
                    key_state['Delete'] += distance * .05
                    input_fields[state[2]] = input_fields[state[2]][:cursor_pos] + input_fields[state[2]][cursor_pos + distance:]
                    input_edit(directory, state, user_info, input_fields, error_group)
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
                settings_group.get(input_to_sprite['SDF'][1]).update(text='inf')
            else:
                settings_group.get(input_to_sprite[state[2]][1]).update(text=str(input_fields[state[2]]))

        ### CLEAR SCREEN
        pygame.draw.rect(screen, colors['b'], screen.get_rect())

        ### DRAW SPRITES
        if state[1] == 'account':
            settings_group.get('user_box').update(text=input_fields['username'], cursor_pos=cursor_pos if state[2] == 'username' else -1)
            settings_group.get('new1_box').update(text='*' * len(input_fields['new_pass1']), cursor_pos=cursor_pos if state[2] == 'new_pass1' else -1)
            settings_group.get('new2_box').update(text='*' * len(input_fields['new_pass2']), cursor_pos=cursor_pos if state[2] == 'new_pass2' else -1)
            settings_group.get('pass_box').update(text='*' * len(input_fields['password']), cursor_pos=cursor_pos if state[2] == 'password' else -1)
            error_group.draw(screen)
        elif state[1] == 'handling':
            slider_range = {'DAS': (0, 400), 'ARR': (0, 80), 'SDF': (5, 41)}
            for i, control in enumerate(handling.keys()):
                value = input_fields[control] if control != 'SDF' or input_fields[control] != 0 else slider_range['SDF'][1]
                percentage = (value - slider_range[control][0]) / (slider_range[control][1] - slider_range[control][0])
                settings_group.get(input_to_sprite[control][0]).update(offset=(-10 + 20 * percentage, settings_group.get(input_to_sprite[control][0]).offset[1]))
        settings_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)

### INPUT FUNCTIONS AND ERROR HANDLING

def input_edit(directory, state, user_info, input_fields, error_group):
    if state[2] == 'username':
        if user_info['username'] == input_fields['username'] or directory.username_available(input_fields['username']):
            error_group.get('error1_text').update(text='')
        else:
            error_group.get('error1_text').update(text='taken')
    elif state[2] == 'new_pass1' or state[2] == 'new_pass2':
        if input_fields['new_pass1'] == input_fields['new_pass2']:
            error_group.get('error2_text').update(text='')
        else:
            error_group.get('error2_text').update(text='doesn\'t match')

def input_submit(db_type, directory, registrar, user_info, input_fields, error_group):
    if user_info['username'] != 'guest':
        if len(input_fields['username']) > 0 and user_info['username'] != input_fields['username']:
            if directory.settings(user_info['username'], {'username': input_fields['username']}):
                registrar.update(user_info['username'], input_fields['username'])
                user_info['username'] = input_fields['username']
        if input_fields['new_pass1'] == input_fields['new_pass2'] and len(input_fields['new_pass1']) > 0 and db_type != 'csv':
            if directory.settings(user_info['username'], {'password': input_fields['new_pass1']}, password=input_fields['password']):
                error_group.get('error3_text').update(text='')
            else:
                error_group.get('error3_text').update(text='incorrect password')
    input_fields['username'] = user_info['username']
    input_fields['password'] = ''
    input_fields['new_pass1'] = ''
    input_fields['new_pass2'] = ''
    error_group.get('error1_text').update(text='')
    error_group.get('error2_text').update(text='')