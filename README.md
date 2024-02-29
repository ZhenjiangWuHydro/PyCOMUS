# Introduction

The COMUS model is developed by the Institute of Water Resources and Hydropower Research (IWHR) of the China Institute of Water Resources and Hydropower Research (IWHR). This model is applicable to various simulation calculations related to the movement of groundwater, such as assessing groundwater source supply, delineating groundwater source protection areas, studying the impact of mine water inflow, investigating the ecological water balance in arid regions, optimizing regional groundwater exploitation layouts, evaluating Managed Aquifer Recharge (MAR) effectiveness, predicting groundwater over-exploitation and remediation, forecasting seawater intrusion (with the density-dependent module), predicting groundwater pollution (with the solute transport model), and more. It serves as the fundamental support for achieving the "Four Predictions" of groundwater resources management.

PyCOMUS is a Python interface built upon the COMUS model, capable of performing all the functions that the COMUS model offers.



# Documentation

```python
# ---------------
# Todo
# --------------- 
```



# Installation

PyCOMUS requires **Python** 3.6+ with:

```python
numpy >= 1.12.0
```

To install type:

```bash
pip install PyCOMUS  # Todo
```



# Getting Started

```python
import numpy as np

import pycomus

if __name__ == "__main__":
    # OneDimSteadyFlow：

    # Create Model
    model = pycomus.ComusModel(model_name="OneDimSteadyFlow")

    # Control Params
    control_pars = pycomus.ComusConPars(model=model, sim_type=1, max_iter=10000)

    # # Output Params
    out_pars = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    num_lyr = 1
    num_row = 1
    num_col = 20
    column_spacing = [493.0318145, 453.5892693, 417.3021278, 383.9179575, 353.2045209, 324.9481593, 298.9523065,
                      275.036122, 253.0332322, 232.7905737, 214.1673278, 197.0339415, 181.2712262, 166.7695281,
                      153.4279659, 141.1537286, 129.8614303, 119.4725159, 109.9147146, 101.1215374]
    model_dis = pycomus.ComusDisBcf(model, num_lyr=num_lyr, num_row=num_row, num_col=num_col, row_space=50,
                                    col_space=column_spacing, lyr_type=[1], lyr_trpy=[1.0], x_coord=-125)

    # Grid Attribute
    ibound = np.full((num_lyr, num_row, num_col), 1, dtype=int)
    shead = np.full((num_lyr, num_row, num_col), 50, dtype=float)
    ibound[0, 0, 0] = -1
    ibound[0, 0, 19] = -1
    shead[0, 0, 0] = 10
    grid_pars = pycomus.ComusGridPars(model, top=50, bot=0, ibound=ibound, kx=1, shead=shead)

    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Write Output
    model.write_files()

    # Run Model
    model.run()
```
