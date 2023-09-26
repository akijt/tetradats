import pygame
from tetris import Tetris
from accounts import Accounts_csv, Accounts_sql, Accounts_msa
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

### DATABASE TYPE
db_type = 'csv'

### INIT DIRECTORY
if db_type == 'csv':
    header = ['username', 'quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop', 'DAS', 'ARR', 'SDF']
    directory = Accounts_csv('accounts', header)
elif db_type == 'sql':
    header = ['username', 'password', 'datetime', 'timezone', 'quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop', 'DAS', 'ARR', 'SDF']
    datatype = ['VARCHAR(16)' if h in ['username', 'password'] else
                'DATETIME'    if h in ['datetime'] else
                'VARCHAR(5)'  if h in ['timezone'] else
                'INT'         for h in header]
    directory = Accounts_sql('tetradats', 'accounts', header, datatype)
elif db_type == 'msa':
    header = ['username', 'password', 'datetime', 'timezone', 'quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop', 'DAS', 'ARR', 'SDF']
    directory = Accounts_msa('tetradats', 'accounts', header)

### INIT REGISTRAR
if db_type == 'csv':
    header = ['username', 'datetime', 'timezone'] + game.stat_names
    registrar = Records_csv('records', ['marathon', 'sprint', 'blitz'], header)
    order_by = {'marathon': (5, 'desc'), 'sprint': (4, 'asc'), 'blitz': (5, 'desc')}
elif db_type == 'sql':
    header = ['username', 'datetime', 'timezone'] + game.stat_names
    datatype = ['VARCHAR(16)' if h in ['username', 'mode'] else
                'DATETIME'    if h in ['datetime'] else
                'VARCHAR(5)'  if h in ['timezone'] else
                'DOUBLE'      if h in ['time'] else
                'INT'         for h in header]
    registrar = Records_sql('tetradats', 'records', header, datatype)
    order_by = {'marathon': 'score DESC', 'sprint': 'time ASC', 'blitz': 'score DESC'}
elif db_type == 'msa':
    registrar = Records_msa('tetradats', 'records')
    order_by = {'marathon': 'score DESC', 'sprint': 'time ASC', 'blitz': 'score DESC'}

### INIT STATE
font_path = 'font/FreeSansBold.ttf'
state = ['login', '', '']

while True:

    # required parameters in the order defined:
    # screen, clock, game, colors, db_type, directory, registrar, order_by, font_path, state, user_info, bindings, handling

    ### LOGIN/SIGNUP STATE
    if state[0] == 'login' or state[0] == 'signup':
        user_info, bindings, handling = state_login(screen, clock, db_type, directory, font_path, state)

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
        state_finish(screen, clock, game, db_type, registrar, order_by, font_path, state, bindings, user_info)

    ### RECORDS STATE
    elif state[0] == 'records':
        state_records(screen, clock, db_type, registrar, order_by, font_path, state, user_info, bindings)

    ### SETTINGS STATE
    elif state[0] == 'settings':
        state_settings(screen, clock, db_type, directory, registrar, font_path, state, user_info, bindings, handling)