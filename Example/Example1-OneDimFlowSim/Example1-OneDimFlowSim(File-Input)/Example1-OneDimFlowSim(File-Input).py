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
    modelDis = pycomus.ComusDisBcf.load(model, "./InputFiles/CtrlPar.in", "./InputFiles/GrdSpace.in",
                                        "./InputFiles/BcfLyr.in")


    # Grid Attribute
    modelGridPar = pycomus.ComusGridPars.load(model, "./InputFiles/BcfGrd.in")

    # Set Period
    modelPeriod = pycomus.ComusPeriod.load(model,"./InputFiles/PerAttr.in")

    model.write_files()

    model.run()


