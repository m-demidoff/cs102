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
    direction = randint(0, 1)
    if (
        direction == 0
        and coord[0] >= 3
        or direction == 1
        and coord[1] > len(grid[0]) - 4
        and coord[0] >= 3
    ):
        grid[coord[0] - 1][coord[1]] = " "
    elif (
        direction == 1
        and coord[1] <= len(grid[0]) - 4
        or direction == 0
        and coord[0] < 3
        and coord[1] <= len(grid[0]) - 4
    ):
        grid[coord[0]][coord[1] + 1] = " "
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

    for i, cell in enumerate(empty_cells):
        remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        
        for i in range(2):
            exit_wall = randint(0, 3)
            if exit_wall == 0:
                index = randint(0, len(grid) - 1)
                while encircled_exit(grid, (index, 0)):
                    index = randint(0, len(grid) - 1)
                grid[index][0] = "X"
            elif exit_wall == 1:
                index = randint(0, len(grid[0]) - 1)
                while encircled_exit(grid, (0, index)):
                    index = randint(0, len(grid[0]) - 1)
                grid[0][index] = "X"
            elif exit_wall == 2:
                index = randint(0, len(grid) - 1)
                while encircled_exit(grid, (index, len(grid[0]) - 1)):
                    index = randint(0, len(grid) - 1)
                grid[index][len(grid[0]) - 1] = "X"
            else:
                index = randint(0, len(grid[0]) - 1)
                while encircled_exit(grid, (len(grid) - 1, index)):
                    index = randint(0, len(grid[0]) - 1)
                grid[len(grid) - 1][index] = "X"
    else:
        en = input()
        ex = input()
        en = tuple(map(int, en.split()))
        ex = tuple(map(int, ex.split()))
        grid[en[0]][en[1]] = "X"
        grid[ex[0]][ex[1]] = 'X'"""

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    exits = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == k:
                if i - 1 >= 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if i + 1 < len(grid) and grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if j - 1 >= 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if j + 1 < len(grid[i]) and grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1
    return grid


def shortest_path(
    grid, exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    path = [(exit_coord[0], exit_coord[1])]
    k = grid[exit_coord[0]][exit_coord[1]] + 1
    i, j = exit_coord
    while k != 1:
        k -= 1
        if i - 1 >= 0 and grid[i - 1][j] == k - 1:
            grid[i - 1][j] = k + 1
            i -= 1
            path.append((i, j))
            continue
        if i + 1 < len(grid) and grid[i + 1][j] == k - 1:
            grid[i + 1][j] = k + 1
            i += 1
            path.append((i, j))
            continue
        if j - 1 >= 0 and grid[i][j - 1] == k - 1:
            grid[i][j - 1] = k + 1
            j -= 1
            path.append((i, j))
            continue
        if j + 1 < len(grid[i]) and grid[i][j + 1] == k - 1:
            grid[i][j + 1] = k + 1
            j += 1
            path.append((i, j))
            continue
    if len(path) != grid[exit_coord[0]][exit_coord[1]]:
        grid[path[-1][0]][path[-1][1]] = " "
        path.pop(len(path) - 1)
        shortest_path(grid, exit_coord)
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """
    if (
        coord == (0, 0)
        or coord == (0, len(grid[0]) - 1)
        or coord == (len(grid) - 1, 0)
        or coord == (len(grid) - 1, len(grid[0]) - 1)
    ):
        return True
    if (
        coord[0] == 0
        and grid[coord[0]][coord[1] - 1] != " "
        and grid[coord[0]][coord[1] + 1] != " "
        and grid[coord[0] + 1][coord[1]] != " "
    ):
        return True
    if (
        coord[0] == len(grid) - 1
        and grid[coord[0]][coord[1] - 1] != " "
        and grid[coord[0]][coord[1] + 1] != " "
        and grid[coord[0] - 1][coord[1]] != " "
    ):
        return True
    if (
        coord[1] == 0
        and grid[coord[0] - 1][coord[1]] != " "
        and grid[coord[0] + 1][coord[1]] != " "
        and grid[coord[0]][coord[1] + 1] != " "
    ):
        return True
    if (
        coord[1] == len(grid[0]) - 1
        and grid[coord[0] - 1][coord[1]] != " "
        and grid[coord[0] + 1][coord[1]] != " "
        and grid[coord[0]][coord[1] - 1] != " "
    ):
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) == 1:
        return (grid, exits[0])
    if encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
        return (grid, None)
    k = 0
    grid[exits[0][0]][exits[0][1]] = 1
    grid[exits[1][0]][exits[1][1]] = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == " ":
                grid[i][j] = 0
    while grid[exits[1][0]][exits[1][1]] == 0:
        k += 1
        make_step(grid, k)
    return (grid, shortest_path(grid, exits[1]))


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
                if type(grid[i][j]) is int:
                    grid[i][j] = " "
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(5, 5)))
    GRID = bin_tree_maze(51, 77)
    print(pd.DataFrame(GRID))
    MAZE, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(MAZE, PATH)
    print(pd.DataFrame(MAZE))
