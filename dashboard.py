# dashboard.py

import pandas as pd
from data_loader import load_data
from data_processor import clean_data, filter_data, compute_statistics
from config_loader import load_config
import visualizer


def load_user_input(config_path="config.json"):
    """Load configuration via config_loader and return normalized config dict."""
    return load_config(config_path)


def main():
    print("=" * 50)
    print("Starting SDA GDP Analysis Project")
    print("=" * 50 + "\n")
    
    # -------------------------------
    # 1️⃣ Load user input
    # -------------------------------
    # Use the project's config.json by default (load_user_input default is config.json)
    user_input = load_user_input()

    # Use `or` to fall back when config contains explicit null/None values
    continent = user_input.get("continent") or "Asia"
    year = user_input.get("year") or 2020
    operation = user_input.get("operation") or "average"
    output_type = user_input.get("output") or "dashboard"
    
    print(f"User Input Configuration:")
    print(f"  • Continent: {continent}")
    print(f"  • Year: {year}")
    print(f"  • Operation: {operation}")
    print(f"  • Output: {output_type}\n")

    # -------------------------------
    # 2️⃣ Load data
    # -------------------------------
    print("Loading data...")
    try:
        # Update this path to your actual CSV file location
        data_path = "data.csv"  # Or get from config: "data/gdp_data.csv"
        df = load_data(data_path)
        print(f"Data loaded successfully. Shape: {df.shape}\n")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the CSV file exists at the specified path.")
        return

    # -------------------------------
    # 3️⃣ Clean & reshape data
    # -------------------------------
    print("Cleaning and reshaping data...")
    try:
        df_clean = clean_data(df)
        print(f"Data cleaned. Available years: {df_clean['Year'].min()} to {df_clean['Year'].max()}")
        print(f"Available continents: {df_clean['Continent'].unique()}\n")
    except KeyError as e:
        print(f"Error: Missing required column in CSV - {e}")
        print("Required columns: 'Country Name', 'Country Code', 'Continent', year columns")
        return

    # Validate config defaults against loaded data. If config contains a region
    # that isn't present in the country-level `Continent` column, treat it as
    # unset so prompts and filtering won't return empty results.
    available_continents = set(df_clean['Continent'].dropna().unique())
    available_years = set(df_clean['Year'].unique())

    if continent not in available_continents:
        print(f"Note: configured continent '{continent}' not present in data. Clearing continent filter.")
        continent = None

    if year not in available_years:
        print(f"Note: configured year '{year}' not present in data. Clearing year filter.")
        year = None

    # -------------------------------
    # 4️⃣ Optional additional filters via user input
    # -------------------------------
    print("Enter additional filter criteria (press Enter to skip):")
    additional_continent = input(f"Continent [{continent}]: ").strip()
    if additional_continent:
        continent = additional_continent
    
    year_input = input(f"Year [{year}]: ").strip()
    if year_input:
        try:
            year = int(year_input)
        except ValueError:
            print("Invalid year. Using default year.")
    
    country = input("Country Name (optional): ").strip() or None

    # -------------------------------
    # 5️⃣ Filter data
    # -------------------------------
    print(f"\nFiltering data for Continent='{continent}', Year={year}" + 
          (f", Country='{country}'" if country else ""))
    
    df_filtered = filter_data(
        df_clean,
        continent=continent,
        year=year,
        country=country
    )

    if df_filtered.empty:
        print("\n❌ No data found for the given filters.")
        print("Please check:")
        print(f"  • Continent '{continent}' exists in data")
        print(f"  • Year {year} exists in data range")
        if country:
            print(f"  • Country '{country}' exists in data")
        return

    print(f"\n✅ Filtered data: {len(df_filtered)} records found")
    print("\nPreview of filtered data:")
    print(df_filtered.head())
    print()

    # -------------------------------
    # 6️⃣ Compute statistics
    # -------------------------------
    try:
        if operation == "average":
            result = compute_statistics(df_filtered, operation="average")
            print(f"📊 Average GDP for filtered data: ${result:,.2f}")
        elif operation == "sum":
            result = compute_statistics(df_filtered, operation="sum")
            print(f"📊 Total GDP for filtered data: ${result:,.2f}")
        else:
            # Calculate both if operation not specified or invalid
            avg_gdp = compute_statistics(df_filtered, operation="average")
            sum_gdp = compute_statistics(df_filtered, operation="sum")
            print(f"📊 Average GDP: ${avg_gdp:,.2f}")
            print(f"📊 Total GDP: ${sum_gdp:,.2f}")
    except Exception as e:
        print(f"Error computing statistics: {e}")

    # -------------------------------
    # 7️⃣ Generate visualizations
    # -------------------------------
    print("\n" + "=" * 50)
    print("Generating Visualizations")
    print("=" * 50)
    
    try:
        if country:
            print(f"📈 Generating line chart for {country}...")
            visualizer.plot_gdp_line(df_clean, country)

        # Region-wise charts: bar + pie
        if continent:
            print(f"📊 Generating region charts for {continent}...")
            visualizer.plot_region_charts(df_clean, continent, year=year, top_n=10)

        # Year-specific charts: bar + pie + histogram
        if year:
            print(f"📊 Generating year charts for {year}...")
            visualizer.plot_year_charts(df_clean, year, top_n=10)
    except Exception as e:
        print(f"Warning: Could not generate visualizations - {e}")
        print("Make sure visualizer.py functions are correctly named.")

    # -------------------------------
    # 8️⃣ Export results if needed
    # -------------------------------
    if output_type == "export":
        output_file = f"gdp_results_{continent}_{year}.csv"
        df_filtered.to_csv(output_file, index=False)
        print(f"\n💾 Results exported to: {output_file}")
    
    print("\n" + "=" * 50)
    print("✅ Project execution completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()