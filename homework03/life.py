import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0] * self.cols] * self.rows
        if randomize:
            grid = [[random.choice([0, 1]) for i in row] for row in grid]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []
        x, y = cell[0], cell[1]
        if x - 1 >= 0:
            if y - 1 >= 0:
                neighbours.append(self.curr_generation[x - 1][y - 1])
            neighbours.append(self.curr_generation[x - 1][y])
            if self.cols > y + 1:
                neighbours.append(self.curr_generation[x - 1][y + 1])
        if 0 <= y - 1:
            neighbours.append(self.curr_generation[x][y - 1])
        if self.cols > y + 1:
            neighbours.append(self.curr_generation[x][y + 1])
        if self.rows > x + 1:
            if 0 <= y - 1:
                neighbours.append(self.curr_generation[x + 1][y - 1])
            neighbours.append(self.curr_generation[x + 1][y])
            if self.cols > y + 1:
                neighbours.append(self.curr_generation[x + 1][y + 1])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        upd_grid = []
        for y, row in enumerate(self.curr_generation):
            new_row = []
            for x, cell in enumerate(row):
                neighbours = self.get_neighbours((y, x))
                live_neighbours = neighbours.count(1)
                if cell and (live_neighbours < 2 or live_neighbours > 3):
                    new_row.append(0)
                elif not cell and live_neighbours == 3:
                    new_row.append(1)
                else:
                    new_row.append(cell)
            upd_grid.append(new_row)
        return upd_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded and self.is_changing:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as file:
            line = file.readlines()
            game = GameOfLife((len(line), len(line[0].strip())), False)
            for i in range(len(line)):
                line[i].strip()
                for j in range(len(line[0].strip())):
                    game.curr_generation[i][j] = int(line[i][j])
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as file:
            for _ in self.curr_generation:
                for t in _:
                    file.write(str(t) + "\n")
                file.close()
