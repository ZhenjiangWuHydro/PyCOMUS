# --------------------------------------------------------------
# CLAK.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With LAK Package.
# --------------------------------------------------------------
import os
import sys
from typing import Dict, Tuple, Union

import numpy as np

from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import LAK_PKG_NAME, LAK_CTRL_FILE_NAME, LAK_PERIOD_FILE_NAME, LAK_GRID_FILE_NAME


class ComusLak:
    """
    Initialize the COMUS Model with the Lake(LAK) package.

    Attributes:
    ----------------------------
    model:
        COMUS Model Object.
    lake_num:
        Number of lakes.

    Methods:
    --------
    __init__(self, model, lake_num: int)
        Initialize the COMUS Model with the Lake(LAK) package.

    set_control_params(self, control_params: Dict[
        int, Tuple[int, int, int, float, float, float, float, float, int, float, float, float, float]])
        Set Lake Control Params.

    set_period_data(self, period_data: Dict[
        int, Dict[int, Tuple[float, float, float, float, float, float, float, float]]])
        Set Lake Period Data.

    set_grid_data(self, btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      lnk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      sc1: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      sc2: Union[int, float, Dict[int, Union[int, float, np.ndarray]]])
        Set Lake Grid Cell Data.

    load(cls, model, ctrl_pars_file: str, period_file: str, grid_file: str)
         Load parameters from LAK(LAKCtrl.in, LAKPer.in, LAKGrd.in) file and create a ComusLak instance.

    write_file(self, folder_path: str)
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusLak`
        module to the specified path as <LAKCtrl.in>, <LAKPer.in> and <LAKGrd.in>.

    Returns:
    --------
    instance: pycomus.ComusLak
       COMUS Lake(LAK) Params Object.

    Example:
    --------
    >>> import pycomus
    >>> model1 = pycomus.ComusModel(model_name="test")
    >>> lakPackage = pycomus.ComusLak(model1, lake_num=1)
    """

    def __init__(self, model, lake_num: int):
        if lake_num < 1:
            raise ValueError("The number of lakes should be greater than or equal to 1.")
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
        self._lake_num = lake_num
        self.lakeValue: Lak = Lak()
        self._model = model
        model.package[LAK_PKG_NAME] = self

    def set_control_params(self, control_params: Dict[
        int, Tuple[int, int, int, float, float, float, float, float, int, float, float, float, float]]) -> None:
        """
        Set Lake Control Params.

        :param control_params:
            A Dict type data where the keys represent the lake IDs, and the values are Tuples containing 13
            elements: STRID, DIVSID, DIVSAT, BETA, INIHLEV, DEADHLEV, EVEXP, EVMAXD, NUMSEG, STRBED, STRWDT, STRNDC, STRSLP.
        """
        for lak_id, params in control_params.items():
            if lak_id < 0 or lak_id >= self._lake_num:
                raise ValueError(f"Lake ID should be between 0 and {self._lake_num - 1}.")

            if len(params) != 13:
                raise ValueError("Control parameters should contain 13 values(STRID, DIVSID, DIVSAT, BETA, INIHLEV,"
                                 " DEADHLEV, EVEXP, EVMAXD, NUMSEG, STRBED, STRWDT, STRNDC, STRSLP).")
            if not all(isinstance(x, (int, float)) for x in params):
                raise ValueError(
                    "All values in period data should be numbers (int or float).")
            isStrExist: bool = False
            if "STR" in self._model.package:
                isStrExist = True
            str_id = params[0]
            divs_id = params[1]
            div_sat = params[2]
            ev_exp = params[6]
            ev_maxd = params[7]
            num_seg = params[8]
            str_wdt = params[10]
            str_ndc = params[11]
            str_slp = params[12]
            # Check is exist stream
            if isStrExist:
                if str_id < 0:
                    raise ValueError(
                        "The downstream river cell unit numbers must be greater than or equal to 0. Please check!")
                if divs_id < 0:
                    raise ValueError(
                        "The diversion water source unit numbers for lake cells must be greater than or equal to 0. Please check!")
                if divs_id != 0:
                    if div_sat not in (1, 2):
                        raise ValueError("The DIVSAT data must be equal to 1 or 2. Please check! ")
            if ev_exp <= 0 or ev_maxd <= 0:
                raise ValueError(
                    f"The EVEXP and EVMAXD parameters for lake number {lak_id} must be greater than 0.0. Please check!")
            if num_seg < 2 or num_seg > 20:
                raise ValueError(
                    f"The NUMSEG parameter for lake number {lak_id} must be between 2 and 20. Please check!")
            if str_id != 0:
                if str_wdt <= 0 or str_ndc <= 0 or str_slp <= 0:
                    raise ValueError(
                        f"Lake number {lak_id} has downstream river reach units. Parameters like STRWDT, STRNDC, STRSLP, etc., must be greater than 0.0. Please verify!")
        self.lakeValue.ControlParams = control_params

    def set_period_data(self, period_data: Dict[
        int, Dict[int, Tuple[float, float, float, float, float, float, float, float]]]) -> None:
        """
        Set Lake Period Data.

        :param period_data:
            A Dict type data where the keys represent the Period IDs, and the values are Dicts with lake IDs as
            keys. Within the inner Dicts, the values are Tuples containing four elements: PCP, RNFCOF, PRHCOF,
             ET0, EVWBCOF, GEVCOF, WATDIV, WATUSE.
        """
        for period_id, periodData in period_data.items():
            if not (0 <= period_id < len(self._period)):
                raise ValueError(
                    f"Invalid key {period_id} in period_data dictionary. Keys should be in the range 0 to {len(self._period) - 1}.")
            for lak_id, value in periodData.items():
                if lak_id < 0 or lak_id >= self._lake_num:
                    raise ValueError(f"Lake ID should be between 0 and {self._lake_num - 1}.")
                if len(value) != 8:
                    raise ValueError(
                        "Each period data should contain 8 values(PCP,RNFCOF,PRHCOF,ET0,EVWBCOF,GEVCOF,WATDIV,WATUSE).")

                if not all(isinstance(x, (int, float)) for x in value):
                    raise ValueError(
                        "All values(PCP,RNFCOF,PRHCOF,ET0,EVWBCOF,GEVCOF,WATDIV,WATUSE) in period data should be float.")

                if value[0] < 0:
                    raise ValueError(
                        f"The PCP data for Lake {lak_id} in period {period_id} must not be less than 0.0. Please check!")
                if value[1] < 0 or value[1] > 1:
                    raise ValueError(
                        f"The RNFCOF data for Lake {lak_id} in period {period_id}  should be between 0.0 and 1.0. Please check!")
                if value[2] < 0 or value[2] > 1:
                    raise ValueError(
                        f"The PRHCOF data for Lake {lak_id} in period {period_id}  should be between 0.0 and 1.0. Please check!")
                if value[1] + value[2] > 1:
                    raise ValueError(
                        f"The sum of PRHCOF and RNFCOF data for Lake {lak_id} in period {period_id} should be less than 1.0. Please check")
                if value[3] < 0:
                    raise ValueError(
                        f"The ET0 data for Lake {lak_id} in period {period_id} should not be less than 0.0. Please check")
                if value[4] < 0:
                    raise ValueError(
                        f"The EVWBCOF data for Lake {lak_id} in period {period_id} should not be less than 0.0. Please check")
                if value[5] < 0:
                    raise ValueError(
                        f"The GEVCOF data for Lake {lak_id} in period {period_id} should not be less than 0.0. Please check")
        self.lakeValue.PeriodData = period_data

    def set_grid_data(self, btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      lnk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      sc1: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                      sc2: Union[int, float, Dict[int, Union[int, float, np.ndarray]]]) -> None:
        """
        Set Lake Grid Cell Data.

        :param btm:
            Lake bed elevation (L) at the grid cell of the lake.
        :param lnk:
            Overland flow coefficient (1/T) between the lake bed and the aquifer.
        :param sc1:
            Storage coefficient (-) when the grid cell of the lake is under pressure condition.
        :param sc2:
            Supply coefficient (-) when the grid cell of the lake is under non-pressure condition.
        """
        resIds = [i for i in range(self._lake_num)]
        btm = BoundaryCheck.CheckValueFormat(btm, "BTM", resIds, self._num_lyr, self._num_row, self._num_col)
        lnk = BoundaryCheck.CheckValueGtZero(lnk, "LNK", resIds, self._num_lyr, self._num_row, self._num_col)
        sc1 = BoundaryCheck.CheckValueGtZero(sc1, "SC1", resIds, self._num_lyr, self._num_row, self._num_col)
        sc2 = BoundaryCheck.CheckValueGtZero(sc2, "SC2", resIds, self._num_lyr, self._num_row, self._num_col)
        if sorted(btm.keys()) != sorted(lnk.keys()) != sorted(sc1.keys()) != sorted(sc2.keys()):
            raise ValueError("The LakeId for the 'BTM' parameter,'LNK','SC1' and 'SC2' should be the same.")
        self.lakeValue.GridData = {"BTM": btm, "LNK": lnk, "SC1": sc1, "SC2": sc2}

    @classmethod
    def load(cls, model, ctrl_pars_file: str, period_file: str, grid_file: str):
        """
        Load parameters from LAK(LAKCtrl.in, LAKPer.in, LAKGrd.in) file and create a ComusLak instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        ctrl_pars_file: str
            LAK Control Params File Path(LAKCtrl.in).
        period_file: str
            LAK Period Params File Path(LAKPer.in).
        grid_file: str
            LAK Grid Params File Path(LAKGrd.in).

        Returns:
        --------
        instance: pycomus.ComusLak
            COMUS Lake(LAK) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> lakPackage = pycomus.ComusLak.load(model1, "LAKCtrl.in", "LAKPer.in", "LAKGrd.in")
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col

        # load ctrl_pars_file
        with open(ctrl_pars_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 14:
            raise ValueError(
                "The Lake(LAK) Control Params Attribute file(LAKCtrl.in) header should have 14 fields.")
        if len(lines[1].strip().split()) != 14:
            raise ValueError(
                "The Lake(LAK) Control Params Attribute file(LAKCtrl.in) data line should have 14 values.")
        lines = lines[1:]
        ctrl_pars_data = {}
        for line in lines:
            line = line.strip().split()
            lake_id = int(line[0]) - 1
            if lake_id not in ctrl_pars_data:
                ctrl_pars_data[lake_id] = (
                    int(line[1]), int(line[2]), int(line[3]), float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), int(line[9]), float(line[10]), float(line[11]), float(line[12]),
                    float(line[13]))
            else:
                raise ValueError(f"The lake ID {lake_id} already exists. Lake IDs should be unique.")
        instance = cls(model, lake_num=len(ctrl_pars_data))
        instance.set_control_params(ctrl_pars_data)

        # load period_file
        with open(period_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 10:
            raise ValueError("The Lake(LAK) Period Params Attribute file(LAKPer.in) header should have 10 fields.")
        if len(lines[1].strip().split()) != 10:
            raise ValueError(
                "The Lake(LAK) Period Params Attribute file(LAKPer.in) data line should have 10 values.")
        lines = lines[1:]
        period_data = {}
        for line in lines:
            line = line.strip().split()
            period_id = int(line[0]) - 1
            lake_id = int(line[1]) - 1
            if period_id not in period_data:
                period_data[period_id] = {}
            if lake_id not in period_data[period_id]:
                period_data[period_id][lake_id] = (
                    float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7]),
                    float(line[8]), float(line[9]))
        instance.set_period_data(period_data)

        # load grid_data
        with open(grid_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 9:
            raise ValueError("The Lake(LAK) Period Params Attribute file(LAKGrd.in) header should have 9 fields.")
        if len(lines[1].strip().split()) != 9:
            raise ValueError(
                "The Lake(LAK) Period Params Attribute file(LAKGrd.in) data line should have 9 values.")
        lines = lines[1:]
        btm = {}
        lnk = {}
        sc1 = {}
        sc2 = {}
        for line in lines:
            line = line.strip().split()
            lake_id = int(line[0]) - 1
            lyr = int(line[2]) - 1
            row = int(line[3]) - 1
            col = int(line[4]) - 1
            if lake_id not in btm:
                btm[lake_id] = np.zeros((num_lyr, num_row, num_col))
                btm[lake_id][lyr, row, col] = float(line[5])
                lnk[lake_id] = np.zeros((num_lyr, num_row, num_col))
                lnk[lake_id][lyr, row, col] = float(line[6])
                sc1[lake_id] = np.zeros((num_lyr, num_row, num_col))
                sc1[lake_id][lyr, row, col] = float(line[7])
                sc2[lake_id] = np.zeros((num_lyr, num_row, num_col))
                sc2[lake_id][lyr, row, col] = float(line[8])
            else:
                btm[lake_id][lyr, row, col] = float(line[5])
                lnk[lake_id][lyr, row, col] = float(line[6])
                sc1[lake_id][lyr, row, col] = float(line[7])
                sc2[lake_id][lyr, row, col] = float(line[8])
        instance.set_grid_data(btm, lnk, sc1, sc2)
        return instance

    def __str__(self):
        res = f"{LAK_PKG_NAME}:\n"
        res += f"    Lake Control Params : {self.lakeValue.ControlParams}\n"
        res += f"    Lake Period Params : {self.lakeValue.PeriodData}\n"
        res += f"    Lake Grid Params : {self.lakeValue.GridData}\n"
        return res

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusLak`
        module to the specified path as <LAKCtrl.in>, <LAKPer.in> and <LAKGrd.in>.

        :param folder_path: Output folder path.
        """
        if not self._write_file_test(folder_path):
            lak_file = os.path.join(folder_path, LAK_CTRL_FILE_NAME)
            if os.path.exists(lak_file):
                os.remove(lak_file)
            lak_file = os.path.join(folder_path, LAK_PERIOD_FILE_NAME)
            if os.path.exists(lak_file):
                os.remove(lak_file)
            lak_file = os.path.join(folder_path, LAK_GRID_FILE_NAME)
            if os.path.exists(lak_file):
                os.remove(lak_file)
            sys.exit()

    def _write_file_test(self, folder_path: str) -> bool:
        # Control Param Check And Write
        ctrl_pars = self.lakeValue.ControlParams
        data_row_index = 0
        with open(os.path.join(folder_path, LAK_CTRL_FILE_NAME), "w") as file:
            file.write("LAKEID  STRID  DIVSID  DIVSAT  BETA  INIHLEV  DEADHLEV  EVEXP  EVMAXD  NUMSEG  "
                       "STRBED  STRWDT  STRNDC  STRSLP\n")
            for lak_id, params in ctrl_pars.items():
                if data_row_index != lak_id:
                    print("LAKEID does not start from 1 or is not consecutive!")
                isStrExist: bool = False
                if "STR" in self._model.package:
                    isStrExist = True
                str_id = params[0]
                divs_id = params[1]
                div_sat = params[2]
                ev_exp = params[6]
                ev_maxd = params[7]
                num_seg = params[8]
                str_wdt = params[10]
                str_ndc = params[11]
                str_slp = params[12]
                # Check is exist stream
                if isStrExist:
                    if str_id < 0:
                        print("The downstream river cell unit numbers must be greater than or equal to 0.Please check!")
                        return False
                    if divs_id < 0:
                        print("The diversion water source unit numbers for lake cells must be greater than or equal to"
                              " 0. Please check!")
                        return False
                    if divs_id != 0:
                        if div_sat not in (1, 2):
                            print("The DIVSAT data must be equal to 1 or 2. Please check! ")
                            return False
                if ev_exp <= 0 or ev_maxd <= 0:
                    print(f"The EVEXP and EVMAXD parameters for lake number {lak_id} must be greater than 0.0. "
                          f"Please check!")
                    return False
                if num_seg < 2 or num_seg > 20:
                    print(f"The NUMSEG parameter for lake number {lak_id} must be between 2 and 20. Please check!")
                    return False
                if str_id != 0:
                    if str_wdt <= 0 or str_ndc <= 0 or str_slp <= 0:
                        print(f"Lake number {lak_id} has downstream river reach units. Parameters like STRWDT, STRNDC,"
                              f" STRSLP, etc., must be greater than 0.0. Please verify!")
                        return False
                file.write(f"{lak_id + 1}  {params[0]}  {params[1]}  {params[2]}  {params[3]}  {params[4]}  {params[5]}"
                           f"  {params[6]}  {params[7]}  {params[8]}  {params[9]}  {params[10]}  {params[11]}  {params[12]}\n")
                data_row_index += 1

        # Check Period Check And Write
        period_data = self.lakeValue.PeriodData
        with open(os.path.join(folder_path, LAK_PERIOD_FILE_NAME), "w") as file:
            file.write("IPER  LAKEID  PCP  RNFCOF  PRHCOF  ET0  EVWBCOF  GEVCOF  WATDIV  WATUSE\n")
            for period_id, periodData in period_data.items():
                for lake_id, value in periodData.items():
                    file.write(f"{period_id + 1}  {lake_id + 1}  {value[0]}  {value[1]}  {value[2]}  {value[3]}"
                               f"  {value[4]}  {value[5]}  {value[6]}  {value[7]}\n")

        # Check Grid Check And Write
        grid_data = self.lakeValue.GridData
        with open(os.path.join(folder_path, LAK_GRID_FILE_NAME), "w") as file:
            file.write("LAKEID  CELLID  ILYR  IROW  ICOL  BTM  LNK  SC1  SC2\n")
            lakIds = sorted(grid_data["BTM"].keys())
            for lakId in lakIds:
                index = 1
                btm_value = grid_data["BTM"][lakId]
                lnk_value = grid_data["LNK"][lakId]
                sc1_value = grid_data["SC1"][lakId]
                sc2_value = grid_data["SC2"][lakId]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if lnk_value[layer, row, col] > 0:
                                file.write(
                                    f"{lakId + 1}  {index}  {layer + 1}  {row + 1}  {col + 1}  {btm_value[layer, row, col]}  "
                                    f"{lnk_value[layer, row, col]}  {sc1_value[layer, row, col]}  {sc2_value[layer, row, col]}\n")
                                index += 1
        return True


class Lak:
    def __init__(self):
        self.ControlParams = None
        self.PeriodData = None
        self.GridData = None
