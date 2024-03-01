# --------------------------------------------------------------
# CRES.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With RES Package.
# --------------------------------------------------------------
import os
import sys
from typing import Dict, Tuple, Union

import numpy as np

from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import RES_PKG_NAME, RES_CTRL_FILE_NAME, RES_PERIOD_FILE_NAME, RES_GRID_FILE_NAME


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
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self._model = model
        self.resValue: Res = Res()
        model.package[RES_PKG_NAME] = self

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
        for period_id, periodData in period_data.items():
            if not (0 <= period_id < len(self._period)):
                raise ValueError(
                    f"Invalid key {period_id} in period_data dictionary. Keys should be in the range 0 to {len(self._period) - 1}.")
            for res_id, value in periodData.items():
                if res_id < 0 or res_id >= self._res_num:
                    raise ValueError(f"Reservoir ID should be between 0 and {self._res_num}.")
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
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col

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
            if period_id not in period_data:
                period_data[period_id] = {}
            if res_id not in period_data[period_id]:
                period_data[period_id][res_id] = (float(line[2]), float(line[3]), float(line[4]), float(line[5]))
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
                bvk[res_id] = np.zeros((num_lyr, num_row, num_col))
                btk[res_id] = np.zeros((num_lyr, num_row, num_col))
            btm[res_id][lyr, row, col] = float(line[5])
            bvk[res_id][lyr, row, col] = float(line[6])
            btk[res_id][lyr, row, col] = float(line[7])
        instance.set_grid_data(btm, bvk, btk)
        return instance

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusRes`
        module to the specified path as <RESCtrl.in>, <RESPer.in> and <RESGrd.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            res_file = os.path.join(folder_path, RES_CTRL_FILE_NAME)
            if os.path.exists(res_file):
                os.remove(res_file)
            res_file = os.path.join(folder_path, RES_PERIOD_FILE_NAME)
            if os.path.exists(res_file):
                os.remove(res_file)
            res_file = os.path.join(folder_path, RES_GRID_FILE_NAME)
            if os.path.exists(res_file):
                os.remove(res_file)
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        # Control Param Check And Write
        ctrl_pars = self.resValue.ControlParams
        data_row_index = 0
        with open(os.path.join(folder_path, RES_CTRL_FILE_NAME), "w") as file:
            file.write("RESID  EVEXP  EVMAXD  NUMSEG  NUMPT\n")
            for res_id, params in ctrl_pars.items():
                if data_row_index != res_id:
                    print("RESID does not start from 1 or is not consecutive!")
                    return False
                if params[0] < 0:
                    print(f"The EVEXP on the reservoir with the ID {res_id} on non-flooded units is unreasonable,"
                          f" it should be greater than 0.")
                    return False
                if params[1] < 0:
                    print(f"The EVMAXD on the reservoir with the ID {res_id} on non-flooded units is unreasonable,"
                          f" it should be greater than 0.")
                    return False
                if params[2] < 2 or params[2] > 20:
                    print(f"The NUMSEG on the reservoir with the ID {res_id} on non-flooded units should "
                          f"be between 2 and 20.")
                    return False
                if params[3] < 2:
                    print(f"The NUMPT of the reservoir with the ID {res_id} should be at least 2.")
                    return False
                file.write(f"{res_id + 1}  {params[0]}  {params[1]}  {params[2]}  {params[3]}\n")
                data_row_index += 1

        # Check Period Check And Write
        period_data = self.resValue.PeriodData
        with open(os.path.join(folder_path, RES_PERIOD_FILE_NAME), "w") as file:
            file.write("IPER  RESID  SHEAD  EHEAD  RCHRG  GEVT\n")
            for period_id, periodData in period_data.items():
                for res_id, value in periodData.items():
                    if value[2] < 0 or value[3] < 0:
                        print(f"The RCHRG and GEVT data for reservoir {res_id} in the {period_id}th period cannot be "
                              f"less than 0.0.")
                        return False
                    file.write(f"{period_id + 1}  {res_id + 1}  {value[0]}  {value[1]}  {value[2]}  {value[3]}\n")

        # Check Grid Check And Write
        grid_data = self.resValue.GridData
        with open(os.path.join(folder_path, RES_GRID_FILE_NAME), "w") as file:
            file.write("RESID  CELLID  ILYR  IROW  ICOL  BTM  BVK  BTK\n")
            resIds = sorted(grid_data["Btm"].keys())
            for resId in resIds:
                index = 1
                btm_value = grid_data["Btm"][resId]
                bvk_value = grid_data["Bvk"][resId]
                btk_value = grid_data["Btk"][resId]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if bvk_value[layer, row, col] >= 0 and btk_value[layer, row, col] > 0:
                                file.write(
                                    f"{resId + 1}  {index}  {layer + 1}  {row + 1}  {col + 1}  {btm_value[layer, row, col]}  "
                                    f"{bvk_value[layer, row, col]}  {btk_value[layer, row, col]}\n")
                                index += 1
        return True


class Res:
    def __init__(self):
        self.ControlParams = None
        self.PeriodData = None
        self.GridData = None
