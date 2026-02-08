# data_processor.py

import pandas as pd
from functools import reduce

# -------------------------------
# 1️⃣ Normalize & Clean Data (support wide and long CSV formats)
# -------------------------------
def clean_data(df):
    """
    Accepts either wide-format CSV (years as columns) or long-format CSV
    with columns like ['Country Name','Region'|'Continent','Year','Value'].
    Returns a cleaned long-format DataFrame with columns:
      Country Name, Country Code (if present), Continent, Year (int), GDP (float)
    """
    cols = [c.lower() for c in df.columns]

    # Detect long format: has 'year' and 'value' or 'gdp' columns
    if 'year' in cols and ('value' in cols or 'gdp' in cols):
        # Normalize column names
        rename_map = {}
        if 'value' in cols:
            rename_map[[c for c in df.columns if c.lower() == 'value'][0]] = 'GDP'
        elif 'gdp' in cols:
            rename_map[[c for c in df.columns if c.lower() == 'gdp'][0]] = 'GDP'

        if 'region' in cols and 'continent' not in cols:
            rename_map[[c for c in df.columns if c.lower() == 'region'][0]] = 'Continent'

        if 'country name' not in [c for c in df.columns]:
            raise KeyError("Expected 'Country Name' column in long-format CSV")

        df = df.rename(columns=rename_map)
        # Ensure columns exist
        df_out = df.rename(columns={
            [c for c in df.columns if c.lower() == 'country name'][0]: 'Country Name'
        })

        # Ensure Year int and GDP float
        df_out['Year'] = df_out[[c for c in df_out.columns if c.lower() == 'year'][0]].astype(int)
        df_out['GDP'] = pd.to_numeric(df_out['GDP'], errors='coerce')
        if 'Continent' not in df_out.columns:
            df_out['Continent'] = None

        df_out = df_out[['Country Name'] + ([c for c in df_out.columns if c == 'Country Code'] if 'Country Code' in df_out.columns else []) + ['Continent', 'Year', 'GDP']]
        df_out = df_out.dropna(subset=['GDP'])
        return df_out

    # Otherwise assume wide format where years are column names
    year_cols = [col for col in df.columns if col.isdigit()]
    if not year_cols:
        # Try columns that look like years (e.g., '1960', '1970') via regex fallback
        year_cols = [col for col in df.columns if col.strip().isdigit()]

    id_vars = [c for c in ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', 'Continent'] if c in df.columns]
    df_long = df.melt(id_vars=id_vars, value_vars=year_cols, var_name='Year', value_name='GDP')
    df_long['GDP'] = pd.to_numeric(df_long['GDP'], errors='coerce')
    df_long['Year'] = df_long['Year'].astype(int)
    df_long = df_long.dropna(subset=['GDP'])
    # Ensure Continent column exists
    if 'Continent' not in df_long.columns:
        df_long['Continent'] = None

    # Keep only relevant columns and normalize order
    cols_keep = [c for c in ['Country Name', 'Country Code', 'Continent', 'Year', 'GDP'] if c in df_long.columns]
    return df_long[cols_keep]

# -------------------------------
# 2️⃣ Filtering using functional programming
# -------------------------------
def filter_data(df, continent=None, year=None, country=None):
    """
    Filters DataFrame by continent, year, or country using functional style.
    """
    # Convert DataFrame to list of dicts
    records = df.to_dict(orient='records')
    
    if continent:
        records = list(filter(lambda x: x['Continent'] == continent, records))
    if year:
        records = list(filter(lambda x: x['Year'] == year, records))
    if country:
        records = list(filter(lambda x: x['Country Name'] == country, records))
    
    # Convert back to DataFrame. If no records matched, return an empty
    # DataFrame with the same columns as the input so callers can safely
    # access expected columns like 'GDP'.
    if not records:
        return df.iloc[0:0].copy()

    return pd.DataFrame(records)

# -------------------------------
# 3️⃣ Statistical Computation
# -------------------------------
def compute_statistics(df, operation='average'):
    """
    Compute statistics on GDP using functional programming.
    """
    gdp_values = list(map(float, df['GDP']))  # ensure floats
    
    if not gdp_values:
        return 0  # handle empty filtered data
    
    if operation == 'average':
        result = sum(gdp_values) / len(gdp_values)
    elif operation == 'sum':
        result = reduce(lambda a, b: a + b, gdp_values, 0)
    else:
        raise ValueError("Operation must be 'average' or 'sum'")
    
    return result

# -------------------------------
# 4️⃣ Example usage
# -------------------------------
if __name__ == "__main__":
    # Read CSV
    df = pd.read_csv("data.csv")
    
    # Clean & reshape
    df_clean = clean_data(df)
    print("Cleaned & reshaped data:\n", df_clean.head())
    
    # Filter
    df_filtered = filter_data(df_clean, continent='Asia', year=2021)
    print("\nFiltered data (Asia, 2021):\n", df_filtered.head())
    
    # Compute stats
    avg_gdp = compute_statistics(df_filtered, operation='average')
    sum_gdp = compute_statistics(df_filtered, operation='sum')
    
    print("\nAverage GDP (Asia, 2021):", avg_gdp)
    print("Sum of GDP (Asia, 2021):", sum_gdp)
