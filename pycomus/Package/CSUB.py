# --------------------------------------------------------------
# CSUB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With SUB Package.
# --------------------------------------------------------------\
import os
from typing import Dict, Union, List, Tuple

import numpy as np

import pycomus
from pycomus.Utils import BoundaryCheck
from pycomus.Utils.CONSTANTS import SUB_PKG_NAME, SUB_DB_GRID_FILE_NAME, SUB_NDB_GRID_FILE_NAME, SUB_DB_FILE_NAME, \
    SUB_NDB_FILE_NAME, SUB_MZ_FILE_NAME, SUB_CTRL_FILE_NAME


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

        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        cms_period = BoundaryCheck.get_period(model)
        self._num_lyr = cms_dis.num_lyr
        self._num_row = cms_dis.num_row
        self._num_col = cms_dis.num_col
        self._period = cms_period.period
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
        model.package[SUB_PKG_NAME] = self

    def set_mz_data(self, mz_data: Union[Dict[int, Tuple[float, float, float]], List[Tuple[float, float, float]]]):
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

    def set_ndb_grid(self, hc: Union[int, float, np.ndarray], sfe: Union[int, float, np.ndarray],
                     sfv: Union[int, float, np.ndarray], com: Union[int, float, np.ndarray]):
        """

        :param hc:
        :param sfe:
        :param sfv:
        :param com:
        :return:
        """
        if isinstance(hc, (int, float)):
            hc = np.full((self._num_ndb, self._num_row, self._num_col), hc, dtype=float)
        if isinstance(sfe, (int, float)):
            sfe = np.full((self._num_ndb, self._num_row, self._num_col), sfe, dtype=float)
        if isinstance(sfv, (int, float)):
            sfv = np.full((self._num_ndb, self._num_row, self._num_col), sfv, dtype=float)
        if isinstance(com, (int, float)):
            com = np.full((self._num_ndb, self._num_row, self._num_col), com, dtype=float)
        hc = BoundaryCheck.check_3d_format(hc, "HC", self._num_ndb, self._num_row, self._num_col)
        sfe = BoundaryCheck.check_3d_zero(sfe, "SFE", self._num_ndb, self._num_row, self._num_col)
        sfv = BoundaryCheck.check_3d_zero(sfv, "SFV", self._num_ndb, self._num_row, self._num_col)
        com = BoundaryCheck.check_3d_format(com, "COM", self._num_ndb, self._num_row, self._num_col)
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

    def set_db_grid(self, rnb: Union[int, float, np.ndarray], dsh: Union[int, float, np.ndarray],
                    dhc: Union[int, float, np.ndarray], dcom: Union[int, float, np.ndarray],
                    dz: Union[int, float, np.ndarray], imz: Union[int, float, np.ndarray]):
        """

        :param rnb:
        :param dsh:
        :param dhc:
        :param dcom:
        :param dz:
        :param imz:
        :return:
        """
        if isinstance(rnb, (int, float)):
            rnb = np.full((self._num_db, self._num_row, self._num_col), rnb, dtype=float)
        if isinstance(dsh, (int, float)):
            dsh = np.full((self._num_db, self._num_row, self._num_col), dsh, dtype=float)
        if isinstance(dhc, (int, float)):
            dhc = np.full((self._num_db, self._num_row, self._num_col), dhc, dtype=float)
        if isinstance(dcom, (int, float)):
            dcom = np.full((self._num_db, self._num_row, self._num_col), dcom, dtype=float)
        if isinstance(dz, (int, float)):
            dz = np.full((self._num_db, self._num_row, self._num_col), dz, dtype=float)
        if isinstance(imz, (int, float)):
            imz = np.full((self._num_db, self._num_row, self._num_col), imz, dtype=float)
        rnb = BoundaryCheck.check_3d_format(rnb, "RNB", self._num_db, self._num_row, self._num_col)
        dsh = BoundaryCheck.check_3d_format(dsh, "DSH", self._num_db, self._num_row, self._num_col)
        dhc = BoundaryCheck.check_3d_format(dhc, "DHC", self._num_db, self._num_row, self._num_col)
        dcom = BoundaryCheck.check_3d_format(dcom, "DCOM", self._num_db, self._num_row, self._num_col)
        dz = BoundaryCheck.check_3d_format(dz, "DZ", self._num_db, self._num_row, self._num_col)
        imz = BoundaryCheck.check_3d_format(imz, "IMZ", self._num_db, self._num_row, self._num_col)
        self.subValue.db_grid = {"RNB": rnb, "DSH": dsh, "DHC": dhc, "DCOM": dcom, "DZ": dz, "IMZ": imz}

    @classmethod
    def load(cls, model, ctrl_file: str, mz_file: str, ndb_lyr_file: str, ndb_grid_file: str, db_lyr_file: str,
             db_grid_file: str):
        """
        Load parameters from SUB(SUBCtrl.in, SUBMZ.in, SUBNDB.in, SUBGrdNDB.in, SUBDB.in, SUBGrdDB.in) file and
        create a ComusSub instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        ctrl_file: str
            SUB Control Params File Path(SUBCtrl.in).
        mz_file: str
            SUB MZ Params File Path(SUBMZ.in).
        ndb_lyr_file: str
            SUB NDB Layer Params File Path(SUBNDB.in).
        ndb_grid_file: str
            SUB NDB Grid Params FilePath(SUBGrdNDB.in).
        db_lyr_file: str
            SUB DB Layer Params FilePath(SUBDB.in).
        db_grid_file: str
            SUB DB Grid Params FilePath(SUBGrdDB.in).

        Returns:
        --------
        instance: pycomus.ComusSub
            COMUS Subsidence(SUB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> subPackage = pycomus.ComusSub.load(model1, "./InputFiles/SUBCtrl.in", "./InputFiles/SUBMZ.in",
        >>> "./InputFiles/SUBNDB.in", "./InputFiles/SUBGrdNDB.in", "./InputFiles/SUBDB.in", "./InputFiles/SUBGrdDB.in")
        """
        BoundaryCheck.check_bnd_queue(model)
        cms_dis = BoundaryCheck.get_cms_pars(model)
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col

        # load ctrl_file
        with open(ctrl_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 7:
            raise ValueError("The Subsidence(SUB) Control Params Attribute file header should have 7 fields.")
        if len(lines[1].strip().split()) != 7:
            raise ValueError("The Subsidence(SUB) Control Params Attribute file data line should have 7 values.")
        line = lines[1:]
        if len(line) != 1:
            raise ValueError("The <SUBCtrl.in> file should contain exactly one line of data.")
        line = line[0].strip().split()
        num_ndb = int(line[0])
        num_db = int(line[1])
        num_mz = int(line[2])
        instance = cls(model, int(line[0]), int(line[1]), int(line[2]), int(line[3]), float(line[4]), int(line[5]),
                       int(line[6]))

        # load mz_file
        with open(mz_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 4:
            raise ValueError(
                "The Subsidence(SUB) MZ Params Attribute file(SUBMZ.in) header should have 4 fields.")
        if len(lines[1].strip().split()) != 4:
            raise ValueError(
                "The Subsidence(SUB) MZ Params Attribute file(SUBMZ.in) data line should have 4 values.")
        lines = lines[1:]
        mz_id = [int(line[0]) for line in lines]
        if mz_id != [i for i in range(1, num_mz + 1)]:
            raise ValueError("IMZ should start from 1 and be continuous.")
        instance.set_mz_data(
            [(float(line.strip().split()[1]), float(line.strip().split()[2]), float(line.strip().split()[3])) for line
             in lines])

        # load ndb_lyr_file
        with open(ndb_lyr_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 2:
            raise ValueError(
                "The Subsidence(SUB) NDB Layers Params Attribute file(SUBNDB.in) header should have 2 fields.")
        if len(lines[1].strip().split()) != 2:
            raise ValueError(
                "The Subsidence(SUB) NDB Layers Params Attribute file(SUBNDB.in) data line should have 2 values.")
        lines = lines[1:]
        ndb_id = [int(line[0]) for line in lines]
        if ndb_id != [i for i in range(1, num_ndb + 1)]:
            raise ValueError("INDB should start from 1 and be continuous.")
        instance.set_ndb_lyr([int(line.strip().split()[1]) - 1 for line in lines])

        # load ndb_grid_file
        with open(ndb_grid_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 7:
            raise ValueError(
                "The Subsidence(SUB) NDB Grid Params Attribute file(SUBGrdNDB.in) header should have 7 fields.")
        if len(lines[1].strip().split()) != 7:
            raise ValueError(
                "The Subsidence(SUB) NDB Grid Params Attribute file(SUBGrdNDB.in) data line should have 7 values.")
        lines = lines[1:]
        hc = np.zeros((num_ndb, num_row, num_col))
        sfe = np.zeros((num_ndb, num_row, num_col))
        sfv = np.zeros((num_ndb, num_row, num_col))
        com = np.zeros((num_ndb, num_row, num_col))
        for line in lines:
            line = line.strip().split()
            ndb_id = int(line[0]) - 1
            row = int(line[1]) - 1
            col = int(line[2]) - 1
            hc[ndb_id, row, col] = float(line[3])
            sfe[ndb_id, row, col] = float(line[4])
            sfv[ndb_id, row, col] = float(line[5])
            com[ndb_id, row, col] = float(line[6])
        instance.set_ndb_grid(hc, sfe, sfv, com)

        # load db_lyr_file
        with open(db_lyr_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 2:
            raise ValueError(
                "The Subsidence(SUB) DB Layers Params Attribute file(SUBDB.in) header should have 2 fields.")
        if len(lines[1].strip().split()) != 2:
            raise ValueError(
                "The Subsidence(SUB) DB Layers Params Attribute file(SUBDB.in) data line should have 2 values.")
        lines = lines[1:]
        db_id = [int(line[0]) for line in lines]
        if db_id != [i for i in range(1, num_db + 1)]:
            raise ValueError("IDB should start from 1 and be continuous.")
        instance.set_db_lyr([int(line.strip().split()[1]) - 1 for line in lines])

        # load db_grid_file
        with open(db_grid_file, 'r') as file:
            lines = file.readlines()
        if len(lines[0].strip().split()) != 9:
            raise ValueError(
                "The Subsidence(SUB) DB Grid Params Attribute file(SUBGrdDB.in) header should have 9 fields.")
        if len(lines[1].strip().split()) != 9:
            raise ValueError(
                "The Subsidence(SUB) DB Grid Params Attribute file(SUBGrdDB.in) data line should have 9 values.")
        lines = lines[1:]
        rnb = np.zeros((num_db, num_row, num_col))
        dsh = np.zeros((num_db, num_row, num_col))
        dhc = np.zeros((num_db, num_row, num_col))
        dcom = np.zeros((num_db, num_row, num_col))
        dz = np.zeros((num_db, num_row, num_col))
        imz = np.zeros((num_db, num_row, num_col))
        for line in lines:
            line = line.strip().split()
            db_id = int(line[0]) - 1
            row = int(line[1]) - 1
            col = int(line[2]) - 1
            rnb[db_id, row, col] = float(line[3])
            dsh[db_id, row, col] = float(line[4])
            dhc[db_id, row, col] = float(line[5])
            dcom[db_id, row, col] = float(line[6])
            dz[db_id, row, col] = float(line[7])
            imz[db_id, row, col] = float(line[8])
        instance.set_db_grid(rnb, dsh, dhc, dcom, dz, imz)
        return instance

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusSub`
        module to the specified path as <SUBCtrl.in>, <SUBMZ.in>, <SUBNDB.in>, <SUBDB.in>, <SUBGrdNDB.in>, <SUBGrdDB.in>.

        :param folder_path: Output folder path.
        """
        ctrl_data = self.subValue.ctrl_params
        num_ndb = ctrl_data[0]
        num_db = ctrl_data[1]
        mz_data = self.subValue.mz
        ndb_lyr_data = self.subValue.ndb_lyr
        ndb_grid_data = self.subValue.ndb_grid
        db_lyr_data = self.subValue.db_lyr
        db_grid_data = self.subValue.db_grid
        with open(os.path.join(folder_path, SUB_CTRL_FILE_NAME), "w") as file:
            file.write("NNDB  NDB  NMZ  NN  ACC  ITMIN  DSHOPT\n")
            file.write(f"{ctrl_data[0]}  {ctrl_data[1]}  {ctrl_data[2]}  {ctrl_data[3]}  {ctrl_data[4]}  {ctrl_data[5]}"
                       f"  {ctrl_data[6]}\n")

        with open(os.path.join(folder_path, SUB_MZ_FILE_NAME), "w") as file:
            file.write("IMZ  MZVK  MZSFE  MZSFV\n")
            for key, value in mz_data.items():
                file.write(f"{key + 1}  {value[0]}  {value[1]}  {value[2]}\n")

        with open(os.path.join(folder_path, SUB_NDB_FILE_NAME), "w") as file:
            file.write("INDB  ILYR\n")
            for key, value in ndb_lyr_data.items():
                file.write(f"{key + 1}  {value + 1}\n")

        with open(os.path.join(folder_path, SUB_DB_FILE_NAME), "w") as file:
            file.write("IDB  ILYR\n")
            for key, value in db_lyr_data.items():
                file.write(f"{key + 1}  {value + 1}\n")

        with open(os.path.join(folder_path, SUB_NDB_GRID_FILE_NAME), "w") as file:
            file.write("INDB  IROW  ICOL  HC  SFE  SFV  COM\n")
            hc = ndb_grid_data["HC"]
            sfe = ndb_grid_data["SFE"]
            sfv = ndb_grid_data["SFV"]
            com = ndb_grid_data["COM"]
            for ndb in range(num_ndb):
                for row in range(self._num_row):
                    for col in range(self._num_col):
                        file.write(
                            f"{ndb + 1}  {row + 1}  {col + 1}  {hc[ndb, row, col]}  "
                            f"{sfe[ndb, row, col]}  {sfv[ndb, row, col]}  {com[ndb, row, col]}\n")

        with open(os.path.join(folder_path, SUB_DB_GRID_FILE_NAME), "w") as file:
            file.write("IDB  IROW  ICOL  RNB  DSH  DHC  DCOM  DZ  IMZ\n")
            rnb = db_grid_data["RNB"]
            dsh = db_grid_data["DSH"]
            dhc = db_grid_data["DHC"]
            dcom = db_grid_data["DCOM"]
            dz = db_grid_data["DZ"]
            imz = db_grid_data["IMZ"]
            for db in range(num_db):
                for row in range(self._num_row):
                    for col in range(self._num_col):
                        file.write(
                            f"{db + 1}  {row + 1}  {col + 1}  {rnb[db, row, col]}  {dsh[db, row, col]}  "
                            f"{dhc[db, row, col]}  {dcom[db, row, col]}  {dz[db, row, col]}  {imz[db, row, col]}\n")


class LandSub:
    def __init__(self):
        self.ctrl_params = None
        self.mz = None
        self.ndb_lyr = None
        self.ndb_grid = None
        self.db_lyr = None
        self.db_grid = None
