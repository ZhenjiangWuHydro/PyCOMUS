# --------------------------------------------------------------
# CSUB.py
# Version: 1.0.0
# Author: Zhenjiang Wu
# Description: Set COMUS Model With SUB Package.
# --------------------------------------------------------------
import pycomus


class ComusSub:
    def __init__(self, model: pycomus.ComusModel, num_ndb: int, num_db: int, num_mz: int, nn: int = 20,
                 acc: float = 0.5, it_min: int = 5, dsh_opt: int = 2):
        """
        Initialize the COMUS Model with the Subsidence(SUB) package.

        Parameters:
        ----------------------------
        model:
            The COMUS model to which the SUB package will be applied.
        num_ndb:
            Number of delayed interbedded body groups without delay.
        num_db:
            Number of delayed interbedded bodies.
        num_mz:
            Only valid when num_ndb > 0, indicating the number of media zones.
        nn:
            Number of discrete points on the half thickness of equivalent interbedded bodies.
        acc:
            Representing the simulation acceleration parameter of delayed interbedded bodies.
        it_min:
            The effective value should be greater than or equal to 2, typically set to 5.
        dsh_opt:
            Representing the option for determining the initial head values of delayed interbedded bodies.

        Returns:
        --------
        instance: pycomus.ComusSub
           COMUS Subsidence(SUB) Params Object.

        Example:
        --------
        >>> import pycomus
        >>> model1 = pycomus.ComusModel(model_name="test")
        >>> subPackage = pycomus.ComusSub(model, 2, 2, 10)
        """

        self._num_lyr = model.CmsDis.num_lyr
        self._num_row = model.CmsDis.num_row
        self._num_col = model.CmsDis.num_col
        self._period = model.CmsTime.period
        if num_ndb < 0 or num_db < 0:
            raise ValueError("The parameters num_ndb and num_db must be greater than or equal to 0. Please check!")
        if num_ndb + num_db == 0:
            raise ValueError(
                "The parameters num_ndb and num_db must have at least one value not equal to 0. Please check!")
        if num_db > 0:
            if num_mz <= 0:
                raise ValueError(
                    "When simulating delayed confining units, the num_mz parameter cannot be set to 0. Please check!")
            if nn <= 5 or nn >= 100:
                raise ValueError("The valid range for the nn parameter is 5 to 100. Please check!")
            if acc < 0 or acc > 0.6:
                raise ValueError("The valid range for the acc parameter is 0.0 to 0.6. Please check!")
            if dsh_opt not in (1, 2):
                raise ValueError("The dsh_opt parameter must be either 1 or 2. Please check!")
        self.num_ndb = num_ndb
        self.num_db = num_db
        self.num_mz = num_mz
        self.nn = nn
        self.acc = acc
        self.it_min = it_min
        self.dsh_opt = dsh_opt
        model.package["SUB"] = self
