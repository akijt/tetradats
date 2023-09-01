import pygame
from tetris import Tetris
from accounts import Accounts_sql, Accounts_msa
from records import Records_csv, Records_sql, Records_msa

from state_login     import state_login
from state_menu      import state_menu
from state_countdown import state_countdown
from state_play      import state_play
from state_pause     import state_pause
from state_finish    import state_finish
from state_records   import state_records
from state_settings  import state_settings

### INIT PYGAME
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Tetradats')
clock = pygame.time.Clock()

### INIT TETRIS
game = Tetris()
colors = {'z': (255, 0,   0),
          'l': (255, 165, 0),
          'o': (255, 255, 0),
          's': (0,   255, 0),
          'i': (0,   255, 255),
          'j': (0,   0,   255),
          't': (160, 32,  240)}

### INIT DIRECTORY
dir_type = 'sql'
if dir_type == 'csv':
    pass
elif dir_type == 'sql':
    header = ['username', 'password', 'quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop', 'DAS', 'ARR', 'SDF']
    datatype = ['VARCHAR(16)' if h in ['username', 'password'] else
                'INT'         for h in header]
    directory = Accounts_sql('tetris', 'accounts', header, datatype) # TODO: rename database to 'tetradats'
elif dir_type == 'msa':
    directory = Accounts_msa('tetradats', 'accounts')

### INIT REGISTRAR
reg_type = 'sql'
if reg_type == 'csv':
    header = ['user', 'datetime', 'timezone'] + game.stat_names
    registrar = Records_csv('records', ['marathon', 'sprint', 'blitz'], header)
    order_by = {'marathon': (5, 'desc'), 'sprint': (4, 'asc'), 'blitz': (5, 'desc')}
elif reg_type == 'sql':
    header = ['user', 'datetime', 'timezone'] + game.stat_names
    datatype = ['VARCHAR(16)'    if h in ['user', 'mode'] else
                'DATETIME'       if h in ['datetime'] else
                'VARCHAR(5)'     if h in ['timezone'] else
                'DOUBLE'         if h in ['time'] else
                'INT'            for h in header]
    registrar = Records_sql('tetris', 'records', header, datatype) # TODO: rename database to 'tetradats'
    order_by = {'marathon': 'score DESC', 'sprint': 'time ASC', 'blitz': 'score DESC'}
elif reg_type == 'msa':
    registrar = Records_msa('tetradats', 'records')
    order_by = {'marathon': 'score DESC', 'sprint': 'time ASC', 'blitz': 'score DESC'}

### INIT STATE
font_path = 'font/FreeSansBold.ttf'
state = ['login', '', '']

while True:

    # required parameters in the order defined:
    # screen, clock, game, colors, dir_type, directory, reg_type, registrar, order_by, font_path, state, user_info, bindings, handling

    ### LOGIN/SIGNUP STATE
    if state[0] == 'login' or state[0] == 'signup':
        acct_info = state_login(screen, clock, dir_type, directory, font_path, state)
        user_info, bindings, handling = acct_info

    ### MENU STATE
    elif state[0] == 'menu':
        state_menu(screen, clock, font_path, state, user_info)

    ### COUNTDOWN STATE
    elif state[0] == 'countdown':
        state_countdown(screen, clock, game, colors, font_path, state, user_info, bindings, handling)

    ### PLAY STATE
    elif state[0] == 'play':
        state_play(screen, clock, game, colors, font_path, state, user_info, bindings)

    ### PAUSE STATE
    elif state[0] == 'pause':
        state_pause(screen, clock, game, font_path, state, user_info, bindings)

    ### FINISH STATE
    elif state[0] == 'finish':
        state_finish(screen, clock, game, reg_type, registrar, order_by, font_path, state, bindings, user_info)

    ### RECORDS STATE
    elif state[0] == 'records':
        state_records(screen, clock, reg_type, registrar, order_by, font_path, state, user_info, bindings)

    ### SETTINGS STATE
    elif state[0] == 'settings':
        state_settings(screen, clock, dir_type, directory, font_path, state, user_info, bindings, handling)