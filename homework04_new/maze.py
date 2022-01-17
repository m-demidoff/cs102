from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    way = randint(0, 1)  # направление
    x, y = coord
    if way:
        if x + 1 != len(grid[0]) - 1:
            grid[y][x + 1] = " "
        elif y != 1:
            grid[y - 1][x] = " "
    else:
        if y != 1:
            grid[y - 1][x] = " "
        elif y + 1 != len(grid[0]) - 1:
            grid[y][x + 1] = " "

    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    exits_coords = []  # нач. значение
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                exits_coords.append((i, j))

    return exits_coords


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    for x, _ in enumerate(rows):  # type: ignore
        for y in range(cols):
            if grid[x][y] == k:
                if x - 1 >= 0 and grid[x - 1][y] == 0:
                    grid[x - 1][y] = k + 1
                if x + 1 < len(grid) and grid[x + 1][y] == 0:
                    grid[x + 1][y] = k + 1
                if y - 1 >= 0 and grid[x][y - 1] == 0:
                    grid[x][y - 1] = k + 1
                if y + 1 < len(grid[x]) and grid[x][y + 1] == 0:
                    grid[x][y + 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    path_way = [exit_coord]
    x, y = exit_coord[0], exit_coord[1]
    shortest = grid[x][y]
    k = int(shortest)
    while k > 1:
        if x != len(grid) - 1 and grid[x + 1][y] == k - 1:
            x += 1
            path_way.append((x, y))
        if y != len(grid[0]) - 1 and grid[x][y + 1] == k - 1:
            y += 1
            path_way.append((x, y))
        if x != 0 and grid[x - 1][y] == k - 1:
            x -= 1
            path_way.append((x, y))
        if y != 0 and grid[x][y - 1] == k - 1:
            y -= 1
            path_way.append((x, y))
        k -= 1
    return path_way


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """
    x = coord[0]
    y = coord[1]
    if x == 0:
        if grid[x + 1][y] == "■":
            return True
    elif x == len(grid) - 1:
        if grid[x - 1][y] == "■":
            return True
    elif y == 0:
        if grid[x][y + 1] == "■":
            return True
    elif y == len(grid[0]) - 1:
        if grid[x][y - 1] == "■":
            return True
    return False


def solve_maze(grid):
    """
    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) != 1:
        start, out = exits

    for i in exits:
        if encircled_exit(grid, i):
            return None
        else:
            grid[start[0]][start[1]] = 1
            grid[out[0]][out[1]] = 0
            k = 1

            for x in range(len(grid) - 1):
                for y in range(len(grid[y]) - 1):  # type: ignore
                    if grid[x][y] == " ":
                        grid[x][y] = 0

            while grid[out[0]][out[1]] == 0:
                grid = make_step(grid, k)
                k += 1

    return grid, out


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))