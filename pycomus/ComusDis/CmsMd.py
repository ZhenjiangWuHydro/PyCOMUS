# --------------------------------------------------------------
# CmsMd.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Create A COMUS Model Object.
# --------------------------------------------------------------
import ctypes
import os.path

import pycomus.Utils.WriteFiles


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
        self.CmsDis = None
        self.CmsPars = None
        self.CmsDis = None
        self.CmsOutPars = None
        self.CmsTime = None
        self.package = {}
        self.layers = []


    def write_files(self) -> None:
        """
        Compile the input data and save it in the <Data.in> directory located at runtime.
        :return:
        """
        writeOutPut = pycomus.Utils.WriteFiles.WriteFiles(self)
        writeOutPut.WriteConPars()
        writeOutPut.WritePackages()
        writeOutPut.WriteOutput()
        writeOutPut.WriteRowColSpace()
        writeOutPut.WritePeriod()
        if self.CmsPars.intblkm == 1:
            writeOutPut.WriteBCFLyrProp()
            writeOutPut.WriteBCFGridCell()
        else:
            writeOutPut.WriteLPFLyrProp()
            writeOutPut.WriteLPFGridCell()
        if "RCH" in self.package:
            writeOutPut.WriteRCH()
        if "DRN" in self.package:
            writeOutPut.WriteDRN()
        if "GHB" in self.package:
            writeOutPut.WriteGHB()
        if "HFB" in self.package:
            writeOutPut.WriteHFB()
        if "WEL" in self.package:
            writeOutPut.WriteWEL()
        if "SHB" in self.package:
            writeOutPut.WriteSHB()
        if "EVT" in self.package:
            writeOutPut.WriteEVT()
        if "RIV" in self.package:
            writeOutPut.WriteRIV()
        if "RES" in self.package:
            writeOutPut.WriteRES()
        if "STR" in self.package:
            writeOutPut.WriteSTR()

    def run(self) -> None:
        """
        Run COMUS Model
        """
        current_file_path = os.path.abspath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        dll_path = os.path.join(current_dir_path, '.././Utils', 'COMUS.dll')
        comusModel = ctypes.CDLL(dll_path)
        comusModel.RunModel.argtypes = [ctypes.c_char_p]
        comusModel.RunModel.restype = ctypes.c_int
        data_path = os.path.join(os.getcwd(), self.model_name).encode('utf-8')
        return comusModel.RunModel(data_path)

    def __str__(self):
        return f"ComusModel:\n    COMUS Model Name: {self.model_name}"

    def __repr__(self):
        return f"ComusModel(model_name='{self.model_name}')"
