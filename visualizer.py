import matplotlib.pyplot as plt

# -------------------------------
# Bar chart: GDP by country (for a given year)
# -------------------------------
def plot_gdp_by_country(df, year):
    """
    Plot GDP of all countries for a specific year as a bar chart.
    """
    df_year = df[df['Year'] == year].sort_values(by='GDP', ascending=False)

    plt.figure(figsize=(12, 6))
    plt.bar(df_year['Country Name'], df_year['GDP'])
    plt.xticks(rotation=90)
    plt.title(f"GDP by Country in {year}")
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.tight_layout()
    plt.show()


# -------------------------------
# Line chart: GDP over time for a country
# -------------------------------
def plot_gdp_over_time(df, country):
    """
    Plot GDP over time for a specific country.
    """
    df_country = df[df['Country Name'] == country].sort_values(by='Year')

    plt.figure(figsize=(10, 5))
    plt.plot(df_country['Year'], df_country['GDP'], marker='o')
    plt.title(f"GDP Over Time - {country}")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.grid(True)
    plt.show()


# -------------------------------
# Pie chart: GDP share (top N countries, given year)
# -------------------------------
def plot_gdp_pie(df, year, top_n=10):
    """
    Plot GDP share of top N countries for a given year as a pie chart.
    """
    df_year = df[df['Year'] == year].sort_values(by='GDP', ascending=False)
    df_top = df_year.head(top_n)

    plt.figure(figsize=(8, 8))
    plt.pie(
        df_top['GDP'],
        labels=df_top['Country Name'],
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title(f"Top {top_n} Countries by GDP in {year}")
    plt.show()
