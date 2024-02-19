# --------------------------------------------------------------
# CSTR.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With STR Package.
# --------------------------------------------------------------
from collections import OrderedDict
from typing import Dict, Tuple, Union

import numpy as np

from pycomus.Utils import BoundaryCheck


class ComusStr:
    def __init__(self, model, stream_num: int):
        """
        Initialize the COMUS Model with the Stream(STR) package.

        Parameters:
        ----------------------------
        model:
           COMUS Model Object.
        stream_num:
           Number of streams.
        """
        if stream_num < 1:
            raise ValueError("The number of streams should be greater than or equal to 1.")
        self._stream_num = stream_num
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        self.streamValue: Stream = Stream()
        model.package["STR"] = self

    def set_ControlData(self, control_params: Dict[int, Tuple[int, int, int, int, int, int, int, int, int]]) -> None:
        """
         Set Stream Control Params.

        :param control_params:
            A Dict type data where the keys represent the streams IDs, and the values are Tuples containing nine
            elements: ["NEXTID", "NEXTAT", "DIVSID", "DIVSAT", "DIVTPOPT", "WUTPOPT", "WUREGID", "WUBKOPT", "DRNOPT"]
        """

        # Sorted Dict
        control_params = OrderedDict(sorted(zip(control_params.keys(), control_params.values())))

        # Check starts from 1 and continues.
        if not self.__is_consecutive_dict_keys(control_params.keys()):
            raise ValueError(
                "The river segment identifier data (SEGMID) is not starting from 1 or is not continuous. Please check!")

        for str_id, params in control_params.items():
            # Check data type
            if not isinstance(str_id, int):
                raise ValueError("control_params's dict key should be int.")
            if not all(isinstance(x, int) for x in params):
                raise ValueError("control_params's value(tuple's value) should be int.")

            # Check stream id
            if str_id < 0 or str_id >= self._stream_num:
                raise ValueError(f"Stream ID should be between 0 and {self._stream_num - 1}.")

            # Check params length

            if len(params) != 9:
                raise ValueError("Control parameters should contain 9 values(NEXTID, NEXTAT, DIVSID, DIVSAT, DIVTPOPT"
                                 ", WUTPOPT, WUREGID, WUBKOPT, DRNOPT).")

            # Check NEXTID
            if params[0] < 0:
                raise ValueError(
                    f"The NEXTID data for the river segment with ID {str_id} must be greater than or equal to 0. Please check!")

            # Check NEXTAT
            if params[0] != 0:
                if params[1] not in [1, 2]:
                    raise ValueError(
                        f"The NEXTAT data for the river segment with ID {str_id} must be 1 or 2. Please check!")

            # Check DIVSID
            if params[2] < 0:
                raise ValueError(
                    f"The DIVSID data for the river segment with ID {str_id} must be greater than or equal to 0. Please check!")

            if params[2] != 0:
                # Check DIVSAT
                if params[3] < 1 or params[3] > 2:
                    raise ValueError(
                        f"The DIVSAT data for the river segment with ID {str_id} must be equal to 1 or 2. Please check!")

                # Check DIVTPOPT
                if params[4] < 1 or params[4] > 3:
                    raise ValueError(
                        f"The DIVTPOPT data for the river segment with ID {str_id} must be between 1 and 3. Please check!")

                # Check WUTPOPT
                if params[3] == 2 and params[4] == 2:
                    raise ValueError(
                        f"The river segment with ID {str_id} discharges from a lake, and its DIVTPOPT data cannot be 2 (proportional discharge). Please check!")
            else:
                if params[4] < 0 or params[4] > 1:
                    raise ValueError(
                        f"The river segment with ID {str_id} does not have any upstream source segments. Its DIVTPOPT data must be 0 or 1. Please check!")

            # Check WUTPOPT
            if params[5] < 1 or params[5] > 2:
                raise ValueError(
                    f"The WUTPOPT data for the river segment with ID {str_id}  must be 1 or 2. Please check!")

            # Check WUREGID
            if params[6] < 0:
                raise ValueError(
                    f"The WUREGID data for the river segment with ID {str_id} must be greater than or equal to 0. Please check!")

            # Check WUBKOPT
            if params[7] < 0 or params[7] > 1:
                raise ValueError(
                    f"The WUBKOPT data for the river segment with ID {str_id} must be 0 or 1. Please check!")

            # Check DRNOPT
            if params[8] < 0 or params[8] > 1:
                raise ValueError(
                    f"The DRNOPT data for the river segment with ID {str_id} must be 0 or 1. Please check!")

        self.streamValue.ControlParams = control_params

    def set_PeriodData(self, period_data: Dict[int, Dict[
        int, Tuple[int, float, float, float, float, float, float, float, float, float, float, float]]]) -> None:
        """
        Set Stream Period Data.

        :param period_data:
            A Dict type data where the keys represent the stream IDs, and the values are Dicts with Period IDs as
            keys. Within the inner Dicts, the values are Tuples containing four elements: (HCALOPT, USLEV, UELEV, DSLEV, DELEV, WATPNT,"
            WATWAY, WATDIV, WATUSE, EVRATE, RCHCOE, WBKCOE)
        """
        if not self.streamValue.ControlParams:
            raise ValueError("ControlParams function of 'ComusStr' should be set first.")
        period_data = OrderedDict(sorted(zip(period_data.keys(), period_data.values())))
        if not self.__is_consecutive_dict_keys(period_data.keys()):
            raise ValueError(
                "The river segment identifier data (SEGMID) is not starting from 1 or is not continuous. Please check!")
        for str_id, periodData in period_data.items():
            # Check data type
            if not isinstance(str_id, int):
                raise ValueError("period_data's dict key should be int.")
            if str_id < 0 or str_id >= self._stream_num:
                raise ValueError(f"Stream ID should be between 0 and {self._stream_num - 1}.")
            for period_id, value in periodData.items():
                # Check period key type
                if not isinstance(period_id, int):
                    raise ValueError("period_data's value's dict key should be int.")

                # Check period id
                if not (0 <= period_id < len(self._period)):
                    raise ValueError(
                        f"Invalid key {period_id} in period_data[{str_id}] dictionary. Keys should be in the range 0 to {len(self._period) - 1}.")

                # Check data length
                if len(value) != 12:
                    raise ValueError(
                        "Each period data should contain 11 values(HCALOPT, USLEV, UELEV, DSLEV, DELEV, WATPNT,"
                        "WATWAY, WATDIV, WATUSE, EVRATE, RCHCOE, WBKCOE).")
                # Check HCALOPT
                if value[0] < 1 or value[0] > 2:
                    raise ValueError(
                        f"The HCALOPT data for the river segment with ID {str_id} and period {period_id} must be equal to 1 or 2. Please check!")

                # Check WATPNT
                if value[5] < 0:
                    raise ValueError(
                        f"The additional inflow data (WATPNT) at the beginning of the river segment for period {period_id} of river segment with ID {str_id} must be greater than or equal to 0.0. Please check!")

                # Check WATWAY
                if value[6] < 0:
                    raise ValueError(
                        f"The along-channel supplementary flow data (WATWAY) for period {period_id} of river segment with ID {str_id} must be greater than or equal to 0.0. Please check!")

                # Check WATDIV
                if self.streamValue.ControlParams[str_id][2] != 0 and self.streamValue.ControlParams[str_id][4] != 3:
                    if self.streamValue.ControlParams[str_id][4] == 1:
                        if value[7] < 0:
                            raise ValueError(
                                f"The WATDIV data for period {period_id} of river segment with ID {str_id}, when dividing flow as specified, must be greater than or equal to 0.0. Please check!")

                    elif value[7] < 0 and value[7] > 1:
                        raise ValueError(
                            f"The WATDIV data for period {period_id} of river segment with ID {str_id}, when dividing flow as specified by a proportion, must be between 0.0 and 1.0 inclusive. Please check!")

                # Check WATUSE
                if value[8] < 0:
                    raise ValueError(
                        f"The WATUSE data for period {period_id} of river segment with ID {str_id} must be greater than or equal to 0.0. Please check!")

                # Check EVRATE
                if value[9] < 0:
                    raise ValueError(
                        f"The EVRATE data for period {period_id} of river segment with ID {str_id} must be greater than or equal to 0.0. Please check!")

                # Check RCHCOE
                if value[8] > 0 and self.streamValue.ControlParams[str_id][6] >= 1:
                    if value[10] < 0 or value[10] > 1:
                        raise ValueError(
                            f"The RCHCOE data for period {period_id} of river segment with ID {str_id} must be between 0.0 and 1.0 inclusive. Please check!")

                # Check WBKCOE
                if value[8] > 0 and self.streamValue.ControlParams[str_id][6] >= 1 and \
                        self.streamValue.ControlParams[str_id][
                            7] == 1:
                    if value[10] + value[11] > 1:
                        raise ValueError(
                            f"The sum of RCHCOE and WBKCOE data for period {period_id} of river segment with ID {str_id} must be less than 1.0. Please check!")
        self.streamValue.PeriodData = period_data

    def set_GridData(self, cell_id: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     length: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     btm: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     bwdt: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     sizh1: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     sizh2: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     bvk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     btk: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     slp: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     ndc: Union[int, float, Dict[int, Union[int, float, np.ndarray]]], ) -> None:
        """
        Set Stream Grid Cell Data.

        :param cell_id:
            cell_id is an integer representing the sequential upstream and downstream order of the river segment within
            its parent river unit (1 indicates that the river segment is the first segment of the river unit).
        :param length:
            length is a double precision floating-point number representing the length of the river segment within the grid cell (L).
        :param btm:
            btm is a double precision floating-point number representing the average bed elevation of the river segment (L).
        :param bwdt:
            bwdt is a double precision floating-point number representing the average bed width of the river segment (L).
        :param sizh1:
            sizh1 is a double precision floating-point number representing the reciprocal of the left bank slope of the river segment (L/L).
        :param sizh2:
            sizh2 is a double precision floating-point number representing the reciprocal of the right bank slope of the river segment (L/L).
        :param bvk:
            bvk is a double precision floating-point number representing the permeability coefficient of the low-permeability medium of the river segment (L/T).
        :param btk:
            btk is a double precision floating-point number representing the thickness of the low-permeability medium of the river segment (L).
        :param slp:
            slp is a double precision floating-point number representing the average bed slope of the river segment (L/L).
        :param ndc:
            ndc is a double precision floating-point number representing the Manning's roughness coefficient (n) of the river segment.
        """
        strIds = [i for i in range(self._stream_num)]
        cell_id = BoundaryCheck.CheckValueGtZero(cell_id, "CELLID", strIds, self._num_lyr, self._num_row,
                                                 self._num_col)
        length = BoundaryCheck.CheckValueGtZero(length, "LEN", strIds, self._num_lyr, self._num_row, self._num_col)
        btm = BoundaryCheck.CheckValueGtZero(btm, "BTM", strIds, self._num_lyr, self._num_row, self._num_col)
        bwdt = BoundaryCheck.CheckValueGtZero(bwdt, "BWDT", strIds, self._num_lyr, self._num_row, self._num_col)
        sizh1 = BoundaryCheck.CheckValueGtZero(sizh1, "SIZH1", strIds, self._num_lyr, self._num_row,
                                               self._num_col)
        sizh2 = BoundaryCheck.CheckValueGtZero(sizh2, "SIZH2", strIds, self._num_lyr, self._num_row,
                                               self._num_col)
        bvk = BoundaryCheck.CheckValueGtZero(bvk, "BVK", strIds, self._num_lyr, self._num_row, self._num_col)
        btk = BoundaryCheck.CheckValueGtZero(btk, "BTK", strIds, self._num_lyr, self._num_row, self._num_col)
        slp = BoundaryCheck.CheckValueGtZero(slp, "SLP", strIds, self._num_lyr, self._num_row, self._num_col)
        ndc = BoundaryCheck.CheckValueGtZero(ndc, "NDC", strIds, self._num_lyr, self._num_row, self._num_col)

        if sorted(cell_id.keys()) != sorted(length.keys()) != sorted(btm.keys()) != sorted(bwdt.keys()) != sorted(
                sizh1.keys()) != sorted(sizh2.keys()) != sorted(bvk.keys()) != sorted(btk.keys()) != sorted(
            slp.keys()) != sorted(ndc.keys()):
            raise ValueError(
                "The StreamId for the 'CELLID','LEN','BTM','BWDT','SIZH1','SIZH2','BVK','BTK','SLP' and 'NDC' should be the same.")
        self.streamValue.GridData = {"CELLID": cell_id, "LEN": length, "BTM": btm, "BWDT": bwdt, "SIZH1": sizh1,
                                     "SIZH2": sizh2, "BVK": bvk, "BTK": btk, "SLP": slp, "NDC": ndc}

    def set_WatUseData(self, wureg_id: Union[int, np.ndarray], ratio: Union[int, float, np.ndarray]) -> None:
        """
        Set Stream Water Use Data.

        :param wureg_id:
            wureg_id is an integer representing the water use zone number for the river unit (starting from 1). A portion
             of the river unit's water use will be allocated to simulate surface infiltration recharge on grid cells
             within the range of this water use zone.
        :param ratio:
            ratio is a double precision floating-point number representing the weight coefficient of surface infiltration
            recharge for the river unit on the grid cell (-). It must be greater than or equal to 0.
        """
        wuGrdIdList = [value[6] for value in self.streamValue.ControlParams.values()]
        wureg_id = BoundaryCheck.Check3DValueExistGrid(wureg_id, "WUREGID", self._num_lyr, self._num_row,
                                                       self._num_col, wuGrdIdList)
        ratio = BoundaryCheck.Check3DValueGtZero(ratio, "RATIO", self._num_lyr, self._num_row,
                                                 self._num_col)
        self.streamValue.WatUseData = {"WUREGID": wureg_id, "RATIO": ratio}

    def set_WatDrnData(self, delev: Union[int, np.ndarray], cond: Union[int, float, np.ndarray],
                       segm_id: Union[int, float, np.ndarray]) -> None:
        """
        Set Stream Water Drn Data.

        :param delev:
            delev is a double precision floating-point number representing the elevation of the drainage ditch bottom
            at the grid cell (in meters). The drainage ditch only discharges groundwater when the groundwater level
            is higher than this elevation.
        :param cond:
            cond is a double precision floating-point number representing the hydraulic conductivity coefficient between
             the drainage ditch and the aquifer at the grid cell (in square meters per second).
        :param segm_id:
            segm_id is a double precision floating-point number representing the drainage area number, which is the
            identifier of the river segment of the seasonal river to which the grid cell drainage flows (starting from 1).
        """
        SegIdList = list(self.streamValue.ControlParams.keys())
        delev = BoundaryCheck.Check3DValueFormat(delev, "DELEV", self._num_lyr, self._num_row, self._num_col)
        cond = BoundaryCheck.Check3DValueGtZero(cond, "COND", self._num_lyr, self._num_row, self._num_col)
        segm_id = BoundaryCheck.Check3DValueExistGrid(segm_id, "SEGMID", self._num_lyr, self._num_row,
                                                      self._num_col, SegIdList)
        self.streamValue.WatDrnData = {"DELEV": delev, "COND": cond, "SEGMID": segm_id}

    def load_ctrlPars_file(self, ctrlParFile):
        with open(ctrlParFile, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 10:
            raise ValueError("The Stream(STR) Control Params Attribute file header should have 10 fields.")
        data = lines[1].strip().split()
        if len(data) != 10:
            raise ValueError("The Stream(STR) Control Params Attribute file data line should have 10 values.")
        lines = lines[1:]
        ctrl_pars_data = {}
        for line in lines:
            line = line.strip().split()
            stream_id = int(line[0]) - 1
            if stream_id not in ctrl_pars_data:
                ctrl_pars_data[stream_id] = (int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]),
                                             int(line[6]), int(line[7]), int(line[8]), int(line[9]))
            else:
                raise ValueError(f"The stream ID {stream_id} already exists. Stream IDs should be unique.")
        self.streamValue.ControlParams = ctrl_pars_data

    def load_period_file(self, period_file: str):
        with open(period_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 14:
            raise ValueError("The Stream(STR) Period Params Attribute file(STRPer.txt) header should have 14 fields.")
        if len(lines[1].strip().split()) != 14:
            raise ValueError(
                "The Stream(STR) Period Params Attribute file(STRPer.txt) data line should have 14 values.")
        lines = lines[1:]
        period_data = {}
        for line in lines:
            line = line.strip().split()
            period_id = int(line[0]) - 1
            stream_id = int(line[1]) - 1
            if stream_id not in period_data:
                period_data[stream_id] = {}
            if period_id not in period_data[stream_id]:
                period_data[stream_id][period_id] = (
                    int(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7]),
                    float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]))
        self.streamValue.PeriodData = period_data

    def load_strGrid_file(self, strGridFile: str):
        with open(strGridFile, 'r') as file:
            CELLID = {}
            LEN = {}
            BTM = {}
            BWDT = {}
            SIZH1 = {}
            SIZH2 = {}
            BVK = {}
            BTK = {}
            SLP = {}
            NDC = {}
            for line_num, line in enumerate(file, start=1):
                if line_num == 1:
                    continue
                line = line.strip()
                parts = line.split()
                if len(parts) != 14:
                    raise ValueError(
                        "The Stream grid cell data file should have 14 columns!(SEGMID	CELLID ILYR IROW ICOL"
                        " LEN BTM BWDT SIZH1 SIZH2 BVK BTK SLP NDC)")
                int_parts = [int(part) for part in parts[:5]]
                float_part = [float(part) for part in parts[5:]]
                if not int_parts[0] - 1 in CELLID:
                    CELLID[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    CELLID[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = int_parts[1]
                else:
                    CELLID[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = int_parts[1]

                if not int_parts[0] - 1 in LEN:
                    LEN[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    LEN[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[0]
                else:
                    LEN[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[0]

                if not int_parts[0] - 1 in BTM:
                    BTM[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    BTM[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[1]
                else:
                    BTM[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[1]

                if not int_parts[0] - 1 in BWDT:
                    BWDT[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    BWDT[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[2]
                else:
                    BWDT[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[2]

                if not int_parts[0] - 1 in SIZH1:
                    SIZH1[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    SIZH1[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[3]
                else:
                    SIZH1[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[3]

                if not int_parts[0] - 1 in SIZH2:
                    SIZH2[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    SIZH2[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[4]
                else:
                    SIZH2[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[4]

                if not int_parts[0] - 1 in BVK:
                    BVK[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    BVK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[5]
                else:
                    BVK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[5]

                if not int_parts[0] - 1 in BTK:
                    BTK[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    BTK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[6]
                else:
                    BTK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[6]

                if not int_parts[0] - 1 in SLP:
                    SLP[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    SLP[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[7]
                else:
                    SLP[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[7]

                if not int_parts[0] - 1 in NDC:
                    NDC[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                    NDC[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[8]
                else:
                    NDC[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[8]

            self.streamValue.GridData = {"CELLID": CELLID, "LEN": LEN, "BTM": BTM, "BWDT": BWDT, "SIZH1": SIZH1,
                                         "SIZH2": SIZH2, "BVK": BVK, "BTK": BTK, "SLP": SLP, "NDC": NDC}

    def load_watUse_file(self, watUseFile: str):
        with open(watUseFile, 'r') as file:
            WUREGID = np.zeros((self._num_lyr, self._num_row, self._num_col))
            RATIO = np.zeros((self._num_lyr, self._num_row, self._num_col))
            for line_num, line in enumerate(file, start=1):
                if line_num == 1:
                    continue
                line = line.strip()
                parts = line.split()
                if len(parts) != 5:
                    raise ValueError(
                        "The Stream grid cell data file should have 5 columns!(WUREGID  ILYR  IROW  ICOL  RATIO)")
                int_parts = [int(part) for part in parts[:4]]
                float_part = float(parts[4])
                WUREGID[int_parts[1] - 1, int_parts[2] - 1, int_parts[3] - 1] = int_parts[0]
                RATIO[int_parts[1] - 1, int_parts[2] - 1, int_parts[3] - 1] = float_part
            self.streamValue.WatUseData = {"WUREGID": WUREGID, "RATIO": RATIO}

    def load_watDrn_file(self, watDrnFile: str):
        with open(watDrnFile, 'r') as file:
            DELEV = np.zeros((self._num_lyr, self._num_row, self._num_col))
            COND = np.zeros((self._num_lyr, self._num_row, self._num_col))
            SEGMID = np.zeros((self._num_lyr, self._num_row, self._num_col))
            for line_num, line in enumerate(file, start=1):
                if line_num == 1:
                    continue
                line = line.strip()
                parts = line.split()
                if len(parts) != 6:
                    raise ValueError(
                        "The Stream grid cell data file should have 6 columns!(ILYR  IROW  ICOL  DELEV  COND  SEGMID)")
                int_parts = [int(part) for part in parts[:3]]
                float_part = [float(part) for part in parts[3:]]
                DELEV[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[0]
                COND[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[1]
                SEGMID[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[2]
            self.streamValue.WatDrnData = {"DELEV": DELEV, "COND": COND, "SEGMID": SEGMID}

    @staticmethod
    def __is_consecutive_dict_keys(key_list):
        if not key_list:
            return False
        sorted_keys = sorted(key_list)
        return sorted_keys == list(range(sorted_keys[0], sorted_keys[-1] + 1))

    @classmethod
    def load(cls, model, ctrl_pars_file: str, period_file: str, grid_file: str, watUse_file: str, watDrn_file: str):
        """
        Load parameters from STR(STRCtrl.in, RESPer.in, RESGrd.in) file and create a ComusStr instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        ctrl_pars_file: str
            STR Control Params File Path(STRCtrl.in).
        period_file: str
            STR Period Params File Path(STRPer.in).
        grid_file: str
            STR Grid Params File Path(STRGrd.in).
        watUse_file: str
            STR WaterUse Params FilePath(STRWatUse.in).
        watDrn_file: str
            STR WaterDrain Params FilePath(STRWatDrn.in).

        Returns:
        --------
        instance: pycomus.ComusStr
            COMUS Stream(STR) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> strPackage = pycomus.ComusRes.load(model1, "./InputFiles/STRCtrl.in", "./InputFiles/STRPer.in",
        >>> "./InputFiles/STRGrd.in", "./InputFiles/STRWatUse.in", "./InputFiles/STRWatDrn.in")
        """
        num_lyr = model.CmsDis.num_lyr
        num_row = model.CmsDis.num_row
        num_col = model.CmsDis.num_col

        # load ctrl_pars_file
        with open(ctrl_pars_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 10:
            raise ValueError("The Stream(STR) Control Params Attribute file header should have 10 fields.")
        if len(lines[1].strip().split()) != 10:
            raise ValueError("The Stream(STR) Control Params Attribute file data line should have 10 values.")
        lines = lines[1:]
        ctrl_pars_data = {}
        for line in lines:
            line = line.strip().split()
            stream_id = int(line[0]) - 1
            if stream_id not in ctrl_pars_data:
                ctrl_pars_data[stream_id] = (int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]),
                                             int(line[6]), int(line[7]), int(line[8]), int(line[9]))
            else:
                raise ValueError(f"The stream ID {stream_id} already exists. Stream IDs should be unique.")
        instance = cls(model, stream_num=len(ctrl_pars_data))
        instance.set_ControlData(ctrl_pars_data)

        # load period_file
        with open(period_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 14:
            raise ValueError("The Stream(STR) Period Params Attribute file(STRPer.txt) header should have 14 fields.")
        if len(lines[1].strip().split()) != 14:
            raise ValueError(
                "The Stream(STR) Period Params Attribute file(STRPer.txt) data line should have 14 values.")
        lines = lines[1:]
        period_data = {}
        for line in lines:
            line = line.strip().split()
            period_id = int(line[0]) - 1
            stream_id = int(line[1]) - 1
            if stream_id not in period_data:
                period_data[stream_id] = {}
            if period_id not in period_data[stream_id]:
                period_data[stream_id][period_id] = (
                    int(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7]),
                    float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]))
        instance.set_PeriodData(period_data)

        # load grid_data
        with open(grid_file, 'r') as file:
            CELLID = {}
            LEN = {}
            BTM = {}
            BWDT = {}
            SIZH1 = {}
            SIZH2 = {}
            BVK = {}
            BTK = {}
            SLP = {}
            NDC = {}
            for line_num, line in enumerate(file, start=1):
                if line_num == 1:
                    continue
                line = line.strip()
                parts = line.split()
                if len(parts) != 14:
                    raise ValueError(
                        "The Stream grid cell data file should have 14 columns!(SEGMID	CELLID ILYR IROW ICOL"
                        " LEN BTM BWDT SIZH1 SIZH2 BVK BTK SLP NDC)")
                int_parts = [int(part) for part in parts[:5]]
                float_part = [float(part) for part in parts[5:]]
                if not int_parts[0] - 1 in CELLID:
                    CELLID[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    CELLID[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = int_parts[1]
                else:
                    CELLID[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = int_parts[1]

                if not int_parts[0] - 1 in LEN:
                    LEN[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    LEN[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[0]
                else:
                    LEN[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[0]

                if not int_parts[0] - 1 in BTM:
                    BTM[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    BTM[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[1]
                else:
                    BTM[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[1]

                if not int_parts[0] - 1 in BWDT:
                    BWDT[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    BWDT[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[2]
                else:
                    BWDT[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[2]

                if not int_parts[0] - 1 in SIZH1:
                    SIZH1[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    SIZH1[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[3]
                else:
                    SIZH1[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[3]

                if not int_parts[0] - 1 in SIZH2:
                    SIZH2[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    SIZH2[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[4]
                else:
                    SIZH2[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[4]

                if not int_parts[0] - 1 in BVK:
                    BVK[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    BVK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[5]
                else:
                    BVK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[5]

                if not int_parts[0] - 1 in BTK:
                    BTK[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    BTK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[6]
                else:
                    BTK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[6]

                if not int_parts[0] - 1 in SLP:
                    SLP[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    SLP[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[7]
                else:
                    SLP[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[7]

                if not int_parts[0] - 1 in NDC:
                    NDC[int_parts[0] - 1] = np.zeros((num_lyr, num_row, num_col))
                    NDC[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[8]
                else:
                    NDC[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[8]

            instance.set_GridData(CELLID, LEN, BTM, BWDT, SIZH1, SIZH2, BVK, BTK, SLP, NDC)

        # load water use file
        with open(watUse_file, 'r') as file:
            WUREGID = np.zeros((num_lyr, num_row, num_col))
            RATIO = np.zeros((num_lyr, num_row, num_col))
            for line_num, line in enumerate(file, start=1):
                if line_num == 1:
                    continue
                line = line.strip()
                parts = line.split()
                if len(parts) != 5:
                    raise ValueError(
                        "The Stream grid cell data file should have 5 columns!(WUREGID  ILYR  IROW  ICOL  RATIO)")
                int_parts = [int(part) for part in parts[:4]]
                float_part = float(parts[4])
                WUREGID[int_parts[1] - 1, int_parts[2] - 1, int_parts[3] - 1] = int_parts[0]
                RATIO[int_parts[1] - 1, int_parts[2] - 1, int_parts[3] - 1] = float_part
            instance.set_WatUseData(WUREGID, RATIO)

        # load water drain file
        with open(watDrn_file, 'r') as file:
            DELEV = np.zeros((num_lyr, num_row, num_col))
            COND = np.zeros((num_lyr, num_row, num_col))
            SEGMID = np.zeros((num_lyr, num_row, num_col))
            for line_num, line in enumerate(file, start=1):
                if line_num == 1:
                    continue
                line = line.strip()
                parts = line.split()
                if len(parts) != 6:
                    raise ValueError(
                        "The Stream grid cell data file should have 6 columns!(ILYR  IROW  ICOL  DELEV  COND  SEGMID)")
                int_parts = [int(part) for part in parts[:3]]
                float_part = [float(part) for part in parts[3:]]
                DELEV[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[0]
                COND[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[1]
                SEGMID[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[2]
            instance.set_WatDrnData(DELEV, COND, SEGMID)
        return instance


class Stream:
    def __init__(self):
        self.ControlParams = None
        self.PeriodData = None
        self.GridData = None
        self.WatUseData = None
        self.WatDrnData = None
