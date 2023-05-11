import pandas as pd

from .utils import *

def router(text_input: str, check_box: bool, data: pd.DataFrame=None):
    """
    Route data to a data_on_csv() or data_on_json() function based on the value of check_box.

    Args:
        text_input (str): Vega-lite JSON specification of the graph.
        check_box (bool): A boolean value indicating the data is available directly on the JSON or no.
        data (pd.DataFrame, Optional): A pandas DataFrame containing the uploaded CSV file.

    Returns:
        None
    """

    if check_box:
        data_on_csv(text_input=text_input, data=data)
    else:
        data_on_json(text_input=text_input)

def data_on_csv(text_input: str, data: pd.DataFrame):
    """
    Vega-lite specification pipeline for "data": {"url": "xxx.csv"}.

    Args:
        text_input (str): A string containing the Vega JSON specification.
        data (pd.DataFrame): A pandas DataFrame containing the data.

    Returns:
        None.
    """
    _encoding_table = create_encoding_table(vega_json=text_input)
    combine(data=data, encoding=_encoding_table)

def data_on_json(text_input: str):
    """
    Vega-lite specification pipeline for "data": {"value": xxx}.

    Args:
        text_input (str): A string containing the Vega JSON specification.

    Returns:
        None.
    """
    _data_table = create_data_table(vega_json=text_input)
    _encoding_table = create_encoding_table(vega_json=text_input)
    combine(data=_data_table, encoding=_encoding_table)