# Introduction

PyCOMUS is a Python interface built upon the COMUS model, capable of performing all the functions that the COMUS model offers.



# Documentation

```python
# ---------------
# Todo
# --------------- 
```



# Installation

PyCOMUS requires **Python 3.8+** with:

```python
numpy >=1.15.0,<2.0.0
matplotlib >=1.4.0
```

To install type:

```bash
pip install PyCOMUS
```



# Getting Started

```python
import numpy as np

import pycomus

if __name__ == "__main__":
    # MultiBoundMixedSim：

    # Create Model
    model = pycomus.ComusModel(model_name="MultiBoundMixedSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, intblkm=2, max_iter=10000, r_close=0.0001)

    # Output Params
    outParams = pycomus.ComusOutputPars(model)

    # Create Grid And Layer
    NumLyr = 2
    NumRow = 20
    NumCol = 20
    modelDis = pycomus.ComusDisLpf(model, num_lyr=NumLyr, num_row=NumRow, num_col=NumCol, row_space=50, col_space=50,
                                   lyr_type=[1 for _ in range(NumLyr)], lyr_cbd=[1, 0], y_coord=1000)

    # Grid Attribute
    bot = np.zeros((NumLyr, NumRow, NumCol))
    bot[0, :, :] = 10
    vkcb = np.zeros((NumLyr, NumRow, NumCol))
    vkcb[0, :, :] = 0.001
    tkcb = np.zeros((NumLyr, NumRow, NumCol))
    tkcb[0, :, :] = 0.1
    modelGridPar = pycomus.ComusGridPars(model, top=20, bot=bot, ibound=1, kx=10, ky=10, kz=5, vkcb=vkcb, tkcb=tkcb,
                                         shead=16, sc1=0.0001, sc2=0.08)

    # Set Period
    period = pycomus.ComusPeriod(model, [(10, 10, 1) for _ in range(2)])

    # Set SHB
    shead_period1 = np.zeros((NumLyr, NumRow, NumCol))
    shead_period1[0, :, 19] = 16
    shead_period2 = np.zeros((NumLyr, NumRow, NumCol))
    shead_period2[0, :, 19] = 17

    ehead_period1 = np.zeros((NumLyr, NumRow, NumCol))
    ehead_period1[0, :, 19] = 17
    ehead_period2 = np.zeros((NumLyr, NumRow, NumCol))
    ehead_period2[0, :, 19] = 18
    shbPackage = pycomus.ComusShb(model, shead={0: shead_period1, 1: shead_period2},
                                  ehead={0: ehead_period1, 1: ehead_period2})

    # Set WEL
    wellr_period1 = np.zeros((NumLyr, NumRow, NumCol))
    wellr_period1[1, 3, 12] = -500
    wellr_period1[1, 16, 12] = -500
    wellr_period2 = np.zeros((NumLyr, NumRow, NumCol))
    wellr_period2[1, 3, 12] = -300
    wellr_period2[1, 16, 12] = -300
    satthr_period1 = np.zeros((NumLyr, NumRow, NumCol))
    satthr_period1[1, 3, 12] = 0.1
    satthr_period1[1, 16, 12] = 0.1
    welPackage = pycomus.ComusWel(model, wellr={0: wellr_period1, 1: wellr_period2},
                                  satthr={0: satthr_period1, 1: satthr_period1})

    # Set EVT
    etSurf = np.zeros((NumLyr, NumRow, NumCol))
    etSurf[0, :, :] = 20
    etRate = np.zeros((NumLyr, NumRow, NumCol))
    etRate[0, :, :] = 0.002
    etMxd = np.zeros((NumLyr, NumRow, NumCol))
    etMxd[0, :, :] = 5
    etExp = np.zeros((NumLyr, NumRow, NumCol))
    etExp[0, :, :] = 2
    evtPackage = pycomus.ComusEvt(model, et_surf={0: etSurf, 1: etSurf}, et_rate={0: etRate, 1: etRate},
                                  et_mxd={0: etMxd, 1: etMxd}, et_exp={0: etExp, 1: etExp}, num_seg=2)

    # Set RIV
    cond = np.zeros((NumLyr, NumRow, NumCol))
    cond[0, :, 0] = 100
    rivBtm = np.zeros((NumLyr, NumRow, NumCol))
    rivBtm[0, :, 0] = 15
    shead_ehead_period1 = np.zeros((NumLyr, NumRow, NumCol))
    shead_ehead_period1[0, :, 0] = 16
    shead_ehead_period2 = np.zeros((NumLyr, NumRow, NumCol))
    shead_ehead_period2[0, :, 0] = 18
    rivPackage = pycomus.ComusRiv(model, cond={0: cond, 1: cond},
                                  shead={0: shead_ehead_period1, 1: shead_ehead_period2},
                                  ehead={0: shead_ehead_period1, 1: shead_ehead_period2},
                                  riv_btm={0: rivBtm, 1: rivBtm})

    # Write Output
    model.write_files()

    # Run Model
    model.run()

    # Data Extract
    data = pycomus.ComusData(model)
    head = data.read_cell_head(tar_period=0, tar_iter=0, tar_layer=0)
    map = pycomus.ComusPlot(model)
    map.plot_grid()
    map.plot_contour(head, contourf_kwargs={'cmap': 'viridis', 'alpha': 0.6},
                     colorbar_kwargs={'orientation': 'vertical'},
                     contour_kwargs={'colors': 'black', 'linestyles': 'dashed','levels':10},
                     clabel_kwargs={'inline': True, 'fontsize': 8})
    map.show_plot()

```

![](./image/myplot.png)
