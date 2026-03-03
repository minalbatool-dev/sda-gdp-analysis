# Core Contracts (Protocols)

## Overview

The **contracts** are the backbone of the system – they define the "shape" that each module must have. Because we use Python's `typing.Protocol`, these are **structural interfaces** (duck typing), not classical inheritance-based interfaces.

## DataSink Protocol

**Where it lives:** `core/contracts.py`

**Purpose:** Defines the output abstraction. The engine calls this; outputs implement it.

```python
@runtime_checkable
class DataSink(Protocol):
    def write(self, data: Dict[str, Any]) -> None:
        """Persist or display the analysis results."""
        ...
```

### Implementers

All of the following satisfy `DataSink`:

- **ConsoleWriter**: Prints dict to stdout
- **JSONWriter**: Writes to JSON file (passed `path` in config)
- **CSVWriter**: Writes to CSV file (passed `path` in config)

### Example Usage

```python
from core.contracts import DataSink
from plugins.outputs import ConsoleWriter

# ConsoleWriter is a valid DataSink
sink: DataSink = ConsoleWriter()
sink.write({"top_10": [...]})  # ✓ works
```

## PipelineService Protocol

**Where it lives:** `core/contracts.py`

**Purpose:** Defines the input abstraction. Inputs call this; the core engine implements it.

```python
class PipelineService(Protocol):
    def execute(self, raw_data: List[Dict[str, Any]]) -> None:
        """Receive and process raw data from an input source."""
        ...
```

### Implementers

- **TransformationEngine**: The only built-in implementer (in `core/engine.py`)

### Example Usage

```python
from core.contracts import PipelineService
from core.engine import TransformationEngine
from plugins.outputs import ConsoleWriter

# TransformationEngine is a valid PipelineService
config = {"continent": "Asia", "year": 2020, ...}
sink = ConsoleWriter()
service: PipelineService = TransformationEngine(sink, config)

# Inputs call this
service.execute(raw_data)  # ✓ works
```

## Why Protocols?

### Benefits

1. **No Import Coupling**: Modules don't need to import concrete classes
2. **True Decoupling**: The core never knows about plugins
3. **Easy Testing**: Mock objects automatically satisfy protocols
4. **Duck Typing**: "If it looks like a DataSink, it is a DataSink"
5. **Pythonic**: Uses standard library (`typing.Protocol`)

### Example: How a New Output Works

Even if you create a custom writer **without importing anything**:

```python
# custom_output.py
class MyCustomWriter:
    def write(self, data):
        # do something custom
        pass
```

It automatically satisfies `DataSink` because it has the `write` method!

```python
from custom_output import MyCustomWriter

# Doesn't fail even though MyCustomWriter never imported DataSink
sink: DataSink = MyCustomWriter()
engine.execute(data)  # Works!
```

## Contract Ownership

**Core owns the contracts.** This is critical for Dependency Inversion:

- Core defines `DataSink` and `PipelineService`
- Core defines what plugs must look like
- Plugins must conform; they don't negotiate

This prevents the tail (plugins) from wagging the dog (core).

---

See also: [Dependency Inversion Principle](dependency_inversion.md)
