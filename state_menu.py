import pygame
from utils import Sprite_rect, Sprite_text, Sprite_button

def state_menu(screen, clock, state, user_info):

    ### INIT STATE
    marathon_button = Sprite_button('marathon', (14, 2), 'midbottom', (0, -4), 'center', 'White', 2, 'White', 4, None)
    sprint_button   = Sprite_button('sprint', (14, 2), 'midbottom', (0, -1), 'center', 'White', 2, 'White', 4, None)
    blitz_button    = Sprite_button('blitz', (14, 2), 'midbottom', (0, 2), 'center', 'White', 2, 'White', 4, None)
    records_button  = Sprite_button('records', (14, 2), 'midbottom', (0, 5), 'center', 'White', 2, 'White', 4, None)
    settings_button = Sprite_button('settings', (14, 2), 'midbottom', (0, 8), 'center', 'White', 2, 'White', 4, None)
    logout_button   = Sprite_button('logout', (8, 2), 'bottomleft', (1, -1), 'bottomleft', 'White', 2, 'White', 4, None)

    menu_group = pygame.sprite.Group()
    menu_group.add(Sprite_text('TETRADATS', 'midbottom', (0, -10), 'center', 'White', 4, None))
    menu_group.add(marathon_button)
    menu_group.add(sprint_button)
    menu_group.add(blitz_button)
    menu_group.add(records_button)
    menu_group.add(settings_button)
    menu_group.add(logout_button)

    account_group = pygame.sprite.Group()
    account_group.add(Sprite_rect((8, 2), 'topright', (-1, 1), 'topright', 'White', 2))
    account_group.add(Sprite_rect((1.5, 1.5), 'topleft', (-8.75, 1.25), 'topright', 'White', 1))
    account_group.add(Sprite_text(user_info['username'], 'bottomright', (-1.5, 2.6), 'topright', 'White', 2, None))

    menu_group.update(screen)
    account_group.update(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                menu_group.update(screen)
                account_group.update(screen)
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

        ### DRAW SPRITES
        menu_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(None, round(.75 * 2 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, 'White')
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)