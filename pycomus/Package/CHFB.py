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

        Returns:
        --------
        instance: pycomus.ComusHfb
           COMUS Horizontal-Flow Barrier(HFB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> data = []
        >>> for i in range(36):
        >>>     data.append((i, 0, 15, 0, 16, 1e-6))
        >>> hfbPackage = pycomus.ComusHfb(model=model, hfb_data=data)
        """
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self.hfb_data: List[Tuple[int, int, int, int, int, Union[int, float]]] = self.__CheckData(hfb_data)
        model.package["HFB"] = self

    def __CheckData(self, hfb_data: List[Tuple[int, int, int, int, int, Union[int, float]]]) -> List:
        valid_hfb_data = []
        for barrier in hfb_data:

            lay, row1, col1, row2, col2, hcdw = barrier

            # Check layer, row, and column indices
            if not (0 <= lay < self._num_lyr):
                raise ValueError(f"Layer index {lay} out of bounds for barrier {barrier}")
            if not (0 <= row1 < self._num_row and 0 <= row2 < self._num_row):
                raise ValueError(f"Row indices {row1} or {row2} out of bounds for barrier {barrier}")
            if not (0 <= col1 < self._num_col and 0 <= col2 < self._num_col):
                raise ValueError(f"Column indices {col1} or {col2} out of bounds for barrier {barrier}")

            # Check hydraulic characteristic
            if hcdw < 0:
                raise ValueError(f"Hydraulic characteristic {hcdw} must be non-negative for barrier {barrier}")

            # Check if the cells are adjacent
            if (abs(row1 - row2) + abs(col1 - col2)) != 1:
                raise ValueError(f"Barrier cells {row1, col1} and {row2, col2} are not adjacent for barrier {barrier}")

            valid_hfb_data.append(barrier)

        return valid_hfb_data

    @classmethod
    def load(cls, model, hfb_params_file: str):
        """
        Load parameters from a HFB.in file and create a ComusHfb instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        hfb_params_file: str
            Grid HFB Params File Path(HFB.in).

        Returns:
        --------
        instance: pycomus.ComusHfb
            COMUS Horizontal-Flow Barrier(HFB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> hfbPackage = pycomus.ComusHfb.load(model, "./InputFiles/HFB.in")
        """
        with open(hfb_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 6:
            raise ValueError("The Horizontal-Flow Barrier(HFB) Period Attribute file header should have 6 fields.")
        data = lines[1].strip().split()
        if len(data) != 6:
            raise ValueError("The Horizontal-Flow Barrier(HFB) Period Attribute file data line should have 6 values.")
        lines = lines[1:]
        hfb_data = []
        for line in lines:
            line = line.strip().split()
            lyr = int(line[0]) - 1
            row1 = int(line[1]) - 1
            col1 = int(line[2]) - 1
            row2 = int(line[3]) - 1
            col2 = int(line[4]) - 1
            hcdw = float(line[5])
            hfb_data.append((lyr, row1, col1, row2, col2, hcdw))
        instance = cls(model, hfb_data=hfb_data)
        return instance
