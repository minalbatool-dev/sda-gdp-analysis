# Quick Start Guide

Get the GDP Analysis Platform running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- A terminal/command prompt
- The workspace directory with source files

## Step 1: Set Up Virtual Environment

Create an isolated Python environment:

```bash
# Create venv
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (macOS/Linux)
source .venv/bin/activate
```

## Step 2: Verify Data Files

Check that data files exist:

```bash
# CSV data
dir data/data.csv

# JSON data (auto-generated)
dir data/data.json
```

If `data.json` doesn't exist, it will be created on first run using the CSV.

## Step 3: Configure the Analysis

Edit `config.json` to specify:
- Input source (CSV or JSON)
- Output destination (console, JSON file, or CSV file)
- Analysis parameters (continent, years)

### Example: Console Output (Quick Test)

```json
{
  "input": {
    "type": "csv",
    "path": "data/data.csv"
  },
  "output": {
    "type": "console"
  },
  "parameters": {
    "continent": "Asia",
    "year": 2020,
    "start_year": 2015,
    "end_year": 2020
  }
}
```

### Example: JSON File Output (For Processing)

```json
{
  "input": {
    "type": "json",
    "path": "data/data.json"
  },
  "output": {
    "type": "json",
    "path": "out/results.json"
  },
  "parameters": {
    "continent": "Europe",
    "year": 2020,
    "start_year": 2015,
    "end_year": 2020
  }
}
```

## Step 4: Run the Pipeline

```bash
python main.py
```

### Console Output Example

```
===== GDP ANALYSIS RESULTS =====

--- TOP_10 ---
[{'Country': 'China', 'GDP': 14996414166715.1}, 
 {'Country': 'Japan', 'GDP': 5054068005376.28}, ...]

--- BOTTOM_10 ---
[{'Country': 'Timor-Leste', 'GDP': 2162619240.87}, ...]

--- GROWTH_RATE ---
[{'Country': 'Bangladesh', 'GrowthRate(%)': 91.64}, ...]

...
```

### File Output Example

If output type is `json`, results are written to the specified file:

```bash
# Results in out/results.json
Results written to out/results.json
```

View the results:

```bash
# On Windows
type out\results.json

# On macOS/Linux
cat out/results.json
```

## Step 5: Experiment

Try different configurations:

### Switch Continents

```json
"parameters": {
  "continent": "Europe",  // Change this
  ...
}
```

### Switch Output Format

```json
"output": {
  "type": "csv",  // or "json"
  "path": "results.csv"
}
```

### Switch Input Format

```json
"input": {
  "type": "json",  // or "csv"
  "path": "data/data.json"
}
```

## Available Continents

- Africa
- Asia
- Europe
- North America
- Oceania
- South America

## Output Formats

| Type | Output Location | Use Case |
|------|-----------------|----------|
| `console` | Stdout | Development, quick inspection |
| `json` | File (JSON) | Integration, archival |
| `csv` | File (CSV) | Spreadsheet tools |

## Troubleshooting

### FileNotFoundError: output directory doesn't exist

Create the output directory first:

```bash
mkdir out
python main.py
```

### json.JSONDecodeError when using JSON input

Make sure the JSON file is valid. Regenerate if needed:

```python
import csv, json
rows = []
with open('data/data.csv', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
json.dump(rows, open('data/data.json', 'w'))
```

### Missing config keys error

Ensure `config.json` has all required keys:

```json
{
  "input": {"type": "...", "path": "..."},
  "output": {"type": "..."},
  "parameters": {"continent": "...", "year": ..., "start_year": ..., "end_year": ...}
}
```

---

Next: [Configuration Deep-Dive](configuration.md)
