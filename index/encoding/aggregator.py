import pandas as pd
from ..consts import VEGA_ENCODING_TIMEUNIT_DICT

def one_aggregation(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
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

    if aggregate_function == 'max':
        return data.groupby([group_by_column]).max()
    elif aggregate_function == 'min':
        return data.groupby([group_by_column]).min()
    elif aggregate_function == 'median':
        return data.groupby([group_by_column]).median()
    elif aggregate_function == 'count':
        return data.groupby([group_by_column]).count()
    elif aggregate_function == 'sum':
        return data.groupby([group_by_column]).sum()
    else:
        raise RuntimeError("Aggregation type not supported yet!")

def two_aggregation(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
    return None

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

    data[group_by_column] = pd.to_datetime(data[group_by_column])

    if aggregate_function == 'max':
        return pd.DataFrame(
            data.groupby(pd.Grouper(
                key=group_by_column, freq=VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value])
            ).max()[group_by_column]
        )
    elif aggregate_function == 'min':
        return pd.DataFrame(
            data.groupby(pd.Grouper(
                key=group_by_column, freq=VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value])
            ).min()[group_by_column]
        )
    elif aggregate_function == 'median':
        return pd.DataFrame(
            data.groupby(pd.Grouper(
                key=group_by_column, freq=VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value])
            ).median()[group_by_column]
        )
    elif aggregate_function == 'count':
        return pd.DataFrame(
            data.groupby(pd.Grouper(
                key=group_by_column, freq=VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value])
            ).count()[group_by_column]
        )
    elif aggregate_function == 'sum':
        return pd.DataFrame(
            data.groupby(pd.Grouper(
                key=group_by_column, freq=VEGA_ENCODING_TIMEUNIT_DICT[time_unit_value])
            ).sum()[group_by_column]
        )
    else:
        raise RuntimeError("Aggregation type not supported yet!")