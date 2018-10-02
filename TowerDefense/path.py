from cell import *


class Path:
    def __init__(self, grid_size):
        self._path = []
        self._grid_size = grid_size

    def __len__(self):
        return len(self._path)

    def add_cell(self, cell):
        assert isinstance(cell, Cell)
        self.assert_valid_cell(cell)
        self._path.append(cell)

    def assert_valid_cell(self, cell):
        if not self._path:
            self.assert_edge_adjacency(cell)
        else:
            self.assert_cell_adjacency(cell)

    def assert_edge_adjacency(self, cell):
        assert cell.get_x() == 0 or cell.get_x() == self._grid_size - 1 or \
               cell.get_y() == 0 or cell.get_y() == self._grid_size - 1

    def assert_cell_adjacency(self, cell):
        previous_cell = self._path[-1]
        assert cell.get_x() == previous_cell.get_x() or cell.get_y() == previous_cell.get_y()
        assert abs(cell.get_x() - previous_cell.get_x()) <= 1 and \
               abs(cell.get_y() - previous_cell.get_y()) <= 1

    def get_cell(self, index):
        return self._path[index]


if __name__ == '__main__':
    p = Path(4)
    cells = [Cell(None, 0, 3, 5), Cell(None, 1, 3, 5), Cell(None, 2, 3, 5),
             Cell(None, 3, 3, 5)]
    for c in cells:
        p.add_cell(c)
    assert len(p) == 4

    # Test starting cell not on an edge
    p = Path(4)
    try:
        p.add_cell(Cell(None, 2, 2, 5))
        assert False
    except AssertionError:
        pass

    # Test adding diagonally-adjacent cell -- not allowed.
    p = Path(4)
    p.add_cell(Cell(None, 3, 3, 5))
    try:
        p.add_cell(Cell(None, 2, 2, 5))
        assert False
    except AssertionError:
        pass
    
    # Test adding totally non-adjacent cell -- not allowed.
    p = Path(4)
    p.add_cell(Cell(None, 3, 3, 5))
    try:
        p.add_cell(Cell(None, 1, 3, 5))
        assert False
    except AssertionError:
        pass

    print("All unit tests passed.")
