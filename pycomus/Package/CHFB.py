# --------------------------------------------------------------
# CHFB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With HFB Package.
# --------------------------------------------------------------
from typing import List, Union, Tuple

import pycomus


class ComusHfb:
    def __init__(self, model: pycomus.ComusModel, hfb_data: List[Tuple[int, int, int, int, int, Union[int, float]]]):
        """
        Initialize the COMUS Model with the Horizontal-Flow Barrier(HFB) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the HFB package will be applied.
        hfb_data:
            List[Tuple] type data, in which the Tuple should contain six parameters: ILYR, IROW1, ICOL1, IROW2, ICOL2, HCDW.
        """
        cmsDis = model._cmsDis
        self.__NumLyr = cmsDis.NumLyr
        self.__NumRow = cmsDis.NumRow
        self.__NumCol = cmsDis.NumCol
        self.__hfb_data: List[Tuple[int, int, int, int, int, Union[int, float]]] = self.__CheckData(hfb_data)
        model._addPackage("HFB", self)

    @property
    def hfb_data(self):
        return self.__hfb_data

    def __CheckData(self, hfb_data: List[Tuple[int, int, int, int, int, Union[int, float]]]) -> List:
        valid_hfb_data = []
        for barrier in hfb_data:
            lay, row1, col1, row2, col2, hydchr = barrier

            # Check layer, row, and column indices
            if not (0 <= lay < self.__NumLyr):
                raise ValueError(f"Layer index {lay} out of bounds for barrier {barrier}")
            if not (0 <= row1 < self.__NumRow and 0 <= row2 < self.__NumRow):
                raise ValueError(f"Row indices {row1} or {row2} out of bounds for barrier {barrier}")
            if not (0 <= col1 < self.__NumCol and 0 <= col2 < self.__NumCol):
                raise ValueError(f"Column indices {col1} or {col2} out of bounds for barrier {barrier}")

            # Check hydraulic characteristic
            if hydchr < 0:
                raise ValueError(f"Hydraulic characteristic {hydchr} must be non-negative for barrier {barrier}")

            # Check if the cells are adjacent
            if (abs(row1 - row2) + abs(col1 - col2)) != 1:
                raise ValueError(f"Barrier cells {row1, col1} and {row2, col2} are not adjacent for barrier {barrier}")

            valid_hfb_data.append(barrier)

        return valid_hfb_data
