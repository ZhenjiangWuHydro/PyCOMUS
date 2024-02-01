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
                       self.__model._cmsDis.XCoord, self.__model._cmsDis.YCoord, self.__conPars.SimMtd, self.__conPars.SimType,
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
        with open(os.path.join(self.folder_path, "模拟控制参数表.in"), "w") as file:
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
        if "RCH" in self.__package:
            SIMRCH = 1
        if "GHB" in self.__package:
            SIMGHB = 1
        if "GHB" in self.__package:
            SIMDRN = 1
        if "SHB" in self.__package:
            SIMSHB = 1
        if "WEL" in self.__package:
            SIMWEL = 1
        if "EVT" in self.__package:
            SIMEVT = 1
        if "HFB" in self.__package:
            SIMHFB = 1

        with open(os.path.join(self.folder_path, "源汇项模拟选项表.in"), "w") as file:
            file.write(
                "SIMSHB  SIMGHB  SIMRCH  SIMWEL  SIMDRN  SIMEVT  SIMHFB  SIMRIV  SIMSTR  SIMRES  SIMLAK  SIMIBS  SIMSUB\n")
            file.write(f"{SIMSHB}  {SIMGHB}  {SIMRCH}  {SIMWEL}  {SIMDRN}  {SIMEVT}  {SIMHFB}  0  0  0  0  0  0")

    def WriteOutput(self):
        with open(os.path.join(self.folder_path, "模拟输出选项表.in"), "w") as file:
            outPars: pycomus.ComusOutputPars  = self.__model._outPars
            file.write(
                "GDWBDPRN  LYRBDPRN  CELLBDPRN  CELLHHPRN  CELLDDPRN  CELLFLPRN  LAKBDPRN  SEGMBDPRN  RECHBDPRN  IBSPRN  SUBPRN  NDBPRN  DBPRN  REGBDPRN\n")
            file.write(f"{outPars.m_GDWBDPRN}  {outPars.m_LYRBDPRN}  {outPars.m_CELLBDPRN}  {outPars.m_CELLHHPRN}  "
                       f"{outPars.m_CELLDDPRN}  {outPars.m_CELLFLPRN}  {outPars.m_LAKBDPRN}  {outPars.m_SEGMBDPRN}  "
                       f"{outPars.m_RECHBDPRN}  {outPars.m_IBSPRN}  {outPars.m_SUBPRN}  {outPars.m_NDBPRN}  {outPars.m_DBPRN}  "
                       f"{outPars.m_REGBDPRN}")


    def WriteRowColSpace(self):
        with open(os.path.join(self.folder_path, "网格单元水平向间距表.in"), "w") as file:
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
        with open(os.path.join(self.folder_path, "应力期属性表.in"), "w") as file:
            # 写入第一行内容
            file.write("IPER  PERLEN  NSTEP  MULTR\n")
            index = 1
            for tuple in self.__model._cmsTime:
                file.write(f"{index}  {tuple[0]}  {tuple[1]}  {tuple[2]}\n")
                index += 1

    def WriteBCFLyrProp(self):
        with open(os.path.join(self.folder_path, "BCF含水层属性表.in"), "w") as file:
            # 写入第一行内容
            file.write("LYRID  LYRCON  LYRTRPY  LYRIBS\n")
            for i in range(self.__NumLyr):
                file.write(
                    f"{self.__model._Layers[i].LyrId}  {self.__model._Layers[i].LyrType}  "
                    f"{self.__model._Layers[i].LyrTrpy}  {self.__model._Layers[i].LyrIbs}\n")

    def WriteBCFGridCell(self):
        with open(os.path.join(self.folder_path, "BCF网格单元属性表.in"), "w") as file:
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
        with open(os.path.join(self.folder_path, "LPF含水层属性表.in"), "w") as file:
            # 写入第一行内容
            file.write("LYRID  LYRTYPE  LYRHANI  LYRVKA  LYRCBD  LYRIBS\n")
            for i in range(self.__NumLyr):
                file.write(
                    f"{self.__model._Layers[i].LyrId}  {self.__model._Layers[i].LyrType}  -1  0  "
                    f"{self.__model._Layers[i].LyrCbd}  {self.__model._Layers[i].LyrIbs}\n")

    def WriteLPFGridCell(self):
        with open(os.path.join(self.folder_path, "LPF网格单元属性表.in"), "w") as file:
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
        with open(os.path.join(self.folder_path, "面上补给_应力期数据表.in"), "w") as file:
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
        with open(os.path.join(self.folder_path, "排水沟_应力期数据表.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  DELEV  COND\n")
            periods = sorted(drn.cond.keys())
            for period in periods:
                cond_value = drn.cond[period]
                delev_value = drn.delev[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {delev_value[layer, row, col]}  "
                                    f"{cond_value[layer, row, col]}\n")

    def WriteGHB(self):
        ghb = self.__package["GHB"]
        with open(os.path.join(self.folder_path, "通用水头_应力期数据表.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD  COND\n")
            periods = sorted(ghb.cond.keys())
            for period in periods:
                cond_value = ghb.cond[period]
                shead_value = ghb.shead[period]
                ehead_value = ghb.ehead[period]
                for layer in range(self.__NumLyr):
                    for row in range(self.__NumRow):
                        for col in range(self.__NumCol):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}  {cond_value[layer, row, col]}\n")

    def WriteHFB(self):
        hfb: pycomus.ComusHfb = self.__package["HFB"]
        with open(os.path.join(self.folder_path, "水平流动屏障数据表.in"), "w") as file:
            file.write("ILYR  IROW1  ICOL1  IROW2  ICOL2  HCDW\n")
            for hfb_data in hfb.hfb_data:
                file.write(
                    f"{hfb_data[0] + 1}  {hfb_data[1] + 1}  {hfb_data[2] + 1}  {hfb_data[3] + 1}  {hfb_data[4] + 1}  "
                    f"{hfb_data[5]}\n")
