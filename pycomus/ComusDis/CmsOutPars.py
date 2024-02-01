class ComusOutputPars:
    def __init__(self, model, GDWBDPRN: int = 1, LYRBDPRN: int = 1, CELLBDPRN: int = 1, CELLHHPRN: int = 1,
                 CELLDDPRN: int = 1,
                 CELLFLPRN: int = 1, LAKBDPRN: int = 1, SEGMBDPRN: int = 1, RECHBDPRN: int = 1, IBSPRN: int = 1,
                 SUBPRN: int = 1, NDBPRN: int = 1,
                 DBPRN: int = 1, REGBDPRN: int = 1):
        """
        Set COMUS Model Output Params Attributes.
        0: No output; 1: Output for each simulation time step within a stress period; 2: Output for each stress period.

        Parameters:
        ----------------------------
        model:
            COMUS Model Object
        GDWBDPRN:
            Groundwater system balance output control option.
        LYRBDPRN:
            Aquifer balance output control option.
        CELLBDPRN:
            Grid cell balance output control option.
        CELLHHPRN:
            Grid cell head output control option.
        CELLDDPRN:
            Grid cell drawdown output control option.
        CELLFLPRN:
            Inter-cell flow output control option.
        LAKBDPRN:
            Lake balance output control option.
        SEGMBDPRN:
            Stream channel balance output control option.
        RECHBDPRN:
            Stream segment balance output control option.
        IBSPRN:
            Interbed simulation results output control option.
        SUBPRN:
            Grid cell land subsidence simulation results output control option.
        NDBPRN:
            For no-delay interbed simulation results output control option.
        DBPRN:
            For delayed interbed simulation results output control option.
        REGBDPRN:
            Regional water balance output control option.
        """
        params = {
            'GDWBDPRN': GDWBDPRN,
            'LYRBDPRN': LYRBDPRN,
            'CELLBDPRN': CELLBDPRN,
            'CELLHHPRN': CELLHHPRN,
            'CELLDDPRN': CELLDDPRN,
            'CELLFLPRN': CELLFLPRN,
            'LAKBDPRN': LAKBDPRN,
            'SEGMBDPRN': SEGMBDPRN,
            'RECHBDPRN': RECHBDPRN,
            'IBSPRN': IBSPRN,
            'SUBPRN': SUBPRN,
            'NDBPRN': NDBPRN,
            'DBPRN': DBPRN,
            'REGBDPRN': REGBDPRN,
        }

        for param_name, param_value in params.items():
            if param_value not in {0, 1, 2}:
                raise ValueError(f'"{param_name}" parameter is invalid. It should be between 0 and 2. Please check!')

        self.m_GDWBDPRN = GDWBDPRN
        self.m_LYRBDPRN = LYRBDPRN
        self.m_CELLBDPRN = CELLBDPRN
        self.m_CELLHHPRN = CELLHHPRN
        self.m_CELLDDPRN = CELLDDPRN
        self.m_CELLFLPRN = CELLFLPRN
        self.m_LAKBDPRN = LAKBDPRN
        self.m_SEGMBDPRN = SEGMBDPRN
        self.m_RECHBDPRN = RECHBDPRN
        self.m_IBSPRN = IBSPRN
        self.m_SUBPRN = SUBPRN
        self.m_NDBPRN = NDBPRN
        self.m_DBPRN = DBPRN
        self.m_REGBDPRN = REGBDPRN
        model._addOutPars(self)
