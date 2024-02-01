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

    def __init__(self, model_name="aaa"):
        """
        Create a COMUS Model object.

        Parameters:
        ----------------------------
        model_name:
            COMUS Model Name
        """
        self._model_name: str = model_name
        self._package = {}
        self._conPars = None
        self._outPars = None
        self._cmsDis = None
        self._cmsTime = None
        self._Layers = []
        self._INTBLKM = ""

    def _addConPars(self, cmsPars):
        self._conPars = cmsPars

    def _addOutPars(self, outPars):
        self._outPars = outPars

    def _addDis(self, cmsDis):
        self._cmsDis = cmsDis

    def _addPeriod(self, cmsTime):
        self._cmsTime = cmsTime

    def _addPackage(self, packageName: str, cmsPackage):
        self._package[packageName] = cmsPackage

    def writeOutPut(self) -> None:
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
        if self._conPars.IntBkm == 1:
            writeOutPut.WriteBCFLyrProp()
            writeOutPut.WriteBCFGridCell()
        else:
            writeOutPut.WriteLPFLyrProp()
            writeOutPut.WriteLPFGridCell()
        if "RCH" in self._package:
            writeOutPut.WriteRCH()
        if "DRN" in self._package:
            writeOutPut.WriteDRN()
        if "GHB" in self._package:
            writeOutPut.WriteGHB()
        if "HFB" in self._package:
            writeOutPut.WriteHFB()
        if "WEL" in self._package:
            writeOutPut.WriteWEL()
        if "SHB" in self._package:
            writeOutPut.WriteSHB()
        if "EVT" in self._package:
            writeOutPut.WriteEVT()
        if "RIV" in self._package:
            writeOutPut.WriteRIV()

    def runModel(self) -> None:
        """
        Run COMUS Model
        """
        current_file_path = os.path.abspath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        dll_path = os.path.join(current_dir_path, '../Utils', 'COMUS.dll')
        comusModel = ctypes.CDLL(dll_path)
        comusModel.RunModel.argtypes = [ctypes.c_char_p]
        comusModel.RunModel.restype = ctypes.c_int
        data_path = os.path.join(os.getcwd(), self._model_name).encode('utf-8')
        return comusModel.RunModel(data_path)

    def __str__(self):
        return f"ComusModel:\n    COMUS Model Name: {self._model_name}"

    def __repr__(self):
        return f"ComusModel(model_name='{self._model_name}')"
