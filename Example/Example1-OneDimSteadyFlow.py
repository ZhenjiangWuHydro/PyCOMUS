import numpy as np

import pycomus

if __name__ == "__main__":
    # OneDimSteadyFlow：

    # Create Model
    model = pycomus.ComusModel(model_name="OneDimSteadyFlow")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, SimType=1, MaxIt=10000)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    NumLyr = 1
    NumRow = 1
    NumCol = 20
    column_spacing = [493.0318145, 453.5892693, 417.3021278, 383.9179575, 353.2045209, 324.9481593, 298.9523065,
                      275.036122, 253.0332322, 232.7905737, 214.1673278, 197.0339415, 181.2712262, 166.7695281,
                      153.4279659, 141.1537286, 129.8614303, 119.4725159, 109.9147146, 101.1215374]
    modelDis = pycomus.ComusDisBcf(model, NumLyr, NumRow, NumCol, RowSpace=50, ColSpace=column_spacing,
                                   LyrType=[1], LyrTrpy=[1.0], XCoord=-246.5159)

    # Grid Attribute
    ibound = np.full((NumLyr, NumRow, NumCol), 1, dtype=int)
    shead = np.full((NumLyr, NumRow, NumCol), 50, dtype=float)
    ibound[0, 0, 0] = -1
    ibound[0, 0, 19] = -1
    shead[0, 0, 0] = 10
    modelGridPar = pycomus.ComusGridPars(model, Top=50, Bot=0, Ibound=ibound, Kx=1, Shead=shead)

    # Set Period
    period = pycomus.ComusPeriod(model, (1, 1, 1))

    # Write Output
    model.writeOutPut()

    # Run Model
    model.runModel()
