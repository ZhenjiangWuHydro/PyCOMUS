import os
import shutil

import pycomus


class WriteFiles:
    def __init__(self, model):
        self.__model = model
        self.__NumLyr = model._cmsDis.NumLyr
        self.__NumRow = model._cmsDis.NumRow
        self.__NumCol = model._cmsDis.NumCol
        self.__conPars: pycomus.ComusConPars = self.__model._conPars
        self.__package = self.__model._package
        folder_name = self.__model._model_name
        current_directory = os.getcwd()
        self.folder_path = os.path.join(current_directory, folder_name)
        if os.path.exists(self.folder_path):
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete file {file_path}: {e}")
            shutil.rmtree(self.folder_path)
        os.mkdir(self.folder_path)
        self.folder_path = self.folder_path + r"\Data.in"
        os.mkdir(self.folder_path)

    def WriteConPars(self):
        conParsData = [self.__NumLyr, self.__NumRow, self.__NumCol, self.__conPars.DimUnit, self.__conPars.TimeUnit,
                       self.__model._cmsDis.XCoord, self.__model._cmsDis.YCoord, self.__conPars.SimMtd,
                       self.__conPars.SimType,
                       self.__conPars.LamBda, self.__conPars.IntBkm, self.__conPars.ISolve, self.__conPars.MaxIt,
                       self.__conPars.Damp, self.__conPars.HClose,
                       self.__conPars.RClose, self.__conPars.IRelax, self.__conPars.Theta, self.__conPars.Gamma,
                       self.__conPars.Akappa, self.__conPars.Niter,
                       self.__conPars.HNoflo, self.__conPars.IchFlg, self.__conPars.IwdFlg, self.__conPars.WetFct,
                       self.__conPars.NweTit, self.__conPars.IhdWet,
                       self.__conPars.IreSta, self.__conPars.ImuLtd, self.__conPars.NumTd]
        # 定义要写入的内容
        header_line = "NUMLYR  NUMROW  NUMCOL  DIMUNIT  TIMEUNIT  XSTCORD  YSTCORD  SIMMTHD  SIMTYPE  LAMBDA  INTBLKM  ISOLVE  MAXIT  DAMP  HCLOSE  RCLOSE  IRELAX  THETA  GAMMA  AKAPPA  NITER  HNOFLO  ICHFLG  IWDFLG  WETFCT  IWETIT  IHDWET  IREGSTA  IMULTD  NUMTD"
        # 打开文件以写入内容
        with open(os.path.join(self.folder_path, "CtrlPar.in"), "w") as file:
            # 写入第一行内容
            file.write(header_line + "\n")
            file.write('    '.join(map(str, conParsData)))

    def WritePackages(self):
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
        if "RCH" in self.__package:
            SIMRCH = 1
        if "GHB" in self.__package:
            SIMGHB = 1
        if "DRN" in self.__package:
            SIMDRN = 1
        if "SHB" in self.__package:
            SIMSHB = 1
        if "WEL" in self.__package:
            SIMWEL = 1
        if "EVT" in self.__package:
            SIMEVT = 1
        if "HFB" in self.__package:
            SIMHFB = 1
        if "RIV" in self.__package:
            SIMRIV = 1
        if "STR" in self.__package:
            SIMSTR = 1
        if "RES" in self.__package:
            SIMRES = 1
        if "LAK" in self.__package:
            SIMLAK = 1
        if "IBS" in self.__package:
            SIMIBS = 1
        if "SUB" in self.__package:
            SIMSUB = 1
        with open(os.path.join(self.folder_path, "BndOpt.in"), "w") as file:
            file.write(
                "SIMSHB  SIMGHB  SIMRCH  SIMWEL  SIMDRN  SIMEVT  SIMHFB  SIMRIV  SIMSTR  SIMRES  SIMLAK  SIMIBS  SIMSUB\n")
            file.write(f"{SIMSHB}  {SIMGHB}  {SIMRCH}  {SIMWEL}  {SIMDRN}  {SIMEVT}  {SIMHFB}  {SIMRIV}  {SIMSTR}  "
                       f"{SIMRES}  {SIMLAK}  {SIMIBS}  {SIMSUB}")

    def WriteOutput(self):
        with open(os.path.join(self.folder_path, "OutOpt.in"), "w") as file:
            outPars: pycomus.ComusOutputPars = self.__model._outPars
            file.write(
                "GDWBDPRN  LYRBDPRN  CELLBDPRN  CELLHHPRN  CELLDDPRN  CELLFLPRN  LAKBDPRN  SEGMBDPRN  RECHBDPRN  IBSPRN  SUBPRN  NDBPRN  DBPRN  REGBDPRN\n")
            file.write(f"{outPars.m_GDWBDPRN}  {outPars.m_LYRBDPRN}  {outPars.m_CELLBDPRN}  {outPars.m_CELLHHPRN}  "
                       f"{outPars.m_CELLDDPRN}  {outPars.m_CELLFLPRN}  {outPars.m_LAKBDPRN}  {outPars.m_SEGMBDPRN}  "
                       f"{outPars.m_RECHBDPRN}  {outPars.m_IBSPRN}  {outPars.m_SUBPRN}  {outPars.m_NDBPRN}  {outPars.m_DBPRN}  "
                       f"{outPars.m_REGBDPRN}")

    def WriteRowColSpace(self):
        with open(os.path.join(self.folder_path, "GrdSpace.in"), "w") as file:
            file.write("ATTI  NUMID  DELT\n")
            index = 1
            for rowSpace in self.__model._cmsDis.RowSpaceList:
                file.write(f"C  {index}  {rowSpace}\n")
                index += 1
            index = 1
            for colSpace in self.__model._cmsDis.ColSpaceList:
                file.write(f"R  {index}  {colSpace}\n")
                index += 1

    def WritePeriod(self):
        with open(os.path.join(self.folder_path, "PerAttr.in"), "w") as file:
            # 写入第一行内容
            file.write("IPER  PERLEN  NSTEP  MULTR\n")
            index = 1
            for tuple in self.__model._cmsTime:
                file.write(f"{index}  {tuple[0]}  {tuple[1]}  {tuple[2]}\n")
                index += 1

    def WriteBCFLyrProp(self):
        with open(os.path.join(self.folder_path, "BcfLyr.in"), "w") as file:
            # 写入第一行内容
            file.write("LYRID  LYRCON  LYRTRPY  LYRIBS\n")
            for i in range(self.__NumLyr):
                file.write(
                    f"{self.__model._Layers[i].LyrId}  {self.__model._Layers[i].LyrType}  "
                    f"{self.__model._Layers[i].LyrTrpy}  {self.__model._Layers[i].LyrIbs}\n")

    def WriteBCFGridCell(self):
        with open(os.path.join(self.folder_path, "BcfGrd.in"), "w") as file:
            # 写入第一行内容
            file.write("ILYR  IROW  ICOL  IBOUND  CELLTOP  CELLBOT  TRANSM  HK  VCONT  SC1  SC2  WETDRY  SHEAD\n")
            for layer in range(self.__NumLyr):
                for row in range(self.__NumRow):
                    for col in range(self.__NumCol):
                        gridCell = self.__model._Layers[layer].GridCells[row][col]
                        file.write(
                            f"{layer + 1}  {row + 1}  {col + 1}  {gridCell.IBOUND}  {gridCell.TOP}  {gridCell.BOT}  {gridCell.TRAN}"
                            f"  {gridCell.HK}  {gridCell.VCONT}  {gridCell.SC1}  {gridCell.SC2}  {gridCell.WETDRY}  {gridCell.SHEAD}\n")

    def WriteLPFLyrProp(self):
        with open(os.path.join(self.folder_path, "LpfLyr.in"), "w") as file:
            # 写入第一行内容
            file.write("LYRID  LYRTYPE  LYRHANI  LYRVKA  LYRCBD  LYRIBS\n")
            for i in range(self.__NumLyr):
                file.write(
                    f"{self.__model._Layers[i].LyrId}  {self.__model._Layers[i].LyrType}  -1  0  "
                    f"{self.__model._Layers[i].LyrCbd}  {self.__model._Layers[i].LyrIbs}\n")

    def WriteLPFGridCell(self):
        with open(os.path.join(self.folder_path, "LpfGrd.in"), "w") as file:
            # 写入第一行内容
            file.write(
                "ILYR  IROW  ICOL  CELLTOP  CELLBOT  IBOUND  HK  HANI  VKA  VKCB  TKCB  SC1  SC2  WETDRY  SHEAD\n")
            for layer in range(self.__NumLyr):
                for row in range(self.__NumRow):
                    for col in range(self.__NumCol):
                        gridCell = self.__model._Layers[layer].GridCells[row][col]
                        file.write(
                            f"{layer + 1}  {row + 1}  {col + 1}  {gridCell.TOP}  {gridCell.BOT}  {gridCell.IBOUND}  {gridCell.HK}"
                            f"  {gridCell.HANI}  {gridCell.VKA}  {gridCell.VKCB}  {gridCell.TKCB}  {gridCell.SC1}  {gridCell.SC2}"
                            f"  {gridCell.WETDRY}  {gridCell.SHEAD}\n")

    def WriteRCH(self):
        rchar = self.__package["RCH"]
        with open(os.path.join(self.folder_path, "RCH.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  IRECH  RECHR\n")
            for period, value in rchar.Rechr.items():
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if value[layer, row, col] != 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {rchar.IRech}  {value[layer, row, col]} \n")

    def WriteDRN(self):
        drn = self.__package["DRN"]
        with open(os.path.join(self.folder_path, "DRN.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  DELEV  COND\n")
            periods = sorted(drn.Cond.keys())
            for period in periods:
                cond_value = drn.Cond[period]
                delev_value = drn.Delev[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {delev_value[layer, row, col]}  "
                                    f"{cond_value[layer, row, col]}\n")

    def WriteGHB(self):
        ghb = self.__package["GHB"]
        with open(os.path.join(self.folder_path, "GHB.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD  COND\n")
            periods = sorted(ghb.Cond.keys())
            for period in periods:
                cond_value = ghb.Cond[period]
                shead_value = ghb.Shead[period]
                ehead_value = ghb.Ehead[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}  {cond_value[layer, row, col]}\n")

    def WriteHFB(self):
        hfb: pycomus.ComusHfb = self.__package["HFB"]
        with open(os.path.join(self.folder_path, "HFB.in"), "w") as file:
            file.write("ILYR  IROW1  ICOL1  IROW2  ICOL2  HCDW\n")
            for hfb_data in hfb.hfb_data:
                file.write(
                    f"{hfb_data[0] + 1}  {hfb_data[1] + 1}  {hfb_data[2] + 1}  {hfb_data[3] + 1}  {hfb_data[4] + 1}  "
                    f"{hfb_data[5]}\n")

    def WriteSHB(self):
        shb = self.__package["SHB"]
        with open(os.path.join(self.folder_path, "SHB.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD\n")
            periods = sorted(shb.Shead.keys())
            for period in periods:
                shead_value = shb.Shead[period]
                ehead_value = shb.Ehead[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if shead_value[layer, row, col] != 0 and ehead_value[layer, row, col] != 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}\n")

    def WriteWEL(self):
        wel = self.__package["WEL"]
        with open(os.path.join(self.folder_path, "WEL.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  WELLR  SATTHR\n")
            periods = sorted(wel.Wellr.keys())
            for period in periods:
                wellr_value = wel.Wellr[period]
                satthr_value = wel.Satthr[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if wellr_value[layer, row, col] != 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {wellr_value[layer, row, col]}  "
                                    f"{satthr_value[layer, row, col]}\n")

    def WriteEVT(self):
        evt = self.__package["EVT"]
        with open(os.path.join(self.folder_path, "EVT.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  IEVT  ETSURF  ETRATE  ETMXD  ETEXP  NUMSEG\n")
            periods = sorted(evt.ETSurf.keys())
            print(periods)
            for period in periods:
                ETSurf_value = evt.ETSurf[period]
                ETRate_value = evt.ETRate[period]
                ETMxd_value = evt.ETMxd[period]
                ETExp_value = evt.ETExp[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if ETExp_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {evt.IEvt}  {ETSurf_value[layer, row, col]}  "
                                    f"{ETRate_value[layer, row, col]}  {ETMxd_value[layer, row, col]}  "
                                    f"{ETExp_value[layer, row, col]}  {evt.NumSeg}\n")

    def WriteRIV(self):
        riv = self.__package["RIV"]
        with open(os.path.join(self.folder_path, "RIV.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD  COND  RIVBTM\n")
            periods = sorted(riv.Cond.keys())
            for period in periods:
                cond_value = riv.Cond[period]
                shead_value = riv.Shead[period]
                ehead_value = riv.Ehead[period]
                rivBtm_value = riv.RivBtm[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}  {cond_value[layer, row, col]}  {rivBtm_value[layer, row, col]}\n")

    def WriteRES(self):
        res = self.__package["RES"].ResValue
        control_data = res.ControlParams
        period_data = res.PeriodData
        grid_data = res.GridData
        with open(os.path.join(self.folder_path, "RESCtrl.in"), "w") as file:
            file.write("RESID  EVEXP  EVMAXD  NUMSEG  NUMPT\n")
            for res_id, params in control_data.items():
                file.write(f"{res_id + 1}  {params[0]}  {params[1]}  {params[2]}  {params[3]}\n")

        with open(os.path.join(self.folder_path, "RESPer.in"), "w") as file:
            file.write("IPER  RESID  SHEAD  EHEAD  RCHRG  GEVT\n")
            for res_id, periodData in period_data.items():
                for period_id, value in periodData.items():
                    file.write(f"{period_id + 1}  {res_id + 1}  {value[0]}  {value[1]}  {value[2]}  {value[3]}\n")

        with open(os.path.join(self.folder_path, "RESGrd.in"), "w") as file:
            file.write("RESID  CELLID  ILYR  IROW  ICOL  BTM  BVK  BTK\n")
            resIds = sorted(grid_data["Btm"].keys())
            for resId in resIds:
                index = 1
                btm_value = grid_data["Btm"][resId]
                bvk_value = grid_data["Bvk"][resId]
                btk_value = grid_data["Btk"][resId]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if bvk_value[layer, row, col] >= 0 and btk_value[layer, row, col] > 0:
                                file.write(
                                    f"{resId + 1}  {index}  {layer + 1}  {row + 1}  {col + 1}  {btm_value[layer, row, col]}  "
                                    f"{bvk_value[layer, row, col]}  {btk_value[layer, row, col]}\n")
                                index += 1

