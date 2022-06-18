class LifeGame(object):
    """
    Class for Game life
    """
    EMPTY = 0
    ROCK = 1
    FISH = 2
    SHRIMP = 3

    def __init__(self, start_board: list[list[int]]):
        """
        Ocean is a rectangle of cells, list of equal length lists
        values in cells mean:
        0 - empty cell
        1 - rock
        2 - fish
        3 - shrimp
        """
        self._board = start_board
        self._rows = len(start_board)
        self._columns = len(start_board[0])

    def _get_neighbours_ids(self, i: int, j: int) -> list[tuple[int, int]]:
        """
        returns indexes of all neighbours
        """
        return [(nb_i, nb_j)
                for nb_i in range(i - 1, i + 2)
                for nb_j in range(j - 1, j + 2)
                if 0 <= nb_i < self._rows and 0 <= nb_j < self._columns and (nb_i, nb_j) != (i, j)
                ]

    def _get_neighbours_number(self, i: int, j: int, value: int) -> int:
        """
        returns number of neighbours with this value
        """
        return sum(self._board[nb_i][nb_j] == value for nb_i, nb_j in self._get_neighbours_ids(i, j))

    def _get_next_value(self, i: int, j: int) -> int:
        """
        returns next value for cell
        """
        new_value = self._board[i][j]
        if new_value in (self.FISH, self.SHRIMP):
            if self._get_neighbours_number(i, j, new_value) not in (2, 3):
                new_value = self.EMPTY
        elif new_value == self.EMPTY:
            if self._get_neighbours_number(i, j, self.FISH) == 3:
                new_value = self.FISH
            elif self._get_neighbours_number(i, j, self.SHRIMP) == 3:
                new_value = self.SHRIMP
        return new_value

    def get_next_generation(self) -> list[list[int]]:
        """
        returns next generation board
        """
        self._board = [[self._get_next_value(i, j) for j in range(self._columns)] for i in range(self._rows)]
        return self._board
