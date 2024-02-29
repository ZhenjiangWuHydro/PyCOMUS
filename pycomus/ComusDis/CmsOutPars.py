# --------------------------------------------------------------
# CmsOutPars.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model Output Parameter Attributes.
# --------------------------------------------------------------
import os

from pycomus.Utils.CONST_VALUE import OUT_PKG_NAME, OUT_FILE_NAME


class ComusOutputPars:
    def __init__(self, model, gdw_bd: int = 1, lyr_bd: int = 1, cell_bd: int = 1, cell_hh: int = 1,
                 cell_dd: int = 1, cell_flp: int = 1, lak_bd: int = 1, segm_bd: int = 1, rech_bd: int = 1,
                 ibs: int = 1, sub: int = 1, ndb: int = 1, db: int = 1, reg_bd: int = 1):
        """
        Set COMUS Model Output Params Attributes.
            0: No output;

            1: Output for each simulation time step within a period;

            2: Output for each period.


        Parameters:
        ----------------------------
        model:
            COMUS Model Object
        gdw_bd: int
            Groundwater system balance output control option.
        lyr_bd: int
            Layer balance output control option.
        cell_bd: int
            Grid cell balance output control option.
        cell_hh: int
            Grid cell head output control option.
        cell_dd: int
            Grid cell draw down output control option.
        cell_flp: int
            Inter-cell flow output control option.
        lak_bd: int
            Lake balance output control option.
        segm_bd: int
            Stream channel balance output control option.
        rech_bd: int
            Stream segment balance output control option.
        ibs: int
            Interbed simulation results output control option.
        sub: int
            Grid cell land subsidence simulation results output control option.
        ndb: int
            For no-delay interbed simulation results output control option.
        db: int
            For delayed interbed simulation results output control option.
        reg_bd: int
            Regional water balance output control option.

        Returns:
        --------
        instance: pycomus.ComusConPars
            COMUS Control Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim")
        >>> outParams = pycomus.ComusOutputPars(model1, 2, 2, 2, 2, 2, 2)
        """
        self.__params = {
            'gdw_bd': gdw_bd,
            'lyr_bd': lyr_bd,
            'cell_bd': cell_bd,
            'cell_hh': cell_hh,
            'cell_dd': cell_dd,
            'cell_flp': cell_flp,
            'lak_bd': lak_bd,
            'segm_bd': segm_bd,
            'rech_bd': rech_bd,
            'ibs': ibs,
            'sub': sub,
            'ndb': ndb,
            'db': db,
            'reg_bd': reg_bd,
        }
        self._model = model

        for param_name, param_value in self.__params.items():
            if param_value not in {0, 1, 2}:
                raise ValueError(f'"{param_name}" parameter is invalid. It should be between 0 and 2. Please check!')

        self.gdw_bd = gdw_bd
        self.lyr_bd = lyr_bd
        self.cell_bd = cell_bd
        self.cell_hh = cell_hh
        self.cell_dd = cell_dd
        self.cell_flp = cell_flp
        self.lak_bd = lak_bd
        self.segm_bd = segm_bd
        self.rech_bd = rech_bd
        self.ibs = ibs
        self.sub = sub
        self.ndb = ndb
        self.db = db
        self.reg_bd = reg_bd
        model.package[OUT_PKG_NAME] = self

    @classmethod
    def load(cls, model, output_params_file: str):
        """
        Load parameters from a load OutOpt.in file and create a ComusOutputPars instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        output_params_file: str
            Output Params file path.

        Returns:
        --------
        instance: pycomus.ComusConPars
            COMUS Control Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")
        >>> outParams = pycomus.ComusOutputPars.load(model1, "./InputFiles/OutOpt.in")
        """
        with open(output_params_file, 'r') as file:
            lines = file.readlines()
        if len(lines) != 2:
            raise ValueError("The Output Params file should have exactly two lines of data.")
        if len(lines[0].strip().split()) != 14:
            raise ValueError("The Output Params file should have 14 fields.")

        data = lines[1].strip().split()
        if len(data) != 14:
            raise ValueError("The Output Params data line should have 14 values.")

        instance = cls(model,
                       gdw_bd=int(data[0]),
                       lyr_bd=int(data[1]),
                       cell_bd=int(data[2]),
                       cell_hh=int(data[3]),
                       cell_dd=int(data[4]),
                       cell_flp=int(data[5]),
                       lak_bd=int(data[6]),
                       segm_bd=int(data[7]),
                       rech_bd=int(data[8]),
                       ibs=int(data[9]),
                       sub=int(data[10]),
                       ndb=int(data[11]),
                       db=int(data[12]),
                       reg_bd=int(data[13]))
        return instance

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusOutputPars`
        module to the specified path as <OutOpt.in>.

        :param folder_path: Output folder path.
        """
        with open(os.path.join(folder_path, OUT_FILE_NAME), "w") as file:
            file.write(
                "GDWBDPRN  LYRBDPRN  CELLBDPRN  CELLHHPRN  CELLDDPRN  CELLFLPRN  LAKBDPRN  SEGMBDPRN  RECHBDPRN  "
                "IBSPRN  SUBPRN  NDBPRN  DBPRN  REGBDPRN\n")
            file.write(f"{self.gdw_bd}  {self.lyr_bd}  {self.cell_bd}  {self.cell_hh}  "
                       f"{self.cell_dd}  {self.cell_flp}  {self.lak_bd}  {self.segm_bd}  "
                       f"{self.rech_bd}  {self.ibs}  {self.sub}  {self.ndb}  {self.db}  "
                       f"{self.reg_bd}")
