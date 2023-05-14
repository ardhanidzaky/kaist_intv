import pandas as pd
import json

from ..consts import AXIS, VEGA_ENCODING

def create_encoding_table(vega_json: str) -> pd.DataFrame:
    """
    Convert a Vega JSON encoding object into a pandas DataFrame.

    Args:
        vega_json (str): A string containing the Vega JSON encoding object.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the encoding information from the Vega JSON object.
    """
    vega_json = json.loads(vega_json)

    axis_list = []
    encoding_type_list = []
    encoding_value_list = []

    for axs in AXIS:
        for enc in VEGA_ENCODING:
            if axs in vega_json['encoding']:
                if enc in vega_json['encoding'][axs]:
                    axis_list.append(axs)
                    encoding_type_list.append(enc)
                    encoding_value_list.append(vega_json['encoding'][axs][enc])

    data = pd.DataFrame({
        'axis': axis_list,
        'encoding_type': encoding_type_list,
        'encoding_value': encoding_value_list
    })

    return data

def check_is_bin(encoding: pd.DataFrame) -> bool:
    """
    Checks if the given encoding specifies a binning operation or not.

    Args:
        encoding (pd.DataFrame): A pandas DataFrame containing the Vega-Lite encoding specification.

    Returns:
        bool: True if the encoding specifies a binning operation, False otherwise.
    """
    if 'bin' not in list(encoding['encoding_type']):
        return False
    else:
        bin_val = encoding[
            encoding['encoding_type'] == 'bin'
        ]['encoding_value'].values[0]
        if bin_val:
            return True
        else:
            return False
        
def check_is_time_unit(encoding: pd.DataFrame) -> bool:
    """
    Checks if the given encoding specifies a time unit operation or not.

    Args:
        encoding (pd.DataFrame): A pandas DataFrame containing the Vega-Lite encoding specification.

    Returns:
        bool: True if the encoding specifies a time unit operation, False otherwise.
    """
    return encoding[encoding['encoding_type'] == 'timeUnit'].shape[0] > 0

def check_third_groping(encoding: pd.DataFrame) -> bool:
    """
    Checks if the given encoding specifies a third grouping operation or not.

    Args:
        encoding (pd.DataFrame): A pandas DataFrame containing the Vega-Lite encoding specification.

    Returns:
        bool: True if the encoding specifies a third grouping operation, False otherwise.
    """
    return encoding[encoding['axis'] == 'color'].shape[0] > 0

def check_for_aggregation(encoding: pd.DataFrame) -> bool:
    """
    Checks if the given encoding specifies an aggregation operation or not.

    Args:
        encoding (pd.DataFrame): A pandas DataFrame containing the Vega-Lite encoding specification.

    Returns:
        bool: True if the encoding specifies an aggregation operation, False otherwise.
    """
    return encoding[encoding['encoding_type'] == 'aggregate'].shape[0] > 0