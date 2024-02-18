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
        Initialize the COMUS Model with the Reservoir(RES) package.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object.
        res_num:
            Number of reservoirs.

        Returns:
        --------
        instance: pycomus.ComusRes
           COMUS Reservoir(RES) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> resPackage = pycomus.ComusRes(model1, res_num=1)
        """
        if res_num < 1:
            raise ValueError("The number of reservoirs should be greater than or equal to 1.")
        self._res_num = res_num
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        self.resValue: Res = Res()
        model.package["RES"] = self

    def set_control_params(self, control_params: Dict[int, Tuple[float, float, int, int]]) -> None:
        """
        Set Reservoir Control Params.

        :param control_params:
            A Dict type data where the keys represent the reservoir IDs, and the values are Tuples containing four
            elements: EvExp, EvMaxd, NumSeg, and NumPt.
        """
        for res_id, params in control_params.items():
            if res_id < 0 or res_id >= self._res_num:
                raise ValueError(f"Reservoir ID should be between 0 and {self._res_num - 1}.")

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

        self.resValue.ControlParams = control_params

    def set_period_data(self, period_data: Dict[int, Dict[int, Tuple[float, float, float, float]]]) -> None:
        """
        Set Reservoir Period Data.

        :param period_data:
            A Dict type data where the keys represent the reservoir IDs, and the values are Dicts with Period IDs as
            keys. Within the inner Dicts, the values are Tuples containing four elements: Shead, Ehead, Rchrg, and Gevt.
        """
        for res_id, periodData in period_data.items():
            if res_id < 0 or res_id >= self._res_num:
                raise ValueError(f"Reservoir ID should be between 0 and {self._res_num - 1}.")
            for period_id, value in periodData.items():
                if not (0 <= period_id < len(self._period)):
                    raise ValueError(
                        f"Invalid key {period_id} in period_data[{res_id}] dictionary. Keys should be in the range 0 to {len(self._period) - 1}.")

                if len(value) != 4:
                    raise ValueError("Each period data should contain 4 values.")

                if not all(isinstance(x, (int, float)) for x in value):
                    raise ValueError(
                        "All values(Shead, Ehead, Rchrg, Gevt) in period data should be numbers (int or float).")

                if value[2] < 0 or value[3] < 0:
                    raise ValueError("Rchrg and Gevt in period data should be greater than or equal to 0.")
        self.resValue.PeriodData = period_data

    def set_grid_data(self, btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      bvk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      btk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]) -> None:
        """
        Set Reservoir Grid Cell Data.

        :param btm:
            btm represents the elevation of the reservoir grid cell's bed (L).
        :param bvk:
            bvk represents the hydraulic conductivity coefficient of the low-permeability medium at the reservoir grid cell (L/T).
        :param btk:
            btk represents the thickness of the low-permeability medium at the reservoir grid cell (L).
        """
        resIds = [i for i in range(self._res_num)]
        btm = BoundaryCheck.CheckValueFormat(btm, "Btm", resIds, self._num_lyr, self._num_row, self._num_col)
        bvk = BoundaryCheck.CheckValueGtZero(bvk, "Bvk", resIds, self._num_lyr, self._num_row, self._num_col)
        btk = BoundaryCheck.CheckValueGtZero(btk, "Btk", resIds, self._num_lyr, self._num_row, self._num_col)
        if sorted(btm.keys()) != sorted(bvk.keys()) != sorted(btk.keys()):
            raise ValueError("The ResId for the 'Btm' parameter,'Bvk' and 'Btk' should be the same.")
        self.resValue.GridData = {"Btm": btm, "Bvk": bvk, "Btk": btk}

    @classmethod
    def load(cls, model, ctrl_pars_file: str, period_file: str, grid_file: str):
        """
        Load parameters from RES(RESCtrl.in, RESPer.in, RESGrd.in) file and create a ComusRes instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        ctrl_pars_file: str
            Grid RES Params File Path(RESCtrl.in).
        period_file: str
            Grid RES Params File Path(RESPer.in).
        grid_file: str
            Grid RES Params File Path(RESGrd.in).

        Returns:
        --------
        instance: pycomus.ComusRes
            COMUS Reservoir(RES) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> resPackage = pycomus.ComusRes.load(model1, "./InputFiles/RESCtrl.in", "./InputFiles/RESPer.in",
        >>> "./InputFiles/RESGrd.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col

        # load ctrl_pars_file
        with open(ctrl_pars_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 5:
            raise ValueError(
                "The Reservoir(RES) Control Params Attribute file(RESCtrl.in) header should have 5 fields.")
        if len(lines[1].strip().split()) != 5:
            raise ValueError(
                "The Reservoir(RES) Control Params Attribute file(RESCtrl.in) data line should have 5 values.")
        lines = lines[1:]
        ctrl_pars_data = {}
        for line in lines:
            line = line.strip().split()
            res_id = int(line[0]) - 1
            if res_id not in ctrl_pars_data:
                ctrl_pars_data[res_id] = (float(line[1]), float(line[2]), int(line[3]), int(line[4]))
            else:
                raise ValueError(f"The reservoir ID {res_id} already exists. Reservoir IDs should be unique.")
        instance = cls(model, res_num=len(ctrl_pars_data))
        instance.set_control_params(ctrl_pars_data)

        # load period_file
        with open(period_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 6:
            raise ValueError("The Reservoir(RES) Period Params Attribute file(RESPer.in) header should have 6 fields.")
        if len(lines[1].strip().split()) != 6:
            raise ValueError(
                "The Reservoir(RES) Period Params Attribute file(RESPer.in) data line should have 6 values.")
        lines = lines[1:]
        period_data = {}
        for line in lines:
            line = line.strip().split()
            period_id = int(line[0]) - 1
            res_id = int(line[1]) - 1
            if res_id not in period_data:
                period_data[res_id] = {}
            if period_id not in period_data[res_id]:
                period_data[res_id][period_id] = (float(line[2]), float(line[3]), float(line[4]), float(line[5]))
        instance.set_period_data(period_data)

        # load grid_data
        with open(grid_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 8:
            raise ValueError("The Reservoir(RES) Period Params Attribute file(RESGrd.in) header should have 8 fields.")
        if len(lines[1].strip().split()) != 8:
            raise ValueError(
                "The Reservoir(RES) Period Params Attribute file(RESGrd.in) data line should have 8 values.")
        lines = lines[1:]
        btm = {}
        bvk = {}
        btk = {}
        for line in lines:
            line = line.strip().split()
            res_id = int(line[0]) - 1
            lyr = int(line[2]) - 1
            row = int(line[3]) - 1
            col = int(line[4]) - 1
            if res_id not in btm:
                btm[res_id] = np.zeros((num_lyr, num_row, num_col))
                btm[res_id][lyr, row, col] = float(line[5])
                bvk[res_id] = np.zeros((num_lyr, num_row, num_col))
                bvk[res_id][lyr, row, col] = float(line[6])
                btk[res_id] = np.zeros((num_lyr, num_row, num_col))
                btk[res_id][lyr, row, col] = float(line[7])
            else:
                btm[res_id][lyr, row, col] = float(line[5])
                bvk[res_id][lyr, row, col] = float(line[6])
                btk[res_id][lyr, row, col] = float(line[7])
        instance.set_grid_data(btm, bvk, btk)
        return instance


class Res:
    def __init__(self):
        self.ControlParams = None
        self.PeriodData = None
        self.GridData = None
