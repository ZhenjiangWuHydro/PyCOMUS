# --------------------------------------------------------------
# CmsPars.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model Control Parameter Attributes.
# --------------------------------------------------------------
import ctypes
import os
import platform
import sys
from typing import List

from pycomus.Utils.CONSTANTS import CON_PKG_NAME, CON_FILE_NAME, BCF_LYR_PKG_NAME, LPF_LYR_PKG_NAME


class ComusConPars:

    def __init__(self, model, dim_unit: str = "m", time_unit: str = "day", sim_mtd: int = 1,
                 sim_type: int = 2, acc_lambda: float = -1, intblkm: int = 1, solve: int = 2,
                 max_iter: int = 200, damp: float = 1, h_close: float = 0.0001,
                 r_close: float = 0.001, relax: int = 0, theta: float = 0.7,
                 gamma: float = 3, akappa: float = 0.001, n_iter: int = 5,
                 hno_flo: float = -1E+30, ch_flg: int = 0, wd_flg: int = 0,
                 wet_fct: float = 0.1, newt_iter: int = 1, hd_wet: int = 1,
                 reg_sta: int = 0, mul_td: int = 0, num_td: int = -1):
        """
        Set COMUS Model Control Params Attributes.

        Parameters:
        --------
        model:
            COMUS Model Object
        dim_unit: str
            The unit of spatial measurement (Length)
        time_unit: str
            The unit of spatial measurement (Time)
        sim_mtd: int
            The simulation method option. 1 for the ACC method; 2 for the original MODFLOW method.
        sim_type: int
            The simulation type option. 1 for steady-flow simulation; 2 for transient-flow simulation.
        acc_lambda: float
            It is the resistance coefficient in the additional term on the right side of the grid cell differential equation.
        intblkm: int
            Option for the input format of layer type and grid cell data. 1 for BCF format; 2 for LPF format.
        solve: int
            The option for the method of solving the matrix equation (1 for SIP; 2 for PCG).
        max_iter: int
            The maximum number of iterations for matrix solving.
        damp: float
            Iterative calculation damping factor (-), usually set to 1.0 (valid range: 0.0001~1.0).
        h_close: float
            The accuracy threshold for water level calculation (L).
        r_close: float
            Valid only when solve=2 (Preconditioned Conjugate Gradient Method).
        relax: int
            Option to enable the deep relaxation iterative algorithm.
        theta: float
            It is the reduction coefficient for the dynamic relaxation factor when oscillations occur during iterative calculations (-).
        gamma: float
            It is the increase coefficient for the dynamic relaxation factor.
        akappa: float
            It is the unit increase value for the dynamic relaxation factor.
        n_iter: int
            It is the number of consecutive non-oscillatory iterations required to increase the dynamic relaxation factor.
        hno_flo: float
            The water head value for invalid computational cells (L).
        ch_flg: int
            Option to calculate the flow between two adjacent fixed head cells.
        wd_flg: int
            An option indicating whether to simulate the conversion between dry and wet cells.
        wet_fct: float
            A multiplier for the trial thickness of the aquifer layer when a cell is reWetted.
        newt_iter: int
            The number of iterations between attempts to convert a cell from dry to wet.
        hd_wet: int
            An option for the algorithm to calculate the trial aquifer thickness when a cell is reWetted.
        reg_sta: int
            An option to enable the functionality for sub-regional water balance statistics.
        mul_td: int
            An option to enable multi-threaded parallel computation.
        num_td: int
            This parameter specifies the number of threads to use for parallel computation.

        Returns:
        --------
        controlParams: pycomus.ComusConPars
            COMUS Control Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> controlParams = pycomus.ComusConPars(model=model1, sim_type=1, max_iter=10000)
        """
        self._CheckLib = None
        self._model = model
        self.dim_unit: str = dim_unit
        self.time_unit: str = time_unit
        self.sim_mtd: int = sim_mtd
        self.sim_type: int = sim_type
        self.acc_lambda: float = acc_lambda
        self.intblkm: int = intblkm
        self.solve: int = solve
        self.max_iter: int = max_iter
        self.damp: float = damp
        self.h_close: float = h_close
        self.r_close: float = r_close
        self.relax: int = relax
        self.theta: float = theta
        self.gamma: float = gamma
        self.akappa: float = akappa
        self.n_iter: int = n_iter
        self.hno_flo: float = hno_flo
        self.ch_flg: int = ch_flg
        self.wd_flg: int = wd_flg
        self.wet_fct: float = wet_fct
        self.newt_iter: int = newt_iter
        self.hd_wet: int = hd_wet
        self.reg_sta: int = reg_sta
        self.mul_td: int = mul_td
        self.num_td: int = num_td
        self._SetDlls()
        self._Check()
        model.package[CON_PKG_NAME] = self

    @classmethod
    def load(cls, model, ctrl_params_file: str):
        """
        Load parameters from a CtrlPar.in file and create a ComusConPars instance.

        Parameters:
        --------
        model: pycomus.ComusModel
            COMUS Model Object.
        ctrl_params_file: str
            Control Params file path.

        Returns:
        --------
        instance: pycomus.ComusConPars
            COMUS Control Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> controlParams = pycomus.ComusConPars.load(model1,"./InputFiles/CtrlPar.in")
        """
        with open(ctrl_params_file, 'r') as file:
            lines: List[str] = file.readlines()

        if len(lines) != 2:
            raise ValueError("The Control Params file should have exactly two lines of data.")

        if len(lines[0].strip().split()) != 30:
            raise ValueError("The Control Params file header should have 30 fields.")

        data = lines[1].strip().split()
        if len(data) != 30:
            raise ValueError("The Control Params data line should have 30 values.")

        params = {
            'dim_unit': data[3],
            'time_unit': data[4],
            'sim_mtd': int(data[7]),
            'sim_type': int(data[8]),
            'acc_lambda': float(data[9]),
            'intblkm': int(data[10]),
            'solve': int(data[11]),
            'max_iter': int(data[12]),
            'damp': float(data[13]),
            'h_close': float(data[14]),
            'r_close': float(data[15]),
            'relax': int(data[16]),
            'theta': float(data[17]),
            'gamma': float(data[18]),
            'akappa': float(data[19]),
            'n_iter': int(data[20]),
            'hno_flo': float(data[21]),
            'ch_flg': int(data[22]),
            'wd_flg': int(data[23]),
            'wet_fct': float(data[24]),
            'newt_iter': int(data[25]),
            'hd_wet': int(data[26]),
            'reg_sta': int(data[27]),
            'mul_td': int(data[28]),
            'num_td': int(data[29]),
        }
        instance = cls(model, **params)
        return instance

    def _SetDlls(self):
        current_file_path = os.path.abspath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        system = platform.system()
        if system == 'Windows':
            dll_path = os.path.join(current_dir_path, '.././Utils', 'WinCheckParams.dll')
        elif system == 'Linux':
            dll_path = os.path.join(current_dir_path, '.././Utils', 'LinuxCheckParams.so')
        else:
            raise ValueError("Pycomus only supports Windows and Linux systems.")
        self._CheckLib = ctypes.CDLL(dll_path)
        self._CheckLib.CheckCtrlParData.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double,
                                                    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,
                                                    ctypes.c_double, ctypes.c_double, ctypes.c_int,
                                                    ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                                    ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                                    ctypes.c_double, ctypes.c_int, ctypes.c_int,
                                                    ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self._CheckLib.CheckCtrlParData.restype = ctypes.c_bool

    def _Check(self):
        if not self._CheckLib.CheckCtrlParData(self.sim_mtd, self.sim_type, self.acc_lambda, self.intblkm,
                                               self.solve, self.max_iter, self.damp, self.h_close, self.r_close,
                                               self.relax, self.theta, self.gamma, self.akappa, self.n_iter,
                                               self.ch_flg, self.wd_flg, self.wet_fct, self.newt_iter,
                                               self.hd_wet, self.reg_sta, self.mul_td, self.num_td):
            sys.exit()

    def write_file(self, folder_path: str):
        """
        Typically used as an internal function but can also be called directly, it outputs the `pycomus.ComusConPars`
        module to the specified path as <CtrlPar.in>.

        :param folder_path: Output folder path.
        """
        if BCF_LYR_PKG_NAME not in self._model.package and LPF_LYR_PKG_NAME not in self._model.package:
            raise ValueError(
                "Before writing the ComusConPars, `pycomus.ComusDisLpf` or `pycomus.ComusDisBcf` should be set first.")
        if BCF_LYR_PKG_NAME in self._model.package:
            cms_dis = self._model.package[BCF_LYR_PKG_NAME]
        else:
            cms_dis = self._model.package[LPF_LYR_PKG_NAME]
        num_lyr = cms_dis.num_lyr
        num_row = cms_dis.num_row
        num_col = cms_dis.num_col
        x_coord = cms_dis.x_coord
        y_coord = cms_dis.y_coord
        header_line = "NUMLYR  NUMROW  NUMCOL  DIMUNIT  TIMEUNIT  XSTCORD  YSTCORD  SIMMTHD  SIMTYPE  LAMBDA  INTBLKM  ISOLVE  MAXIT  DAMP  HCLOSE  " \
                      "RCLOSE  IRELAX  THETA  GAMMA  AKAPPA  NITER  HNOFLO  ICHFLG  IWDFLG  WETFCT  IWETIT  IHDWET  IREGSTA  IMULTD  NUMTD"
        conParsData = [num_lyr, num_row, num_col, self.dim_unit, self.time_unit, x_coord, y_coord, self.sim_mtd,
                       self.sim_type, self.acc_lambda, self.intblkm, self.solve, self.max_iter, self.damp, self.h_close,
                       self.r_close, self.relax, self.theta, self.gamma, self.akappa, self.n_iter, self.hno_flo,
                       self.ch_flg, self.wd_flg, self.wet_fct, self.newt_iter, self.hd_wet, self.reg_sta, self.mul_td,
                       self.num_td]
        with open(os.path.join(folder_path, CON_FILE_NAME), "w") as file:
            file.write(header_line + "\n")
            file.write('    '.join(map(str, conParsData)))
