# API Reference: Input Plugins

Complete reference for `plugins/inputs.py`.

## Class: CSVReader

**Location:** `plugins/inputs.py`

Reads GDP data from a CSV file and submits to a PipelineService.

### Constructor

```python
def __init__(self, filepath: str, service: PipelineService)
```

**Parameters:**
- `filepath` (str): Path to CSV file
- `service` (PipelineService): Engine to call with parsed rows

### Public Methods

#### read() → None

```python
def read(self) -> None
```

Parses the CSV file using `csv.DictReader` and calls `service.execute(data)`.

**Raises:**
- `FileNotFoundError` if filepath doesn't exist
- `csv.Error` if parsing fails

**Example:**

```python
from plugins.inputs import CSVReader
from core.engine import TransformationEngine
from plugins.outputs import ConsoleWriter

sink = ConsoleWriter()
config = {"continent": "Asia", "year": 2020, "start_year": 2015, "end_year": 2020}
engine = TransformationEngine(sink, config)

reader = CSVReader("data/data.csv", engine)
reader.read()  # Parses CSV, calls engine.execute()
```

---

## Class: JSONReader

**Location:** `plugins/inputs.py`

Reads GDP data from a JSON file and submits to a PipelineService.

### Constructor

```python
def __init__(self, filepath: str, service: PipelineService)
```

**Parameters:**
- `filepath` (str): Path to JSON file
- `service` (PipelineService): Engine to call with parsed array

### Public Methods

#### read() → None

```python
def read(self) -> None
```

Parses the JSON file (expects top-level array) and calls `service.execute(data)`.

**Raises:**
- `FileNotFoundError` if filepath doesn't exist
- `json.JSONDecodeError` if JSON is malformed

**Example:**

```python
from plugins.inputs import JSONReader
from core.engine import TransformationEngine
from plugins.outputs import ConsoleWriter

sink = ConsoleWriter()
config = {"continent": "Europe", "year": 2020, "start_year": 2015, "end_year": 2020}
engine = TransformationEngine(sink, config)

reader = JSONReader("data/data.json", engine)
reader.read()  # Parses JSON, calls engine.execute()
```

---

## Data Format

Both readers expect data in the same format:

```python
[
    {
        "Country Name": str,      # e.g., "China"
        "Country Code": str,      # e.g., "CHN" (3-letter ISO)
        "Continent": str,         # e.g., "Asia"
        "2015": str or float,     # GDP value
        "2016": str or float,
        ...
        "2020": str or float,
    },
    {...},
    ...
]
```

### CSV Format

```csv
Country Name,Country Code,Continent,2015,2016,...,2020
China,CHN,Asia,10050000000000,10480000000000,...,14720000000000
India,IND,Asia,2103590000000,2298170000000,...,2622990000000
```

### JSON Format

```json
[
  {"Country Name": "China", "Country Code": "CHN", "Continent": "Asia", "2015": "10050000000000", ...},
  {"Country Name": "India", "Country Code": "IND", "Continent": "Asia", "2015": "2103590000000", ...},
  ...
]
```

---

See also: [PipelineService Protocol](contracts.md)
