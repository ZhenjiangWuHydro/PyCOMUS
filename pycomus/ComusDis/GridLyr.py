from typing import List

from .GridCell import GridCell


class LPFLayers:
    def __init__(self, LyrId: int, LyrType: int, LyrCbd: int, LyrIbs: int, GridCells: List[List[GridCell]]):
        self.LyrId = LyrId
        self.LyrType = LyrType
        self.LyrCbd = LyrCbd
        self.LyrIbs = LyrIbs
        self.GridCells = GridCells


class BCFLayers:
    def __init__(self, LyrId: int, LyrType: int, LyrTrpy: float, LyrIbs: int, GridCells: List[List[GridCell]]):
        self.LyrId = LyrId
        self.LyrType = LyrType
        self.LyrTrpy = LyrTrpy
        self.LyrIbs = LyrIbs
        self.GridCells = GridCells
