# --------------------------------------------------------------
# CmsPars.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model Control Parameter Attributes.
# --------------------------------------------------------------
import ctypes
import os
import sys


class ComusConPars:
    def __init__(self, model, DimUnit: str = "m", TimeUnit: str = "day", SimMtd: int = 1,
                 SimType: int = 2, LamBda: float = -1, IntBkm: int = 1, ISolve: int = 2,
                 MaxIt: int = 200, Damp: float = 1, HClose: float = 0.0001,
                 RClose: float = 0.001, IRelax: int = 0, Theta: float = 0.7,
                 Gamma: float = 3, Akappa: float = 0.001, Niter: int = 3,
                 HNoflo: float = -1E+30, IchFlg: int = 0, IwdFlg: int = 0,
                 WetFct: float = 0.1, NweTit: int = 1, IhdWet: int = 1,
                 IreSta: int = 0, ImuLtd: int = 0, NumTd: int = -1):
        """
        Set COMUS Model Control Params Attributes.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object
        DimUnit:
            The unit of spatial measurement(Length)
        TimeUnit:
            The unit of spatial measurement(Time)
        SimMtd:
            The simulation method option. 1 for the fully effective cell method; 2 for the original MODFLOW method.
        SimType:
            The simulation type option. 1 for steady-flow simulation; 2 for transient-flow simulation.
        LamBda:
            it is the resistance coefficient in the additional term on the right side of the grid cell differential equation.
        IntBkm:
            Option for the input format of layer type and grid cell data. 1 for BCF format; 2 for LPF format.
        ISolve:
            The option for the method of solving the matrix equation(SIP or PCG).
        MaxIt:
            The maximum number of iterations for matrix solving.
        Damp:
            Iterative calculation damping factor (-), usually set to 1.0 (valid range: 0.0001~1.0).
        HClose:
            The accuracy threshold for water level calculation (L).
        RClose:
            Valid only when ISOLVE=2 (Preconditioned Conjugate Gradient Method).
        IRelax:
            Option to enable the deep relaxation iterative algorithm.
        Theta:
            It is the reduction coefficient for the dynamic relaxation factor when oscillations occur during iterative calculations (-).
        Gamma:
            It is the increase coefficient for the dynamic relaxation factor.
        Akappa:
            It is the unit increase value for the dynamic relaxation factor.
        Niter:
            It is the number of consecutive non-oscillatory iterations required to increase the dynamic relaxation factor.
        HNoflo:
            The water head value for invalid computational cells (L).
        IchFlg:
            Option to calculate the flow between two adjacent fixed head cells.
        IwdFlg:
            An option indicating whether to simulate the conversion between dry and wet cells.
        WetFct:
            A multiplier for the trial thickness of the aquifer layer when a cell is rewetted.
        NweTit:
            The number of iterations between attempts to convert a cell from dry to wet
        IhdWet:
            An option for the algorithm to calculate the trial aquifer thickness when a cell is rewetted.
        IreSta:
            An option to enable the functionality for sub-regional water balance statistics.
        ImuLtd:
            An option to enable multi-threaded parallel computation.
        NumTd:
            This parameter specifies the number of threads to use for parallel computation.
        """
        self.DimUnit: str = DimUnit
        self.TimeUnit: str = TimeUnit
        self.SimMtd: int = SimMtd
        self.SimType: int = SimType
        self.LamBda: float = LamBda
        self.IntBkm: int = IntBkm
        self.ISolve: int = ISolve
        self.MaxIt: int = MaxIt
        self.Damp: float = Damp
        self.HClose: float = HClose
        self.RClose: float = RClose
        self.IRelax: int = IRelax
        self.Theta: float = Theta
        self.Gamma: float = Gamma
        self.Akappa: float = Akappa
        self.Niter: int = Niter
        self.HNoflo: float = HNoflo
        self.IchFlg: int = IchFlg
        self.IwdFlg: int = IwdFlg
        self.WetFct: float = WetFct
        self.NweTit: int = NweTit
        self.IhdWet: int = IhdWet
        self.IreSta: int = IreSta
        self.ImuLtd: int = ImuLtd
        self.NumTd: int = NumTd
        self.__SetDlls()
        self.__Check()
        model._addConPars(self)

    def __SetDlls(self):
        current_file_path = os.path.abspath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        dll_path = os.path.join(current_dir_path, '../Utils', 'CheckParams.dll')
        self.CheckLib = ctypes.CDLL(dll_path)
        self.CheckLib.CheckCtrlParData.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double,
                                                   ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double,
                                                   ctypes.c_double, ctypes.c_double, ctypes.c_int,
                                                   ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                                   ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                                   ctypes.c_double, ctypes.c_int, ctypes.c_int,
                                                   ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.CheckLib.CheckCtrlParData.restype = ctypes.c_bool

    def __Check(self):
        if not self.CheckLib.CheckCtrlParData(self.SimMtd, self.SimType, self.LamBda, self.IntBkm, self.ISolve,
                                              self.MaxIt,
                                              self.Damp, self.HClose, self.RClose, self.IRelax, self.Theta, self.Gamma,
                                              self.Akappa, self.Niter, self.IchFlg, self.IwdFlg, self.WetFct,
                                              self.NweTit,
                                              self.IhdWet, self.IreSta, self.ImuLtd, self.NumTd):
            sys.exit()

    def __str__(self):
        return f"Control Parameter:\n    DimUnit {self.DimUnit}; TimeUnit {self.TimeUnit}; SimMtd {self.SimMtd}; SimType {self.SimType}; LamBda " \
               f"{self.LamBda}; IntBkm {self.IntBkm}; ISolve {self.ISolve}; MaxIt {self.MaxIt}; Damp {self.Damp}; HClose " \
               f"{self.HClose}; RClose {self.RClose}; IRelax {self.IRelax}; Theta {self.Theta}; Gamma {self.Gamma}; Akappa " \
               f"{self.Akappa}; Niter {self.Niter}; HNoflo {self.HNoflo}; IchFlg {self.IchFlg}; IwdFlg {self.IwdFlg}; WetFct " \
               f"{self.WetFct}; NweTit {self.NweTit}; IhdWet {self.IhdWet}; IreSta {self.IreSta}; ImuLtd {self.ImuLtd}; NumTd " \
               f"{self.NumTd}"
