import pandas as pd

def create_data_encoding_agg_table(data: pd.DataFrame, encoding: pd.DataFrame) -> pd.DataFrame:
    """
    Create a new DataFrame that aggregates data based on the Vega encoding specification.

    Args:
        data (pd.DataFrame): A pandas DataFrame containing the data.
        encoding (pd.DataFrame): A pandas DataFrame containing the encoding information.

    Returns:
        A pandas DataFrame with aggregated data.
    """
    axis_aggregated = encoding[encoding['encoding_type'] == 'aggregate']['axis'].values[0]
    axis_grouped = 'x' if axis_aggregated == 'y' else 'y'
    grouped_by = encoding[
        (encoding['encoding_type'] == 'field') &
        (encoding['axis'] == axis_grouped)
    ]['encoding_value'].values[0]
    aggregated_by = encoding[
        (encoding['encoding_type'] == 'aggregate') &
        (encoding['axis'] == axis_aggregated)
    ]['encoding_value'].values[0]

    if aggregated_by == 'max':
        data.groupby([grouped_by]).max().to_excel('max.xlsx')
    elif aggregated_by == 'min':
        data.groupby([grouped_by]).min().to_excel('max.xlsx')
    elif aggregated_by == 'median':
        data.groupby([grouped_by]).median().to_excel('max.xlsx')
    elif aggregated_by == 'count':
        data.groupby([grouped_by]).count().to_excel('max.xlsx')
    elif aggregated_by == 'sum':
        data.groupby([grouped_by]).sum().to_excel('max.xlsx')
    else:
        data
