# --------------------------------------------------------------
# CmsMd.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Create A COMUS Model Object.
# --------------------------------------------------------------
import ctypes
import os.path
import platform

from pycomus.Utils import CONSTANTS


class ComusModel:
    """
    Create a COMUS Model object.

    Attributes:
    -----------
    model_name : str
        COMUS Model Name

    Methods:
    --------
    __init__(self, model_name: str = "ComusTest")
        Instantiate an instance of ComusModel.

    write_files(self)
        Compile the input data and save it in the <Data.in> directory located at runtime.

    run(self)
        Run COMUS Model.

    Returns:
    --------
    instance: pycomus.ComusModel
        COMUS Model object.

    Example:
    --------
    >>> import pycomus
    >>> model1 = pycomus.ComusModel(model_name="test")
    """

    def __init__(self, model_name: str = "ComusTest"):
        if not isinstance(model_name, str):
            raise ValueError("model_name should be of type str.")
        self.model_name: str = model_name
        self.package = {}
        self.layers = []

    def write_files(self) -> None:
        """
        Compile the input data and save it in the <Data.in> directory located at runtime.

        """
        required_packages = [
            CONSTANTS.CON_PKG_NAME, CONSTANTS.OUT_PKG_NAME,
            CONSTANTS.GRID_PKG_NAME, CONSTANTS.PERIOD_PKG_NAME
        ]
        for package_name in required_packages:
            if package_name not in self.package:
                raise ValueError(f"<pycomus.{package_name}> needs to be set!")

        ctrl_pars = self.package[CONSTANTS.CON_PKG_NAME]
        if ctrl_pars.intblkm == 1:
            if CONSTANTS.BCF_LYR_PKG_NAME not in self.package:
                raise ValueError(
                    "In the control parameter settings, the BCF mode has been designated for use, but "
                    "<pycomus.ComusDisBcf> has not been implemented.")
        else:
            if CONSTANTS.LPF_LYR_PKG_NAME not in self.package:
                raise ValueError(
                    "In the control parameter settings, the LPF mode has been designated for use, but "
                    "<pycomus.ComusDisLpf> has not been implemented.")

        folder_name = self.model_name
        folder_path = os.path.join(os.getcwd(), folder_name, "Data.in")
        os.makedirs(folder_path, exist_ok=True)
        SIM_FLAGS = {
            "RCH": 0, "GHB": 0, "DRN": 0, "SHB": 0, "WEL": 0,
            "EVT": 0, "HFB": 0, "RIV": 0, "STR": 0, "RES": 0,
            "LAK": 0, "IBS": 0, "SUB": 0
        }

        for key in SIM_FLAGS.keys():
            if key in self.package:
                SIM_FLAGS[key] = 1

        with open(os.path.join(folder_path, "BndOpt.in"), "w") as file:
            file.write(
                "SIMSHB  SIMGHB  SIMRCH  SIMWEL  SIMDRN  SIMEVT  SIMHFB  SIMRIV  SIMSTR  SIMRES  SIMLAK  SIMIBS  SIMSUB\n")
            file.write(
                f"{SIM_FLAGS['SHB']}  {SIM_FLAGS['GHB']}  {SIM_FLAGS['RCH']}  {SIM_FLAGS['WEL']}  {SIM_FLAGS['DRN']}  {SIM_FLAGS['EVT']}  {SIM_FLAGS['HFB']}  {SIM_FLAGS['RIV']}  {SIM_FLAGS['STR']}  {SIM_FLAGS['RES']}  {SIM_FLAGS['LAK']}  {SIM_FLAGS['IBS']}  {SIM_FLAGS['SUB']}")

        for pkg in self.package.values():
            pkg.write_file(folder_path)

    def run(self) -> None:
        """
        Run COMUS Model.

        """
        system = platform.system()
        current_file_path = os.path.abspath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        if system == 'Windows':
            dll_path = os.path.join(current_dir_path, '.././Utils', 'WinComus.dll')
            comusModel = ctypes.CDLL(dll_path)
            comusModel.RunModel.argtypes = [ctypes.c_wchar_p]
            comusModel.RunModel.restype = ctypes.c_int
            data_path = os.path.join(os.getcwd(), self.model_name)
            comusModel.RunModel(data_path)
        elif system == 'Linux':
            dll_path = os.path.join(current_dir_path, '.././Utils', 'LinuxComus.so')
            comusModel = ctypes.CDLL(dll_path)
            comusModel.RunModel.argtypes = [ctypes.c_char_p]
            comusModel.RunModel.restype = ctypes.c_int
            data_path = os.path.join(os.getcwd(), self.model_name)
            comusModel.RunModel(ctypes.c_char_p(data_path.encode('utf-8')))
        else:
            raise ValueError("PyCOMUS only supports Windows and Linux systems.")

    def __str__(self):
        return f"ComusModel:\n    COMUS Model Name: {self.model_name}"

    def __repr__(self):
        return f"ComusModel(model_name='{self.model_name}')"
