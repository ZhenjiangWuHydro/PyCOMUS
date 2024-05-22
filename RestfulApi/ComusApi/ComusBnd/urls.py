from django.urls import path

from .views import ComusSHBView, ComusGHBView, ComusRCHView, ComusWELView, ComusDRNView, ComusEVTView, ComusHFBView, \
    ComusRIVView, ComusIBSView, ComusSTRCtrlView, ComusSTRPeriodView, ComusSTRGridView, ComusSTRWaterUseView, \
    ComusSTRDrnView, ComusRESCtrlView, ComusRESPeriodView, ComusRESGridView, ComusLAKCtrlView, ComusLAKPeriodView, \
    ComusLAKGridView, ComusREGView, ComusSUBCtrlView, ComusSUBMzView, ComusSUBNdbLyrView, ComusSUBNdbGridView, \
    ComusSUBDbLyrView, ComusSUBDbGridView

urlpatterns = [
    path('comusSHB/', ComusSHBView.as_view(), name='comus_shb'),
    path('comusGHB/', ComusGHBView.as_view(), name='comus_ghb'),
    path('comusRCH/', ComusRCHView.as_view(), name='comus_rch'),
    path('comusWEL/', ComusWELView.as_view(), name='comus_wel'),
    path('comusDRN/', ComusDRNView.as_view(), name='comus_drn'),
    path('comusEVT/', ComusEVTView.as_view(), name='comus_evt'),
    path('comusHFB/', ComusHFBView.as_view(), name='comus_hfb'),
    path('comusRIV/', ComusRIVView.as_view(), name='comus_riv'),
    path('comusIBS/', ComusIBSView.as_view(), name='comus_ibs'),
    path('comusSTR/ctrlpars/', ComusSTRCtrlView.as_view(), name='comus_str_ctrl'),
    path('comusSTR/period/', ComusSTRPeriodView.as_view(), name='comus_str_period'),
    path('comusSTR/grid/', ComusSTRGridView.as_view(), name='comus_str_grid'),
    path('comusSTR/wateruse/', ComusSTRWaterUseView.as_view(), name='comus_str_water_use'),
    path('comusSTR/drn/', ComusSTRDrnView.as_view(), name='comus_str_drn'),
    path('comusRES/ctrlpars/', ComusRESCtrlView.as_view(), name='comus_res_ctrl'),
    path('comusRES/period/', ComusRESPeriodView.as_view(), name='comus_res_period'),
    path('comusRES/grid/', ComusRESGridView.as_view(), name='comus_res_grid'),
    path('comusLAK/ctrlpars/', ComusLAKCtrlView.as_view(), name='comus_lak_ctrl'),
    path('comusLAK/period/', ComusLAKPeriodView.as_view(), name='comus_lak_period'),
    path('comusLAK/grid/', ComusLAKGridView.as_view(), name='comus_lak_grid'),
    path('comusREG/', ComusREGView.as_view(), name='comus_reg'),
    path('comusSUB/ctrlpars/', ComusSUBCtrlView.as_view(), name='comus_sub_ctrl'),
    path('comusSUB/mz/', ComusSUBMzView.as_view(), name='comus_sub_mz'),
    path('comusSUB/ndb/lyr/', ComusSUBNdbLyrView.as_view(), name='comus_sub_ndb_lyr'),
    path('comusSUB/ndb/grid/', ComusSUBNdbGridView.as_view(), name='comus_sub_ndb_grid'),
    path('comusSUB/db/lyr/', ComusSUBDbLyrView.as_view(), name='comus_sub_db_lyr'),
    path('comusSUB/db/grid/', ComusSUBDbGridView.as_view(), name='comus_sub_db_grid'),
]
