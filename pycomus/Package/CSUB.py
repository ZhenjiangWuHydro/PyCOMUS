# --------------------------------------------------------------
# CSUB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With SUB Package.
# --------------------------------------------------------------\
from typing import Dict, Union, List

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck


class ComusSub:
    def __init__(self, model: pycomus.ComusModel, num_ndb: int, num_db: int, num_mz: int, nn: int = 20,
                 acc: float = 0.5, it_min: int = 5, dsh_opt: int = 2):
        """
        Initialize the COMUS Model with the Subsidence(SUB) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the SUB package will be applied.
        num_ndb:
            Number of delayed interbedded body groups without delay.
        num_db:
            Number of delayed interbedded bodies.
        num_mz:
            Only valid when num_ndb > 0, indicating the number of media zones.
        nn:
            Number of discrete points on the half thickness of equivalent interbedded bodies.
        acc:
            Representing the simulation acceleration parameter of delayed interbedded bodies.
        it_min:
            The effective value should be greater than or equal to 2, typically set to 5.
        dsh_opt:
            Representing the option for determining the initial head values of delayed interbedded bodies.

        Returns:
        --------
        instance: pycomus.ComusSub
           COMUS Subsidence(SUB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> subPackage = pycomus.ComusSub(model, 2, 2, 10)
        """

        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        if num_ndb < 0 or num_db < 0:
            raise ValueError("The parameters num_ndb and num_db must be greater than or equal to 0. Please check!")
        if num_ndb + num_db == 0:
            raise ValueError(
                "The parameters num_ndb and num_db must have at least one value not equal to 0. Please check!")
        if num_db > 0:
            if num_mz <= 0:
                raise ValueError(
                    "When simulating delayed confining units, the num_mz parameter cannot be set to 0. Please check!")
            if nn <= 5 or nn >= 100:
                raise ValueError("The valid range for the nn parameter is 5 to 100. Please check!")
            if acc < 0 or acc > 0.6:
                raise ValueError("The valid range for the acc parameter is 0.0 to 0.6. Please check!")
            if dsh_opt not in (1, 2):
                raise ValueError("The dsh_opt parameter must be either 1 or 2. Please check!")
        self._num_ndb = num_ndb
        self._num_db = num_db
        self._num_mz = num_mz
        self._nn = nn
        self._acc = acc
        self._it_min = it_min
        self._dsh_opt = dsh_opt
        self.subValue: LandSub = LandSub()
        self.subValue.ctrl_params = (num_ndb, num_db, num_mz, nn, acc, it_min, dsh_opt)
        model.package["SUB"] = self

    def set_mz_data(self, mz_data: Union[Dict[int, (float, float, float)], List[(float, float, float)]]):
        """

        :param mz_data:
        :return:
        """
        mz_data_len = len(mz_data)
        mz_dict_data: Dict = {}
        if mz_data_len != self._num_mz:
            raise ValueError(f"The length of mz_data should be consistent with num_mz({self._num_mz})!")
        if isinstance(mz_data, dict):
            if sorted(mz_data.keys()) != [i for i in range(self._num_mz)]:
                raise ValueError(f"The keys of mz_data should start from 0 and be less than {self._num_mz}.")
            mz_dict_data = mz_data
        elif isinstance(mz_data, List):
            for i in range(self._num_mz):
                mz_dict_data[i] = mz_data[i]
        else:
            raise ValueError(
                "mz_data should be of type Dict[int, (float, float, float)] or List[(float, float, float)].")
        for value in mz_dict_data.values():
            if len(value) != 3:
                raise ValueError("The values of mz_data should consist of three elements (MZVK, MZSFE, MZSFV).")
            if value[0] < 0 or value[1] < 0 or value[2] < 0:
                raise ValueError(
                    "The fields MZVK, MZSFE, and MZSFV must be greater than or equal to 0.0. Please check!")
        self.subValue.mz = mz_dict_data

    def set_ndb_lyr(self, ndb_lyr: Union[Dict[int, int], List[int]]):
        """

        :param ndb_lyr:
        :return:
        """
        ndb_lyr_len: int = len(ndb_lyr)
        ndb_lyr_dict: Dict = {}
        if ndb_lyr_len != self._num_ndb:
            raise ValueError(f"The length of ndb_lyr should be consistent with num_ndb({self._num_ndb})!")
        if isinstance(ndb_lyr, Dict):
            if sorted(ndb_lyr.keys()) != [i for i in range(self._num_ndb)]:
                raise ValueError(f"The keys of ndb_lyr should start from 0 and be less than {self._num_ndb}.")
            ndb_lyr_dict = ndb_lyr
        elif isinstance(ndb_lyr, List):
            for i in range(self._num_ndb):
                ndb_lyr_dict[i] = ndb_lyr[i]
        else:
            raise ValueError("ndb_lyr should be of type Dict[int, int] or List[int].")
        for value in ndb_lyr_dict.values():
            if value < 0 or value >= self._num_lyr:
                raise ValueError(
                    f"The value of ndb_lyr should be greater than or equal to 0 and less than {self._num_lyr}.")
        self.subValue.ndb_lyr = ndb_lyr_dict

    def set_ndb_grid(self, hc: np.ndarray, sfe: np.ndarray, sfv: np.ndarray, com: np.ndarray):
        """

        :param hc:
        :param sfe:
        :param sfv:
        :param com:
        :return:
        """
        hc = BoundaryCheck.Check3DValueFormat(hc, "HC", self._num_lyr, self._num_row, self._num_col)
        sfe = BoundaryCheck.Check3DValueGtZero(sfe, "SFE", self._num_lyr, self._num_row, self._num_col)
        sfv = BoundaryCheck.Check3DValueGtZero(sfv, "SFV", self._num_lyr, self._num_row, self._num_col)
        com = BoundaryCheck.Check3DValueFormat(com, "COM", self._num_lyr, self._num_row, self._num_col)
        self.subValue.ndb_grid = {"HC": hc, "SFE": sfe, "SFV": sfv, "COM": com}

    def set_db_lyr(self, db_lyr: Union[Dict[int, int], List[int]]):
        """

        :param db_lyr:
        :return:
        """
        db_lyr_len: int = len(db_lyr)
        db_lyr_dict: Dict = {}
        if db_lyr_len != self._num_db:
            raise ValueError(f"The length of db_lyr should be consistent with num_db({self._num_db})!")
        if isinstance(db_lyr, Dict):
            if sorted(db_lyr.keys()) != [i for i in range(self._num_db)]:
                raise ValueError(f"The keys of db_lyr should start from 0 and be less than {self._num_db}.")
            db_lyr_dict = db_lyr
        elif isinstance(db_lyr, List):
            for i in range(self._num_db):
                db_lyr_dict[i] = db_lyr[i]
        else:
            raise ValueError("db_lyr should be of type Dict[int, int] or List[int].")
        for value in db_lyr_dict.values():
            if value < 0 or value >= self._num_lyr:
                raise ValueError(
                    f"The value of db_lyr should be greater than or equal to 0 and less than {self._num_lyr}.")
        self.subValue.db_lyr = db_lyr_dict

    def set_db_grid(self, rnb: np.ndarray, dsh: np.ndarray, dhc: np.ndarray, dcom: np.ndarray, dz: np.ndarray,
                    imz: np.ndarray):
        """

        :param rnb:
        :param dsh:
        :param dhc:
        :param dcom:
        :param dz:
        :param imz:
        :return:
        """
        rnb = BoundaryCheck.Check3DValueFormat(rnb, "RNB", self._num_lyr, self._num_row, self._num_col)
        dsh = BoundaryCheck.Check3DValueFormat(dsh, "DSH", self._num_lyr, self._num_row, self._num_col)
        dhc = BoundaryCheck.Check3DValueFormat(dhc, "DHC", self._num_lyr, self._num_row, self._num_col)
        dcom = BoundaryCheck.Check3DValueFormat(dcom, "DCOM", self._num_lyr, self._num_row, self._num_col)
        dz = BoundaryCheck.Check3DValueFormat(dz, "DZ", self._num_lyr, self._num_row, self._num_col)
        imz = BoundaryCheck.Check3DValueFormat(imz, "IMZ", self._num_lyr, self._num_row, self._num_col)
        self.subValue.db_grid = {"RNB": rnb, "DSH": dsh, "DHC": dhc, "DCOM": dcom, "DZ": dz, "IMZ": imz}

class LandSub:
    def __init__(self):
        self.ctrl_params = None
        self.mz = None
        self.ndb_lyr = None
        self.ndb_grid = None
        self.db_lyr = None
        self.db_grid = None
