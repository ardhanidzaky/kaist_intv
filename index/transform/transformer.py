import pandas as pd

def transform_data(data: pd.DataFrame, col: str, exp: str, val: str) -> pd.DataFrame:
    if exp == '==' or exp == '===':
        return data[data[col] == val]
    elif exp == '>':
        return data[data[col] > int(val)]
    elif exp == '<':
        return data[data[col] < int(val)]
    elif exp == '>=':
        return data[data[col] >= int(val)]
    elif exp == '<=':
        return data[data[col] <= int(val)]
    else:
        raise RuntimeWarning('Expression not supported yet!')