import pygame

def state_lose(screen, clock, state, bindings):

    ### INIT STATE
    pass

    while True:

        ### ADJUST DIM
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        fonts = []
        fonts.append(pygame.font.Font(None, round(.75 * 2 * dim)))
        fonts.append(pygame.font.Font(None, round(.75 * 4 * dim)))
        border_width = 1

        ### INIT INTERACTABLES
        retry_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        retry_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 - 2 * dim)

        menu_button = pygame.Rect(0, 0, 8 * dim, 2 * dim)
        menu_button.midbottom = (screen.get_width() / 2, screen.get_height() / 2 + 2 * dim)

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                    return
                elif event.key == bindings['reset']:
                    state[0] = 'countdown'
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if retry_button.collidepoint(pos):
                        state[0] = 'countdown'
                        return
                    elif menu_button.collidepoint(pos):
                        state[0] = 'menu'
                        return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, 'Black', screen.get_rect())

        ### DRAW BUTTONS
        pygame.draw.rect(screen, 'White', retry_button, border_width + 1)
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

        ### CLOCK
        pygame.display.update()
        clock.tick(60)