# --------------------------------------------------------------
# CRES.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With RES Package.
# --------------------------------------------------------------
from typing import Dict, Tuple, Union

import numpy as np

from pycomus.Utils import BoundaryCheck


class ComusRes:
    def __init__(self, model, res_num: int):
        """
        Set COMUS Model With RES Package.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object.
        res_num:
            Number of reservoirs.
        """
        if res_num < 1:
            raise ValueError("The number of reservoirs should be greater than or equal to 1.")
        self.__res_num = res_num
        cmsDis = model._cmsDis
        self.__NumLyr = cmsDis.NumLyr
        self.__NumRow = cmsDis.NumRow
        self.__NumCol = cmsDis.NumCol
        self.__period = model._cmsTime.period
        self.__res: Res = Res()
        model._addPackage("RES", self)

    @property
    def ResValue(self):
        return self.__res

    def setControlParams(self, control_params: Dict[int, Tuple[float, float, int, int]]) -> None:
        """
        Set Reservoir Control Params.

        :param control_params:
            A Dict type data where the keys represent the reservoir IDs, and the values are Tuples containing four
            elements: EvExp, EvMaxd, NumSeg, and NumPt.
        """
        for res_id, params in control_params.items():
            if res_id < 0 or res_id >= self.__res_num:
                raise ValueError(f"Reservoir ID should be between 0 and {self.__res_num - 1}.")

            if len(params) != 4:
                raise ValueError("Control parameters should contain 4 values(EvExp, EvMaxd, NumSeg, NumPt).")

            if not isinstance(params[0], (int, float)) or not isinstance(params[1], (int, float)):
                raise ValueError("EvExp and EvMaxd should be numbers (int or float).")

            if not isinstance(params[2], int) or not isinstance(params[3], int):
                raise ValueError("NumSeg and NumPt should be integers.")

            if params[2] < 2 or params[2] > 20:
                raise ValueError("NumSeg should be between 2 and 20.")

            if params[3] <= 2:
                raise ValueError("NumPt should be greater than 2.")

        self.__res.ControlParams = control_params

    def setPeriodData(self, period_data: Dict[int, Dict[int, Tuple[float, float, float, float]]]) -> None:
        """
        Set Reservoir Period Data.

        :param period_data:
            A Dict type data where the keys represent the reservoir IDs, and the values are Dicts with Period IDs as
            keys. Within the inner Dicts, the values are Tuples containing four elements: Shead, Ehead, Rchrg, and Gevt.
        """
        for res_id, periodData in period_data.items():
            if res_id < 0 or res_id >= self.__res_num:
                raise ValueError(f"Reservoir ID should be between 0 and {self.__res_num - 1}.")
            for period_id, value in periodData.items():
                if not (0 <= period_id < len(self.__period)):
                    raise ValueError(
                        f"Invalid key {period_id} in period_data[{res_id}] dictionary. Keys should be in the range 0 to {len(self.__period) - 1}.")

                if len(value) != 4:
                    raise ValueError("Each period data should contain 4 values.")

                if not all(isinstance(x, (int, float)) for x in value):
                    raise ValueError(
                        "All values(Shead, Ehead, Rchrg, Gevt) in period data should be numbers (int or float).")

                if value[2] < 0 or value[3] < 0:
                    raise ValueError("Rchrg and Gevt in period data should be greater than or equal to 0.")
        self.__res.PeriodData = period_data

    def setGridData(self, Btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    Bvk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    Btk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]) -> None:
        """
        Set Reservoir Grid Cell Data.

        :param Btm:
            BTM represents the elevation of the reservoir grid cell's bed (L).
        :param Bvk:
            BVK represents the hydraulic conductivity coefficient of the low-permeability medium at the reservoir grid cell (L/T).
        :param Btk:
            BTK represents the thickness of the low-permeability medium at the reservoir grid cell (L).
        """
        resIds = [i for i in range(self.__res_num)]
        self.__btm = BoundaryCheck.CheckValueFormat(Btm, "Btm", resIds, self.__NumLyr, self.__NumRow, self.__NumCol)
        self.__bvk = BoundaryCheck.CheckValueGtZero(Bvk, "Bvk", resIds, self.__NumLyr, self.__NumRow, self.__NumCol)
        self.__btk = BoundaryCheck.CheckValueGtZero(Btk, "Btk", resIds, self.__NumLyr, self.__NumRow, self.__NumCol)
        if sorted(self.__btm.keys()) != sorted(self.__bvk.keys()) != sorted(self.__btk.keys()):
            raise ValueError("The ResId for the 'Btm' parameter,'Bvk' and 'Btk' should be the same.")
        self.__res.GridData = {"Btm": self.__btm, "Bvk": self.__bvk, "Btk": self.__btk}


class Res:
    def __init__(self):
        self.ControlParams = None
        self.PeriodData = None
        self.GridData = None
