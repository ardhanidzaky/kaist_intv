import pandas as pd
import numpy as np

from ..consts import VEGA_ENCODING_TIMEUNIT_DICT

def basic_aggregation(data: pd.DataFrame, encoding: pd.DataFrame, third_grouping: bool) -> pd.DataFrame:
    """
    Perform basic aggregation on a given DataFrame based on the encoding.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be aggregated.
        encoding (pd.DataFrame): The DataFrame containing the encoding of the data.
        third_grouping (bool): Whether there's a third grouping (stacking, etc).

    Returns:
        pd.DataFrame: The aggregated DataFrame.

    Raises:
        RuntimeError: If the aggregation type is not supported.
    """
    aggregate_axis = encoding[encoding['encoding_type'] == 'aggregate']['axis'].values[0]
    group_by_axis = 'x' if aggregate_axis == 'y' else 'y'
    group_by_column = encoding[
        (encoding['encoding_type'] == 'field') &
        (encoding['axis'] == group_by_axis)
    ]['encoding_value'].values[0]
    aggregate_function = encoding[
        (encoding['encoding_type'] == 'aggregate') &
        (encoding['axis'] == aggregate_axis)
    ]['encoding_value'].values[0]
    aggregate_value = encoding[
        (encoding['encoding_type'] == 'field') &
        (encoding['axis'] == aggregate_axis)
    ]['encoding_value'].values[0]

    aggregate_function = 'mean' if 'average' else aggregate_function
    try:
        if third_grouping:
            third_group_column = encoding[
                (encoding['encoding_type'] == 'field') &
                (encoding['axis'] == 'color')
            ]['encoding_value'].values[0]
            table = data.groupby([group_by_column, third_group_column])[aggregate_value].agg([aggregate_function])
            table = table.reset_index()
            return table.pivot_table(index=group_by_column, columns=third_group_column, values=aggregate_function)
        else:
            return data.groupby([group_by_column])[aggregate_value].agg([aggregate_function])
    except:
        raise RuntimeError("Aggregation type not supported yet!")

def timeunit_aggregation(data: pd.DataFrame, encoding: pd.DataFrame, third_grouping: bool) -> pd.DataFrame:
    """
    Computes an aggregation on a DataFrame by grouping it by a time unit.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be aggregated.
        encoding (pd.DataFrame): The DataFrame containing the encoding of the data.
        third_grouping (bool): Whether there's a third grouping (stacking, etc).

    Returns:
        pd.DataFrame: The aggregated DataFrame.

    Raises:
        RuntimeError: If the aggregation type is not supported.
    """
    aggregate_axis = encoding[encoding['encoding_type'] == 'aggregate']['axis'].values[0]
    group_by_axis = 'x' if aggregate_axis == 'y' else 'y'
    group_by_column = encoding[
        (encoding['encoding_type'] == 'field') &
        (encoding['axis'] == group_by_axis)
    ]['encoding_value'].values[0]
    time_unit_value = encoding[
        (encoding['encoding_type'] == 'timeUnit') &
        (encoding['axis'] == group_by_axis)
    ]['encoding_value'].values[0]
    aggregate_function = encoding[
        (encoding['encoding_type'] == 'aggregate') &
        (encoding['axis'] == aggregate_axis)
    ]['encoding_value'].values[0]
    aggregate_value = encoding[
        (encoding['encoding_type'] == 'field') &
        (encoding['axis'] == aggregate_axis)
    ]['encoding_value'].values[0]

    aggregate_function = 'mean' if 'average' else aggregate_function
    data[group_by_column] = pd.to_datetime(data[group_by_column])
    try:
        if third_grouping:
            third_group_column = encoding[
                (encoding['encoding_type'] == 'field') &
                (encoding['axis'] == 'color')
            ]['encoding_value'].values[0]
            table = data.groupby(
                [data[group_by_column].dt.to_period(VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value]),
                third_group_column]
            )[aggregate_value].agg([aggregate_function])
            return table.pivot_table(
                index=data[group_by_column].dt.to_period(VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value]), 
                columns=third_group_column, 
                values=aggregate_function)
        else:
            tu_aggregated = data.groupby(
                data[group_by_column].dt.to_period(VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value])
            )[aggregate_value].agg([aggregate_function])
            return tu_aggregated
    except:
        raise RuntimeError("Aggregation type not supported yet!")
    
def binning_aggregation(data: pd.DataFrame, encoding: pd.DataFrame, third_grouping: bool) -> pd.DataFrame:
    """
    Perform binning aggregation on data.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be aggregated.
        encoding (pd.DataFrame): The DataFrame containing the encoding of the data.
        third_grouping (bool): Whether there's a third grouping (stacking, etc).

    Returns:
        pd.DataFrame: The aggregated DataFrame.

    Raises:
        RuntimeError: If the aggregation type is not supported.
    """
    temp_data = data.copy()
    aggregate_axis = encoding[encoding['encoding_type'] == 'aggregate']['axis'].values[0]
    bin_by_axis = 'x' if aggregate_axis == 'y' else 'y'
    bin_by_column = encoding[
        (encoding['encoding_type'] == 'field') &
        (encoding['axis'] == bin_by_axis)
    ]['encoding_value'].values[0]

    # Binning logic will always assume an equal division by 10 bin.
    max_val_rounded = int(np.ceil(temp_data[bin_by_column].max() / 5) * 5)
    temp_data['bin'] = pd.cut(
        temp_data[bin_by_column], 
        bins=np.linspace(0, max_val_rounded, num=11)
    )

    try:
        if third_grouping:
            third_group_column = encoding[
                (encoding['encoding_type'] == 'field') &
                (encoding['axis'] == 'color')
            ]['encoding_value'].values[0]
            table = temp_data.groupby(['bin', third_group_column])[third_group_column].agg(['count'])
            return table.pivot_table(index='bin', columns=third_group_column, values='count')
        else:
            return temp_data['bin'].value_counts(sort=False)
    except:
        raise RuntimeError("Aggregation type not supported yet!")
    
def no_aggregation(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the subset of the input data containing the fields specified in the encoding DataFrame.
    If third_grouping is True, the column specified as color in the encoding DataFrame is also returned.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data to be aggregated.
        encoding (pd.DataFrame): The DataFrame containing the encoding of the data.

    Returns:
        pd.DataFrame: The subset of the input data containing the fields specified in the encoding DataFrame.
    """
    col_lst = list(
        encoding[encoding['encoding_type'] == 'field']['encoding_value']
    )

    return data[col_lst]