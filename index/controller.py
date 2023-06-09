import pandas as pd

from . import utils as global_utils
from .transform import utils as tns_utils
from .encoding import utils as enc_utils

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
    data_table = data if check_box else global_utils.create_data_table(vega_json=text_input)
    encoding_table = enc_utils.create_encoding_table(vega_json=text_input)
    transform_table = pd.DataFrame()

    is_transform = tns_utils.check_for_transform(vega_json=text_input)
    if is_transform:
        transform_table = tns_utils.create_transform_table(vega_json=text_input)
        data_table = global_utils.create_transform_agg_table(data=data_table, transform=transform_table)
        transform_table['exp'] = transform_table['exp'].replace('==', 'equal(==)')

    enc_res_table = global_utils.create_encoding_agg_table(
            data=data_table, encoding=encoding_table)
    
    return global_utils.combine(
            data=data_table, encoding=encoding_table, 
            data_enc_res=enc_res_table, transform=transform_table)