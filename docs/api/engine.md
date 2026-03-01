# API Reference: TransformationEngine

Complete reference for `core/engine.py`.

## Class: TransformationEngine

**Location:** `core/engine.py`

**Parent:** Implements `PipelineService` protocol

### Constructor

```python
def __init__(self, sink: DataSink, config: Dict[str, Any]) -> None
```

**Parameters:**

- `sink` (DataSink): Output writer (ConsoleWriter, JSONWriter, etc.)
- `config` (Dict): Analysis parameters with keys:
  - `continent` (str): Target continent
  - `year` (int): Reference year
  - `start_year` (int): First analysis year
  - `end_year` (int): Last analysis year

**Raises:** `ValueError` if required config keys are missing.

### Public Methods

#### execute(raw_data)

```python
def execute(self, raw_data: List[Dict[str, Any]]) -> None
```

Main entry point. Processes raw data and outputs results via injected sink.

**Parameters:**
- `raw_data`: List of country data dicts (from CSVReader or JSONReader)

**Behavior:**
1. Validates config
2. Processes data via `_process()`
3. Calls `sink.write(result)`

**Example:**

```python
from core.engine import TransformationEngine
from plugins.outputs import ConsoleWriter

sink = ConsoleWriter()
config = {"continent": "Asia", "year": 2020, "start_year": 2015, "end_year": 2020}
engine = TransformationEngine(sink, config)

# Raw data typically comes from CSVReader or JSONReader
raw_data = [
    {"Country Name": "China", "Country Code": "CHN", "Continent": "Asia", "2015": "...", ...},
    {...},
]

engine.execute(raw_data)  # Processes and outputs
```

### Private Methods (Analytics)

Each of these is called by `_process()` and returns data for the output dict:

#### _top_10(data, continent, year) → List[Dict]

Returns the top 10 countries by GDP in a continent for a given year.

#### _bottom_10(data, continent, year) → List[Dict]

Returns the bottom 10 countries by GDP in a continent for a given year.

#### _growth_rate(data, continent, start_year, end_year) → List[Dict]

Computes percent change in GDP for each country from start to end year.

#### _average_by_continent(data, end_year) → Dict[str, float]

Average GDP per continent for the given year.

#### _global_trend(data, start_year, end_year) → Dict[str, float]

Year-by-year global GDP totals.

#### _fastest_growing_continent(data, start_year, end_year) → str

Which continent had the highest absolute GDP growth.

#### _consistent_decline(data, start_year, end_year) → List[str]

Lists countries whose GDP declined every single year in the range.

#### _global_contribution(data, end_year) → Dict[str, float]

Each continent's percentage share of global GDP.

### Validation Methods

#### _validate_config()

Checks that all required config keys are present. Raises `ValueError` if not.

#### _is_valid_country(record) → bool

Filters out invalid/aggregate countries:
- Excludes rows with global/regional aggregates
- Requires 3-letter ISO country code

#### _safe_float(value) → float

Safely converts string values to float, returning 0.0 if conversion fails.

### Data Flow

```
raw_data (List[Dict])
    ↓
execute()
    ↓
_process()
    ├─→ _top_10()
    ├─→ _bottom_10()
    ├─→ _growth_rate()
    ├─→ _average_by_continent()
    ├─→ _global_trend()
    ├─→ _fastest_growing_continent()
    ├─→ _consistent_decline()
    └─→ _global_contribution()
    ↓
result_dict = {
    "top_10": [...],
    "bottom_10": [...],
    "growth_rate": [...],
    ...
}
    ↓
sink.write(result_dict)
```

### Output Structure

The result dict passed to sink has these keys:

```python
{
    "top_10": [{"Country": str, "GDP": float}, ...],
    "bottom_10": [{"Country": str, "GDP": float}, ...],
    "growth_rate": [{"Country": str, "GrowthRate(%)": float}, ...],
    "average_by_continent": {"Asia": float, ...},
    "global_trend": {"2015": float, "2016": float, ...},
    "fastest_growing_continent": str,
    "consistent_decline": [str, ...],
    "global_contribution": {"Asia": float, ...}
}
```

---

See also: [PipelineService Protocol](contracts.md)
