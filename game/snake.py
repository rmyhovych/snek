from collections import deque


class Snake(object):
    def __init__(self, head):
        self.cells = deque([head])

        self.direction = (1, 0)
        self.has_eaten = False

    def get_head(self):
        return self.cells[-1]

    def get_tail(self):
        return self.cells[0]

    def set_direction(self, direction):
        opposite = (-direction[0], -direction[1])
        if opposite != self.direction:
            self.direction = direction

    def move(self):
        new_head = (
            self.cells[-1][0] + self.direction[0],
            self.cells[-1][1] + self.direction[1],
        )

        self.cells.append(new_head)
        if not self.has_eaten:
            self.cells.popleft()
        else:
            self.has_eaten = False
        return new_head

    def is_dead(self, width, height):
        head = self.cells[-1]
        for c in list(self.cells)[:-1]:
            if head == c:
                return True
        return (head[0] < 0 or head[0] >= width) or (head[1] < 0 or head[1] >= height)

    def check_eaten_state(self, apple):
        self.has_eaten = self.cells[-1] == apple
        return self.has_eaten
