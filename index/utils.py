import pandas as pd
import json

from .consts import AXIS, VEGA_ENCODING

def create_data_table(vega_json: str) -> pd.DataFrame:
    """
    Convert a Vega JSON data object into a pandas DataFrame.

    Args:
        vega_json (str): A string containing the Vega JSON data object.

    Returns:
        A pandas DataFrame containing the data from the Vega JSON object.
    """
    vega_json = json.loads(vega_json)
    vega_json_data = vega_json['data']['values']

    return pd.DataFrame(vega_json_data)

def create_encoding_table(vega_json: str) -> pd.DataFrame:
    """
    Convert a Vega JSON encoding object into a pandas DataFrame.

    Args:
        vega_json (str): A string containing the Vega JSON encoding object.

    Returns:
        A pandas DataFrame containing the encoding information from the Vega JSON object.
    """
    vega_json = json.loads(vega_json)

    axis_list = []
    encoding_type_list = []
    encoding_value_list = []

    for axs in AXIS:
        for enc in VEGA_ENCODING:
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

def combine(data: pd.DataFrame, encoding: pd.DataFrame):
    """
    Combine two pandas DataFrames and write them to an Excel file.

    Args:
        data (pd.DataFrame): A pandas DataFrame containing the data.
        encoding (pd.DataFrame): A pandas DataFrame containing the encoding information.

    Returns:
        None.
    """
    with pd.ExcelWriter('output.xlsx') as writer:
        data.to_excel(writer, sheet_name='Data', index=False)
        encoding.to_excel(writer, sheet_name='Encoding', index=False)