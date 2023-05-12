import pandas as pd

from . import utils as global_utils

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
    
    enc_res_table = global_utils.create_encoding_agg_table(
            data=data_table, encoding=encoding_table)
    
    global_utils.combine(
        data=data_table, encoding=encoding_table, data_enc_res=enc_res_table)