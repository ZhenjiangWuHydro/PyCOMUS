import os
import shutil
from collections import OrderedDict

import pycomus


class WriteFiles:
    def __init__(self, model):
        self._model = model
        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._conPars: pycomus.ComusConPars = self._model.CmsPars
        self._package = self._model.package
        folder_name = self._model.model_name
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
        conParsData = [self._num_lyr, self._num_row, self._num_col, self._conPars.dim_unit, self._conPars.time_unit,
                       self._model.CmsDis.x_coord, self._model.CmsDis.y_coord, self._conPars.sim_mtd,
                       self._conPars.sim_type, self._conPars.acc_lambda, self._conPars.intblkm, self._conPars.solve,
                       self._conPars.max_iter, self._conPars.damp, self._conPars.h_close, self._conPars.r_close,
                       self._conPars.relax, self._conPars.theta, self._conPars.gamma, self._conPars.akappa,
                       self._conPars.n_iter, self._conPars.hno_flo, self._conPars.ch_flg, self._conPars.wd_flg,
                       self._conPars.wet_fct, self._conPars.newt_iter, self._conPars.hd_wet, self._conPars.reg_sta,
                       self._conPars.mul_td, self._conPars.num_td]
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
        if "RCH" in self._package:
            SIMRCH = 1
        if "GHB" in self._package:
            SIMGHB = 1
        if "DRN" in self._package:
            SIMDRN = 1
        if "SHB" in self._package:
            SIMSHB = 1
        if "WEL" in self._package:
            SIMWEL = 1
        if "EVT" in self._package:
            SIMEVT = 1
        if "HFB" in self._package:
            SIMHFB = 1
        if "RIV" in self._package:
            SIMRIV = 1
        if "STR" in self._package:
            SIMSTR = 1
        if "RES" in self._package:
            SIMRES = 1
        if "LAK" in self._package:
            SIMLAK = 1
        if "IBS" in self._package:
            SIMIBS = 1
        if "SUB" in self._package:
            SIMSUB = 1
        with open(os.path.join(self.folder_path, "BndOpt.in"), "w") as file:
            file.write(
                "SIMSHB  SIMGHB  SIMRCH  SIMWEL  SIMDRN  SIMEVT  SIMHFB  SIMRIV  SIMSTR  SIMRES  SIMLAK  SIMIBS  SIMSUB\n")
            file.write(f"{SIMSHB}  {SIMGHB}  {SIMRCH}  {SIMWEL}  {SIMDRN}  {SIMEVT}  {SIMHFB}  {SIMRIV}  {SIMSTR}  "
                       f"{SIMRES}  {SIMLAK}  {SIMIBS}  {SIMSUB}")

    def WriteOutput(self):
        with open(os.path.join(self.folder_path, "OutOpt.in"), "w") as file:
            outPars: pycomus.ComusOutputPars = self._model.CmsOutPars
            file.write(
                "GDWBDPRN  LYRBDPRN  CELLBDPRN  CELLHHPRN  CELLDDPRN  CELLFLPRN  LAKBDPRN  SEGMBDPRN  RECHBDPRN  IBSPRN  SUBPRN  NDBPRN  DBPRN  REGBDPRN\n")
            file.write(f"{outPars.gdw_bd}  {outPars.lyr_bd}  {outPars.cell_bd}  {outPars.cell_hh}  "
                       f"{outPars.cell_dd}  {outPars.cell_flp}  {outPars.lak_bd}  {outPars.segm_bd}  "
                       f"{outPars.rech_bd}  {outPars.ibs}  {outPars.sub}  {outPars.ndb}  {outPars.db}  "
                       f"{outPars.reg_bd}")

    def WriteRowColSpace(self):
        with open(os.path.join(self.folder_path, "GrdSpace.in"), "w") as file:
            file.write("ATTI  NUMID  DELT\n")
            index = 1
            for rowSpace in self._model.CmsDis.row_space:
                file.write(f"C  {index}  {rowSpace}\n")
                index += 1
            index = 1
            for colSpace in self._model.CmsDis.col_space:
                file.write(f"R  {index}  {colSpace}\n")
                index += 1

    def WritePeriod(self):
        with open(os.path.join(self.folder_path, "PerAttr.in"), "w") as file:
            # 写入第一行内容
            file.write("IPER  PERLEN  NSTEP  MULTR\n")
            index = 1
            for tuple in self._model.CmsTime:
                file.write(f"{int(index)}   {float(tuple[0])}   {int(tuple[1])}   {float(tuple[2])} \n")
                index += 1

    def WriteBCFLyrProp(self):
        with open(os.path.join(self.folder_path, "BcfLyr.in"), "w") as file:
            # 写入第一行内容
            file.write("LYRID  LYRCON  LYRTRPY  LYRIBS\n")
            for i in range(self._num_lyr):
                file.write(
                    f"{self._model.layers[i].lyr_id}  {self._model.layers[i].lyr_type}  "
                    f"{self._model.layers[i].lyr_trpy}  {self._model.layers[i].lyr_ibs}\n")

    def WriteBCFGridCell(self):
        with open(os.path.join(self.folder_path, "BcfGrd.in"), "w") as file:
            # 写入第一行内容
            file.write("ILYR  IROW  ICOL  IBOUND  CELLTOP  CELLBOT  TRANSM  HK  VCONT  SC1  SC2  WETDRY  SHEAD\n")
            for layer in range(self._num_lyr):
                for row in range(self._num_row):
                    for col in range(self._num_col):
                        grid_cell = self._model.layers[layer].grid_cells[row][col]
                        file.write(
                            f"{int(layer + 1)}  {int(row + 1)}  {int(col + 1)}  {int(grid_cell.ibound)}  {grid_cell.top}  {grid_cell.bot}  {grid_cell.tran}"
                            f"  {grid_cell.hk}  {grid_cell.vcont}  {grid_cell.sc1}  {grid_cell.sc2}  {grid_cell.wetdry}  {grid_cell.shead}\n")

    def WriteLPFLyrProp(self):
        with open(os.path.join(self.folder_path, "LpfLyr.in"), "w") as file:
            # 写入第一行内容
            file.write("LYRID  LYRTYPE  LYRHANI  LYRVKA  LYRCBD  LYRIBS\n")
            for i in range(self._num_lyr):
                file.write(
                    f"{self._model.layers[i].lyr_id}  {self._model.layers[i].lyr_type}  -1  0  "
                    f"{self._model.layers[i].lyr_cbd}  {self._model.layers[i].lyr_ibs}\n")

    def WriteLPFGridCell(self):
        with open(os.path.join(self.folder_path, "LpfGrd.in"), "w") as file:
            # 写入第一行内容
            file.write(
                "ILYR  IROW  ICOL  CELLTOP  CELLBOT  IBOUND  HK  HANI  VKA  VKCB  TKCB  SC1  SC2  WETDRY  SHEAD\n")
            for layer in range(self._num_lyr):
                for row in range(self._num_row):
                    for col in range(self._num_col):
                        grid_cell = self._model.layers[layer].grid_cells[row][col]
                        file.write(
                            f"{int(layer + 1)}  {int(row + 1)}  {int(col + 1)}  {grid_cell.top}  {grid_cell.bot}  {int(grid_cell.ibound)}  {grid_cell.hk}"
                            f"  {grid_cell.hani}  {grid_cell.vka}  {grid_cell.vkcb}  {grid_cell.tkcb}  {grid_cell.sc1}  {grid_cell.sc2}"
                            f"  {grid_cell.wetdry}  {grid_cell.shead}\n")

    def WriteRCH(self):
        rechr = self._package["RCH"]
        with open(os.path.join(self.folder_path, "RCH.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  IRECH  RECHR\n")
            for period, value in rechr.rechr.items():
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if value[layer, row, col] != 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {rechr.rech}  {value[layer, row, col]} \n")

    def WriteDRN(self):
        drn = self._package["DRN"]
        with open(os.path.join(self.folder_path, "DRN.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  DELEV  COND\n")
            periods = sorted(drn.cond.keys())
            for period in periods:
                cond_value = drn.cond[period]
                delev_value = drn.delev[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {delev_value[layer, row, col]}  "
                                    f"{cond_value[layer, row, col]}\n")

    def WriteGHB(self):
        ghb = self._package["GHB"]
        with open(os.path.join(self.folder_path, "GHB.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD  COND\n")
            periods = sorted(ghb.cond.keys())
            for period in periods:
                cond_value = ghb.cond[period]
                shead_value = ghb.shead[period]
                ehead_value = ghb.ehead[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}  {cond_value[layer, row, col]}\n")

    def WriteHFB(self):
        hfb: pycomus.ComusHfb = self._package["HFB"]
        with open(os.path.join(self.folder_path, "HFB.in"), "w") as file:
            file.write("ILYR  IROW1  ICOL1  IROW2  ICOL2  HCDW\n")
            for hfb_data in hfb.hfb_data:
                file.write(
                    f"{hfb_data[0] + 1}  {hfb_data[1] + 1}  {hfb_data[2] + 1}  {hfb_data[3] + 1}  {hfb_data[4] + 1}  "
                    f"{hfb_data[5]}\n")

    def WriteSHB(self):
        shb = self._package["SHB"]
        with open(os.path.join(self.folder_path, "SHB.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD\n")
            periods = sorted(shb.shead.keys())
            for period in periods:
                shead_value = shb.shead[period]
                ehead_value = shb.ehead[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if shead_value[layer, row, col] != 0 and ehead_value[layer, row, col] != 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}\n")

    def WriteWEL(self):
        wel = self._package["WEL"]
        with open(os.path.join(self.folder_path, "WEL.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  WELLR  SATTHR\n")
            periods = sorted(wel.wellr.keys())
            for period in periods:
                wellr_value = wel.wellr[period]
                satthr_value = wel.satthr[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if wellr_value[layer, row, col] != 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {wellr_value[layer, row, col]}  "
                                    f"{satthr_value[layer, row, col]}\n")

    def WriteEVT(self):
        evt = self._package["EVT"]
        with open(os.path.join(self.folder_path, "EVT.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  IEVT  ETSURF  ETRATE  ETMXD  ETEXP  NUMSEG\n")
            periods = sorted(evt.et_surf.keys())
            print(periods)
            for period in periods:
                ETSurf_value = evt.et_surf[period]
                ETRate_value = evt.et_rate[period]
                ETMxd_value = evt.et_mxd[period]
                ETExp_value = evt.et_exp[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if ETExp_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {evt.evt}  {ETSurf_value[layer, row, col]}  "
                                    f"{ETRate_value[layer, row, col]}  {ETMxd_value[layer, row, col]}  "
                                    f"{ETExp_value[layer, row, col]}  {evt.num_seg}\n")

    def WriteRIV(self):
        riv = self._package["RIV"]
        with open(os.path.join(self.folder_path, "RIV.in"), "w") as file:
            file.write("IPER  ILYR  IROW  ICOL  SHEAD  EHEAD  COND  RIVBTM\n")
            periods = sorted(riv.cond.keys())
            for period in periods:
                cond_value = riv.cond[period]
                shead_value = riv.shead[period]
                ehead_value = riv.ehead[period]
                rivBtm_value = riv.riv_btm[period]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if cond_value[layer, row, col] > 0:
                                file.write(
                                    f"{period + 1}  {layer + 1}  {row + 1}  {col + 1}  {shead_value[layer, row, col]}  "
                                    f"{ehead_value[layer, row, col]}  {cond_value[layer, row, col]}  {rivBtm_value[layer, row, col]}\n")

    def WriteRES(self):
        res = self._package["RES"].res
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
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if bvk_value[layer, row, col] >= 0 and btk_value[layer, row, col] > 0:
                                file.write(
                                    f"{resId + 1}  {index}  {layer + 1}  {row + 1}  {col + 1}  {btm_value[layer, row, col]}  "
                                    f"{bvk_value[layer, row, col]}  {btk_value[layer, row, col]}\n")
                                index += 1

    def WriteSTR(self):
        str = self._package["STR"].streamValue
        control_data = str.ControlParams
        period_data = str.PeriodData
        grid_data = str.GridData
        watUse_data = str.WatUseData
        watDrn_data = str.WatDrnData
        with open(os.path.join(self.folder_path, "STRCtrl.in"), "w") as file:
            file.write("SEGMID  NEXTID  NEXTAT  DIVSID  DIVSAT  DIVTPOPT  WUTPOPT  WUREGID  WUBKOPT  DRNOPT\n")
            for stream_id, params in control_data.items():
                file.write(f"{stream_id + 1}  {params[0]}  {params[1]}  {params[2]}  {params[3]}  {params[4]}  {params[5]}"
                           f"  {params[6]}  {params[7]}  {params[8]}\n")

        with open(os.path.join(self.folder_path, "STRPer.in"), "w") as file:
            file.write("IPER  SEGMID  HCALOPT  USLEV  UELEV  DSLEV  DELEV  WATPNT  WATWAY  WATDIV  WATUSE  EVRATE  RCHCOE  WBKCOE\n")
            period_data = OrderedDict(sorted(period_data.items()))
            for key, value in period_data.items():
                period_data[key] = OrderedDict(sorted(value.items()))
            for res_id, periodData in period_data.items():
                for period_id, value in periodData.items():
                    file.write(f"{int(period_id + 1)}  {int(res_id + 1)}  {int(value[0])}  {float(value[1])}  {float(value[2])}  {float(value[3])}  "
                               f"{float(value[4])}  {float(value[5])}  {float(value[6])}  {float(value[7])}  {float(value[8])}  {float(value[9])}  {float(value[10])}  {float(value[11])}\n")

        with open(os.path.join(self.folder_path, "STRGrd.in"), "w") as file:
            file.write("SEGMID  CELLID  ILYR  IROW  ICOL  LEN  BTM  BWDT  SIZH1  SIZH2  BVK  BTK  SLP  NDC\n")
            segIds = sorted(grid_data["CELLID"].keys())
            for segId in segIds:
                index = 1
                cellID_value = grid_data["CELLID"][segId]
                len_value = grid_data["LEN"][segId]
                btm_value = grid_data["BTM"][segId]
                bwdt_value = grid_data["BWDT"][segId]
                sizh1_value = grid_data["SIZH1"][segId]
                sizh2_value = grid_data["SIZH2"][segId]
                bvk_value = grid_data["BVK"][segId]
                btk_value = grid_data["BTK"][segId]
                slp_value = grid_data["SLP"][segId]
                ndc_value = grid_data["NDC"][segId]
                for layer in range(self._num_lyr):
                    for row in range(self._num_row):
                        for col in range(self._num_col):
                            if bvk_value[layer, row, col] >= 0 and btk_value[layer, row, col] > 0:
                                file.write(
                                    f"{segId + 1}  {int(cellID_value[layer, row, col])}  {layer + 1}  {row + 1}  {col + 1}  {len_value[layer, row, col]}  "
                                    f"{btm_value[layer, row, col]}  {bwdt_value[layer, row, col]}  {sizh1_value[layer, row, col]}  {sizh2_value[layer, row, col]}  "
                                    f"{bvk_value[layer, row, col]}  {btk_value[layer, row, col]}  {slp_value[layer, row, col]}  {ndc_value[layer, row, col]}\n")
                                index += 1

        with open(os.path.join(self.folder_path, "STRWatUse.in"), "w") as file:
            file.write("WUREGID  ILYR  IROW  ICOL  RATIO\n")
            print(watUse_data.keys())
            wuregId_value = watUse_data["WUREGID"]
            ratio_value = watUse_data["RATIO"]
            for layer in range(self._num_lyr):
                for row in range(self._num_row):
                    for col in range(self._num_col):
                        if wuregId_value[layer, row, col] > 0:
                            file.write(
                                f"{int(wuregId_value[layer, row, col])}  {layer + 1}  {row + 1}  {col + 1}  {ratio_value[layer, row, col]}\n")

        with open(os.path.join(self.folder_path, "STRWatDrn.in"), "w") as file:
            file.write("ILYR  IROW  ICOL  DELEV  COND  SEGMID\n")
            delev_value = watDrn_data["DELEV"]
            cond_value = watDrn_data["COND"]
            segmid_value = watDrn_data["SEGMID"]
            for layer in range(self._num_lyr):
                for row in range(self._num_row):
                    for col in range(self._num_col):
                        if segmid_value[layer, row, col] > 0:
                            file.write(
                                f"{layer + 1}  {row + 1}  {col + 1}  {delev_value[layer, row, col]}  "
                                f"{cond_value[layer, row, col]}  {segmid_value[layer, row, col]}\n")
