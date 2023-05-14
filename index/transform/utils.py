import pandas as pd

def check_for_transform(encoding: pd.DataFrame) -> bool:
    """
    Checks if the given encoding have transformation needed or not.

    Args:
        encoding (pd.DataFrame): A pandas DataFrame containing the Vega-Lite encoding specification.

    Returns:
        bool: True
    """
    return encoding[encoding['axis'] == 'tranform'].shape[0] > 0

def create_transform_table(vega_json: str) -> pd.DataFrame:
    transforms = []
    
    if 'transform' in vega_json:
        for transform in vega_json['transform']:
            if 'filter' in transform:
                parts = transform['filter'].split('==')
                transforms.append({
                    'tns': parts[0].strip().split('.')[1],
                    'exp': '==',
                    'val': parts[1].strip().strip("'")
                })
        
    return pd.DataFrame(transforms)