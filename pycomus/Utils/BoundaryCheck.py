from typing import Union, Dict, List

import numpy as np

from pycomus.Utils import CONSTANTS


def CheckValueFormat(Value: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     ValueName: str, period: List, num_lyr: int, num_row: int, num_col: int) -> Dict:
    res = {}
    if isinstance(Value, (float, int)):
        for i in range(len(period)):
            res[i] = np.full((num_lyr, num_row, num_col), Value, dtype=float)
        return res
    elif isinstance(Value, Dict):
        # Check for duplicate keys
        if len(Value) != len(set(Value.keys())):
            raise ValueError("Duplicate Key found in the Value.")

        # Check dictionary length
        if len(Value) < 1 or len(Value) > len(period):
            raise ValueError(f"Invalid {ValueName} dict length. It should be between 1 and {len(period)}.")

        # Iterate through dictionary and validate values
        for key, value in Value.items():
            if not (0 <= key < len(period)):
                raise ValueError(
                    f"Invalid key {key} in {ValueName} dictionary. Keys should be in the range 0 to {len(period) - 1}.")
            if isinstance(value, (int, float)):
                res[key] = np.full((num_lyr, num_row, num_col), value, dtype=float)
            elif isinstance(value, np.ndarray):
                if value.shape == (num_lyr, num_row, num_col):
                    res[key] = value
                else:
                    raise ValueError(f"Invalid shape or values in the {ValueName} numpy array.")
            else:
                raise ValueError(
                    "Invalid value type in the dictionary. Values should be int, float, or numpy.ndarray.")
        return res
    else:
        raise ValueError(f"Invalid value type for '{ValueName}'. It should be int, float, or a dictionary.")


def CheckValueGtZero(Value: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     ValueName: str, period: List, num_lyr: int, num_row: int, num_col: int) -> Dict:
    res = {}
    if isinstance(Value, (float, int)):
        if Value < 0:
            raise ValueError(f"{ValueName} value must be greater than or equal to 0.")
        for i in range(len(period)):
            res[i] = np.full((num_lyr, num_row, num_col), Value, dtype=float)
        return res
    elif isinstance(Value, Dict):
        if len(Value) != len(set(Value.keys())):
            raise ValueError(f"Duplicate Key found in the {ValueName}.")

        if len(Value) < 1 or len(Value) > len(period):
            raise ValueError(f"Invalid {ValueName} dict length. It should be between 1 and {len(period)}.")

        for key, value in Value.items():
            if not (0 <= key < len(period)):
                raise ValueError(
                    f"Invalid key {key} in {ValueName} dictionary. Keys should be in the range 0 to {len(period) - 1}.")
            if isinstance(value, (int, float)):
                if value < 0:
                    raise ValueError(f"{ValueName} value must be greater than or equal to 0.")
                res[key] = np.full((num_lyr, num_row, num_col), value, dtype=float)
            elif isinstance(value, np.ndarray):
                if value.shape == (num_lyr, num_row, num_col):
                    if (value < 0).all():
                        raise ValueError(f"{ValueName} value must be greater than or equal to 0.")
                    res[key] = value
                else:
                    raise ValueError(f"Invalid shape or values in the {ValueName} numpy array.")
            else:
                raise ValueError(
                    "Invalid value type in the dictionary. Values should be int, float, or numpy.ndarray.")
        return res
    else:
        raise ValueError(f"Invalid value type for '{ValueName}'. It should be int, float, or a dictionary.")


def Check3DValueExistGrid(Value: Union[int, float, np.ndarray], ValueName: str, num_lyr: int, num_row: int,
                          num_col: int, OriginValueList: List) -> np.ndarray:
    if isinstance(Value, (int, float)):
        if Value not in OriginValueList:
            raise ValueError(f"{ValueName} : should exist in {OriginValueList}.")
        return np.full((num_lyr, num_row, num_col), Value, dtype=float)
    elif isinstance(Value, np.ndarray):
        if Value.shape == (num_lyr, num_row, num_col):
            if np.all(np.isin(Value, OriginValueList)):
                return Value
            else:
                raise ValueError(f"{ValueName} : should exist in {OriginValueList}.")
        else:
            raise ValueError(f"{ValueName} : Invalid shape or values in the {ValueName} numpy array.")
    else:
        raise ValueError(f"Invalid value type for '{ValueName}'. It should be int, float, or a np.ndarray.")


