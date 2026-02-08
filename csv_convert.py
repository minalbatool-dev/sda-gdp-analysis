import pandas as pd
import os

def convert_excel_to_csv(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found -> {file_path}")
        return
    df = pd.read_excel(file_path)  # No engine parameter
    
    # Save CSV in the same folder as Excel
    csv_file = os.path.join(os.path.dirname(file_path), "data.csv")
    df.to_csv(csv_file, index=False)
    print(f"Excel converted to CSV successfully: {csv_file}")
    return csv_file