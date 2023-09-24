import pygame
from sys import exit
import time
from utils import Sprite_group, Sprite_rect, Sprite_text, Sprite_button

def state_countdown(screen, clock, game, colors, font_path, state, user_info, bindings, handling):

    ### INIT STATE
    game.reset(state[1], handling)
    countdown = time.time()

    menu_button = Sprite_button('menu', (8, 2), 'topleft', (1, 1), 'topleft', (255, 255, 255), 2, (255, 255, 255), 4, font_path)
    int_rect    = Sprite_button('3', (8, 2), 'midbottom', (0, -2), 'center', (255, 255, 255), 0, (0, 0, 0), 4, font_path)

    countdown_group = Sprite_group(
        menu_button,
        int_rect,
        Sprite_text('time', 'bottomleft', (6, 5), 'center', (255, 255, 255), 2, font_path),
        Sprite_text('0:00.000', 'bottomleft', (6, 7), 'center', (255, 255, 255), 4, font_path),
        Sprite_text('score', 'bottomleft', (6, 8), 'center', (255, 255, 255), 2, font_path),
        Sprite_text('0', 'bottomleft', (6, 10), 'center', (255, 255, 255), 4, font_path),
        Sprite_text('pieces', 'bottomright', (-6, 2), 'center', (255, 255, 255), 2, font_path),
        Sprite_text('0', 'bottomright', (-6, 4), 'center', (255, 255, 255), 4, font_path),
        Sprite_text('lines', 'bottomright', (-6, 5), 'center', (255, 255, 255), 2, font_path),
        Sprite_text('0', 'bottomright', (-6, 7), 'center', (255, 255, 255), 4, font_path),
        Sprite_text('level', 'bottomright', (-6, 8), 'center', (255, 255, 255), 2, font_path),
        Sprite_text('1', 'bottomright', (-6, 10), 'center', (255, 255, 255), 4, font_path),
        Sprite_text(f'{game.stats["mode"]}', 'midbottom', (0, 12), 'center', (255, 255, 255), 4, font_path)
    )

    account_group = Sprite_group(
        Sprite_rect((8, 2), 'topright', (-1, 1), 'topright', (255, 255, 255), 2),
        Sprite_rect((1.5, 1.5), 'topleft', (-8.75, 1.25), 'topright', (255, 255, 255), 1),
        Sprite_text(user_info['username'], 'bottomright', (-1.5, 2.6), 'topright', (255, 255, 255), 2, font_path)
    )

    countdown_group.resize(screen)
    account_group.resize(screen)

    while True:

        ### EVENT LOOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                countdown_group.resize(screen)
                account_group.resize(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == bindings['quit']:
                    state[0] = 'menu'
                    return
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
                    if menu_button.rect.collidepoint(pos):
                        state[0] = 'menu'
                        return

        if time.time() - countdown > 3:
            state[0] = 'play'
            return

        ### CLEAR SCREEN
        pygame.draw.rect(screen, (0, 0, 0), screen.get_rect())

        ### DRAW EMPTY BOARD
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        border_width = 1
        for r in range(20):
            for c in range(10):
                left = screen.get_width() / 2 + (-5 + c) * dim
                top = screen.get_height() / 2 + (9 - r) * dim
                pygame.draw.rect(screen, (128, 128, 128), [left, top, dim + border_width, dim + border_width], border_width)

        ### DRAW NEXT PIECES
        next_num = 3
        for p in range(next_num):
            for dr, dc in game.minos[game.queue[p]][0]:
                left = screen.get_width() / 2 + (6 + dc) * dim
                top = screen.get_height() / 2 + (-7 - dr + p * 4) * dim
                pygame.draw.rect(screen, colors[game.queue[p]], [left, top, dim + border_width, dim + border_width])

        ### DRAW SPRITES
        int_rect.update(text=f'{3 - int(time.time() - countdown)}')
        countdown_group.draw(screen)
        account_group.draw(screen)

        ### CLOCK
        dim = min(screen.get_width() / 40, screen.get_height() / 30) # To fit in a 4:3 aspect ratio
        font = pygame.font.Font(font_path, round(.5 * 3 * dim))
        image = font.render(f'{round(clock.get_fps())}', False, (255, 255, 255))
        rect = image.get_rect(bottomright=(screen.get_width() - 1 * dim, 5 * dim))
        screen.blit(image, rect)

        pygame.display.update()
        clock.tick(60)