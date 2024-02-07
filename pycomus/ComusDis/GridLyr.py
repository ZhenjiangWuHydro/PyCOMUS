from typing import List

from .GridCell import GridCell


class LpfLayers:
    def __init__(self, lyr_id: int, lyr_type: int, lyr_cbd: int, lyr_ibs: int, grid_cells: List[List[GridCell]]):
        self.lyr_id = lyr_id
        self.lyr_type = lyr_type
        self.lyr_cbd = lyr_cbd
        self.lyr_ibs = lyr_ibs
        self.grid_cells = grid_cells


class BcfLayers:
    def __init__(self, lyr_id: int, lyr_type: int, lyr_trpy: float, lyr_ibs: int, grid_cells: List[List[GridCell]]):
        self.lyr_id = lyr_id
        self.lyr_type = lyr_type
        self.lyr_trpy = lyr_trpy
        self.lyr_ibs = lyr_ibs
        self.grid_cells = grid_cells
