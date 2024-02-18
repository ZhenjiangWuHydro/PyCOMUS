# --------------------------------------------------------------
# CSTR.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With STR Package.
# --------------------------------------------------------------
from typing import Dict, Tuple, Union
from collections import OrderedDict
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


    def setControlParams(self, control_params: Dict[int, Tuple[int, int, int, int, int, int, int, int, int]]) -> None:
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

    def setPeriodData(self, period_data: Dict[int, Dict[
        int, Tuple[int, float, float, float, float, float, float, float, float, float, float, float]]]) -> None:
        """
        Set Stream Period Data.

        :param period_data:
            A Dict type data where the keys represent the stream IDs, and the values are Dicts with Period IDs as
            keys. Within the inner Dicts, the values are Tuples containing four elements: (HCALOPT, USLEV, UELEV, DSLEV, DELEV, WATPNT,"
            WATWAY, WATDIV, WATUSE, EVRATE, RCHCOE, WBKCOE)

        :param period_data:
        :return:
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

                    else:
                        if value[7] < 0 and value[7] > 1:
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
                if value[8] > 0 and self.streamValue.ControlParams[str_id][6] >= 1 and self.streamValue.ControlParams[str_id][
                    7] == 1:
                    if value[10] + value[11] > 1:
                        raise ValueError(
                            f"The sum of RCHCOE and WBKCOE data for period {period_id} of river segment with ID {str_id} must be less than 1.0. Please check!")
        self.streamValue.PeriodData = period_data

    def setGridData(self, CELLID: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    LEN: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    BTM: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    BWDT: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    SIZH1: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    SIZH2: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    BVK: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    BTK: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    SLP: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                    NDC: Union[int, float, Dict[int, Union[int, float, np.ndarray]]], ) -> None:
        """
        Set Stream Grid Cell Data.

        :param CELLID:
            CELLID is an integer representing the sequential upstream and downstream order of the river segment within
            its parent river unit (1 indicates that the river segment is the first segment of the river unit).
        :param LEN:
            LEN is a double precision floating-point number representing the length of the river segment within the grid cell (L).
        :param BTM:
            BTM is a double precision floating-point number representing the average bed elevation of the river segment (L).
        :param BWDT:
            BWDT is a double precision floating-point number representing the average bed width of the river segment (L).
        :param SIZH1:
            SIZH1 is a double precision floating-point number representing the reciprocal of the left bank slope of the river segment (L/L).
        :param SIZH2:
            SIZH2 is a double precision floating-point number representing the reciprocal of the right bank slope of the river segment (L/L).
        :param BVK:
            BVK is a double precision floating-point number representing the permeability coefficient of the low-permeability medium of the river segment (L/T).
        :param BTK:
            BTK is a double precision floating-point number representing the thickness of the low-permeability medium of the river segment (L).
        :param SLP:
            SLP is a double precision floating-point number representing the average bed slope of the river segment (L/L).
        :param NDC:
            NDC is a double precision floating-point number representing the Manning's roughness coefficient (n) of the river segment.
        """
        strIds = [i for i in range(self._stream_num)]
        CELLID = BoundaryCheck.CheckValueGtZero(CELLID, "CELLID", strIds, self._num_lyr, self._num_row,
                                                self._num_col)
        LEN = BoundaryCheck.CheckValueGtZero(LEN, "LEN", strIds, self._num_lyr, self._num_row, self._num_col)
        BTM = BoundaryCheck.CheckValueGtZero(BTM, "BTM", strIds, self._num_lyr, self._num_row, self._num_col)
        BWDT = BoundaryCheck.CheckValueGtZero(BWDT, "BWDT", strIds, self._num_lyr, self._num_row, self._num_col)
        SIZH1 = BoundaryCheck.CheckValueGtZero(SIZH1, "SIZH1", strIds, self._num_lyr, self._num_row,
                                               self._num_col)
        SIZH2 = BoundaryCheck.CheckValueGtZero(SIZH2, "SIZH2", strIds, self._num_lyr, self._num_row,
                                               self._num_col)
        BVK = BoundaryCheck.CheckValueGtZero(BVK, "BVK", strIds, self._num_lyr, self._num_row, self._num_col)
        BTK = BoundaryCheck.CheckValueGtZero(BTK, "BTK", strIds, self._num_lyr, self._num_row, self._num_col)
        SLP = BoundaryCheck.CheckValueGtZero(SLP, "SLP", strIds, self._num_lyr, self._num_row, self._num_col)
        NDC = BoundaryCheck.CheckValueGtZero(NDC, "NDC", strIds, self._num_lyr, self._num_row, self._num_col)

        if sorted(CELLID.keys()) != sorted(LEN.keys()) != sorted(BTM.keys()) != sorted(BWDT.keys()) != sorted(
                SIZH1.keys()) != sorted(SIZH2.keys()) != sorted(BVK.keys()) != sorted(BTK.keys()) != sorted(
            SLP.keys()) != sorted(NDC.keys()):
            raise ValueError(
                "The StreamId for the 'CELLID','LEN','BTM','BWDT','SIZH1','SIZH2','BVK','BTK','SLP' and 'NDC' should be the same.")
        self.streamValue.GridData = {"CELLID": CELLID, "LEN": LEN, "BTM": BTM, "BWDT": BWDT, "SIZH1": SIZH1,
                                  "SIZH2": SIZH2, "BVK": BVK, "SLP": SLP, "DC": NDC}

    def setWatUseGrid(self, WUREGID: Union[int, np.ndarray], RATIO: Union[int, float, np.ndarray]) -> None:
        """
        Set Stream Water Use Data.

        :param WUREGID:
            WUREGID is an integer representing the water use zone number for the river unit (starting from 1). A portion
             of the river unit's water use will be allocated to simulate surface infiltration recharge on grid cells
             within the range of this water use zone.
        :param RATIO:
            RATIO is a double precision floating-point number representing the weight coefficient of surface infiltration
            recharge for the river unit on the grid cell (-). It must be greater than or equal to 0.
        """
        wuGrdIdList = [value[6] for value in self.__stream.ControlParams.values()]
        WUREGID = BoundaryCheck.Check3DValueExistGrid(WUREGID, "WUREGID", self._num_lyr, self._num_row,
                                                      self._num_col, wuGrdIdList)
        RATIO = BoundaryCheck.Check3DValueGtZero(RATIO, "RATIO", self._num_lyr, self._num_row,
                                                 self._num_col)
        self.__stream.WatUseData = [WUREGID, RATIO]

    def setWatDrnGrid(self, DELEV: Union[int, np.ndarray], COND: Union[int, float, np.ndarray],
                      SEGMID: Union[int, float, np.ndarray]) -> None:
        """
        Set Stream Water Drn Data.

        :param DELEV:
            DELEV is a double precision floating-point number representing the elevation of the drainage ditch bottom
            at the grid cell (in meters). The drainage ditch only discharges groundwater when the groundwater level
            is higher than this elevation.
        :param COND:
            COND is a double precision floating-point number representing the hydraulic conductivity coefficient between
             the drainage ditch and the aquifer at the grid cell (in square meters per second).
        :param SEGMID:
            SEGMID is a double precision floating-point number representing the drainage area number, which is the
            identifier of the river segment of the seasonal river to which the grid cell drainage flows (starting from 1).
        """
        SegIdList = list(self.__stream.ControlParams.keys())
        DELEV = BoundaryCheck.Check3DValueFormat(DELEV, "DELEV", self._num_lyr, self._num_row, self._num_col)
        COND = BoundaryCheck.Check3DValueGtZero(COND, "COND", self._num_lyr, self._num_row, self._num_col)
        SEGMID = BoundaryCheck.Check3DValueExistGrid(SEGMID, "SEGMID", self._num_lyr, self._num_row,
                                                     self._num_col, SegIdList)
        self.__stream.WatUseData = [DELEV, COND, SEGMID]

    def loadCtrlParFile(self, ctrlFile: str):
        with open(ctrlFile, 'r') as file:
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
                else:
                    CELLID[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = int_parts[1]

                if not int_parts[0] - 1 in LEN:
                    LEN[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    LEN[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[0]

                if not int_parts[0] - 1 in BTM:
                    BTM[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    BTM[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[1]

                if not int_parts[0] - 1 in BWDT:
                    BWDT[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    BWDT[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[2]

                if not int_parts[0] - 1 in SIZH1:
                    SIZH1[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    SIZH1[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[3]

                if not int_parts[0] - 1 in SIZH2:
                    SIZH2[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    SIZH2[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[4]

                if not int_parts[0] - 1 in BVK:
                    BVK[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    BVK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[5]

                if not int_parts[0] - 1 in BTK:
                    BTK[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    BTK[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[5]

                if not int_parts[0] - 1 in SLP:
                    SLP[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    SLP[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[6]

                if not int_parts[0] - 1 in NDC:
                    NDC[int_parts[0] - 1] = np.zeros((self._num_lyr, self._num_row, self._num_col))
                else:
                    NDC[int_parts[0] - 1][int_parts[2] - 1, int_parts[3] - 1, int_parts[4] - 1] = float_part[7]

            self.__stream.GridData = {"CELLID": CELLID, "LEN": LEN, "BTM": BTM, "BWDT": BWDT, "SIZH1": SIZH1,
                                  "SIZH2": SIZH2, "BVK": BVK, "SLP": SLP, "DC": NDC}

    def loadWatUseFile(self, watUseFile: str):
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
                WUREGID[int_parts[1] - 1,int_parts[2] - 1,int_parts[3] - 1] = int_parts[0]
                WUREGID[int_parts[1] - 1, int_parts[2] - 1, int_parts[3] - 1] = float_part
            self.__stream.WatUseData = [WUREGID, RATIO]

    def loadWatDrnFile(self, watDrnFile: str):
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
                float_part =[float(part) for part in parts[3:]]
                DELEV[int_parts[0] - 1,int_parts[1] - 1,int_parts[2] - 1] = float_part[0]
                COND[int_parts[0] - 1,int_parts[1] - 1,int_parts[2] - 1] = float_part[1]
                SEGMID[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[2]
            self.__stream.WatUseData = [DELEV, COND, SEGMID]


    def __is_consecutive_dict_keys(self, key_list):
        if not key_list:
            return False
        sorted_keys = sorted(key_list)
        return sorted_keys == list(range(sorted_keys[0], sorted_keys[-1] + 1))


class Stream:
    def __init__(self):
        self.ControlParams = None
        self.PeriodData = None
        self.GridData = None
        self.WatUseData = None
        self.WatDrnData = None
