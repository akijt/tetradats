import random

class Tetris():

    def __init__(self):
        self.minos  = {'t': (((2, 1), (2, 0), (3, 1), (2, 2)),
                             ((2, 1), (3, 1), (2, 2), (1, 1)),
                             ((2, 1), (2, 2), (1, 1), (2, 0)),
                             ((2, 1), (1, 1), (2, 0), (3, 1))),
                       'i': (((2, 0), (2, 1), (2, 2), (2, 3)),
                             ((0, 2), (1, 2), (2, 2), (3, 2)),
                             ((1, 0), (1, 1), (1, 2), (1, 3)),
                             ((0, 1), (1, 1), (2, 1), (3, 1))),
                       'o': (((2, 1), (2, 2), (3, 1), (3, 2)),
                             ((2, 1), (2, 2), (3, 1), (3, 2)),
                             ((2, 1), (2, 2), (3, 1), (3, 2)),
                             ((2, 1), (2, 2), (3, 1), (3, 2))),
                       'j': (((2, 0), (2, 1), (2, 2), (3, 0)),
                             ((1, 1), (2, 1), (3, 1), (3, 2)),
                             ((2, 0), (2, 1), (2, 2), (1, 2)),
                             ((1, 1), (2, 1), (3, 1), (1, 0))),
                       'l': (((2, 0), (2, 1), (2, 2), (3, 2)),
                             ((1, 1), (2, 1), (3, 1), (1, 2)),
                             ((2, 0), (2, 1), (2, 2), (1, 0)),
                             ((1, 1), (2, 1), (3, 1), (3, 0))),
                       's': (((2, 0), (2, 1), (3, 1), (3, 2)),
                             ((1, 2), (2, 1), (2, 2), (3, 1)),
                             ((1, 0), (1, 1), (2, 1), (2, 2)),
                             ((1, 1), (2, 0), (2, 1), (3, 0))),
                       'z': (((2, 1), (2, 2), (3, 0), (3, 1)),
                             ((1, 1), (2, 1), (2, 2), (3, 2)),
                             ((1, 1), (1, 2), (2, 0), (2, 1)),
                             ((1, 0), (2, 0), (2, 1), (3, 1)))}
        self.bag    = list(self.minos.keys())
        self.start_position = (18, 3)
        self.kicks  = {'t': (((),                                     # 0 >> 0
                              ((-1, 0), (-1, 1), ( 0,-2), (-1,-2)),   # 0 >> 1
                              (( 0, 1), ( 1, 1), (-1, 1)),            # 0 >> 2
                              (( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2))),  # 0 >> 3
                             ((( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),   # 1 >> 0
                              (),                                     # 1 >> 1
                              (( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),   # 1 >> 2
                              (( 1, 0), ( 1, 1))),                    # 1 >> 3
                             ((( 0,-1), (-1,-1), ( 1,-1)),            # 2 >> 0
                              ((-1, 0), (-1, 1), ( 0,-2), (-1,-2)),   # 2 >> 1
                              (),                                     # 2 >> 2
                              (( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2))),  # 2 >> 3
                             (((-1, 0), (-1,-1), ( 0, 2), (-1, 2)),   # 3 >> 0
                              ((-1, 0), (-1, 1)),                     # 3 >> 1
                              ((-1, 0), (-1,-1), ( 0, 2), (-1, 2)),   # 3 >> 2
                              ())),                                   # 3 >> 3
                       'i': (((),                                     # 0 >> 0
                              ((-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),   # 0 >> 1
                              (( 0, 1)),                              # 0 >> 2
                              ((-1, 0), ( 2, 0), (-1, 2), ( 2,-1))),  # 0 >> 3
                             ((( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),   # 1 >> 0
                              (),                                     # 1 >> 1
                              ((-1, 0), ( 2, 0), (-1, 2), ( 2,-1)),   # 1 >> 2
                              (( 1, 0))),                             # 1 >> 3
                             ((( 0,-1)),                              # 2 >> 0
                              (( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),   # 2 >> 1
                              (),                                     # 2 >> 2
                              (( 2, 0), (-1, 0), ( 2, 1), (-1,-2))),  # 2 >> 3
                             ((( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),   # 3 >> 0
                              ((-1, 0)),                              # 3 >> 1
                              ((-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),   # 3 >> 2
                              ()))}                                   # 3 >> 3
        self.corner = ((3, 0), (3, 2), (1, 2), (1, 0))
        self.stat_names = ['mode', 'time', 'score', 'pieces', 'lines', 'level', # Top row is REQUIRED
                           'DAS', 'ARR', 'SDF', 'keys', 'holds', # 'DAS', 'ARR', 'SDF' are REQUIRED
                           'single', 'double', 'triple', 'tetris',
                           'mini t-spin null', 'mini t-spin single', 'mini t-spin double',
                           't-spin null', 't-spin single', 't-spin double', 't-spin triple',
                           'perfect clear single', 'perfect clear double', 'perfect clear triple',
                           'perfect clear tetris', 'max B2B', 'max combo'] # TODO: add finess
        self.key_state  = {'soft_drop': 0, 'move_left': [0, 0], 'move_right': [0, 0]}
        self.lock = {'time': .5, 'count': 15}
        # TODO: add classic mode:
        # disable hold(), hard_drop(), and rotate(2)
        # in reset() and new_piece() add random bag system (display only one next piece)
        # in reset() make start level selectable
        # in reset() turn ghost (new variable) off
        # in piece_lock() self.lock_count > self.lock['count'] is not checked
        # in move() and rotate() when self.lock_count += 1, self.lock_time is not reset

    def reset(self, mode, handling):
        self.board     = [[None for c in range(10)] for r in range(40)]
        self.queue     = random.sample(self.bag, k=7)
        self.held      = None
        self.hold_used = False
        self.b2b       = -1
        self.combo     = -1

        self.last_action = 'reset'
        self.last_clear  = ''
        self.stats       = {x: 0 for x in self.stat_names}

        for k, v in handling.items():
            self.stats[k] = v
        self.stats['mode']  = mode # 'marathon', 'sprint', or 'blitz'
        self.stats['level'] = 1 # This needs to be in reset (countdown screen should show correct level)
        self.gravity        = self.gravity = (0.8 - (self.stats['level'] - 1) * 0.007) ** (self.stats['level'] - 1)
        self.lose           = False
        self.finish         = False

    def start(self, current_time):
        self.stats['time'] = current_time
        self.new_piece(self.queue.pop(0), current_time)

    def new_piece(self, piece, current_time):
        self.piece    = piece
        self.position = [x for x in self.start_position]
        self.rotation = 0

        if self.collision():
            self.lose = True
            return
        if len(self.queue) < 4:
            self.queue.extend(random.sample(self.bag, k=7))
        self.set_height()

        self.gravity_time = current_time - self.gravity # when the last drop was
        self.lock_time    = 0 # when lock_time started/reset
        self.lock_count   = 0 # number of moves/rotations since touchdown
        self.lock_lowest  = 18 # the lowest row the piece has been on
        

    def hold(self, current_time):
        self.stats['keys'] += 1
        if not self.hold_used:
            if self.held == None:
                self.held = self.piece
                self.new_piece(self.queue.pop(0), current_time)
            else:
                temp = self.piece
                self.new_piece(self.held, current_time)
                self.held = temp
            self.hold_used = True
            self.stats['holds'] += 1
            self.last_action = 'hold'

    def move(self, distance, current_time):
        orig_height = self.height
        step = 1 if distance > 0 else -1
        for i in range(abs(distance)):
            self.position[1] += step
            if self.collision():
                self.position[1] -= step
                if i == 0:
                    return False
                break
        self.set_height() # move that causes height == 0 counts in lock_count
        if orig_height == 0 or self.height == 0 or self.lock_count > 0: # if height == 0 or lock_count has already started
            if self.lock_count < self.lock['count']:
                self.lock_time = current_time
            self.lock_count += i + 1
        self.last_action = 'move'
        return True

    def rotate(self, turns, current_time):
        self.stats['keys'] += 1
        orig_height   = self.height
        orig_position = self.position
        orig_rotation = self.rotation
        self.rotation = (self.rotation + turns) % 4
        if self.collision():
            for i, (x, y) in enumerate(self.kicks['i' if self.piece == 'i' else 't'][orig_rotation][self.rotation]):
                self.position = [orig_position[0] + y, orig_position[1] + x]
                if not self.collision():
                    self.set_height() # rotation that causes height == 0 counts in lock_count
                    if orig_height == 0 or self.height == 0 or self.lock_count > 0: # if height == 0 or lock_count has already started
                        if self.lock_count < self.lock['count']:
                            self.lock_time = current_time
                        self.lock_count += 1
                    self.last_action = f'rotate{i}'
                    return True
            self.position = orig_position
            self.rotation = orig_rotation
            return False
        else:
            self.set_height() # rotation that causes height == 0 counts in lock_count
            if orig_height == 0 or self.height == 0 or self.lock_count > 0: # if height == 0 or lock_count has already started
                if self.lock_count < self.lock['count']:
                    self.lock_time = current_time
                self.lock_count += 1
            self.last_action = 'rotate'
            return True

    def drop(self, distance):
        '''
        (7/17/26) The lowest row reached by a piece can be interpreted in two different ways. The
        way it is interpreted in this implementation is the lowest row that the 4x4 piece rotation
        area, whose coordinates of its lower left corner are saved in self.position, has been on.
        The other interpretation is the lowest row that any mino of the current piece has been on.
        Because this would require lock_lowest updates in rotation() too, the former was chosen.
        (7/18/23) Soft drops and hard drops reward points for the number of rows dropped, even if
        points were rewarded for dropping that row already. An example would be where if the player
        soft drops to a position, rotates in a way where height increases, and soft/hard drops
        again to get more points.
        '''
        distance = min(distance, self.height)
        if distance > 0:
            self.position[0] -= distance
            self.height -= distance
            if self.position[0] < self.lock_lowest:
                self.lock_lowest = self.position[0]
                self.lock_count  = 0
            self.stats['score'] += distance * self.key_state['soft_drop']
            self.last_action = 'drop'
            return True
        else:
            return False

    def soft_drop(self, current_time, down=True):
        if down:
            self.stats['keys'] += 1
            self.key_state['soft_drop'] = 1
            if self.stats['SDF'] <= 1:
                self.gravity = 0
            else:
                self.gravity /= self.stats['SDF']
                self.gravity_time = current_time - self.gravity
        else:
            self.key_state['soft_drop'] = 0
            self.gravity = self.gravity = (0.8 - (self.stats['level'] - 1) * 0.007) ** (self.stats['level'] - 1)

    def hard_drop(self, current_time):
        '''
        (7/16/23) It is an option to treat hard_drop() like soft_drop(). In hard_drop(),
        self.key_state['hard_drop'] will be set to 1 (that's it). In gravity_drop,
        self.key_state['hard_drop'] will be an additional condition for
        self.drop(40, current_time). After the drop() call, self.key_state['hard_drop'] is reverted
        back to 0. In drop(), the addition to self.stats['score'] will need to muliply distance by
        2 if self.key_state['hard_drop'].
        '''
        self.stats['keys'] += 1
        self.stats['score'] += self.height * 2
        self.position[0] -= self.height
        self.place(current_time)

    def place(self, current_time): 
        below = False
        for dr, dc in self.minos[self.piece][self.rotation]:
            self.board[self.position[0] + dr][self.position[1] + dc] = self.piece
            if self.position[0] + dr < 20:
                below = True
        if not below:
            self.lose = True # if entire mino is above 20, game is lost
            return
        self.stats['pieces'] += 1
        self.clear()
        self.new_piece(self.queue.pop(0), current_time)
        self.hold_used = False
        self.last_action = 'place' # must be after clear()

    def clear(self):
        t_check = self.t_check()
        rows = 0
        for r in range(40):
            if None in self.board[r]:
                self.board[rows] = self.board[r]
                rows += 1
        clear_count = 40 - rows
        while rows < 40:
            self.board[rows] = [None for _ in range(10)]
            rows += 1
        self.stats['lines'] += clear_count
        clear_string = {0: 'null', 1: 'single', 2: 'double', 3: 'triple', 4: 'tetris'}[clear_count]
        if clear_count == 4 or t_check > 0 and clear_count > 0:
            self.b2b += 1
            if self.b2b > self.stats['max B2B']:
                self.stats['max B2B'] = self.b2b
        elif clear_count > 0:
            self.b2b = -1
        if all(all(c == None for c in r) for r in self.board):
            self.stats['score'] += {1: 800, 2: 1200, 3: 1800, 4: 2000}[clear_count] * (1.6 if self.b2b > 0 else 1) * self.stats['level']
            self.last_clear = f'perfect clear {clear_string}'
            self.stats[self.last_clear] += 1
        elif t_check == 1:
            self.stats['score'] += {0: 100, 1: 200, 2: 400}[clear_count] * (1.5 if self.b2b > 0 else 1) * self.stats['level']
            self.last_clear = f'mini t-spin {clear_string}'
            self.stats[self.last_clear] += 1
        elif t_check == 2:
            self.stats['score'] += {0: 400, 1: 800, 2: 1200, 3: 1600}[clear_count] * (1.5 if self.b2b > 0 else 1) * self.stats['level']
            self.last_clear = f't-spin {clear_string}'
            self.stats[self.last_clear] += 1
        else:
            self.stats['score'] += {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}[clear_count] * (1.5 if self.b2b > 0 else 1) * self.stats['level']
            if clear_count > 0:
                self.last_clear = clear_string
                self.stats[self.last_clear] += 1
        if clear_count > 0:
            self.combo += 1
            self.stats['score'] += 50 * self.combo * self.stats['level']
            if self.combo > self.stats['max combo']:
                self.stats['max combo'] = self.combo
            if self.stats['lines'] >= self.stats['level'] * 10:
                self.stats['level'] += 1 # level is incremented after all scoring
                self.gravity = (0.8 - (self.stats['level'] - 1) * 0.007) ** (self.stats['level'] - 1)
        else:
            self.combo = -1
        self.stats['score'] = int(self.stats['score']) # just in case

    def t_check(self):
        if self.piece == 't' and self.last_action[0] == 'r':
            front = 0
            back  = 0
            for i, (dr, dc) in enumerate(self.corner):
                if self.position[0] + dr < 0 or self.position[1] + dc < 0 or self.position[1] + dc > 9:
                    back += 1
                elif self.board[self.position[0] + dr][self.position[1] + dc] != None:
                    if i == self.rotation or i == (self.rotation + 1) % 4:
                        front += 1
                    else:
                        back += 1
            if front + back >= 3:
                if front == 2 or self.last_action[-1] == '3':
                    return 2 # t-spin
                else:
                    return 1 # t-spin mini
        return 0

    def set_height(self):
        self.height = 0
        while not self.collision(self.height):
            self.height += 1
        self.height -= 1

    def collision(self, lower=0):
        for dr, dc in self.minos[self.piece][self.rotation]:
            r = self.position[0] + dr - lower
            c = self.position[1] + dc
            if r < 0 or c < 0 or c > 9 or self.board[r][c] != None:
                return True
        return False

    def move_press(self, direction, current_time, down=True):
        '''
        (7/16/23) move_press() in intentionally implemented incorrectly. When both directions are
        pressed and the one pressed second is released, the first must wait its DAS period again.
        (On the other hand, when both directions are pressed and the first is released, the second
        continues its movement as it normally would.) In this implementation, when the second is
        released, the first returns to its ARR without waiting for DAS. This change is made to
        reward holding on to the first direction and to raise the skill ceiling. To impliment the
        correct way, in the else block, uncomment the line marked "Correct implementation" and
        comment the line above. 
        '''
        direction_string     = {-1: 'move_left', 1: 'move_right'}[direction]
        direction_string_opp = {-1: 'move_left', 1: 'move_right'}[-direction]
        if down:
            self.stats['keys'] += 1
            # self.move(direction, current_time) # Removed because self.position is not initialized before start()
            self.key_state[direction_string][0] = current_time
            self.key_state[direction_string][1] = current_time - (self.stats['ARR'] - self.stats['DAS']) / 1000
        else:
            if self.key_state[direction_string_opp][0] < self.key_state[direction_string][0]:
                self.key_state[direction_string_opp][1] = current_time - self.stats['ARR'] / 1000
                # self.key_state[direction_string_opp][1] = current_time - (self.stats['ARR'] - self.stats['DAS']) / 1000 # Correct implementation
            self.key_state[direction_string] = [0, 0]

    def move_hold(self, current_time):
        if self.key_state['move_left'][0] or self.key_state['move_right'][0]:
            direction = 'move_left' if self.key_state['move_left'][0] > self.key_state['move_right'][0] else 'move_right'
            step = {'move_left': -1, 'move_right': 1}[direction]
            DAS_timer = current_time - self.key_state[direction][0] # time since pressed
            ARR_timer = current_time - self.key_state[direction][1] # time since last repeat
            if ARR_timer > self.stats['ARR'] / 1000:
                if self.stats['ARR'] <= 0:
                    self.move(8 * step, current_time)
                else:
                    distance = int(ARR_timer // (self.stats['ARR'] / 1000))
                    self.move(distance * step, current_time)
                    self.key_state[direction][1] += distance * self.stats['ARR'] / 1000

    def gravity_drop(self, current_time):
        gravity_timer = current_time - self.gravity_time
        if gravity_timer > self.gravity:
            if self.gravity <= 0:
                self.drop(40)
                self.gravity_time = current_time
            else:
                distance = int(gravity_timer // self.gravity)
                self.drop(distance)
                self.gravity_time += distance * self.gravity

    def piece_lock(self, current_time):
        if self.height == 0:
            if self.lock_time == 0:
                self.lock_time = current_time
            if current_time - self.lock_time > self.lock['time'] or self.lock_count >= self.lock['count']:
                self.place(current_time)
        else:
            self.lock_time = 0

    def finished(self, current_time):
        self.finish = self.lose \
            or (self.stats['mode'] == 'sprint' and self.stats['lines'] >= 40) \
            or (self.stats['mode'] == 'blitz' and current_time - self.stats['time'] >= 120)
        if self.finish:
            self.stats['time'] = current_time - self.stats['time']
            if self.stats['mode'] == 'marathon':
                self.lose = False # in marathon, it's always a finish, not a lose

    def frame_update(self, current_time):
        self.move_hold(current_time)
        self.gravity_drop(current_time)
        self.piece_lock(current_time)
        self.finished(current_time)

    def pause(self, current_time):
        self.stats['time'] = current_time - self.stats['time']
        self.gravity_time = current_time - self.gravity_time
        if self.lock_time:
            self.lock_time = current_time - self.lock_time