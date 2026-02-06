#data processor
import pandas as pd
from functools import reduce

# -------------------------------
# 1️⃣ Reshape & Clean Data
# -------------------------------
def clean_data(df):
    """
    Reshape wide CSV (years as columns) to long format,
    remove missing GDP values, and convert types.
    """

    # Identify year columns (columns that are digits)
    year_cols = [col for col in df.columns if col.isdigit()]

    # Convert wide format to long format
    df_long = df.melt(
        id_vars=[
            'Country Name',
            'Country Code',
            'Indicator Name',
            'Indicator Code',
            'Continent'
        ],
        value_vars=year_cols,
        var_name='Year',
        value_name='GDP'
    )

    # Convert data types
    df_long['GDP'] = pd.to_numeric(df_long['GDP'], errors='coerce')
    df_long['Year'] = df_long['Year'].astype(int)

    # Remove rows with missing GDP
    df_long = df_long.dropna(subset=['GDP'])

    return df_long


# -------------------------------
# 2️⃣ Filter Data (Functional Style)
# -------------------------------
def filter_data(df, continent=None, year=None, country=None):
    """
    Filter data by continent, year, and/or country
    using functional programming (filter + lambda).
    """

    records = df.to_dict(orient='records')

    if continent is not None:
        records = list(filter(lambda x: x['Continent'] == continent, records))

    if year is not None:
        records = list(filter(lambda x: x['Year'] == year, records))

    if country is not None:
        records = list(filter(lambda x: x['Country Name'] == country, records))

    return pd.DataFrame(records)


# -------------------------------
# 3️⃣ Compute Statistics
# -------------------------------
def compute_statistics(df, operation='average'):
    """
    Compute GDP statistics using functional programming.
    Supported operations: 'average', 'sum'
    """

    gdp_values = list(map(float, df['GDP']))

    if not gdp_values:
        return 0

    if operation == 'average':
        return sum(gdp_values) / len(gdp_values)

    if operation == 'sum':
        return reduce(lambda a, b: a + b, gdp_values)

    raise ValueError("Operation must be 'average' or 'sum'")
