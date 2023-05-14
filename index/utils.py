import pandas as pd
import json
import io

from django.http import HttpResponse

from .consts import AXIS, VEGA_ENCODING
from .encoding import aggregator as enc_agg
from .encoding import utils as enc_utils

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
        pd.DataFrame: A pandas DataFrame containing the data from the Vega JSON object.
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

def combine(data: pd.DataFrame, encoding: pd.DataFrame,
            data_enc_res: pd.DataFrame):
    """
    Combine two pandas DataFrames and write them to an Excel file.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be aggregated.
        encoding (pd.DataFrame): The DataFrame containing the encoding of the data.

    Returns:
        None.
    """
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as writer:
        data.to_excel(writer, sheet_name='Data', index=False)
        encoding.to_excel(writer, sheet_name='Encoding', index=False)
        if data_enc_res is not None:
            data_enc_res.to_excel(writer, sheet_name='Data Encoding-transformed')
    excel_buffer.seek(0)

    response = HttpResponse(excel_buffer.getvalue(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=extracted_table.xlsx'
    return response

def create_encoding_agg_table(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
    """
    Creates an aggregation table based on the given data and encoding.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be aggregated.
        encoding (pd.DataFrame): The DataFrame containing the encoding of the data.

    Returns:
        pd.DataFrame: A pandas DataFrame representing the aggregation table.
    """
    num_aggregate = enc_utils.check_for_aggregation(encoding)
    is_bin = enc_utils.check_is_bin(encoding)
    is_timeunit = enc_utils.check_is_time_unit(encoding)
    is_third_grouping = enc_utils.check_third_groping(encoding)

    if num_aggregate:
        if is_bin:
            return enc_agg.binning_aggregation(data=data, encoding=encoding, third_grouping=is_third_grouping)
        elif is_timeunit:
            return enc_agg.timeunit_aggregation(data=data, encoding=encoding, third_grouping=is_third_grouping)
        else:
            return enc_agg.basic_aggregation(data=data, encoding=encoding, third_grouping=is_third_grouping)
    else:
        return enc_agg.no_aggregation(data=data, encoding=encoding)
        
