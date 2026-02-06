# main.py

import json
from data_loader import load_data
from data_processor import clean_data, filter_data, compute_statistics
import visualizer


def load_config(config_path="config.json"):
    """Load configuration settings from config.json"""
    with open(config_path, "r") as f:
        return json.load(f)


def main():
    print("Starting SDA GDP Analysis Project...\n")

    # -------------------------------
    # 1️⃣ Load configuration
    # -------------------------------
    config = load_config()

    data_path = config["data"]["csv_path"]
    default_year = config["filters"].get("year")
    default_continent = config["filters"].get("continent")

    # -------------------------------
    # 2️⃣ Load data
    # -------------------------------
    print("Loading data...")
    df = load_data(data_path)
    print("Data loaded successfully.\n")

    # -------------------------------
    # 3️⃣ Clean & reshape data
    # -------------------------------
    print("Cleaning and reshaping data...")
    df_clean = clean_data(df)
    print("Data cleaned.\n")

    # -------------------------------
    # 4️⃣ User input (optional filters)
    # -------------------------------
    print("Enter filter criteria (press Enter to skip):")
    continent = input(f"Continent [{default_continent}]: ").strip() or default_continent

    year_input = input(f"Year [{default_year}]: ").strip()
    year = int(year_input) if year_input else default_year

    country = input("Country Name: ").strip() or None

    # -------------------------------
    # 5️⃣ Filter data
    # -------------------------------
    df_filtered = filter_data(
        df_clean,
        continent=continent,
        year=year,
        country=country
    )

    if df_filtered.empty:
        print("\nNo data found for the given filters.")
        return

    print("\nFiltered data preview:")
    print(df_filtered.head())

    # -------------------------------
    # 6️⃣ Compute statistics
    # -------------------------------
    avg_gdp = compute_statistics(df_filtered, operation="average")
    sum_gdp = compute_statistics(df_filtered, operation="sum")

    print(f"\nAverage GDP: {avg_gdp}")
    print(f"Total GDP: {sum_gdp}")

    # -------------------------------
    # 7️⃣ Visualizations
    # -------------------------------
    if country:
        visualizer.plot_gdp_line(df_clean, country)

    if year:
        visualizer.plot_gdp_bar(df_clean, year)
        visualizer.plot_gdp_pie(df_clean, year, top_n=10)

    print("\nProject execution completed successfully!")


if __name__ == "__main__":
    main()
