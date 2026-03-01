# Adding Output Plugins

Learn how to extend the system with new output destinations.

## Overview

Output plugins write analysis results to various destinations (console, files, databases, APIs, charts, etc.). Because we use the `DataSink` protocol, new outputs can be added without modifying any core code.

## Step-by-Step Guide

### Step 1: Create the Writer Class

In `plugins/outputs.py`, create a new class:

```python
class MyCustomWriter:
    \"\"\"Write analysis results to a custom destination.\"\"\"
    
    def __init__(self, destination: str = \"default\", **kwargs):
        \"\"\"
        Args:
            destination: Where to write (file path, URL, etc.)
            **kwargs: Additional config parameters (from config.json)
        \"\"\"
        self.destination = destination
        # Store any additional config
        self.config = kwargs
    
    def write(self, data: Dict[str, Any]) -> None:
        \"\"\"Persist or display the analysis results.
        
        Args:
            data: Result dict with keys:
                - top_10, bottom_10, growth_rate, average_by_continent,
                  global_trend, fastest_growing_continent,
                  consistent_decline, global_contribution
        \"\"\"
        # 1. Format results as needed
        formatted = self._format(data)
        
        # 2. Write to destination
        self._write(formatted)
        
        # 3. Confirm to user
        print(f\"Results written to {self.destination}\")
    
    def _format(self, data):
        \"\"\"Format data for your destination.\"\"\"
        # Custom formatting logic
        return data
    
    def _write(self, formatted):
        \"\"\"Write formatted data to destination.\"\"\"
        # Your custom writing logic
        pass
```

### Step 2: The Data Contract

Your writer **must** implement the `DataSink` protocol. The `write` method receives:

```python
{
    \"top_10\": [{\"Country\": str, \"GDP\": float}, ...],
    \"bottom_10\": [{\"Country\": str, \"GDP\": float}, ...],
    \"growth_rate\": [{\"Country\": str, \"GrowthRate(%)\": float}, ...],
    \"average_by_continent\": {continent: avg_gdp, ...},
    \"global_trend\": {year: total_gdp, ...},
    \"fastest_growing_continent\": str,
    \"consistent_decline\": [country_names],
    \"global_contribution\": {continent: percentage, ...},
}
```

You can use any or all of this data.

### Step 3: Register in main.py

Add your writer to the factory:

```python
from plugins.outputs import ConsoleWriter, JSONWriter, CSVWriter, MyCustomWriter

OUTPUT_DRIVERS = {
    \"console\": ConsoleWriter,
    \"json\": JSONWriter,
    \"csv\": CSVWriter,
    \"my_format\": MyCustomWriter,  # Add this
}
```

### Step 4: Use in config.json

```json
{
  \"output\": {
    \"type\": \"my_format\",
    \"destination\": \"/path/to/output\",
    \"other_param\": \"value\"
  }
}
```

Any keys besides `type` are forwarded as kwargs to your constructor.

### Step 5: Run

```bash
python main.py
```

---

## Example: Excel Writer

```python
class ExcelWriter:
    \"\"\"Write analysis results to an Excel file.\"\"\"
    
    def __init__(self, path: str = \"results.xlsx\", **kwargs):
        self.path = path
    
    def write(self, data: Dict[str, Any]) -> None:
        try:
            import openpyxl
            from openpyxl.utils import get_column_letter
        except ImportError:
            raise ImportError(\"openpyxl not installed. pip install openpyxl\")
        
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Write top_10
        ws[\"A1\"] = \"Top 10 Countries\"
        row = 2
        for item in data[\"top_10\"]:
            ws[f\"A{row}\"] = item[\"Country\"]
            ws[f\"B{row}\"] = item[\"GDP\"]
            row += 1
        
        # Write other sections...
        
        wb.save(self.path)
        print(f\"Results written to {self.path}\")
```

**Register:**

```python
OUTPUT_DRIVERS[\"excel\"] = ExcelWriter
```

**Use:**

```json
{
  \"output\": {
    \"type\": \"excel\",
    \"path\": \"out/results.xlsx\"
  }
}
```

---

## Example: Database Writer

```python
import sqlite3

class DatabaseWriter:
    \"\"\"Write analysis results to a SQLite database.\"\"\"
    
    def __init__(self, db_path: str = \"results.db\", **kwargs):
        self.db_path = db_path
    
    def write(self, data: Dict[str, Any]) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS top_10 (
                country TEXT,
                gdp REAL
            )
        \"\"\")
        
        # Insert top_10
        for item in data[\"top_10\"]:
            cursor.execute(
                \"INSERT INTO top_10 VALUES (?, ?)\",
                (item[\"Country\"], item[\"GDP\"])
            )
        
        # Insert other metrics...
        
        conn.commit()
        conn.close()
        print(f\"Results written to {self.db_path}\")
```

---

## Example: Visualization Writer

```python
class ChartWriter:
    \"\"\"Generate charts from analysis results.\"\"\"
    
    def __init__(self, output_dir: str = \"charts\", **kwargs):
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def write(self, data: Dict[str, Any]) -> None:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError(\"matplotlib not installed\")
        
        # Chart 1: Top 10 countries
        countries = [x[\"Country\"] for x in data[\"top_10\"]]
        gdps = [x[\"GDP\"] for x in data[\"top_10\"]]
        
        plt.figure(figsize=(12, 6))
        plt.bar(countries, gdps)
        plt.title(\"Top 10 Countries by GDP\")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f\"{self.output_dir}/top_10.png\")
        plt.close()
        
        # Chart 2: Global trend
        years = sorted([int(y) for y in data[\"global_trend\"].keys()])
        values = [data[\"global_trend\"][str(y)] for y in years]
        
        plt.figure(figsize=(12, 6))
        plt.plot(years, values, marker=\"o\")
        plt.title(\"Global GDP Trend\")
        plt.xlabel(\"Year\")
        plt.ylabel(\"GDP\")
        plt.grid(True)
        plt.savefig(f\"{self.output_dir}/trend.png\")
        plt.close()
        
        print(f\"Charts saved to {self.output_dir}\")
```

---

## Design Principles

1. **No Core Dependencies**: Your writer should not import core engine code (except the protocol hint)
2. **One Job**: Focus only on formatting and writing your destination
3. **Configuration**: Accept parameters via kwargs from config.json
4. **Error Handling**: Raise exceptions for missing directories, I/O errors, etc.
5. **User Feedback**: Print confirmation messages when data is written
6. **Documentation**: Add docstrings explaining usage and parameters

---

## Testing Your Writer

```python
from plugins.outputs import MyCustomWriter
from core.engine import TransformationEngine

# Create test data
test_data = {
    \"top_10\": [{\"Country\": \"China\", \"GDP\": 14996414166715.1}],
    \"bottom_10\": [{\"Country\": \"Timor-Leste\", \"GDP\": 2162619240.87}],
    \"growth_rate\": [{\"Country\": \"Bangladesh\", \"GrowthRate(%)\": 91.64}],
    \"average_by_continent\": {\"Asia\": 1186724516781.87},
    \"global_trend\": {\"2015\": 254982339316356.7, \"2020\": 289191698345157.9},
    \"fastest_growing_continent\": \"Europe\",
    \"consistent_decline\": [\"Yemen, Rep.\"],
    \"global_contribution\": {\"Asia\": 21.34, \"Europe\": 45.22},
}

# Test your writer
writer = MyCustomWriter(\"test_output\")
writer.write(test_data)  # Should produce output without errors
```

---

See also: [Adding Input Plugins](input_plugins.md)
