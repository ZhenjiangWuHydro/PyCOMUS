from django.urls import path

from .views import ComusModelView, ComusCtrlParsView, ComusOutParsView, ComusSpaceView, ComusLpfPropView, \
    ComusBcfPropView, ComusGridParsView, ComusPeriodView

urlpatterns = [
    path('createModel/', ComusModelView.as_view(), name='create_directory'),
    path('comusCtrlPars/', ComusCtrlParsView.as_view(), name='comus_ctrl_pars'),
    path('comusOutPars/', ComusOutParsView.as_view(), name='comus_output_pars'),
    path('comusSpace/', ComusSpaceView.as_view(), name='comus_space_pars'),
    path('comusLpfProperty/', ComusLpfPropView.as_view(), name='comus_lpf_property'),
    path('comusBcfProperty/',ComusBcfPropView.as_view(), name='comus_bcf_property'),
    path('comusGridPars/', ComusGridParsView.as_view(), name='comus_grid_pars'),
    path('comusPeriod/', ComusPeriodView.as_view(), name='comus_period'),
]
