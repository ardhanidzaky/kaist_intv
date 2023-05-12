import pandas as pd
from ..consts import VEGA_ENCODING_TIMEUNIT_DICT

def basic_aggregation(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic aggregation on a given DataFrame based on the encoding.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the data to be aggregated.
    encoding (pd.DataFrame): The DataFrame containing the encoding of the data.

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

    try:
        return data.groupby([group_by_column])[aggregate_value].agg([aggregate_function])
    except:
        raise RuntimeError("Aggregation type not supported yet!")

def timeunit_aggregation(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
    """
    Computes an aggregation on a DataFrame by grouping it by a time unit.

    Args:
        data (pd.DataFrame): The input DataFrame to aggregate.
        encoding (pd.DataFrame): The encoding DataFrame that specifies how to perform the aggregation.

    Returns:
        pd.DataFrame: A new DataFrame with the aggregation result.

    Raises:
        RuntimeError: If the specified aggregation type is not supported.

    The function retrieves the encoding information from the provided encoding DataFrame to determine how to perform the aggregation.
    It extracts the group by column, time unit, aggregation function, and aggregation value from the encoding DataFrame.
    It then converts the group by column to datetime and aggregates the data by grouping it by the specified time unit.
    The aggregation function is applied to the specified aggregation value column.
    The function returns a new DataFrame with the aggregation result.
    If the specified aggregation type is not supported, a RuntimeError is raised.

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

    data[group_by_column] = pd.to_datetime(data[group_by_column])
    try:
        tu_aggregated = data.groupby(
            data[group_by_column].dt.to_period(VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value])
        )[aggregate_value].agg([aggregate_function])
        return tu_aggregated
    except:
        raise RuntimeError("Aggregation type not supported yet!")