# API Reference: Output Plugins

Complete reference for `plugins/outputs.py`.

## Class: ConsoleWriter

**Location:** `plugins/outputs.py`

Writes analysis results to stdout (console).

### Constructor

```python
def __init__(self, **kwargs: Any)
```

**Parameters:**
- `**kwargs`: Ignored; accepts arbitrary kwargs for factory compatibility.

### Public Methods

#### write(data) → None

```python
def write(self, data: Dict[str, Any]) -> None
```

Pretty-prints the result dict to stdout.

**Parameters:**
- `data`: Result dict with keys: `top_10`, `bottom_10`, `growth_rate`, etc.

**Output Example:**

```
===== GDP ANALYSIS RESULTS =====

--- TOP_10 ---
[{'Country': 'China', 'GDP': 14996414166715.1}, ...]

--- BOTTOM_10 ---
[{'Country': 'Timor-Leste', 'GDP': 2162619240.87}, ...]

...
```

---

## Class: JSONWriter

**Location:** `plugins/outputs.py`

Writes analysis results to a JSON file.

### Constructor

```python
def __init__(self, path: str = "output.json", **kwargs: Any)
```

**Parameters:**
- `path` (str): Output file path. Default is `"output.json"`.
- `**kwargs`: Ignored; accepts arbitrary kwargs for factory compatibility.

**Raises:** `FileNotFoundError` if parent directory doesn't exist.

### Public Methods

#### write(data) → None

```python
def write(self, data: Dict[str, Any]) -> None
```

Serializes result dict to JSON (2-space indent) and writes to file.

**Parameters:**
- `data`: Result dict with all analytics

**Output Format:**

```json
{
  "top_10": [
    {"Country": "China", "GDP": 14996414166715.1},
    ...
  ],
  "bottom_10": [...],
  "growth_rate": [...],
  ...
}
```

**Example Usage:**

```python
from plugins.outputs import JSONWriter
from core.engine import TransformationEngine

sink = JSONWriter(path="out/results.json")
config = {"continent": "Asia", "year": 2020, ...}
engine = TransformationEngine(sink, config)
engine.execute(raw_data)  # Results written to out/results.json
```

---

## Class: CSVWriter

**Location:** `plugins/outputs.py`

Writes analysis results to a CSV file (two columns: section, payload).

### Constructor

```python
def __init__(self, path: str = "output.csv", **kwargs: Any)
```

**Parameters:**
- `path` (str): Output file path. Default is `"output.csv"`.
- `**kwargs`: Ignored; accepts arbitrary kwargs for factory compatibility.

**Raises:** `FileNotFoundError` if parent directory doesn't exist.

### Public Methods

#### write(data) → None

```python
def write(self, data: Dict[str, Any]) -> None
```

Writes result dict as a two-column CSV (section name → stringified payload).

**Parameters:**
- `data`: Result dict with all analytics

**Output Format:**

```csv
section,payload
top_10,"[{'Country': 'China', 'GDP': 14996414166715.1}, ...]"
bottom_10,"[{'Country': 'Timor-Leste', 'GDP': 2162619240.87}, ...]"
growth_rate,"[{'Country': 'Afghanistan', 'GrowthRate(%)': 4.29}, ...]"
...
```

**Example Usage:**

```python
from plugins.outputs import CSVWriter
from core.engine import TransformationEngine

sink = CSVWriter(path="results.csv")
config = {"continent": "Europe", "year": 2020, ...}
engine = TransformationEngine(sink, config)
engine.execute(raw_data)  # Results written to results.csv
```

---

## Configuration Integration

All writers are registered in `main.py`:

```python
OUTPUT_DRIVERS = {
    "console": ConsoleWriter,
    "json": JSONWriter,
    "csv": CSVWriter,
}
```

And used via `config.json`:

```json
{
  "output": {
    "type": "json",
    "path": "out/results.json"
  }
}
```

The `_make_sink()` helper in `main.py` instantiates the writer with config kwargs:

```python
def _make_sink(output_cfg):
    typ = output_cfg.get("type")
    cls = OUTPUT_DRIVERS[typ]
    kwargs = {k: v for k, v in output_cfg.items() if k != "type"}
    return cls(**kwargs)  # path is passed as kwarg
```

---

See also: [DataSink Protocol](contracts.md)
