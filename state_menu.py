import pygame
from utils import Sprite_rect

def state_menu(screen, clock, state, user_info):

    ### INIT STATE
    marathon_button = Sprite_rect((14, 2), 'midbottom', (0, -4), 'center', 'White')
    sprint_button = Sprite_rect((14, 2), 'midbottom', (0, -1), 'center', 'White')
    blitz_button = Sprite_rect((14, 2), 'midbottom', (0, 2), 'center', 'White')
    records_button = Sprite_rect((14, 2), 'midbottom', (0, 5), 'center', 'White')
    settings_button = Sprite_rect((14, 2), 'midbottom', (0, 8), 'center', 'White')
    logout_button = Sprite_rect((8, 2), 'bottomleft', (1, -1), 'bottomleft', 'White')
    group = pygame.sprite.Group()
    group.add(marathon_button)
    group.add(sprint_button)
    group.add(blitz_button)
    group.add(records_button)
    group.add(settings_button)
    group.add(logout_button)

    while True:

        ### ADJUST DIM
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        fonts = []
        fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
        fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
        border_width = 1

        ### UPDATE SPRITES
        group.update(screen.get_size(), dim, border_width + 1)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if logout_button.rect.collidepoint(pos):
                        state[0] = 'login'
                        return
                    elif marathon_button.rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'marathon'
                        return
                    elif sprint_button.rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'sprint'
                        return
                    elif blitz_button.rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'blitz'
                        return
                    elif records_button.rect.collidepoint(pos):
                        state[0] = 'records'
                        state[1] = 'marathon'
                        if user_info['username'] == 'guest':
                            state[2] = 'global'
                        return
                    elif settings_button.rect.collidepoint(pos):
                        state[0] = 'settings'
                        state[1] = 'account'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        group.draw(screen)

        ### WRITE TEXT
        state_text = fonts[1].render('TETRADATS', False, 'White')
        state_rect = state_text.get_rect(midbottom=(screen.get_width() / 2, screen.get_height() / 2 - 10 * dim))
        screen.blit(state_text, state_rect)

        marathon_text = fonts[1].render('marathon', False, 'White')
        marathon_rect = marathon_text.get_rect(midbottom=marathon_button.rect.midbottom)
        screen.blit(marathon_text, marathon_rect)

        sprint_text = fonts[1].render('sprint', False, 'White')
        sprint_rect = sprint_text.get_rect(midbottom=sprint_button.rect.midbottom)
        screen.blit(sprint_text, sprint_rect)

        blitz_text = fonts[1].render('blitz', False, 'White')
        blitz_rect = blitz_text.get_rect(midbottom=blitz_button.rect.midbottom)
        screen.blit(blitz_text, blitz_rect)

        records_text = fonts[1].render('records', False, 'White')
        records_rect = records_text.get_rect(midbottom=records_button.rect.midbottom)
        screen.blit(records_text, records_rect)

        settings_text = fonts[1].render('settings', False, 'White')
        settings_rect = settings_text.get_rect(midbottom=settings_button.rect.midbottom)
        screen.blit(settings_text, settings_rect)

        logout_text = fonts[1].render('logout', False, 'White')
        logout_rect = logout_text.get_rect(midbottom=logout_button.rect.midbottom)
        screen.blit(logout_text, logout_rect)

        ### ACCOUNT TAB
        account_tab = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        account_tab.topright = (screen.get_width() - 1 * dim, 1 * dim)
        pygame.draw.rect(screen, 'White', account_tab, border_width + 1)

        account_text = fonts[0].render(user_info['username'], False, 'White')
        account_rect = account_text.get_rect(bottomright=(account_tab.right - .5 * dim, account_tab.bottom - .4 * dim))
        screen.blit(account_text, account_rect)

        pfp_tab = pygame.Rect(0, 0, 1.5 * dim, 1.5 * dim)
        pfp_tab.bottomleft = (account_tab.left + .25 * dim, account_tab.bottom - .25 * dim)
        pygame.draw.rect(screen, 'White', pfp_tab, border_width)

        ### CLOCK
        pygame.display.update()
        clock.tick(60)