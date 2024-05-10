import pygame
from sys import exit
from utils import Sprite_group, Sprite_rect, Sprite_text, Sprite_button

def state_menu(screen, clock, colors, font_path, state, user_info):

    ### INIT STATE
    menu_group = Sprite_group(
        title_text      = Sprite_text('midbottom', (0, -10), 'center', 'TETRADATS', (255, 255, 255), 4, font_path),
        marathon_button = Sprite_button('bottomright', (-1, -5), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'marathon', (255, 255, 255), 4, font_path),
        sprint_button   = Sprite_button('bottomright', (-1, -2), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'sprint', (255, 255, 255), 4, font_path),
        blitz_button    = Sprite_button('bottomright', (-1,  1), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'blitz', (255, 255, 255), 4, font_path),
        classic_button  = Sprite_button('bottomleft', (1, -5), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'classic', (255, 255, 255), 4, font_path),
        finesse_button  = Sprite_button('bottomleft', (1, -2), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'finesse', (255, 255, 255), 4, font_path),
        cheese_button   = Sprite_button('bottomleft', (1, 1), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'cheese', (255, 255, 255), 4, font_path),
        records_button  = Sprite_button('midbottom', (0, 5), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'records', (255, 255, 255), 4, font_path),
        settings_button = Sprite_button('midbottom', (0, 8), 'center', (14, 2), (0, 0, 0), (255, 255, 255), 2, 'settings', (255, 255, 255), 4, font_path),
        logout_button   = Sprite_button('bottomleft', (1, -1), 'bottomleft', (8, 2), (0, 0, 0), (255, 255, 255), 2, 'logout', (255, 255, 255), 4, font_path)
    )

    account_group = Sprite_group(
        tab_rect  = Sprite_rect('topright', (-1, 1), 'topright', (8, 2), (0, 0, 0), (255, 255, 255), 2),
        pfp_rect  = Sprite_rect('topleft', (-8.75, 1.25), 'topright', (1.5, 1.5), (0, 0, 0), (255, 255, 255), 1),
        user_text = Sprite_text('bottomright', (-1.5, 2.6), 'topright', user_info['username'], (255, 255, 255), 2, font_path)
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
                    if menu_group.get('logout_button').rect.collidepoint(pos):
                        state[0] = 'login'
                        return
                    elif menu_group.get('marathon_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'marathon'
                        state[2] = 1
                        return
                    elif menu_group.get('sprint_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'sprint'
                        state[2] = 1
                        return
                    elif menu_group.get('blitz_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'blitz'
                        state[2] = 1
                        return
                    elif menu_group.get('classic_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'classic'
                        state[2] = 1
                        return
                    elif menu_group.get('finesse_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'finesse'
                        state[2] = 1
                        return
                    elif menu_group.get('cheese_button').rect.collidepoint(pos):
                        state[0] = 'countdown'
                        state[1] = 'cheese'
                        state[2] = 1
                        return
                    elif menu_group.get('records_button').rect.collidepoint(pos):
                        state[0] = 'records'
                        state[1] = 'marathon'
                        state[2] = 'global' if user_info['username'] == 'guest' else ''
                        return
                    elif menu_group.get('settings_button').rect.collidepoint(pos):
                        state[0] = 'settings'
                        state[1] = 'account'
                        return
                    # elif menu_group.get('title_text').rect.collidepoint(pos):
                    #     state[0] = 'countdown'
                    #     state[1] = 'finesse'
                    #     state[2] = 1
                    #     return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, colors['b'], screen.get_rect())

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