def check_3d_zero(Value: Union[int, float, np.ndarray], ValueName: str, num_lyr: int, num_row: int,
                  num_col: int) -> np.ndarray:
    if isinstance(Value, (int, float)):
        if Value < 0:
            raise ValueError(f"{ValueName} value must be greater than or equal to 0.")
        return np.full((num_lyr, num_row, num_col), Value, dtype=float)
    elif isinstance(Value, np.ndarray):
        if Value.shape == (num_lyr, num_row, num_col):
            if (Value < 0).all():
                raise ValueError(f"{ValueName} value must be greater than or equal to 0.")
            return Value
        else:
            raise ValueError(f"{ValueName} : Invalid shape or values in the {ValueName} numpy array.")
    else:
        raise ValueError(f"Invalid value type for '{ValueName}'. It should be int, float, or a np.ndarray.")


def check_3d_format(Value: Union[int, float, np.ndarray], ValueName: str, num_lyr: int, num_row: int,
                    num_col: int) -> np.ndarray:
    if isinstance(Value, (int, float)):
        return np.full((num_lyr, num_row, num_col), Value, dtype=float)
    elif isinstance(Value, np.ndarray):
        if Value.shape == (num_lyr, num_row, num_col):
            return Value
        else:
            raise ValueError(f"{ValueName} : Invalid shape or values in the {ValueName} numpy array.")
    else:
        raise ValueError(f"Invalid value type for '{ValueName}'. It should be int, float, or a np.ndarray.")


def check_bnd_queue(model):
    if CONSTANTS.CON_PKG_NAME not in model.package:
        raise ValueError("Before setting the boundary, `pycomus.ComusConPars` should be set first.")
    if CONSTANTS.OUT_PKG_NAME not in model.package:
        raise ValueError("Before setting the boundary, `pycomus.ComusOutputPars` should be set first.")
    if CONSTANTS.BCF_LYR_PKG_NAME not in model.package and CONSTANTS.LPF_LYR_PKG_NAME not in model.package:
        raise ValueError(
            "Before setting the boundary, `pycomus.ComusDisLpf` or `pycomus.ComusDisBcf` should be set first.")
    if CONSTANTS.PERIOD_PKG_NAME not in model.package:
        raise ValueError("Before setting the boundary, `pycomus.CmsTime` should be set first.")
    if CONSTANTS.GRID_PKG_NAME not in model.package:
        raise ValueError("Before setting the boundary, `pycomus.ComusGridPars` should be set first.")


def get_cms_pars(model):
    if CONSTANTS.BCF_LYR_PKG_NAME not in model.package and CONSTANTS.LPF_LYR_PKG_NAME not in model.package:
        raise ValueError("`pycomus.ComusDisLpf` or `pycomus.ComusDisBcf` should be set first.")
    if CONSTANTS.BCF_LYR_PKG_NAME in model.package:
        return model.package[CONSTANTS.BCF_LYR_PKG_NAME]
    else:
        return model.package[CONSTANTS.LPF_LYR_PKG_NAME]


def get_con_pars(model):
    if CONSTANTS.CON_PKG_NAME not in model.package:
        raise ValueError("`pycomus.ComusConPars` should be set first.")
    return model.package[CONSTANTS.CON_PKG_NAME]


def get_period(model):
    if CONSTANTS.PERIOD_PKG_NAME not in model.package:
        raise ValueError("`pycomus.CmsTime` should be set first.")
    return model.package[CONSTANTS.PERIOD_PKG_NAME]


def check_period(tar_period: int, period: int) -> bool:
    if tar_period < 0 or tar_period >= period:
        print(f"The period should be greater than or equal to 0 and less than {period}.")
        return False
    return True


def check_layer(tar_layer: int, layer: int) -> bool:
    if tar_layer < 0 or tar_layer >= layer:
        print(f"The layer should be greater than or equal to 0 and less than {layer}.")
        return False
    return True


def check_row(tar_row: int, row: int) -> bool:
    if tar_row < 0 or tar_row >= row:
        print(f"The row should be greater than or equal to 0 and less than {row}.")
        return False
    return True


def check_col(tar_col: int, col: int) -> bool:
    if tar_col < 0 or tar_col >= col:
        print(f"The col should be greater than or equal to 0 and less than {col}.")
        return False
    return True


def check_dict_zero(Value: np.ndarray, ValueName: str, num_lyr: int, num_row: int,
                    num_col: int):
    if Value.shape == (num_lyr, num_row, num_col):
        if (Value < 0).all():
            print(f"{ValueName} value must be greater than or equal to 0.")
            return False
    else:
        print(f"{ValueName} : Invalid shape in the {ValueName} numpy array(need {num_lyr},{num_row},{num_col}).")
        return False
    return True
