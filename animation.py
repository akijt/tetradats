class Animation():

    def __init__(self, interval, current_time):
        self.cycle = 'ostlijtzo'
        self.positions = (((4, 2), (2, 2), (2, 0), (4, 0)),
                          ((5, 2), (3, 2), (1, 0), (3, 0)),
                          ((5, 0), (3, 2), (1, 0), (3, 0)),
                          ((5, 0), (5, 2), (1, 0), (3, 0)),
                          ((4, 0), (6, 0), (0, 0), (2, 0)),
                          ((3, 0), (5, 0), (1, 2), (1, 0)),
                          ((3, 0), (5, 0), (3, 2), (1, 0)),
                          ((3, 0), (5, 0), (3, 2), (1, 2)),
                          ((2, 0), (4, 0), (4, 2), (2, 2)))
        self.colors = {'z': (255, 0,   0),
                       'l': (255, 165, 0),
                       'o': (255, 255, 0),
                       's': (0,   255, 0),
                       'i': (0,   255, 255),
                       'j': (0,   0,   255),
                       't': (160, 32,  240)}
        self.state = 0 # even is static, odd is dynamic
        self.interval = interval # in seconds
        self.time = current_time # time since last change
        self.position = [[self.positions[0][0], self.positions[0][1], self.positions[0][2], self.positions[0][3]], # last position
                  [self.positions[0][0], self.positions[0][1], self.positions[0][2], self.positions[0][3]]] # next position
        self.color = [self.colors[self.cycle[0]], self.colors[self.cycle[0]]]

    def transform(self, current_time):
        step = int((current_time - self.time) // self.interval)
        if step:
            self.time += self.interval * step
            self.state = (self.state + step) % 16
            self.position[0] = [self.positions[(self.state) // 2][i] for i in range(4)]
            self.position[1] = [self.positions[(self.state + 1) // 2][i] for i in range(4)]
            self.color[0] = self.colors[self.cycle[(self.state) // 2]]
            self.color[1] = self.colors[self.cycle[(self.state + 1) // 2]]

    def get(self, current_time):
        self.transform(current_time)
        n = (current_time - self.time) / self.interval
        l = 1 - n
        blocks = []
        for i in range(4):
            x = l * self.position[0][i][0] + n * self.position[1][i][0]
            y = l * self.position[0][i][1] + n * self.position[1][i][1]
            blocks.append([x / 2, y / 2])
        shade = []
        for i in range(3):
            c = l * self.color[0][i] + n * self.color[1][i]
            shade.append(c)
        return blocks, shade