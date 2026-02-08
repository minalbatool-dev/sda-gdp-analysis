# visualizer.py

import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# 1️⃣ Bar chart for GDP by country
# -------------------------------
def plot_gdp_by_country(df, year):
    """
    Plots GDP of all countries in a given year.
    """
    # Filter for the year
    df_year = df[df['Year'] == year]
    
    # Sort by GDP descending
    df_year = df_year.sort_values(by='GDP', ascending=False)
    
    plt.figure(figsize=(12,6))
    plt.bar(df_year['Country Name'], df_year['GDP'])
    plt.xticks(rotation=90)
    plt.title(f"GDP by Country in {year}")
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.tight_layout()
    plt.show()

# -------------------------------
# 2️⃣ Line chart for GDP over years for a country
# -------------------------------
def plot_gdp_over_time(df, country):
    """
    Plots GDP over years for a specific country.
    """
    df_country = df[df['Country Name'] == country]
    df_country = df_country.sort_values(by='Year')
    
    plt.figure(figsize=(10,5))
    plt.plot(df_country['Year'], df_country['GDP'], marker='o')
    plt.title(f"GDP Over Time - {country}")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.grid(True)
    plt.show()


# -------------------------------
# 1️⃣ Bar chart for GDP by country
# -------------------------------
def plot_gdp_bar(df, year):
    """
    Plots GDP of all countries in a given year as a bar chart.
    """
    df_year = df[df['Year'] == year].sort_values(by='GDP', ascending=False)
    
    plt.figure(figsize=(12,6))
    plt.bar(df_year['Country Name'], df_year['GDP'], color='skyblue')
    plt.xticks(rotation=90)
    plt.title(f"GDP by Country in {year} - Bar Chart")
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.tight_layout()
    plt.show()

# -------------------------------
# 2️⃣ Pie chart for GDP by country
# -------------------------------
def plot_gdp_pie(df, year, top_n=10):
    """
    Plots GDP of top N countries in a given year as a pie chart.
    """
    df_year = df[df['Year'] == year].sort_values(by='GDP', ascending=False)
    df_top = df_year.head(top_n)
    
    plt.figure(figsize=(8,8))
    plt.pie(df_top['GDP'], labels=df_top['Country Name'], autopct='%1.1f%%', startangle=140)
    plt.title(f"Top {top_n} Countries by GDP in {year} - Pie Chart")
    plt.show()


def plot_gdp_hist(df, year, bins=30):
    """Plot a histogram of GDP values across countries for a specific year."""
    df_year = df[df['Year'] == year]
    values = df_year['GDP'].dropna()
    if values.empty:
        print(f"No GDP data for year {year} to plot histogram.")
        return

    plt.figure(figsize=(10,6))
    plt.hist(values, bins=bins, color='teal', edgecolor='black')
    plt.title(f"GDP Distribution Across Countries - {year} (Histogram)")
    plt.xlabel("GDP")
    plt.ylabel("Number of Countries")
    plt.tight_layout()
    plt.show()

# -------------------------------
# 3️⃣ Line chart for GDP over years for a country
# -------------------------------
def plot_gdp_line(df, country):
    """
    Plots GDP over years for a specific country as a line chart.
    """
    df_country = df[df['Country Name'] == country].sort_values(by='Year')
    
    plt.figure(figsize=(10,5))
    plt.plot(df_country['Year'], df_country['GDP'], marker='o', linestyle='-', color='green')
    plt.title(f"GDP Over Time - {country} - Line Chart")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.grid(True)
    plt.show()


def plot_region_charts(df, continent, year=None, top_n=10):
    """Produce a bar chart + pie chart for a continent (region). Optionally filter by year."""
    if year:
        df_region = df[(df['Continent'] == continent) & (df['Year'] == year)]
    else:
        df_region = df[df['Continent'] == continent]

    if df_region.empty:
        print(f"No data for region '{continent}'{f' in {year}' if year else ''}.")
        return

    df_grouped = df_region.groupby('Country Name', as_index=False)['GDP'].sum().sort_values('GDP', ascending=False)
    df_top = df_grouped.head(top_n)

    # Bar
    plt.figure(figsize=(12,6))
    plt.bar(df_top['Country Name'], df_top['GDP'], color='coral')
    plt.xticks(rotation=90)
    plt.title(f"Top {top_n} Countries in {continent} by GDP" + (f" ({year})" if year else ""))
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.tight_layout()
    plt.show()

    # Pie
    plt.figure(figsize=(8,8))
    plt.pie(df_top['GDP'], labels=df_top['Country Name'], autopct='%1.1f%%', startangle=140)
    plt.title(f"Top {top_n} Countries in {continent} by GDP - Pie")
    plt.show()


def plot_year_charts(df, year, top_n=10):
    """Produce multiple chart types for a specific year: bar, pie, histogram."""
    df_year = df[df['Year'] == year]
    if df_year.empty:
        print(f"No data for year {year} to plot charts.")
        return

    df_grouped = df_year.groupby('Country Name', as_index=False)['GDP'].sum().sort_values('GDP', ascending=False)
    df_top = df_grouped.head(top_n)

    # Bar
    plt.figure(figsize=(12,6))
    plt.bar(df_top['Country Name'], df_top['GDP'], color='skyblue')
    plt.xticks(rotation=90)
    plt.title(f"Top {top_n} Countries by GDP in {year} - Bar")
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.tight_layout()
    plt.show()

    # Pie
    plt.figure(figsize=(8,8))
    plt.pie(df_top['GDP'], labels=df_top['Country Name'], autopct='%1.1f%%', startangle=140)
    plt.title(f"Top {top_n} Countries by GDP in {year} - Pie")
    plt.show()

    # Histogram
    plot_gdp_hist(df, year)

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("data.csv")
    
    # Example: clean & reshape using previous processor logic
    from data_processor import clean_data
    df_clean = clean_data(df)
    """
    plot_gdp_by_country(df_clean, 2021)
    plot_gdp_over_time(df_clean, "India")
    """
    plot_gdp_bar(df_clean, 2021)
    plot_gdp_pie(df_clean, 2021, top_n=10)
    plot_gdp_line(df_clean, "India")