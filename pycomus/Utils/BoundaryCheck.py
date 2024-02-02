from typing import Union, Dict, List

import numpy as np


def CheckValueFormat(Value: Union[int, float, Dict[int, Union[int, float, np.ndarray]]],
                     ValueName: str, period: List, NumLyr: int, NumRow: int, NumCol: int) -> Dict:
    res = {}
    if isinstance(Value, (float, int)):
        for i in range(len(period)):
            res[i] = np.full((NumLyr, NumRow, NumCol), Value, dtype=float)
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
                res[key] = np.full((NumLyr, NumRow, NumCol), value, dtype=float)
            elif isinstance(value, np.ndarray):
                if value.shape == (NumLyr, NumRow, NumCol):
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
                ValueName: str, period: List, NumLyr: int, NumRow: int, NumCol: int) -> Dict:
    res = {}
    if isinstance(Value, (float, int)):
        if Value < 0:
            raise ValueError(f"{ValueName} value must be greater than or equal to 0.")
        for i in range(len(period)):
            res[i] = np.full((NumLyr, NumRow, NumCol), Value, dtype=float)
        return res
    elif isinstance(Value, Dict):
        # Check for duplicate keys
        if len(Value) != len(set(Value.keys())):
            raise ValueError(f"Duplicate Key found in the {ValueName}.")

        # Check dictionary length
        if len(Value) < 1 or len(Value) > len(period):
            raise ValueError(f"Invalid {ValueName} dict length. It should be between 1 and {len(period)}.")

        # Iterate through dictionary and validate values
        for key, value in Value.items():
            if not (0 <= key < len(period)):
                raise ValueError(
                    f"Invalid key {key} in {ValueName} dictionary. Keys should be in the range 0 to {len(period) - 1}.")
            if isinstance(value, (int, float)):
                if value < 0:
                    raise ValueError(f"{ValueName} value must be greater than or equal to 0.")
                res[key] = np.full((NumLyr, NumRow, NumCol), value, dtype=float)
            elif isinstance(value, np.ndarray):
                if value.shape == (NumLyr, NumRow, NumCol) and (value >= 0).all():
                    res[key] = value
                else:
                    raise ValueError(f"Invalid shape or values in the {ValueName} numpy array.")
            else:
                raise ValueError(
                    "Invalid value type in the dictionary. Values should be int, float, or numpy.ndarray.")
        return res
    else:
        raise ValueError(f"Invalid value type for '{ValueName}'. It should be int, float, or a dictionary.")