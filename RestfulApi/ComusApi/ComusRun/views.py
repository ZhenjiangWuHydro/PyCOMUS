import itertools
import itertools
import os
import subprocess
import tempfile

import pandas as pd
from ComusBnd.models import ComusSHBModel, ComusGHBModel, ComusRCHModel, ComusWELModel, ComusDRNModel, ComusEVTModel, \
    ComusHFBModel, ComusRIVModel, ComusIBSModel, ComusSTRCtrlModel, ComusSTRPeriodModel, ComusSTRGridModel, \
    ComusSTRWaterUseModel, ComusSTRDrnModel, ComusRESCtrlModel, ComusRESPeriodModel, ComusRESGridModel, \
    ComusLAKCtrlModel, ComusLAKPeriodModel, ComusLAKGridModel, ComusREGModel, ComusSUBCtrlModel, ComusSUBMzModel, \
    ComusSUBNdbLyrModel, ComusSUBNdbGridModel, ComusSUBDbLyrModel, ComusSUBDbGridModel
from ComusDis.models import ComusDisModel, ComusCtrlParsModel, ComusOutParsModel, ComusSpaceModel, ComusBcfPropModel, \
    ComusLpfPropModel, ComusGridParsModel, ComusPeriodModel
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .CONSTANTS import CON_FILE_NAME, OUT_FILE_NAME, GRID_SPACE_FILE_NAME, BCF_LYR_FILE_NAME, LPF_LYR_FILE_NAME, \
    LPF_GRID_FILE_NAME, BCF_GRID_FILE_NAME, PERIOD_FILE_NAME, SHB_FILE_NAME, GHB_FILE_NAME, RCH_FILE_NAME, \
    WEL_FILE_NAME, DRN_FILE_NAME, EVT_FILE_NAME, HFB_FILE_NAME, RIV_FILE_NAME, IBS_FILE_NAME, BND_FILE_NAME, \
    STR_CTRL_FILE_NAME, STR_PERIOD_FILE_NAME, STR_GRID_FILE_NAME, STR_WAT_USE_FILE_NAME, STR_WAT_DRN_FILE_NAME, \
    RES_CTRL_FILE_NAME, RES_PERIOD_FILE_NAME, RES_GRID_FILE_NAME, LAK_CTRL_FILE_NAME, LAK_PERIOD_FILE_NAME, \
    LAK_GRID_FILE_NAME, REG_FILE_NAME, SUB_CTRL_FILE_NAME, SUB_MZ_FILE_NAME, SUB_NDB_FILE_NAME, SUB_NDB_GRID_FILE_NAME, \
    SUB_DB_FILE_NAME, SUB_DB_GRID_FILE_NAME


