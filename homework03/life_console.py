import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.box("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                char = "*" if cell == 1 else " "
                screen.addch(y + 1, x + 1, char)

    def run(self) -> None:
        screen = curses.initscr()
        game_running = True
        while game_running:
            self.draw_grid(screen)
            self.draw_borders(screen)
            self.life.step()
            screen.refresh()
            curses.napms(500)
        curses.endwin()
