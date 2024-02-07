import pycomus

if __name__ == "__main__":
    # OneDimFlowSim(File-Input)：

    # Create Model
    model = pycomus.ComusModel(model_name="OneDimFlowSim(File-Input)")

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
    modelPeriod = pycomus.ComusPeriod.load(model,"./InputFiles/PerAttr.in")

    # Set RCH
    rechargePackage = pycomus.ComusRch.load(model, "./InputFiles/RCH.in")

    model.write_files()

    model.run()