class ComusRunView(APIView):
    temp_dir = tempfile.gettempdir()
    bnd_dict = {
        "SIMSHB": 0,
        "SIMGHB": 0,
        "SIMRCH": 0,
        "SIMWEL": 0,
        "SIMDRN": 0,
        "SIMEVT": 0,
        "SIMHFB": 0,
        "SIMRIV": 0,
        "SIMSTR": 0,
        "SIMRES": 0,
        "SIMLAK": 0,
        "SIMIBS": 0,
        "SIMSUB": 0,
    }

    def post(self, request):
        user_name = request.data.get('user_name')
        project_name = request.data.get('project_name')

        if not user_name or not project_name:
            return Response({"error": "'user_name' and 'project_name' parameters are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            comus_dis = ComusDisModel.objects.get(user_name=user_name, project_name=project_name)
        except (ComusDisModel.DoesNotExist):
            return Response({'error': 'This COMUS model not found'}, status=status.HTTP_404_NOT_FOUND)

        # Make directory
        project_dir = os.path.join(self.temp_dir, f"{user_name}_{project_name}", "Data.in")
        if not os.path.exists(project_dir):
            os.makedirs(project_dir, exist_ok=True)

        # Write control parameters
        try:
            ctrl_pars = ComusCtrlParsModel.objects.get(comus_dis=comus_dis)
            num_lyr, num_row, num_col, sim_type, intblkm = self.write_ctrl(project_dir, ctrl_pars)
        except ComusCtrlParsModel.DoesNotExist:
            return Response({'error': 'ComusCtrlParsModel not found for this COMUS model'},
                            status=status.HTTP_404_NOT_FOUND)

        # Write output parameters
        try:
            output_pars = ComusOutParsModel.objects.get(comus_dis=comus_dis)
            self.write_output(project_dir, output_pars)
        except ComusOutParsModel.DoesNotExist:
            return Response({'error': 'ComusOutParsModel not found for this COMUS model'},
                            status=status.HTTP_404_NOT_FOUND)

        # Write space parameters
        try:
            space_pars = ComusSpaceModel.objects.get(comus_dis=comus_dis)
            self.write_space(project_dir, space_pars)
        except ComusSpaceModel.DoesNotExist:
            return Response({'error': 'ComusSpaceModel not found for this COMUS model'},
                            status=status.HTTP_404_NOT_FOUND)

        # Write layer property
        if intblkm == 1:
            try:
                bcf_prop = ComusBcfPropModel.objects.get(comus_dis=comus_dis)
                self.write_bcf_property(project_dir, bcf_prop)
            except ComusBcfPropModel.DoesNotExist:
                return Response({'error': 'ComusBcfPropModel not found for this COMUS model'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                lpf_prop = ComusLpfPropModel.objects.get(comus_dis=comus_dis)
                self.write_lpf_property(project_dir, lpf_prop)
            except ComusLpfPropModel.DoesNotExist:
                return Response({'error': 'ComusLpfPropModel not found for this COMUS model'},
                                status=status.HTTP_404_NOT_FOUND)

        # Write grid parameters
        try:
            grid_pars = ComusGridParsModel.objects.get(comus_dis=comus_dis)
            msg = self.write_grid_pars(project_dir, grid_pars, num_lyr, num_row, num_col, intblkm)
            if msg:
                return Response({'error': msg},
                                status=status.HTTP_404_NOT_FOUND)
        except ComusGridParsModel.DoesNotExist:
            return Response({'error': 'ComusGridParsModel not found for this COMUS model'},
                            status=status.HTTP_404_NOT_FOUND)

        # Write period
        try:
            space_pars = ComusPeriodModel.objects.get(comus_dis=comus_dis)
            self.write_period(project_dir, space_pars)
        except ComusPeriodModel.DoesNotExist:
            return Response({'error': 'ComusPeriodModel not found for this COMUS model'},
                            status=status.HTTP_404_NOT_FOUND)
        # --------------------------------------Boundary---------------------------
        # SHB
        if ComusSHBModel.objects.filter(comus_dis=comus_dis).exists():
            shb_pars = ComusSHBModel.objects.get(comus_dis=comus_dis)
            self.write_shb(project_dir, shb_pars)
        # GHB
        if ComusGHBModel.objects.filter(comus_dis=comus_dis).exists():
            ghb_pars = ComusGHBModel.objects.get(comus_dis=comus_dis)
            self.write_ghb(project_dir, ghb_pars)

        # RCH
        if ComusRCHModel.objects.filter(comus_dis=comus_dis).exists():
            rch_pars = ComusRCHModel.objects.get(comus_dis=comus_dis)
            self.write_rch(project_dir, rch_pars)

        # WEL
        if ComusWELModel.objects.filter(comus_dis=comus_dis).exists():
            wel_pars = ComusWELModel.objects.get(comus_dis=comus_dis)
            self.write_wel(project_dir, wel_pars)

        # DRN
        if ComusDRNModel.objects.filter(comus_dis=comus_dis).exists():
            drn_pars = ComusDRNModel.objects.get(comus_dis=comus_dis)
            self.write_drn(project_dir, drn_pars)

        # EVT
        if ComusEVTModel.objects.filter(comus_dis=comus_dis).exists():
            evt_pars = ComusEVTModel.objects.get(comus_dis=comus_dis)
            self.write_evt(project_dir, evt_pars)

        # HFB
        if ComusHFBModel.objects.filter(comus_dis=comus_dis).exists():
            hfb_pars = ComusHFBModel.objects.get(comus_dis=comus_dis)
            self.write_hfb(project_dir, hfb_pars)

        # RIV
        if ComusRIVModel.objects.filter(comus_dis=comus_dis).exists():
            riv_pars = ComusRIVModel.objects.get(comus_dis=comus_dis)
            self.write_riv(project_dir, riv_pars)

        # IBS
        if ComusIBSModel.objects.filter(comus_dis=comus_dis).exists():
            ibs_pars = ComusIBSModel.objects.get(comus_dis=comus_dis)
            self.write_ibs(project_dir, ibs_pars)

        # STR
        if ComusSTRCtrlModel.objects.filter(comus_dis=comus_dis).exists():
            str_ctrl_pars = ComusSTRCtrlModel.objects.get(comus_dis=comus_dis)
            self.write_str_ctrl(project_dir, str_ctrl_pars)
        if ComusSTRPeriodModel.objects.filter(comus_dis=comus_dis).exists():
            str_period_pars = ComusSTRPeriodModel.objects.get(comus_dis=comus_dis)
            self.write_str_period(project_dir, str_period_pars)
        if ComusSTRGridModel.objects.filter(comus_dis=comus_dis).exists():
            str_grid_pars = ComusSTRGridModel.objects.get(comus_dis=comus_dis)
            self.write_str_grid(project_dir, str_grid_pars)
        if ComusSTRWaterUseModel.objects.filter(comus_dis=comus_dis).exists():
            str_water_use_pars = ComusSTRWaterUseModel.objects.get(comus_dis=comus_dis)
            self.write_str_water_use(project_dir, str_water_use_pars)
        if ComusSTRDrnModel.objects.filter(comus_dis=comus_dis).exists():
            str_drn_pars = ComusSTRDrnModel.objects.get(comus_dis=comus_dis)
            self.write_str_drn(project_dir, str_drn_pars)

        # RES
        if ComusRESCtrlModel.objects.filter(comus_dis=comus_dis).exists():
            res_ctrl_pars = ComusRESCtrlModel.objects.get(comus_dis=comus_dis)
            self.write_res_ctrl(project_dir, res_ctrl_pars)
        if ComusRESPeriodModel.objects.filter(comus_dis=comus_dis).exists():
            res_period_pars = ComusRESPeriodModel.objects.get(comus_dis=comus_dis)
            self.write_res_period(project_dir, res_period_pars)
        if ComusRESGridModel.objects.filter(comus_dis=comus_dis).exists():
            res_grid_pars = ComusRESGridModel.objects.get(comus_dis=comus_dis)
            self.write_res_grid(project_dir, res_grid_pars)

        # LAK
        if ComusLAKCtrlModel.objects.filter(comus_dis=comus_dis).exists():
            lak_ctrl_pars = ComusLAKCtrlModel.objects.get(comus_dis=comus_dis)
            self.write_lak_ctrl(project_dir, lak_ctrl_pars)
        if ComusLAKPeriodModel.objects.filter(comus_dis=comus_dis).exists():
            lak_period_pars = ComusLAKPeriodModel.objects.get(comus_dis=comus_dis)
            self.write_res_period(project_dir, lak_period_pars)
        if ComusLAKGridModel.objects.filter(comus_dis=comus_dis).exists():
            lak_grid_pars = ComusLAKGridModel.objects.get(comus_dis=comus_dis)
            self.write_res_grid(project_dir, lak_grid_pars)

        # Zone Budget
        if ComusREGModel.objects.filter(comus_dis=comus_dis).exists():
            reg_pars = ComusREGModel.objects.get(comus_dis=comus_dis)
            self.write_reg(project_dir, reg_pars)

            # STR
        if ComusSUBCtrlModel.objects.filter(comus_dis=comus_dis).exists():
            sub_ctrl_pars = ComusSUBCtrlModel.objects.get(comus_dis=comus_dis)
            self.write_sub_ctrl(project_dir, sub_ctrl_pars)
        if ComusSUBMzModel.objects.filter(comus_dis=comus_dis).exists():
            sub_mz_pars = ComusSUBMzModel.objects.get(comus_dis=comus_dis)
            self.write_sub_mz(project_dir, sub_mz_pars)
        if ComusSUBNdbLyrModel.objects.filter(comus_dis=comus_dis).exists():
            sub_ndb_lyr_pars = ComusSUBNdbLyrModel.objects.get(comus_dis=comus_dis)
            self.write_sub_ndb_lyr(project_dir, sub_ndb_lyr_pars)
        if ComusSUBNdbGridModel.objects.filter(comus_dis=comus_dis).exists():
            sub_ndb_grid_pars = ComusSUBNdbGridModel.objects.get(comus_dis=comus_dis)
            self.write_sub_ndb_grid(project_dir, sub_ndb_grid_pars)
        if ComusSUBDbLyrModel.objects.filter(comus_dis=comus_dis).exists():
            sub_db_lyr_pars = ComusSUBDbLyrModel.objects.get(comus_dis=comus_dis)
            self.write_sub_db_lyr(project_dir, sub_db_lyr_pars)
        if ComusSUBDbGridModel.objects.filter(comus_dis=comus_dis).exists():
            sub_db_grid_pars = ComusSUBDbGridModel.objects.get(comus_dis=comus_dis)
            self.write_sub_db_grid(project_dir, sub_db_grid_pars)
        # --------------------------------------Boundary---------------------------

        self.write_bnd(project_dir)

        # Run
        flag, msg = self.run(project_dir)
        if not flag:
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Model run successful!'}, status=status.HTTP_200_OK)

    def write_ctrl(self, project_dir, ctrl_pars):
        header_line = "NUMLYR  NUMROW  NUMCOL  DIMUNIT  TIMEUNIT  XSTCORD  YSTCORD  SIMMTHD  SIMTYPE  LAMBDA  INTBLKM  ISOLVE  MAXIT  DAMP  HCLOSE  " \
                      "RCLOSE  IRELAX  THETA  GAMMA  AKAPPA  NITER  HNOFLO  ICHFLG  IWDFLG  WETFCT  IWETIT  IHDWET  IREGSTA  IMULTD  NUMTD"
        conParsData = [ctrl_pars.num_layer, ctrl_pars.num_row, ctrl_pars.num_col, ctrl_pars.dim_unit,
                       ctrl_pars.time_unit, ctrl_pars.x_coord, ctrl_pars.y_coord, ctrl_pars.sim_mtd,
                       ctrl_pars.sim_type, ctrl_pars.acc_lambda, ctrl_pars.intblkm, ctrl_pars.solve, ctrl_pars.max_iter,
                       ctrl_pars.damp, ctrl_pars.h_close,
                       ctrl_pars.r_close, ctrl_pars.relax, ctrl_pars.theta, ctrl_pars.gamma, ctrl_pars.akappa,
                       ctrl_pars.n_iter, ctrl_pars.hno_flo,
                       ctrl_pars.ch_flg, ctrl_pars.wd_flg, ctrl_pars.wet_fct, ctrl_pars.newt_iter, ctrl_pars.hd_wet,
                       ctrl_pars.reg_sta, ctrl_pars.mul_td,
                       ctrl_pars.num_td]
        with open(os.path.join(project_dir, CON_FILE_NAME), "w") as file:
            file.write(header_line + "\n")
            file.write('    '.join(map(str, conParsData)))
        return int(ctrl_pars.num_layer), int(ctrl_pars.num_row), int(ctrl_pars.num_col), int(ctrl_pars.sim_type), int(
            ctrl_pars.intblkm)

    def write_output(self, project_dir, output_pars):
        with open(os.path.join(project_dir, OUT_FILE_NAME), "w") as file:
            file.write(
                "GDWBDPRN  LYRBDPRN  CELLBDPRN  CELLHHPRN  CELLDDPRN  CELLFLPRN  LAKBDPRN  SEGMBDPRN  RECHBDPRN  "
                "IBSPRN  SUBPRN  NDBPRN  DBPRN  REGBDPRN\n")
            file.write(f"{output_pars.gdw_bd}  {output_pars.lyr_bd}  {output_pars.cell_bd}  {output_pars.cell_hh}  "
                       f"{output_pars.cell_dd}  {output_pars.cell_flo}  {output_pars.lak_bd}  {output_pars.segm_bd}  "
                       f"{output_pars.rech_bd}  {output_pars.ibs}  {output_pars.sub}  {output_pars.ndb}  {output_pars.db}  "
                       f"{output_pars.reg_bd}")

    def write_space(self, project_dir, space_pars):
        data_dict = space_pars.data
        df = pd.DataFrame({
            'ATTI': data_dict['atti'],
            'NUMID': data_dict['num_id'],
            'DELT': data_dict['delt']
        })
        df_sorted = df.sort_values(by=['ATTI', 'NUMID'])
        output_file_path = os.path.join(project_dir, GRID_SPACE_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_bcf_property(self, project_dir, bcf_prop):
        data_dict = bcf_prop.data
        df = pd.DataFrame({
            'LYRID': range(1, len(data_dict['type']) + 1),
            'LYRCON': data_dict['type'],
            'LYRIBS': data_dict['ibs'],
            'LYRTRPY': data_dict['trpy']
        })
        df = df[['LYRID', 'LYRCON', 'LYRTRPY', 'LYRIBS']]
        output_file_path = os.path.join(project_dir, BCF_LYR_FILE_NAME)
        df.to_csv(output_file_path, sep=' ', index=False)

    def write_lpf_property(self, project_dir, lpf_prop):
        data_dict = lpf_prop.data
        df = pd.DataFrame({
            'LYRID': range(1, len(data_dict['type']) + 1),
            'LYRTYPE': data_dict['type'],
            'LYRHANI': -1,
            'LYRVKA': 0,
            'LYRCBD': data_dict['cbd'],
            'LYRIBS': data_dict['ibs']
        })
        df = df[['LYRID', 'LYRTYPE', 'LYRHANI', 'LYRVKA', 'LYRCBD', 'LYRIBS']]
        output_file_path = os.path.join(project_dir, LPF_LYR_FILE_NAME)
        df.to_csv(output_file_path, sep=' ', index=False)

    def write_grid_pars(self, project_dir, grid_pars, num_lyr, num_row, num_col, intblkm):
        data_dict: dict = grid_pars.data
        require_keys = ['ibound', 'top', 'bot']
        for require_key in require_keys:
            if require_key not in data_dict.keys():
                return f"{require_key} should exist in the input data! Please reset."
        for key, value in data_dict.items():
            if len(value) != num_lyr * num_row * num_col:
                return f"The length of {key} should be equal to {num_lyr * num_row * num_col}."
        layers, rows, cols = zip(
            *[(layer + 1, row + 1, col + 1) for layer in range(num_lyr) for row in range(num_row) for col in
              range(num_col)])
        if intblkm == 1:
            df = pd.DataFrame({
                'ILYR': layers,
                'IROW': rows,
                'ICOL': cols,
                'IBOUND': data_dict['ibound'],
                'CELLTOP': data_dict['top'],
                'CELLBOT': data_dict['bot'],
                'TRANSM': data_dict['transm'] if "transm" in data_dict.keys() else 0,
                'HK': data_dict['kx'] if "kx" in data_dict.keys() else 0,
                'VCONT': data_dict['vcont'] if "vcont" in data_dict.keys() else 0,
                'SC1': data_dict['sc1'] if "sc1" in data_dict.keys() else 0,
                'SC2': data_dict['sc2'] if "sc2" in data_dict.keys() else 0,
                'WETDRY': data_dict['wet_dry'] if "wet_dry" in data_dict.keys() else 0,
                'SHEAD': data_dict['shead'] if "shead" in data_dict.keys() else 0
            })
            output_file_path = os.path.join(project_dir, BCF_GRID_FILE_NAME)
        else:
            df = pd.DataFrame({
                'ILYR': layers,
                'IROW': rows,
                'ICOL': cols,
                'CELLTOP': data_dict['top'],
                'CELLBOT': data_dict['bot'],
                'IBOUND': data_dict['ibound'],
                'HK': data_dict['kx'] if "kx" in data_dict.keys() else 0,
                'HANI': [(ky / hk) if hk != 0 else 0 for hk, ky in
                         zip(data_dict.get('kx') or itertools.repeat(0, num_lyr * num_row * num_col),
                             data_dict.get('ky') or itertools.repeat(0, num_lyr * num_row * num_col))],
                'VKA': data_dict['kz'] if "kz" in data_dict.keys() else 0,
                'VKCB': data_dict['vkcb'] if "vkcb" in data_dict.keys() else 0,
                'TKCB': data_dict['tkcb'] if "tkcb" in data_dict.keys() else 0,
                'SC1': data_dict['sc1'] if "sc1" in data_dict.keys() else 0,
                'SC2': data_dict['sc2'] if "sc2" in data_dict.keys() else 0,
                'WETDRY': data_dict['wet_dry'] if "wet_dry" in data_dict.keys() else 0,
                'SHEAD': data_dict['shead'] if "shead" in data_dict.keys() else 0,
            })
            output_file_path = os.path.join(project_dir, LPF_GRID_FILE_NAME)

        df.to_csv(output_file_path, sep=' ', index=False)

    def write_period(self, project_dir, period_data):
        data_dict = period_data.period
        with open(os.path.join(project_dir, PERIOD_FILE_NAME), "w") as file:
            file.write("IPER  PERLEN  NSTEP  MULTR\n")
            for period, data in data_dict.items():
                file.write(f"{period}   {data['period_len']}   {data['num_step']}   {data['multr']}\n")

    def write_shb(self, project_dir, shb_data):
        self.bnd_dict["SIMSHB"] = 1
        data_dict = shb_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IPER': key,
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'SHEAD': sublist[3],
                    'EHEAD': sublist[4]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, SHB_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_ghb(self, project_dir, ghb_data):
        self.bnd_dict["SIMGHB"] = 1
        data_dict = ghb_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IPER': key,
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'SHEAD': sublist[3],
                    'EHEAD': sublist[4],
                    'COND': sublist[5]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, GHB_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_rch(self, project_dir, rch_data):
        self.bnd_dict["SIMRCH"] = 1
        data_dict = rch_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IPER': key,
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'RECHR': sublist[3]
                })
        all_df = pd.DataFrame(rows)
        all_df["IRECH"] = rch_data.rech
        all_df = all_df[['IPER', 'ILYR', 'IROW', 'ICOL', 'IRECH', 'RECHR']]
        df_sorted = all_df.sort_values(by=['IPER', 'ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, RCH_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_wel(self, project_dir, wel_data):
        self.bnd_dict["SIMWEL"] = 1
        data_dict = wel_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IPER': key,
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'WELLR': sublist[3],
                    'SATTHR': sublist[4]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, WEL_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_drn(self, project_dir, drn_data):
        self.bnd_dict["SIMDRN"] = 1
        data_dict = drn_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IPER': key,
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'DELEV': sublist[3],
                    'COND': sublist[4]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, DRN_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_evt(self, project_dir, evt_data):
        self.bnd_dict["SIMEVT"] = 1
        data_dict = evt_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IPER': key,
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'ETSURF': sublist[3],
                    'ETRATE': sublist[4],
                    'ETMXD': sublist[5],
                    'ETEXP': sublist[6]
                })
        all_df = pd.DataFrame(rows)
        all_df["IEVT"] = evt_data.evt
        all_df["NUMSEG"] = evt_data.num_seg
        all_df = all_df[['IPER', 'ILYR', 'IROW', 'ICOL', 'IEVT', 'ETSURF', 'ETRATE', 'ETMXD', 'ETEXP', 'NUMSEG']]
        df_sorted = all_df.sort_values(by=['IPER', 'ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, EVT_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_hfb(self, project_dir, hfb_data):
        self.bnd_dict["SIMHFB"] = 1
        data_dict = hfb_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'ILYR': key,
                    'IROW1': sublist[0],
                    'ICOL1': sublist[1],
                    'IROW2': sublist[2],
                    'ICOL2': sublist[3],
                    'HCDW': sublist[4]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['ILYR', 'IROW1', 'ICOL1'])
        output_file_path = os.path.join(project_dir, HFB_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_riv(self, project_dir, riv_data):
        self.bnd_dict["SIMRIV"] = 1
        data_dict = riv_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IPER': key,
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'SHEAD': sublist[3],
                    'EHEAD': sublist[4],
                    'COND': sublist[5],
                    'RIVBTM': sublist[6]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, RIV_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_ibs(self, project_dir, ibs_data):
        self.bnd_dict["SIMIBS"] = 1
        data_dict = ibs_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'ILYR': key,
                    'IROW': sublist[0],
                    'ICOL': sublist[1],
                    'SHEAD': sublist[2],
                    'EHEAD': sublist[3],
                    'COND': sublist[4],
                    'RIVBTM': sublist[5]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, IBS_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_str_ctrl(self, project_dir, str_ctrl_data):
        self.bnd_dict["SIMSTR"] = 1
        data_dict = str_ctrl_data.data
        rows = []
        for key, value in data_dict.items():
            rows.append({
                'SEGMID': key,
                'NEXTID': value[0],
                'NEXTAT': value[1],
                'DIVSID': value[2],
                'DIVSAT': value[3],
                'DIVTPOPT': value[4],
                'WUTPOPT': value[5],
                'WUREGID': value[6],
                'WUBKOPT': value[7],
                'DRNOPT': value[8]
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['SEGMID'])
        output_file_path = os.path.join(project_dir, STR_CTRL_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_str_period(self, project_dir, str_period_data):
        data_dict = str_period_data.data
        rows = []
        for str_id, value in data_dict.items():
            for period, rea_value in value.items():
                rows.append({
                    'IPER': period,
                    'SEGMID': str_id,
                    'HCALOPT': rea_value[0],
                    'USLEV': rea_value[1],
                    'UELEV': rea_value[2],
                    'DSLEV': rea_value[3],
                    'DELEV': rea_value[4],
                    'WATPNT': rea_value[5],
                    'WATWAY': rea_value[6],
                    'WATDIV': rea_value[7],
                    'WATUSE': rea_value[8],
                    'EVRATE': rea_value[9],
                    'RCHCOE': rea_value[10],
                    'WBKCOE': rea_value[11],
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'SEGMID'])
        output_file_path = os.path.join(project_dir, STR_PERIOD_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_str_grid(self, project_dir, str_grid_data):
        data_dict = str_grid_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'SEGMID': key,
                    'CELLID': sublist[3],
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'LEN': sublist[4],
                    'BTM': sublist[5],
                    'BWDT': sublist[6],
                    'SIZH1': sublist[7],
                    'SIZH2': sublist[8],
                    'BVK': sublist[9],
                    'BTK': sublist[10],
                    'SLP': sublist[11],
                    'NDC': sublist[12],
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['SEGMID', 'CELLID'])
        output_file_path = os.path.join(project_dir, STR_GRID_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_str_water_use(self, project_dir, str_water_use_data):
        data_list = str_water_use_data.data
        rows = []
        for sublist in data_list:
            rows.append({
                'WUREGID': sublist[3],
                'ILYR': sublist[0],
                'IROW': sublist[1],
                'ICOL': sublist[2],
                'RATIO': sublist[4]
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['WUREGID', 'ILYR'])
        output_file_path = os.path.join(project_dir, STR_WAT_USE_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_str_drn(self, project_dir, str_drn_data):
        data_list = str_drn_data.data
        rows = []
        for sublist in data_list:
            rows.append({
                'ILYR': sublist[0],
                'IROW': sublist[1],
                'ICOL': sublist[2],
                'DELEV': sublist[3],
                'COND': sublist[4],
                'SEGMID': sublist[5]
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['ILYR', 'IROW', 'ICOL'])
        output_file_path = os.path.join(project_dir, STR_WAT_DRN_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_res_ctrl(self, project_dir, res_ctrl_data):
        self.bnd_dict["SIMRES"] = 1
        data_dict = res_ctrl_data.data
        rows = []
        for key, value in data_dict.items():
            rows.append({
                'RESID': key,
                'EVEXP': value[0],
                'EVMAXD': value[1],
                'NUMSEG': value[2],
                'NUMPT': value[3]
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['RESID'])
        output_file_path = os.path.join(project_dir, RES_CTRL_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_res_period(self, project_dir, res_period_data):
        data_dict = res_period_data.data
        rows = []
        for res_id, value in data_dict.items():
            for period, rea_value in value.items():
                rows.append({
                    'IPER': period,
                    'RESID': res_id,
                    'SHEAD': rea_value[0],
                    'EHEAD': rea_value[1],
                    'RCHRG': rea_value[2],
                    'GEVT': rea_value[3]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'RESID'])
        output_file_path = os.path.join(project_dir, RES_PERIOD_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_res_grid(self, project_dir, res_grid_data):
        data_dict = res_grid_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'RESID': key,
                    'CELLID': sublist[3],
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'BTM': sublist[4],
                    'BVK': sublist[5],
                    'BTK': sublist[6]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['RESID', 'CELLID'])
        output_file_path = os.path.join(project_dir, RES_GRID_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_lak_ctrl(self, project_dir, lak_ctrl_data):
        self.bnd_dict["SIMLAK"] = 1
        data_dict = lak_ctrl_data.data
        rows = []
        for key, value in data_dict.items():
            rows.append({
                'LAKEID': key,
                'STRID': value[0],
                'DIVSID': value[1],
                'DIVSAT': value[2],
                'BETA': value[3],
                'INIHLEV': value[4],
                'DEADHLEV': value[5],
                'EVEXP': value[6],
                'EVMAXD': value[7],
                'NUMSEG': value[8],
                'STRBED': value[9],
                'STRWDT': value[10],
                'STRNDC': value[11],
                'STRSLP': value[12]
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['LAKEID'])
        output_file_path = os.path.join(project_dir, LAK_CTRL_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_lak_period(self, project_dir, lak_period_data):
        data_dict = lak_period_data.data
        rows = []
        for lak_id, value in data_dict.items():
            for period, rea_value in value.items():
                rows.append({
                    'IPER': period,
                    'LAKEID': lak_id,
                    'PCP': rea_value[0],
                    'RNFCOF': rea_value[1],
                    'PRHCOF': rea_value[2],
                    'ET0': rea_value[3],
                    'EVWBCOF': rea_value[4],
                    'GEVCOF': rea_value[5],
                    'WATDIV': rea_value[6],
                    'WATUSE': rea_value[7]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IPER', 'LAKEID'])
        output_file_path = os.path.join(project_dir, LAK_PERIOD_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_lak_grid(self, project_dir, lak_grid_data):
        data_dict = lak_grid_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'LAKEID': key,
                    'CELLID': sublist[3],
                    'ILYR': sublist[0],
                    'IROW': sublist[1],
                    'ICOL': sublist[2],
                    'BTM': sublist[4],
                    'LNK': sublist[5],
                    'SC1': sublist[6],
                    'SC2': sublist[7]
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['LAKEID', 'CELLID'])
        output_file_path = os.path.join(project_dir, LAK_GRID_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_reg(self, project_dir, reg_data):
        data_dict = reg_data.data
        rows = []
        sch_id = 1
        for sch_name, sch_value in data_dict.items():
            reg_id = 1
            for reg_name, reg_value in sch_value.items():
                rows.append({
                    'SCHID': sch_id,
                    'SCHNAM': sch_name,
                    'IREG': reg_id,
                    'REGNAM': reg_name,
                    'ILYR': reg_value[0],
                    'IROW': reg_value[1],
                    'ICOL': reg_value[2]
                })
                reg_id += 1
            sch_id += 1
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['SCHID', 'IREG'])
        output_file_path = os.path.join(project_dir, REG_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_sub_ctrl(self, project_dir, sub_ctrl_data):
        self.bnd_dict["SIMSUB"] = 1
        with open(os.path.join(project_dir, SUB_CTRL_FILE_NAME), "w") as file:
            file.write("NNDB    NDB    NMZ    NN    ACC    ITMIN    DSHOPT\n")
            file.write("    ".join(map(str, [
                sub_ctrl_data.num_ndb, sub_ctrl_data.num_db, sub_ctrl_data.num_mz, sub_ctrl_data.nn, sub_ctrl_data.acc,
                sub_ctrl_data.it_min, sub_ctrl_data.dsh_opt
            ])))

    def write_sub_mz(self, project_dir, sub_mz_data):
        data_dict = sub_mz_data.data
        rows = []
        for key, value in data_dict.items():
            rows.append({
                'IMZ': key,
                'MZVK': value[0],
                'MZSFE': value[1],
                'MZSFV': value[2]
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IMZ'])
        output_file_path = os.path.join(project_dir, SUB_MZ_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_sub_ndb_lyr(self, project_dir, sub_ndb_lyr_data):
        data_dict = sub_ndb_lyr_data.data
        rows = []
        for key, value in data_dict.items():
            rows.append({
                'INDB': key,
                'ILYR': value
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['INDB'])
        output_file_path = os.path.join(project_dir, SUB_NDB_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_sub_ndb_grid(self, project_dir, sub_ndb_grid_data):
        data_dict = sub_ndb_grid_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'INDB': key,
                    'IROW': sublist[0],
                    'ICOL': sublist[1],
                    'HC': sublist[2],
                    'SFE': sublist[3],
                    'SFV': sublist[4],
                    'COM': sublist[5],
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['INDB'])
        output_file_path = os.path.join(project_dir, SUB_NDB_GRID_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_sub_db_lyr(self, project_dir, sub_db_lyr_data):
        data_dict = sub_db_lyr_data.data
        rows = []
        for key, value in data_dict.items():
            rows.append({
                'IDB': key,
                'ILYR': value
            })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IDB'])
        output_file_path = os.path.join(project_dir, SUB_DB_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_sub_db_grid(self, project_dir, sub_db_grid_data):
        data_dict = sub_db_grid_data.data
        rows = []
        for key, value in data_dict.items():
            for sublist in value:
                rows.append({
                    'IDB': key,
                    'IROW': sublist[0],
                    'ICOL': sublist[1],
                    'RNB': sublist[2],
                    'DSH': sublist[3],
                    'DHC': sublist[4],
                    'DCOM': sublist[5],
                    'DZ': sublist[6],
                    'IMZ': sublist[7],
                })
        all_df = pd.DataFrame(rows)
        df_sorted = all_df.sort_values(by=['IDB'])
        output_file_path = os.path.join(project_dir, SUB_DB_GRID_FILE_NAME)
        df_sorted.to_csv(output_file_path, sep=' ', index=False)

    def write_bnd(self, project_dir):
        with open(os.path.join(project_dir, BND_FILE_NAME), "w") as file:
            file.write("    ".join(self.bnd_dict.keys()) + "\n")
            file.write("    ".join(str(value) for value in self.bnd_dict.values()) + "\n")

    def run(self, project_dir):
        current_file_path = os.path.abspath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        process = subprocess.Popen(
            ['python', os.path.join(current_dir_path, 'run_dll.py'), os.path.dirname(project_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        stdout_str = stdout.decode('utf-8')
        stdout_str = stdout_str.split('\n')
        flag_msg = stdout_str[0]
        stdout_lines = stdout_str[0:]
        clean_stdout = '\n'.join(stdout_lines)
        print(clean_stdout)
        if flag_msg[:3] == "DLL":
            return False, clean_stdout
        return True, clean_stdout
