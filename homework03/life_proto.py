import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [
                [random.choice([0, 1]) for i in range(self.cell_width)]
                for j in range(self.cell_height)
            ]
        else:
            return [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(1, self.height, self.cell_size):
            for x in range(1, self.width, self.cell_size):
                if self.grid[y // self.cell_size][x // self.cell_size] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x, y, self.cell_size - 1, self.cell_size - 1),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (x, y, self.cell_size - 1, self.cell_size - 1),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        x = cell[0] // self.cell_size
        y = cell[1] // self.cell_size
        if x - 1 >= 0:
            if y - 1 >= 0:
                neighbours.append(self.grid[x - 1][y - 1])
            neighbours.append(self.grid[x - 1][y])
            if self.cell_width > y + 1:
                neighbours.append(self.grid[x - 1][y + 1])
        if y - 1 >= 0:
            neighbours.append(self.grid[x][y - 1])
        if self.cell_width > y + 1:
            neighbours.append(self.grid[x][y + 1])
        if self.cell_height > x + 1:
            if y - 1 >= 0:
                neighbours.append(self.grid[x + 1][y - 1])
            neighbours.append(self.grid[x + 1][y])
            if self.cell_width > y + 1:
                neighbours.append(self.grid[x + 1][y + 1])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        upd_grid = []
        for y in range(0, self.height, self.cell_size):
            row = []
            for x in range(0, self.width, self.cell_size):
                if sum(self.get_neighbours((y, x))) == 3 or (
                    self.grid[y // self.cell_size][x // self.cell_size] == 1
                    and sum(self.get_neighbours((y, x))) == 2
                ):
                    row.append(1)
                else:
                    row.append(0)
            upd_grid.append(row)
        self.grid = upd_grid
        return self.grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
