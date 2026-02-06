import pandas as pd
import os

def load_data(file_path):
    """
    Load GDP data from a CSV file and return a pandas DataFrame.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at: {file_path}")

    df = pd.read_csv(file_path)
    return df
