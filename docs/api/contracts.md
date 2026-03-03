# API Reference: Contracts

Complete reference for `core/contracts.py`.

## Module Documentation

```python
"""Core protocol contracts for Dependency Inversion.

This module defines the two structural interfaces (Protocols) that enable
complete decoupling of the system...
"""
```

## DataSink Protocol

**Location:** `core/contracts.py`

**Purpose:** Output abstraction – where the engine sends results.

```python
@runtime_checkable
class DataSink(Protocol):
    """Outbound abstraction: where the core sends processed results."""
    
    def write(self, data: Dict[str, Any]) -> None:
        """Persist or display the analysis results."""
```

### Parameters

**data** (Dict[str, Any])

- `top_10`: List of top 10 countries by GDP
- `bottom_10`: List of bottom 10 countries by GDP
- `growth_rate`: List of dictionaries with growth_rate per country
- `average_by_continent`: Dict with continent → average GDP
- `global_trend`: Dict with year (str) → global GDP
- `fastest_growing_continent`: String name of continent
- `consistent_decline`: List of country names
- `global_contribution`: Dict with continent → % of global GDP

### Returns

None. Side effects are the contract (persisting data somewhere).

### Implementations

| Class | Module | Description |
|-------|--------|-------------|
| `ConsoleWriter` | `plugins.outputs` | Prints to stdout |
| `JSONWriter` | `plugins.outputs` | Writes to JSON file |
| `CSVWriter` | `plugins.outputs` | Writes to CSV file |

### Example Usage

```python
from core.contracts import DataSink
from plugins.outputs import ConsoleWriter

sink: DataSink = ConsoleWriter()
sink.write({
    "top_10": [{"Country": "China", "GDP": 14996414166715.1}, ...],
    "bottom_10": [...],
    # ... other keys
})
```

### Duck Typing

Any class with a `write(self, data: Dict[str, Any]) -> None` method automatically satisfies this protocol:

```python
class CustomWriter:
    def write(self, data):
        # Custom logic
        pass

sink: DataSink = CustomWriter()  # ✓ Works!
```

## PipelineService Protocol

**Location:** `core/contracts.py`

**Purpose:** Input abstraction – how external sources feed data to the engine.

```python
class PipelineService(Protocol):
    """Inbound abstraction: how input sources feed data to the core."""
    
    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        """Receive and process raw data from an input source."""
```

### Parameters

**raw_data** (List[Dict[str, Any]])

A list of dictionaries where each dict represents a data row. Expected keys:

- `Country Name`: String (e.g., "China", "India")
- `Country Code`: 3-letter ISO code (e.g., "CHN", "IND")
- `Continent`: Continent name (e.g., "Asia", "Europe")
- Years as string keys: `"2015"`, `"2016"`, ..., `"2020"`, etc.

Each value is a GDP figure (typically a string that will be converted to float).

### Returns

None. Side effects are the contract (processing and outputting data).

### Implementations

| Class | Module | Description |
|-------|--------|-------------|
| `TransformationEngine` | `core.engine` | Processes data and outputs via injected sink |

### Example Usage

```python
from core.contracts import PipelineService
from core.engine import TransformationEngine
from plugins.outputs import ConsoleWriter

config = {
    "continent": "Asia",
    "year": 2020,
    "start_year": 2015,
    "end_year": 2020
}
sink = ConsoleWriter()

service: PipelineService = TransformationEngine(sink, config)
service.execute([
    {"Country Name": "China", "Country Code": "CHN", "Continent": "Asia", "2015": "...", ...},
    {"Country Name": "India", "Country Code": "IND", "Continent": "Asia", "2015": "...", ...},
    # ...
])
```

## Design Notes

### Why Protocols?

1. **No inheritance coupling** – implementers don't inherit from the protocol
2. **Duck typing** – if it quacks like a DataSink, it is a DataSink
3. **Clear intent** – the protocol clearly documents the contract
4. **Easy testing** – mock implementations are trivial

### Contract Ownership

The **core owns the contracts**. This is critical:

- Core defines what inputs must do (`PipelineService`)
- Core defines what outputs must do (`DataSink`)
- Plugins conform to these rules
- If requirements change, core changes the rules

This prevents plugins from dictating core behavior (true inversion).

### No Circular Dependencies

```
core/contracts.py
    ↑
    | (imported by)
    ↓
core/engine.py, plugins/inputs.py, plugins/outputs.py
    ↓
    | (no imports of the above)
    ↓
core/contracts.py
```

The contracts are at the bottom of the dependency graph – nothing depends on the implementers, only on the protocols themselves.

---

See also: [TransformationEngine API](engine.md)
