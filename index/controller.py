import pandas as pd
import json

from .utils import global_utils
from .bar import utils as bar_utils

def base_router(text_input: str, check_box: bool, data: pd.DataFrame=None):
    """
    Check data routing based on the value of check_box.

    Args:
        text_input (str): Vega-lite JSON specification of the graph.
        check_box (bool): A boolean value indicating the data is available directly on the JSON or no.
        data (pd.DataFrame, Optional): A pandas DataFrame containing the uploaded CSV file.

    Returns:
        None
    """
    data_table = None
    if check_box:
        data_table = data
    else:
        data_table = global_utils.create_data_table(vega_json=text_input)
    
    encoding_table = global_utils.create_encoding_table(vega_json=text_input)
    transform_table = None
    
    enc_res_table, trans_res_table = transform_router(
        json.loads(text_input)['mark'], data=data_table,
        encoding=encoding_table, transform=transform_table)
    
    global_utils.combine(
        data=data_table, encoding=encoding_table)

def transform_router(
        mark_type: str, data: pd.DataFrame,
        encoding: pd.DataFrame=None, tranform: pd.DataFrame=None):
    """
    Route data transformation to a specific function based on the mark type.

    Args:
        mark_type (str): The type of mark to transform the data for ('bar', 'point', or 'line').
        data (pd.DataFrame): A pandas DataFrame containing the data.
        encoding (pd.DataFrame, optional): A pandas DataFrame containing the encoding information.
        transform (pd.DataFrame, optional): A pandas DataFrame containing transformation rules.

    Returns:
        A pandas DataFrame with the transformed data.
    """

    if mark_type == 'bar':
        enc_res_table = bar_utils.create_data_encoding_agg_table(
            data=data, encoding=encoding)
        
        raise RuntimeError("Mark type not supported yet!")
    elif mark_type == 'point':
        raise RuntimeError("Mark type not supported yet!")
    elif mark_type == 'line':
        raise RuntimeError("Mark type not supported yet!")
    else:
        raise RuntimeError("Mark type not supported yet!")