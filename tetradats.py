import pygame
from tetris import Tetris
from accounts import Accounts_sql
from records import Records_csv, Records_sql

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
colors = {'z': 'Red',
          'l': 'Orange',
          'o': 'Yellow',
          's': 'Green',
          'i': 'Cyan',
          'j': 'Blue',
          't': 'Purple'}

### INIT DIRECTORY
header = ['username', 'password', 'quit', 'reset', 'hold', 'move_left', 'move_right', 'rotate_cw', 'rotate_180', 'rotate_ccw', 'soft_drop', 'hard_drop', 'DAS', 'ARR', 'SDF']
datatype = ['VARCHAR(16)' if h in ['username', 'password'] else
            'INT(4)'      if h in ['DAS', 'ARR', 'SDF'] else
            'INT'         for h in header]
sql_directory = Accounts_sql(header, datatype)

### INIT REGISTRAR
header = ['user', 'datetime', 'timezone'] + game.stat_names
datatype = ['VARCHAR(30)'    if h in ['user', 'mode'] else
            'DATETIME'       if h in ['datetime'] else
            'VARCHAR(5)'     if h in ['timezone'] else
            'DOUBLE(30, 15)' if h in ['time'] else
            'INT'            for h in header]
csv_registrar = Records_csv('records', ['marathon', 'sprint', 'blitz'], header)
sql_registrar = Records_sql('tetris', 'records', header, datatype)
order_by = {'marathon': 'score DESC', 'sprint': 'time ASC', 'blitz': 'score DESC'}

### INIT STATE
state = ['login', '', '']

while True:

    # required parameters in the order defined:
    # screen, clock, game, colors, sql_directory, csv_registrar, sql_registrar, order_by, state, user_info, bindings, handling

    ### LOGIN/SIGNUP STATE
    if state[0] == 'login' or state[0] == 'signup':
        acct_info = state_login(screen, clock, sql_directory, state)
        user_info, bindings, handling = acct_info

    ### MENU STATE
    elif state[0] == 'menu':
        state_menu(screen, clock, state, user_info)

    ### COUNTDOWN STATE
    elif state[0] == 'countdown':
        state_countdown(screen, clock, game, colors, state, user_info, bindings, handling)

    ### PLAY STATE
    elif state[0] == 'play':
        state_play(screen, clock, game, colors, state, user_info, bindings)

    ### PAUSE STATE
    elif state[0] == 'pause':
        state_pause(screen, clock, game, state, user_info, bindings)

    ### FINISH STATE
    elif state[0] == 'finish':
        state_finish(screen, clock, game, csv_registrar, sql_registrar, order_by, state, bindings, user_info)

    ### RECORDS STATE
    elif state[0] == 'records':
        state_records(screen, clock, csv_registrar, sql_registrar, order_by, state, user_info, bindings)

    ### SETTINGS STATE
    elif state[0] == 'settings':
        state_settings(screen, clock, sql_directory, state, user_info, bindings, handling)