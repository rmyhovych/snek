import time
import pygame
import os

from .game import Game

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"


class VisualGame(Game):

    CELL_SIZE = 50

    def __init__(self, width, height):
        super(VisualGame, self).__init__(width, height)
        self.display = None
        self._visual_start()

    def __del__(self):
        self._visual_end()

    def step(self, action: int):
        data = super().step(action=action)
        self._render()
        return data

    def _render(self):
        self.display.fill((10, 10, 10,))
        self._drawCell(self.apple, (200, 20, 20))

        for cell in self.snake.cells:
            self._drawCell(cell, (20, 150, 20))

        time.sleep(0.1)
        pygame.display.update()

    def _visual_start(self):
        pygame.init()
        self.display = pygame.display.set_mode(
            (VisualGame.CELL_SIZE * self.width, VisualGame.CELL_SIZE * self.height,)
        )

    def _visual_end(self):
        pygame.quit()
        self.display = None

    def _drawCell(self, pos, color):
        actual_cell_pos = [VisualGame.CELL_SIZE * p for p in pos]
        cell_rect_dim = (
            actual_cell_pos[0],
            actual_cell_pos[1],
            VisualGame.CELL_SIZE,
            VisualGame.CELL_SIZE,
        )

        pygame.draw.rect(self.display, color, cell_rect_dim)
