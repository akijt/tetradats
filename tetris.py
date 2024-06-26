import random

class Tetris():

    def __init__(self):
        self.minos  = {'i': (((2, 0), (2, 1), (2, 2), (2, 3)),
                             ((0, 2), (1, 2), (2, 2), (3, 2)),
                             ((1, 0), (1, 1), (1, 2), (1, 3)),
                             ((0, 1), (1, 1), (2, 1), (3, 1))),
                       'j': (((2, 0), (2, 1), (2, 2), (3, 0)),
                             ((1, 1), (2, 1), (3, 1), (3, 2)),
                             ((2, 0), (2, 1), (2, 2), (1, 2)),
                             ((1, 1), (2, 1), (3, 1), (1, 0))),
                       'l': (((2, 0), (2, 1), (2, 2), (3, 2)),
                             ((1, 1), (2, 1), (3, 1), (1, 2)),
                             ((2, 0), (2, 1), (2, 2), (1, 0)),
                             ((1, 1), (2, 1), (3, 1), (3, 0))),
                       'o': (((2, 1), (2, 2), (3, 1), (3, 2)),
                             ((2, 1), (2, 2), (3, 1), (3, 2)),
                             ((2, 1), (2, 2), (3, 1), (3, 2)),
                             ((2, 1), (2, 2), (3, 1), (3, 2))),
                       's': (((2, 0), (2, 1), (3, 1), (3, 2)),
                             ((1, 2), (2, 1), (2, 2), (3, 1)),
                             ((1, 0), (1, 1), (2, 1), (2, 2)),
                             ((1, 1), (2, 0), (2, 1), (3, 0))),
                       't': (((2, 1), (2, 0), (3, 1), (2, 2)),
                             ((2, 1), (3, 1), (2, 2), (1, 1)),
                             ((2, 1), (2, 2), (1, 1), (2, 0)),
                             ((2, 1), (1, 1), (2, 0), (3, 1))),
                       'z': (((2, 1), (2, 2), (3, 0), (3, 1)),
                             ((1, 1), (2, 1), (2, 2), (3, 2)),
                             ((1, 1), (1, 2), (2, 0), (2, 1)),
                             ((1, 0), (2, 0), (2, 1), (3, 1)))}
        self.bag = list(self.minos.keys())
        self.kicks  = {'t': (((( 0, 0)),                                        # 0 >> 0
                              (( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)),    # 0 >> 1
                              (( 0, 0), ( 0, 1), ( 1, 1), (-1, 1)),             # 0 >> 2
                              (( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2))),   # 0 >> 3
                             ((( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),    # 1 >> 0
                              (( 0, 0)),                                        # 1 >> 1
                              (( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),    # 1 >> 2
                              (( 0, 0), ( 1, 0), ( 1, 1))),                     # 1 >> 3
                             ((( 0, 0), ( 0,-1), (-1,-1), ( 1,-1)),             # 2 >> 0
                              (( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)),    # 2 >> 1
                              (( 0, 0)),                                        # 2 >> 2
                              (( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2))),   # 2 >> 3
                             ((( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)),    # 3 >> 0
                              (( 0, 0), (-1, 0), (-1, 1)),                      # 3 >> 1
                              (( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)),    # 3 >> 2
                              (( 0, 0)))),                                      # 3 >> 3
                       'i': (((( 0, 0)),                                        # 0 >> 0
                              (( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),    # 0 >> 1
                              (( 0, 0), ( 0, 1)),                               # 0 >> 2
                              (( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1))),   # 0 >> 3
                             ((( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),    # 1 >> 0
                              (( 0, 0)),                                        # 1 >> 1
                              (( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1)),    # 1 >> 2
                              (( 0, 0), ( 1, 0))),                              # 1 >> 3
                             ((( 0, 0), ( 0,-1)),                               # 2 >> 0
                              (( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),    # 2 >> 1
                              (( 0, 0)),                                        # 2 >> 2
                              (( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2))),   # 2 >> 3
                             ((( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),    # 3 >> 0
                              (( 0, 0), (-1, 0)),                               # 3 >> 1
                              (( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),    # 3 >> 2
                              (( 0, 0))))}                                      # 3 >> 3
        self.finesse = {'o': ((1, 2, 2, 1, 0, 1, 2, 2, 1),
                              (1, 2, 2, 1, 0, 1, 2, 2, 1),
                              (1, 2, 2, 1, 0, 1, 2, 2, 1),
                              (1, 2, 2, 1, 0, 1, 2, 2, 1)),
                        'i': ((1, 2, 1, 0, 1, 2, 1),
                              (2, 2, 2, 2, 1, 1, 2, 2, 2, 2),
                              (1, 2, 1, 0, 1, 2, 1),
                              (2, 2, 2, 2, 1, 1, 2, 2, 2, 2)),
                        's': ((1, 2, 1, 0, 1, 2, 2, 1),
                              (2, 2, 2, 1, 1, 2, 3, 2, 2),
                              (1, 2, 1, 0, 1, 2, 2, 1),
                              (2, 2, 2, 1, 1, 2, 3, 2, 2)),
                        'z': ((1, 2, 1, 0, 1, 2, 2, 1),
                              (2, 2, 2, 1, 1, 2, 3, 2, 2),
                              (1, 2, 1, 0, 1, 2, 2, 1),
                              (2, 2, 2, 1, 1, 2, 3, 2, 2)),
                        't': ((1, 2, 1, 0, 1, 2, 2, 1),
                              (2, 2, 3, 2, 1, 2, 3, 3, 2),
                              (3, 4, 3, 2, 3, 4, 4, 3),
                              (2, 3, 2, 1, 2, 3, 3, 2, 2)),
                        'j': ((1, 2, 1, 0, 1, 2, 2, 1),
                              (2, 2, 3, 2, 1, 2, 3, 3, 2),
                              (3, 4, 3, 2, 3, 4, 4, 3),
                              (2, 3, 2, 1, 2, 3, 3, 2, 2)),
                        'l': ((1, 2, 1, 0, 1, 2, 2, 1),
                              (2, 2, 3, 2, 1, 2, 3, 3, 2),
                              (3, 4, 3, 2, 3, 4, 4, 3),
                              (2, 3, 2, 1, 2, 3, 3, 2, 2))}
        self.orientations = {'t': 4, 'i': 2, 'o': 1, 'j': 4, 'l': 4, 's': 2, 'z': 2}
        self.key_state = {'soft_drop': 0, 'move_left': 0, 'move_right': 0}
        self.lock = {'time': .5, 'count': 15}
        self.stat_names = ['mode', 'time', 'score', 'pieces', 'lines', 'level', # Top row is REQUIRED
                           'DAS', 'ARR', 'SDF', 'keys', 'holds', # 'DAS', 'ARR', 'SDF' are REQUIRED
                           'single', 'double', 'triple', 'tetris',
                           'mini t-spin null', 'mini t-spin single', 'mini t-spin double',
                           't-spin null', 't-spin single', 't-spin double', 't-spin triple',
                           'perfect clear single', 'perfect clear double', 'perfect clear triple',
                           'perfect clear tetris', 'max B2B', 'max combo', 'finesse']

    def reset(self, mode, level, handling): # TODO: clean and add key state check
        '''
        (12/10/23) A possibly better way to implement classic mode and other variations would be to
        only make changes in the __init__() and reset() functions. In essence, variables like
        hold_allowed, r180_allowed, hard_drop_allowed can be set to False, and self.kicks can
        remove disallowed kicks (most). However, things get complicated for the queue extention and
        piece lock functionality. Queue extention would require storing a function. For piece lock,
        self.lock['count'] would be set to 0, but that also requires a new condition for its
        associated lock condition in piece_lock(). The finish condition also requires a fix.
        '''
        self.board     = [[None for c in range(10)] for r in range(40)]
        if mode == 'classic':
            self.queue = random.choices(self.bag, k=1)
        else:
            self.queue = random.sample(self.bag, k=7)
        self.held      = None
        self.hold_used = False
        self.b2b       = -1
        self.combo     = -1
        self.fin_keys  = 0

        self.last_clear  = ''
        self.stats       = {x: 0 for x in self.stat_names}

        for k, v in handling.items():
            self.stats[k] = v
        self.stats['mode']  = mode # 'marathon', 'sprint', 'blitz', or 'classic'
        self.stats['level'] = level # This needs to be in reset (countdown screen should show correct level)
        self.gravity        = self.gravity = (0.8 - (self.stats['level'] - 1) * 0.007) ** (self.stats['level'] - 1)
        self.lose           = False
        self.finish         = False

        self.ghost    = mode != 'classic'
        self.next_num = 1 if mode == 'classic' or mode == 'finesse' else 3

        if mode == 'classic':
            self.stats['DAS'] = 300
            self.stats['ARR'] = 100
            self.stats['SDF'] = 33
        elif mode == 'cheese':
            self.add_cheese(5)

        self.move_time = 0

    def start(self, current_time):
        self.stats['keys'] = 0
        self.stats['time'] = current_time
        self.new_piece(self.queue.pop(0), current_time)

    def new_piece(self, piece, current_time):
        self.piece    = piece
        self.position = [18, 3]
        self.rotation = 0

        if self.collision():
            self.lose = True
            return
        if len(self.queue) < self.next_num:
            if self.stats['mode'] == 'classic':
                self.queue.extend(random.choices(self.bag, k=1))
            else:
                self.queue.extend(random.sample(self.bag, k=7))

        self.gravity_time = current_time - self.gravity # when the last drop was
        self.lock_time    = 0 # when lock_time started/reset
        self.lock_count   = 0 # number of moves/rotations since touchdown
        self.lock_lowest  = 18 # the lowest row the piece has been on
        self.set_height()
        self.set_lock(current_time)
        self.last_action  = ''
        self.fin_keys = 0
        if self.stats['mode'] == 'finesse':
            self.set_target()
    
    def set_target(self):
        self.target = dict()
        self.target['rotation'] = random.randint(0, 3)
        self.target['location'] = random.randint(0, len(self.finesse[self.piece][self.rotation]) - 1)
        self.target['position'] = [-min(dr for dr, _ in self.minos[self.piece][self.target['rotation']]), self.target['location'] - min(dc for _, dc in self.minos[self.piece][self.target['rotation']])]

    def hold(self, current_time):
        if self.stats['mode'] not in ['classic', 'finesse']:
            self.stats['keys'] += 1
            if not self.hold_used:
                self.stats['holds'] += 1
                self.hold_used = True
                if self.held == None:
                    self.held = self.piece
                    self.new_piece(self.queue.pop(0), current_time)
                else:
                    temp = self.held
                    self.held = self.piece
                    self.new_piece(temp, current_time)

    def move(self, distance, current_time):
        step = 1 if distance > 0 else -1
        for i in range(abs(distance)):
            self.position[1] += step
            if self.collision():
                self.position[1] -= step
                if i == 0:
                    return
                i -= 1
                break
        self.set_height()
        self.set_lock(current_time, i + 1)
        self.last_action = 'move'

    def rotate(self, turns, current_time):
        if self.stats['mode'] != 'classic' or turns != 2:
            self.stats['keys'] += 1
            self.fin_keys += 1 if turns % 2 == 1 else 2
            orig_position = self.position
            orig_rotation = self.rotation
            self.rotation = (self.rotation + turns) % 4
            for i, (x, y) in enumerate(self.kicks['i' if self.piece == 'i' else 't'][orig_rotation][self.rotation]):
                self.position = [orig_position[0] + y, orig_position[1] + x]
                if not self.collision():
                    self.set_height()
                    self.set_lock(current_time, 1 if turns % 2 == 1 else 2)
                    self.last_action = f'rotate{i}'
                    return
                if self.stats['mode'] == 'classic':
                    break # If classic mode, don't check other kicks
            self.position = orig_position
            self.rotation = orig_rotation

    def drop(self, distance, current_time):
        '''
        (7/17/23) The lowest row reached by a piece can be interpreted in two different ways. The
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
        if distance:
            self.position[0] -= distance
            self.set_height()
            self.set_lock(current_time)
            if self.position[0] < self.lock_lowest:
                self.lock_lowest = self.position[0]
                self.lock_count  = 0
            self.stats['score'] += distance * self.key_state['soft_drop']
            self.last_action = 'drop'

    def soft_drop(self, current_time):
        '''
        (9/2/23) When self.stats['SDF'] > 1, both self.gravity and self.gravity_time must be
        updated. Though unintuitive, self.gravity_time is updated because otherwise, the piece will
        drop more rows than intended in most cases (see gravity_drop() implementation).
        Because the piece should drop on the same frame soft_drop() is called, self.gravity_time is
        set to current_time - self.gravity. However, if soft_drop() is called on the same frame the
        piece would have dropped anyways, there would be a difference of a couple milliseconds in
        self.gravity_time after gravity_drop() depending on whether the regular drop or soft drop
        was interpreted as the cause of the drop. By choosing to assign the cause of these drops to
        soft drop whenever the soft drop key is pressed, the consistency of soft drops is
        preserved.
        (9/24/23) Soft drops can be treated three different ways for finesse. It can count as a
        move, it can be an automatic pass, or it can be an automatic fail (if not tucked/spun). The
        first only makes sense when SDF is infinity; otherwise, the soft drop will take unnecessary
        time. The second is the easy way out; the situation is deemed uncalculatable, so it is an
        automatic pass. The third is the strictest; it considers all (non tuck/spin) soft drops as
        incorrect, even if the number of key presses is within finesse limits. Of the three, the
        first was chosen. The second is way too forgiving. The third punishes creative movements.
        Though the first doesn't make sense when SDF is not infinity, the players at this level
        probably don't care too much about finesse.
        '''
        self.stats['keys'] += 1
        self.fin_keys += 1
        self.key_state['soft_drop'] = 1
        if self.stats['SDF'] <= 1:
            self.gravity = 0
        else:
            if self.stats['mode'] != 'classic':
                self.gravity /= self.stats['SDF']
            elif self.gravity > self.stats['SDF'] / 1000:
                self.gravity = self.stats['SDF'] / 1000
            self.gravity_time = current_time - self.gravity


    def unsoft_drop(self):
        self.key_state['soft_drop'] = 0
        self.gravity = (0.8 - (self.stats['level'] - 1) * 0.007) ** (self.stats['level'] - 1)

    def hard_drop(self, current_time):
        '''
        (7/16/23) It is an option to treat hard_drop() like soft_drop(). In hard_drop(),
        self.key_state['hard_drop'] will be set to 1 (that's it). In gravity_drop,
        self.key_state['hard_drop'] will be an additional condition for
        self.drop(40, current_time). After the drop() call, self.key_state['hard_drop'] is reverted
        back to 0. In drop(), the addition to self.stats['score'] will need to multiply distance by
        2 if self.key_state['hard_drop'].
        '''
        if self.stats['mode'] != 'classic':
            self.stats['keys'] += 1
            if self.height:
                self.position[0] -= self.height
                self.stats['score'] += self.height * 2
                self.last_action = 'drop'
            self.place(current_time)

    def place(self, current_time):
        if all([self.position[0] + dr >= 20 for dr, _ in self.minos[self.piece][self.rotation]]):
            self.lose = True # if entire mino is above 20, game is lost
            return

        self.stats['pieces'] += 1
        self.f_check()
        if self.stats['mode'] != 'finesse':
            for dr, dc in self.minos[self.piece][self.rotation]:
                self.board[self.position[0] + dr][self.position[1] + dc] = self.piece
            self.clear()
        self.new_piece(self.queue.pop(0), current_time)
        self.hold_used = False

    def clear(self):
        t_score = self.t_check()
        rows = 0
        cheese_cleared = 0
        for r in range(40):
            if None in self.board[r]:
                self.board[rows] = self.board[r]
                rows += 1
            elif r < 5 and self.stats['mode'] == 'cheese':
                cheese_cleared += 1
        clear_count = 40 - rows
        while rows < 40:
            self.board[rows] = [None for _ in range(10)]
            rows += 1
        self.add_cheese(cheese_cleared)
        clear_string = {0: 'null', 1: 'single', 2: 'double', 3: 'triple', 4: 'tetris'}[clear_count]
        if clear_count == 4 or t_score >= 10 and clear_count > 0:
            self.b2b += 1
            if self.b2b > self.stats['max B2B']:
                self.stats['max B2B'] = self.b2b
        elif clear_count > 0:
            self.b2b = -1
        if all(all(c == None for c in r) for r in self.board):
            self.stats['score'] += {1: 800, 2: 1200, 3: 1800, 4: 2000}[clear_count] * (1.6 if self.b2b > 0 else 1) * self.stats['level']
            self.last_clear = f'perfect clear {clear_string}'
        elif t_score > 10:
            self.stats['score'] += {0: 400, 1: 800, 2: 1200, 3: 1600}[clear_count] * (1.5 if self.b2b > 0 else 1) * self.stats['level']
            self.last_clear = f't-spin {clear_string}'
        elif t_score == 10:
            self.stats['score'] += {0: 100, 1: 200, 2: 400}[clear_count] * (1.5 if self.b2b > 0 else 1) * self.stats['level']
            self.last_clear = f'mini t-spin {clear_string}'
        elif clear_count > 0:
            self.stats['score'] += {1: 100, 2: 300, 3: 500, 4: 800}[clear_count] * (1.5 if self.b2b > 0 else 1) * self.stats['level']
            self.last_clear = clear_string
        if clear_count > 0 or t_score >= 10:
            self.stats[self.last_clear] += 1
        if clear_count > 0:
            self.combo += 1
            self.stats['score'] += 50 * self.combo * self.stats['level']
            if self.combo > self.stats['max combo']:
                self.stats['max combo'] = self.combo
            self.stats['lines'] += clear_count
            if self.stats['lines'] >= self.stats['level'] * 10:
                self.stats['level'] += 1 # level is incremented after all scoring
                self.gravity = (0.8 - (self.stats['level'] - 1) * 0.007) ** (self.stats['level'] - 1)
        else:
            self.combo = -1
        self.stats['score'] = int(self.stats['score']) # just in case

    def t_check(self):
        t_score = 0
        if self.piece == 't' and self.last_action[0] == 'r':
            for i, (dr, dc) in enumerate(((3, 0), (3, 2), (1, 2), (1, 0))):
                r = self.position[0] + dr
                c = self.position[1] + dc
                if r < 0 or c < 0 or c > 9 or self.board[r][c] != None:
                    if i == self.rotation or i == (self.rotation + 1) % 4:
                        t_score += 4
                    else:
                        t_score += 3
            t_score += self.last_action[-1] == '4'
        return t_score
    
    def f_check(self):
        col = self.position[1] + min([dc for _, dc in self.minos[self.piece][self.rotation]])
        if self.stats['mode'] == 'finesse':
            if self.rotation % self.orientations[self.piece] != self.target['rotation'] % self.orientations[self.piece] or col != self.target['location']:
                self.stats['pieces'] -= 1
                self.lose = True
                return
        for dr, dc in self.minos[self.piece][self.rotation]:
            c = self.position[1] + dc
            if any([self.board[r][c] for r in range(self.position[0] + dr + 1, 22)]):
                self.stats['finesse'] += 1 # automatic finesse pass if there are any minos above the piece
                return
        if self.fin_keys <= self.finesse[self.piece][self.rotation][col]:
            self.stats['finesse'] += 1
        elif self.stats['mode'] == 'finesse':
            self.stats['pieces'] -= 1
            self.lose = True

    def add_cheese(self, n):
        for r in range(n):
            if any([x != None for x in self.board[r]]):
                self.lose = True
                return
        for r in range(39, n - 1, -1):
            self.board[r] = self.board[r - n]
        for r in range(n - 1, -1, -1):
            row = ['g' for _ in range(10)]
            row[random.randint(0, 9)] = None
            self.board[r] = row

    def set_height(self):
        self.height = 1
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

    def move_press(self, direction1, direction2, current_time):
        self.stats['keys'] += 1
        self.fin_keys += 1
        # self.move(direction, current_time) # Removed because self.position is not initialized before start()
        self.key_state[direction1] = self.key_state[direction2] + 1
        self.move_time = current_time - (self.stats['ARR'] - self.stats['DAS']) / 1000

    def move_unpress(self, direction1, direction2, current_time):
        '''
        (7/16/23) move_unpress() in intentionally implemented incorrectly. When both directions are
        pressed and the one pressed second is released, the first must wait its DAS period again.
        (On the other hand, when both directions are pressed and the first is released, the second
        continues its movement as it normally would.) In this implementation, when the second is
        released, the first returns to its ARR without waiting for DAS. This change is made to
        reward holding on to the first direction and to raise the skill ceiling. To implement the
        correct way, in the else block, uncomment the line marked "Correct implementation" and
        comment the line above.
        (5/10/24) Though the implementation presented above is interesting and still possible, it
        would require more complex code to get it right. With the way it was implemented, it was
        possible to perform a "DAS skip". When pressing and holding a direction key, the DAS period
        could be skipped by quickly pressing and releasing the other direction key. This only
        affected gameplay with high DAS, but is incorrect implementation nonetheless. Thus, the
        correct implementation is now uncommented.
        '''
        self.key_state[direction1] = 0
        if self.key_state[direction2] == 0:
            self.move_time = 0
        elif self.key_state[direction2] == 1:
            # self.move_time = current_time - self.stats['ARR'] / 1000 # Incorrect implementation
            self.move_time = current_time - (self.stats['ARR'] - self.stats['DAS']) / 1000 # Correct implementation
        else:
            self.key_state[direction2] = 1

    def move_hold(self, current_time):
        if self.move_time:
            step = self.key_state['move_right'] - self.key_state['move_left']
            move_timer = current_time - self.move_time
            if move_timer > (self.stats['ARR'] / 1000):
                if self.stats['ARR'] <= 0:
                    self.move_time = current_time
                    self.move(9 * step, current_time)
                else:
                    distance = int(move_timer // (self.stats['ARR'] / 1000))
                    self.move_time += distance * (self.stats['ARR'] / 1000)
                    self.move(distance * step, current_time)

    def gravity_drop(self, current_time):
        gravity_timer = current_time - self.gravity_time
        if gravity_timer > self.gravity:
            if self.gravity == 0:
                self.gravity_time = current_time
                self.drop(40, current_time)
            else:
                distance = int(gravity_timer // self.gravity)
                self.gravity_time += distance * self.gravity
                self.drop(distance, current_time)

    def set_lock(self, current_time, actions=0):
        if actions and self.stats['mode'] != 'classic':
            if self.lock_time > 0 or self.height == 0 or self.lock_count > 0: # move that causes height == 0 counts in lock_count
                self.lock_count += actions
            if self.lock_time > 0:
                self.lock_time = current_time
        if self.height == 0 and self.lock_time == 0:
            self.lock_time = current_time
        elif self.height > 0:
            self.lock_time = 0

    def piece_lock(self, current_time):
        if self.lock_time:
            lock_timer = current_time - self.lock_time
            if lock_timer > self.lock['time'] or self.lock_count >= self.lock['count']:
                self.place(current_time)

    def finished(self, current_time):
        self.finish = self.lose \
            or (self.stats['mode'] == 'sprint' and self.stats['lines'] >= 40) \
            or (self.stats['mode'] == 'blitz' and current_time - self.stats['time'] >= 120)
        if self.finish:
            self.stats['time'] = current_time - self.stats['time']
            if self.stats['mode'] not in ['sprint', 'blitz']:
                self.lose = False

    def frame_update(self, current_time):
        self.move_hold(current_time)
        self.gravity_drop(current_time)
        self.piece_lock(current_time)
        self.finished(current_time)

    def pause(self, current_time): # TODO: add key state check
        self.stats['time'] = current_time - self.stats['time']
        self.gravity_time = current_time - self.gravity_time
        # if self.move_time:
        #     self.move_time = current_time - self.move_time
        if self.lock_time:
            self.lock_time = current_time - self.lock_time
        self.unsoft_drop()
        self.move_unpress('move_left', 'move_right', current_time)
        self.move_unpress('move_right', 'move_left', current_time)