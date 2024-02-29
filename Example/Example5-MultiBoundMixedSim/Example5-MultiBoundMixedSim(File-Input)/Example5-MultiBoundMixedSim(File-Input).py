import pycomus

if __name__ == "__main__":
    # MultiBoundMixedSim(File-Input)：

    # Create Model
    model = pycomus.ComusModel(model_name="MultiBoundMixedSim(File-Input)")

    # Control Params
    modelControlParams = pycomus.ComusConPars.load(model, "./InputFiles/CtrlPar.in")

    # Output Params
    modelOutParams = pycomus.ComusOutputPars.load(model, "./InputFiles/OutOpt.in")

    # Create Grid And Layer
    modelDis = pycomus.ComusDisLpf.load(model, "./InputFiles/CtrlPar.in", "./InputFiles/GrdSpace.in",
                                        "./InputFiles/LpfLyr.in")

    # Grid Attribute
    modelGridPar = pycomus.ComusGridPars.load(model, "./InputFiles/LpfGrd.in")

    # Set Period
    modelPeriod = pycomus.ComusPeriod.load(model, "./InputFiles/PerAttr.in")

    # Set SHB
    shbPackage = pycomus.ComusShb.load(model, "./InputFiles/SHB.in")

    # Set WEL
    welPackage = pycomus.ComusWel.load(model, "./InputFiles/WEL.in")

    # Set EVT
    evtPackage = pycomus.ComusEvt.load(model, "./InputFiles/EVT.in")

    # Set RIV
    rivPackage = pycomus.ComusRiv.load(model, "./InputFiles/RIV.in")
    #
    # model.write_files()
    #
    # model.run()
