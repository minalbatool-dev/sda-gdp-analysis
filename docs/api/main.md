# API Reference: main.py

Complete reference for `main.py` (orchestrator).

## Module Documentation

```python
\"\"\"Orchestrator: bootstrap layer for the GDP analysis pipeline.

This module is the entry point. It reads configuration from config.json,
instantiates concrete implementations using dictionary-based factories,
and wires the components together via Dependency Injection.
\"\"\"
```

## Module-Level Variables

### INPUT_DRIVERS

```python
INPUT_DRIVERS: Dict[str, Type] = {
    "csv": CSVReader,
    "json": JSONReader,
}
```

Maps input type strings to reader classes. Used by `bootstrap()` to instantiate the appropriate reader.

**Usage in config.json:**

```json
{"input": {"type": "csv", ...}}
```

### OUTPUT_DRIVERS

```python
OUTPUT_DRIVERS: Dict[str, Type] = {
    "console": ConsoleWriter,
    "json": JSONWriter,
    "csv": CSVWriter,
}
```

Maps output type strings to writer classes. Used by `_make_sink()` to instantiate the appropriate writer.

**Usage in config.json:**

```json
{"output": {"type": "json", ...}}
```

---

## Functions

### _make_sink(output_cfg) → Any

```python
def _make_sink(output_cfg: Dict[str, Any]) -> Any
```

Instantiates an output driver from configuration dictionary.

**Parameters:**
- `output_cfg` (Dict): Configuration dict with keys:
  - `type` (str): Driver type (e.g., "console", "json", "csv")
  - Other keys are forwarded as kwargs to the driver constructor

**Returns:** Concrete sink instance (satisfies DataSink protocol)

**Raises:** `ValueError` if output type is unknown

**Implementation:**

```python
def _make_sink(output_cfg):
    typ = output_cfg.get("type")
    if typ not in OUTPUT_DRIVERS:
        raise ValueError(f"unknown output type {typ!r}")
    cls = OUTPUT_DRIVERS[typ]
    # Forward all non-type keys as kwargs
    kwargs = {k: v for k, v in output_cfg.items() if k != "type"}
    return cls(**kwargs)
```

**Example:**

```python
# config.json
{"output": {"type": "json", "path": "results.json"}}

# In bootstrap()
output_cfg = config["output"]
sink = _make_sink(output_cfg)  # returns JSONWriter(path="results.json")
```

### bootstrap() → None

```python
def bootstrap() -> None
```

Main orchestrator. Coordinates the entire pipeline:

1. Loads `config.json`
2. Extracts input config, output config, and parameters
3. Creates sink via `_make_sink()`
4. Creates `TransformationEngine(sink, parameters)`
5. Creates input reader via factory
6. Calls `reader.read()` to execute pipeline

**Raises:**
- `FileNotFoundError` if `config.json` doesn't exist
- `ValueError` if config is invalid
- File I/O errors propagated from readers/writers

**Example:**

```python
# In your code (or run via command line)
bootstrap()  # Parses config.json, runs pipeline, outputs results
```

**Execution Flow:**

```
bootstrap()
    ↓
Load config.json
    ↓
Extract input type, path
Extract output type, path (if any)
Extract parameters (continent, years)
    ↓
_make_sink(output_cfg) → ConsoleWriter/JSONWriter/CSVWriter
    ↓
TransformationEngine(sink, parameters)
    ↓
INPUT_DRIVERS[input_type] → CSVReader/JSONReader
    ↓
reader.read()
    ├─→ Parse file
    ├─→ reader.service.execute(data)  [PipelineService contract]
    │   ├─→ engine._process(data)
    │   ├─→ engine.sink.write(results)  [DataSink contract]
    │   └─→ Output written/displayed
```

---

## Extending the System

### Adding a New Input Format

1. Create reader class in `plugins/inputs.py`:
   ```python
   class YAMLReader:
       def __init__(self, filepath, service: PipelineService): ...
       def read(self): ...
   ```

2. Register in `main.py`:
   ```python
   INPUT_DRIVERS["yaml"] = YAMLReader
   ```

3. Use in `config.json`:
   ```json
   {"input": {"type": "yaml", "path": "data.yaml"}}
   ```

### Adding a New Output Format

1. Create writer class in `plugins/outputs.py`:
   ```python
   class DatabaseWriter:
       def __init__(self, host, port, **kwargs): ...
       def write(self, data): ...
   ```

2. Register in `main.py`:
   ```python
   OUTPUT_DRIVERS["database"] = DatabaseWriter
   ```

3. Use in `config.json`:
   ```json
   {"output": {"type": "database", "host": "localhost", "port": 5432}}
   ```

---

## Main Guard

```python
if __name__ == "__main__":
    bootstrap()
```

Ensures pipeline only runs when script is executed directly (not imported).

---

See also: [Orchestration & Factories](../guide/quickstart.md)
