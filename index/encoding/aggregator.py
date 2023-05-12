import pandas as pd
from ..consts import VEGA_ENCODING_TIMEUNIT_DICT

def basic_aggregation(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
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