from typing import Tuple

import numpy as np

import pycomus


def getResValue(filePath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    btm = np.zeros((NumLyr, NumRow, NumCol), dtype=float)
    bvk = np.zeros((NumLyr, NumRow, NumCol), dtype=float)
    btk = np.zeros((NumLyr, NumRow, NumCol), dtype=float)
    with open(filePath, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num == 1:
                continue
            line = line.strip()
            parts = line.split()
            int_parts = [int(part) for part in parts[:3]]
            float_part = [float(part) for part in parts[3:]]
            btm[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[0]
            bvk[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[1]
            btk[int_parts[0] - 1, int_parts[1] - 1, int_parts[2] - 1] = float_part[2]
    return (btm, bvk, btk)


if __name__ == "__main__":
    # ResGroundWaterSim：

    # Create Model
    model = pycomus.ComusModel(model_name="ResGroundWaterSim")

    # Control Params
    controlParams = pycomus.ComusConPars(model=model, ISolve=1, MaxIt=10000, RClose=0.01)

    # Output Params
    outParams = pycomus.ComusOutputPars(model, 2, 2, 2, 2, 2, 2)

    # Create Grid And Layer
    NumLyr = 1
    NumRow = 12
    NumCol = 12
    modelDis = pycomus.ComusDisBcf(model, NumLyr, NumRow, NumCol, RowSpace=100, ColSpace=100, LyrType=[0], LyrTrpy=[1],
                                   YCoord=1200)

    # Grid Attribute
    modelGridPar = pycomus.ComusGridPars(model, Top=21, Bot=0, Ibound=1, Transm=10000, SC1=0.2, Kx=0, Shead=0)

    # Set Period
    period = pycomus.ComusPeriod(model, [(2, 2, 1) for _ in range(2)] + [(5, 5, 1)])

    # Set GHB
    cond_data = np.zeros((NumLyr, NumRow, NumCol))
    for i in range(12):
        cond_data[0, i, 0] = 1000
        cond_data[0, i, 11] = 1000
    shead_ehead_data = np.zeros((NumLyr, NumRow, NumCol))
    shbPackage = pycomus.Package.ComusGhb(model, Cond={0: cond_data}, Shead={0: shead_ehead_data},
                                          Ehead={0: shead_ehead_data})

    # Set RES
    resPackage = pycomus.ComusRes(model, res_num=1)
    resPackage.setControlParams(
        {0: (2.5, 3, 10, 20)}
    )
    resPackage.setPeriodData(
        {0:  # res id
             {0:  # period id
                  (4, 12, 0, 0),
              1:
                  (12, 14, 0, 0),
              2:
                  (14, 4, 0, 0)
              }
         }
    )
    btm, bvk, btk = getResValue("./GridValue.txt")
    resPackage.setGridData(Btm={0: btm}, Bvk={0: bvk}, Btk={0: btk})

    # Write Output
    model.writeOutPut()

    # Run Model
    model.runModel()
