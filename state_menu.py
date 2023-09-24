import pygame
from sys import exit
from utils import Sprite_group, Sprite_rect, Sprite_text, Sprite_button

def state_menu(screen, clock, font_path, state, user_info):

    ### INIT STATE
    marathon_button = Sprite_button('marathon', (14, 2), 'midbottom', (0, -4), 'center', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    sprint_button   = Sprite_button('sprint', (14, 2), 'midbottom', (0, -1), 'center', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    blitz_button    = Sprite_button('blitz', (14, 2), 'midbottom', (0, 2), 'center', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    records_button  = Sprite_button('records', (14, 2), 'midbottom', (0, 5), 'center', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    settings_button = Sprite_button('settings', (14, 2), 'midbottom', (0, 8), 'center', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    logout_button   = Sprite_button('logout', (8, 2), 'bottomleft', (1, -1), 'bottomleft', (255, 255, 255), 2, (255, 255, 255), 4, font_path)

    menu_group = Sprite_group(
        Sprite_text('TETRADATS', 'midbottom', (0, -10), 'center', (255, 255, 255), 4, font_path),
        marathon_button,
        sprint_button,
        blitz_button,
        records_button,
        settings_button,
        logout_button
    )

    account_group = Sprite_group(
        Sprite_rect((8, 2), 'topright', (-1, 1), 'topright', (255, 255, 255), 2),
        Sprite_rect((1.5, 1.5), 'topleft', (-8.75, 1.25), 'topright', (255, 255, 255), 1),
        Sprite_text(user_info['username'], 'bottomright', (-1.5, 2.6), 'topright', (255, 255, 255), 2, font_path)
    )

    menu_group.resize(screen)
    account_group.resize(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                menu_group.resize(screen)
                account_group.resize(screen)
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
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())

        ### DRAW SPRITES
        menu_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)