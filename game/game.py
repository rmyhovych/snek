import aitools
import torch
import random

from .snake import Snake


class Game(aitools.rl.IEnvironment):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.steps_before_eat = 0

        self.DIRECTIONS = (
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
        )
        self.reset()

    def step(self, action: int):
        self.snake.set_direction(self.DIRECTIONS[action])
        self.snake.move()
        self.steps_before_eat += 1

        reward = 0.0
        if self.snake.check_eaten_state(self.apple):
            self.apple = self._generate_apple()
            self.steps_before_eat = 0
            reward = 1.0

        dead = self.snake.is_dead(self.width, self.height) or self.steps_before_eat >= (
            self.width * self.height / 2
        )
        if dead:
            reward = -1.0
        return (self._state(), torch.tensor([reward]), dead)

    def reset(self):
        self.snake = Snake((int(self.width / 2), int(self.height / 2)))
        self.apple = self._generate_apple()
        self.steps_before_eat = 0

        return self._state()

    def _render(self):
        raise NotImplementedError

    def get_size_obs(self):
        return self._state().size()[0]

    def get_size_action(self):
        return len(self.DIRECTIONS)

    def _state(self):
        state = [0 for _ in range(3 * self.height * self.width)]

        self._set_state_cell(state, self.apple, 0)

        head = self.snake.cells[-1]
        for c in self.snake.cells:
            if c != head:
                self._set_state_cell(state, c, 1)
        self._set_state_cell(state, head, 2)

        return torch.tensor(state, dtype=torch.float)

    def _set_state_cell(self, state, pos, offset):
        p = 3 * (pos[1] * self.width + pos[0]) + offset
        if p >= 0 and p < len(state):
            state[p] = 1

    def _generate_apple(self):
        all_possibilities = set(
            [(x, y) for x in range(self.width) for y in range(self.height)]
        )
        for cell in self.snake.cells:
            all_possibilities.remove(cell)

        return random.choice(list(all_possibilities))
