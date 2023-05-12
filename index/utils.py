import pandas as pd
import json

from .consts import AXIS, VEGA_ENCODING
from .encoding import aggregator as enc_agg

def convert_datetime_to_str(val):
    """
    Converts a Pandas Timestamp object to a string representation in the format '%Y-%m-%d'.
    If the input value is not a Timestamp object, returns the input value unchanged.

    Args:
        val (any): The value to convert.

    Returns:
        str or any: The converted value as a string, or the input value unchanged.
    """
    if isinstance(val, pd.Timestamp):
        return val.strftime('%Y-%m-%d')
    else:
        return val

def update_data(json_data: str, uploaded_df: pd.DataFrame) -> str:
    """
    Update the JSON data with the uploaded dataframe and return the updated JSON string.

    Args:
        json_data (str): JSON string to be updated.
        uploaded_df (pd.DataFrame): Uploaded dataframe to be added to the JSON.

    Returns:
        str: Updated JSON string with the uploaded dataframe added to the 'values' field of the 'data' dictionary.
    """
    data_dict = json.loads(json_data)
    uploaded_df = uploaded_df.applymap(convert_datetime_to_str)

    data_dict["data"] = {"values": uploaded_df.to_dict('records')}
    updated_json = json.dumps(data_dict)
    return updated_json

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

def combine(data: pd.DataFrame, encoding: pd.DataFrame,
            data_enc_res: pd.DataFrame):
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
        if data_enc_res is not None:
            data_enc_res.to_excel(writer, sheet_name='Data Encoding-transformed')

def create_encoding_agg_table(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
    """
    Create an encoding aggregation table based on the given data and encoding information.

    Args:
        data: A pandas DataFrame containing the data to be aggregated.
        encoding: A pandas DataFrame containing the encoding information.

    Returns:
        A pandas DataFrame containing the encoding aggregation table.

    Raises:
        RuntimeError: If two encoding aggregations are specified in the encoding DataFrame, or if the
                        specified aggregation type is not supported.
    """
    num_aggregate = encoding[encoding['encoding_type'] == 'aggregate'].shape[0]
    num_timeunit = encoding[encoding['encoding_type'] == 'timeUnit'].shape[0]

    enc_res_table = None

    if num_aggregate == 1:
        if num_timeunit == 0:
            enc_res_table = enc_agg.basic_aggregation(data=data, encoding=encoding)
        else:
            enc_res_table = enc_agg.timeunit_aggregation(data=data, encoding=encoding)

    return enc_res_table