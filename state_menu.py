import pygame

def state_menu(current_time):

    ### EVENT LOOP
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
    pygame.draw.rect(screen, 'Black', [0, 0, screen_width * dim, screen_height * dim])

    ### DRAW BUTTONS
    rect_width  = 14 * dim
    rect_height = 2 * dim

    marathon_button = pygame.Rect(0, 0, rect_width, rect_height)
    marathon_button.midbottom = ((screen_width / 2) * dim, (top_margin + 8) * dim)
    pygame.draw.rect(screen, 'White', marathon_button, border_width + 1)

    sprint_button = pygame.Rect(0, 0, rect_width, rect_height)
    sprint_button.midbottom = ((screen_width / 2) * dim, (top_margin + 11) * dim)
    pygame.draw.rect(screen, 'White', sprint_button, border_width + 1)

    blitz_button = pygame.Rect(0, 0, rect_width, rect_height)
    blitz_button.midbottom = ((screen_width / 2) * dim, (top_margin + 14) * dim)
    pygame.draw.rect(screen, 'White', blitz_button, border_width + 1)

    records_button = pygame.Rect(0, 0, rect_width, rect_height)
    records_button.midbottom = ((screen_width / 2) * dim, (top_margin + 17) * dim)
    pygame.draw.rect(screen, 'White', records_button, border_width + 1)

    settings_button = pygame.Rect(0, 0, rect_width, rect_height)
    settings_button.midbottom = ((screen_width / 2) * dim, (top_margin + 20) * dim)
    pygame.draw.rect(screen, 'White', settings_button, border_width + 1)

    logout_button = pygame.Rect(0, 0, 8 * dim, rect_height)
    logout_button.bottomleft = (1 * dim, (screen_height - 1) * dim)
    pygame.draw.rect(screen, 'White', logout_button, border_width + 1)

    ### WRITE TEXT
    state_text = font_large.render('TETRADATS', False, 'White')
    state_rect = state_text.get_rect()
    state_rect.midbottom = ((screen_width / 2) * dim, (top_margin + 2) * dim)
    screen.blit(state_text, state_rect)

    marathon_text = font_large.render('marathon', False, 'White')
    marathon_rect = marathon_text.get_rect()
    marathon_rect.midbottom = marathon_button.midbottom
    screen.blit(marathon_text, marathon_rect)

    sprint_text = font_large.render('sprint', False, 'White')
    sprint_rect = sprint_text.get_rect()
    sprint_rect.midbottom = sprint_button.midbottom
    screen.blit(sprint_text, sprint_rect)

    blitz_text = font_large.render('blitz', False, 'White')
    blitz_rect = blitz_text.get_rect()
    blitz_rect.midbottom = blitz_button.midbottom
    screen.blit(blitz_text, blitz_rect)

    records_text = font_large.render('records', False, 'White')
    records_rect = records_text.get_rect()
    records_rect.midbottom = records_button.midbottom
    screen.blit(records_text, records_rect)

    settings_text = font_large.render('settings', False, 'White')
    settings_rect = settings_text.get_rect()
    settings_rect.midbottom = settings_button.midbottom
    screen.blit(settings_text, settings_rect)

    logout_text = font_large.render('logout', False, 'White')
    logout_rect = logout_text.get_rect()
    logout_rect.midbottom = logout_button.midbottom
    screen.blit(logout_text, logout_rect)

    ### ACCOUNT TAB
    account_tab = pygame.Rect(0, 0, 8 * dim, 2 * dim)
    account_tab.topright = ((screen_width - 1) * dim, 1 * dim)
    pygame.draw.rect(screen, 'White', account_tab, border_width + 1)

    account_text = font_small.render(user_info['username'], False, 'White')
    account_rect = account_text.get_rect()
    account_rect.bottomright = (account_tab.right - .5 * dim, account_tab.bottom - .4 * dim)
    screen.blit(account_text, account_rect)

    pfp_tab = pygame.Rect(0, 0, 1.5 * dim, 1.5 * dim)
    pfp_tab.bottomleft = (account_tab.left + .25 * dim, account_tab.bottom - .25 * dim)
    pygame.draw.rect(screen, 'White', pfp_tab, border_width)