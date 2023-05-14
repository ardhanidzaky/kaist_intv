import pandas as pd
import json
import re

def check_for_transform(vega_json: str) -> bool:
    """
    Checks if the given encoding have transformation needed or not.

    Args:
        vega_json (str): A string containing the Vega JSON data object.

    Returns:
        bool: True
    """
    return 'transform' in json.loads(vega_json)

def create_transform_table(vega_json: str) -> pd.DataFrame:
    transforms = []
    vega_json = json.loads(vega_json)
    
    if 'transform' in vega_json:
        for transform in vega_json['transform']:
            if 'filter' in transform:
                match = re.match(r'datum\.(\w+)\s*([=!><]+)\s*(.*)', transform['filter'])
                if match:
                    col, exp, val = match.groups()
                    transforms.append({
                        'tns': col,
                        'exp': exp,
                        'val': val.strip("'")
                    })
                else:
                    raise RuntimeError("Invalid filter expression: {}".format(transform['filter']))
        
    return pd.DataFrame(transforms)