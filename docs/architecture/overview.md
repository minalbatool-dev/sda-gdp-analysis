# Architecture Overview

## System Design Principles

The GDP Analysis Platform follows **SOLID principles**, specifically:

- **S**ingle Responsibility: Each module has one reason to change
- **O**pen/Closed: Extensible for new plugins without modifying core
- **L**iskov Substitution: Any plugin satisfying the protocol works
- **I**nterface Segregation: Small, focused protocols
- **D**ependency Inversion: Core depends on abstractions, not concrete classes

## Package Structure

```
project_root/
├── main.py                 # Bootstrap / Orchestrator
├── config.json             # Configuration (JSON)
├── core/
│   ├── __init__.py
│   ├── contracts.py        # Protocol definitions
│   └── engine.py           # Business logic & analytics
├── plugins/
│   ├── __init__.py
│   ├── inputs.py           # Data source readers
│   └── outputs.py          # Result writers
└── data/
    ├── data.csv            # World Bank GDP data (CSV)
    └── data.json           # Same data (JSON format)
```

## Dependency Graph

```
┌─────────────────────────────────────┐
│          main.py                    │
│   (Orchestrator / Bootstrap)        │
│                                     │
│  • Reads config.json                │
│  • Instantiates factories           │
│  • Performs Dependency Injection    │
└──────────┬──────────┬──────────────┘
           │          │
           ▼          ▼
    ┌──────────┐  ┌──────────┐
    │ Input    │  │ Output   │
    │ Drivers  │  │ Drivers  │
    │(Plugins) │  │(Plugins) │
    └──────┬───┘  └────┬─────┘
           │           │
           └─────┬─────┘
                 ▼
         ┌───────────────┐
         │  Protocols:   │
         │               │
         │ • DataSink    │
         │ • Pipeline    │
         │   Service     │
         │               │
         │  (in core/)   │
         └───────┬───────┘
                 ▼
    ┌────────────────────────┐
    │  TransformationEngine  │
    │   (implements both)    │
    │                        │
    │  • Processes data      │
    │  • Computes analytics  │
    │  • Outputs via sink    │
    └────────────────────────┘
```

**Key insight:** Arrows point **toward** the core. No module leaks business logic.

## Information Flow

1. **Input Phase**
   - `CSVReader` or `JSONReader` parses raw file
   - Calls `engine.execute(raw_data)`

2. **Processing Phase**
   - `TransformationEngine` validates data
   - Filters invalid/aggregate countries
   - Computes eight analytics

3. **Output Phase**
   - Engine calls `sink.write(results)`
   - Sink (ConsoleWriter, JSONWriter, etc.) persists results

```
raw_data (CSV/JSON) ──→ Reader ──→ engine.execute() 
                                      ↓
                              Engine processes
                                      ↓
                            sink.write(results)
                                      ↓
                         Output (console/file/...)
```

## Protocols (Structural Interfaces)

The system uses `typing.Protocol` for duck typing:

```python
@runtime_checkable
class DataSink(Protocol):
    """Implemented by ConsoleWriter, JSONWriter, CSVWriter, etc."""
    def write(self, data: Dict[str, Any]) -> None: ...

class PipelineService(Protocol):
    """Implemented by TransformationEngine."""
    def execute(self, raw_data: List[Dict[str, Any]]) -> None: ...
```

No inheritance needed – any class with matching methods satisfies the protocol.

## Extensibility

### Adding a New Input Format

1. Create a class in `plugins/inputs.py`:
   ```python
   class YAMLReader:
       def __init__(self, filepath, service: PipelineService): ...
       def read(self): ...  # calls service.execute(data)
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

1. Create a class in `plugins/outputs.py`:
   ```python
   class DatabaseWriter:
       def __init__(self, host, port, **kwargs): ...
       def write(self, data): ...  # implements DataSink
   ```

2. Register in `main.py`:
   ```python
   OUTPUT_DRIVERS["database"] = DatabaseWriter
   ```

3. Use in `config.json`:
   ```json
   {"output": {"type": "database", "host": "localhost", "port": 5432}}
   ```

## Configuration-Driven Behavior

The `config.json` file drives the entire pipeline:

- **Input type & path**: Which data source to read
- **Output type & parameters**: Where/how to write results
- **Analysis parameters**: continent, year, date range for metrics

This means you can switch implementations **without changing code** – just edit the JSON file.

---

See also: [**Dependency Inversion** deep-dive](dependency_inversion.md)
