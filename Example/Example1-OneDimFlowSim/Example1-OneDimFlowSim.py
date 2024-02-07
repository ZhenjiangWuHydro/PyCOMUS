import numpy as np

import pycomus

if __name__ == "__main__":
    # OneDimSteadyFlow：

    # Create Model
    model = pycomus.ComusModel(model_name="OneDimSteadyFlow")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, sim_type=1, max_iter=10000)

    # # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)


    # Create Grid And Layer
    NumLyr = 1
    NumRow = 1
    NumCol = 20
    column_spacing = [493.0318145, 453.5892693, 417.3021278, 383.9179575, 353.2045209, 324.9481593, 298.9523065,
                      275.036122, 253.0332322, 232.7905737, 214.1673278, 197.0339415, 181.2712262, 166.7695281,
                      153.4279659, 141.1537286, 129.8614303, 119.4725159, 109.9147146, 101.1215374]
    modelDis = pycomus.ComusDisBcf(model, NumLyr, NumRow, NumCol, row_space=50, col_space=column_spacing,
                                   lyr_type=[1], lyr_trpy=[1.0], x_coord=-125)

    # Grid Attribute
    ibound = np.full((NumLyr, NumRow, NumCol), 1, dtype=int)
    shead = np.full((NumLyr, NumRow, NumCol), 50, dtype=float)
    ibound[0, 0, 0] = -1
    ibound[0, 0, 19] = -1
    shead[0, 0, 0] = 10
    modelGridPar = pycomus.ComusGridPars(model, top=50, bot=0, ibound=ibound, kx=1, shead=shead)

    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Write Output
    model.write_files()

    # Run Model
    model.run()
