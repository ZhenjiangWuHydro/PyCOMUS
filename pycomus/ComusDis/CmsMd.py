# --------------------------------------------------------------
# CmsMd.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Create A COMUS Model Object.
# --------------------------------------------------------------
import ctypes
import os.path
import platform

from pycomus.Utils import CONST_VALUE


class ComusModel:

    def __init__(self, model_name: str = "ComusTest"):
        """
        Create a COMUS Model object.

        Parameters:
        ----------------------------
        model_name:
            COMUS Model Name
        """
        if not isinstance(model_name, str):
            raise ValueError("model_name should be of type str.")
        self.model_name: str = model_name
        self.package = {}
        self.layers = []

    def write_files(self) -> None:
        """
        Compile the input data and save it in the <Data.in> directory located at runtime.

        """
        if CONST_VALUE.CON_PKG_NAME not in self.package:
            raise ValueError("<pycomus.ComusConPars> needs to be set!")

        if CONST_VALUE.OUT_PKG_NAME not in self.package:
            raise ValueError("<pycomus.ComusOutputPars> needs to be set!")

        ctrl_pars = self.package[CONST_VALUE.CON_PKG_NAME]
        if ctrl_pars.intblkm == 1:
            if CONST_VALUE.BCF_LYR_PKG_NAME not in self.package:
                raise ValueError(
                    "In the control parameter settings, the BCF mode has been designated for use, but "
                    "<pycomus.ComusDisBcf> has not been implemented.")
        else:
            if CONST_VALUE.LPF_LYR_PKG_NAME not in self.package:
                raise ValueError(
                    "In the control parameter settings, the LPF mode has been designated for use, but "
                    "<pycomus.ComusDisLpf> has not been implemented.")

        if CONST_VALUE.GRID_PKG_NAME not in self.package:
            raise ValueError("<pycomus.ComusGridPars> needs to be set!")

        if CONST_VALUE.PERIOD_PKG_NAME not in self.package:
            raise ValueError("<pycomus.ComusPeriod> needs to be set!")

        folder_name = self.model_name
        current_directory = os.getcwd()
        folder_path = os.path.join(current_directory, folder_name, "Data.in")
        os.makedirs(folder_path, exist_ok=True)
        self._write_files(folder_path)

    def run(self) -> None:
        """
        Run COMUS Model.
        """
        system = platform.system()
        if system == 'Windows':
            current_file_path = os.path.abspath(__file__)
            current_dir_path = os.path.dirname(current_file_path)
            dll_path = os.path.join(current_dir_path, '.././Utils', 'COMUS.dll')
            comusModel = ctypes.CDLL(dll_path)
            comusModel.RunModel.argtypes = [ctypes.c_char_p]
            comusModel.RunModel.restype = ctypes.c_int
            data_path = os.path.join(os.getcwd(), self.model_name).encode('utf-8')
            comusModel.RunModel(data_path)
        elif system == 'Linux':
            print('Linux')
        else:
            print('Unknown')

    def __str__(self):
        return f"ComusModel:\n    COMUS Model Name: {self.model_name}"

    def __repr__(self):
        return f"ComusModel(model_name='{self.model_name}')"

    def _write_files(self, folder_path: str):
        SIMRCH = 0
        SIMGHB = 0
        SIMDRN = 0
        SIMSHB = 0
        SIMWEL = 0
        SIMEVT = 0
        SIMHFB = 0
        SIMRIV = 0
        SIMSTR = 0
        SIMRES = 0
        SIMLAK = 0
        SIMIBS = 0
        SIMSUB = 0
        if "RCH" in self.package:
            SIMRCH = 1
        if "GHB" in self.package:
            SIMGHB = 1
        if "DRN" in self.package:
            SIMDRN = 1
        if "SHB" in self.package:
            SIMSHB = 1
        if "WEL" in self.package:
            SIMWEL = 1
        if "EVT" in self.package:
            SIMEVT = 1
        if "HFB" in self.package:
            SIMHFB = 1
        if "RIV" in self.package:
            SIMRIV = 1
        if "STR" in self.package:
            SIMSTR = 1
        if "RES" in self.package:
            SIMRES = 1
        if "LAK" in self.package:
            SIMLAK = 1
        if "IBS" in self.package:
            SIMIBS = 1
        if "SUB" in self.package:
            SIMSUB = 1
        with open(os.path.join(folder_path, "BndOpt.in"), "w") as file:
            file.write(
                "SIMSHB  SIMGHB  SIMRCH  SIMWEL  SIMDRN  SIMEVT  SIMHFB  SIMRIV  SIMSTR  SIMRES  SIMLAK  SIMIBS  SIMSUB\n")
            file.write(f"{SIMSHB}  {SIMGHB}  {SIMRCH}  {SIMWEL}  {SIMDRN}  {SIMEVT}  {SIMHFB}  {SIMRIV}  {SIMSTR}  "
                       f"{SIMRES}  {SIMLAK}  {SIMIBS}  {SIMSUB}")
        for _, pkg in self.package.items():
            pkg.write_file(folder_path)
