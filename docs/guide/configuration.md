# Configuration Guide

The `config.json` file controls the entire pipeline behavior. Edit it to customize input sources, output destinations, and analysis parameters without touching Python code.

## Structure

```json
{
  "input": {
    "type": "csv",         // or "json"
    "path": "data/data.csv"
  },
  "output": {
    "type": "console",     // or "json", "csv"
    "path": "results.json" // optional, path for file outputs
  },
  "parameters": {
    "continent": "Asia",
    "year": 2020,
    "start_year": 2015,
    "end_year": 2020,
    "decline_years": 3
  }
}
```

## Input Configuration

### CSV

```json
{
  "input": {
    "type": "csv",
    "path": "data/data.csv"
  }
}
```

- **type**: `"csv"` – reads comma-separated values
- **path**: Relative or absolute path to CSV file

### JSON

```json
{
  "input": {
    "type": "json",
    "path": "data/data.json"
  }
}
```

- **type**: `"json"` – reads JSON array of objects
- **path**: Relative or absolute path to JSON file

## Output Configuration

### Console (Terminal)

```json
{
  "output": {
    "type": "console"
  }
}
```

Results are pretty-printed to stdout. The `path` key is ignored.

**Best for:** Development, debugging, interactive use

### JSON File

```json
{
  "output": {
    "type": "json",
    "path": "out/results.json"
  }
}
```

Results are serialized to JSON with 2-space indentation.

**Best for:** Integration, archival, downstream processing

**Note:** Parent directory must exist; create `mkdir out` if needed.

### CSV File

```json
{
  "output": {
    "type": "csv",
    "path": "out/results.csv"
  }
}
```

Results are written as a two-column CSV: `[section, payload]`

**Best for:** Spreadsheet tools (Excel, Google Sheets)

**Note:** Parent directory must exist; create `mkdir out` if needed.

## Parameters

All analysis-related settings go in `parameters`:

```json
{
  "parameters": {
    "continent": "Asia",           // Required: target continent
    "year": 2020,                  // Required: reference year for rankings
    "start_year": 2015,            // Required: first year in trend
    "end_year": 2020,              // Required: last year in trend
    "decline_years": 3             // Optional: (unused in current impl.)
  }
}
```

### continent (string, required)

One of:
- `"Africa"`
- `"Asia"`
- `"Europe"`
- `"North America"`
- `"Oceania"`
- `"South America"`

### year (int, required)

The reference year for top-10 and bottom-10 rankings. Must be in the range `start_year` to `end_year`.

Example: `2020`

### start_year, end_year (int, required)

The date range for trend analysis. Inclusive on both ends.

Example: `2015` to `2020` analyzes 6 years of data.

## Real-World Examples

### Quick Inspection (Console Output)

```json
{
  "input": {"type": "csv", "path": "data/data.csv"},
  "output": {"type": "console"},
  "parameters": {
    "continent": "Africa",
    "year": 2020,
    "start_year": 2015,
    "end_year": 2020
  }
}
```

**Usage:** `python main.py` – see results immediately

### Archival (JSON Output)

```json
{
  "input": {"type": "csv", "path": "data/data.csv"},
  "output": {"type": "json", "path": "archive/2020_analysis.json"},
  "parameters": {
    "continent": "Europe",
    "year": 2020,
    "start_year": 2010,
    "end_year": 2020
  }
}
```

**Usage:** Results saved to `archive/2020_analysis.json` for later retrieval

### Spreadsheet Export (CSV Output)

```json
{
  "input": {"type": "json", "path": "data/data.json"},
  "output": {"type": "csv", "path": "export/report.csv"},
  "parameters": {
    "continent": "Asia",
    "year": 2019,
    "start_year": 2015,
    "end_year": 2019
  }
}
```

**Usage:** `python main.py` – results written to `export/report.csv` for Excel

---

Next: [Running the Pipeline](running.md)
