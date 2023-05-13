import pandas as pd

def check_is_bin(encoding: pd.DataFrame) -> bool:
    if 'bin' not in list(encoding['encoding_type']):
        return False
    else:
        bin_val = encoding[
            encoding['encoding_type'] == 'bin'
        ]['encoding_value'].values[0]
        if bin_val:
            return True
        else:
            return False
        
def check_is_time_unit(encoding: pd.DataFrame) -> bool:
    return encoding[encoding['encoding_type'] == 'timeUnit'].shape[0] > 0

def check_third_groping(encoding: pd.DataFrame) -> bool:
    return encoding[encoding['axis'] == 'color'].shape[0] > 0