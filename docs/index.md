# GDP Analysis Platform

Welcome to the **GDP Analysis Platform** – a production-ready, modular system for advanced statistical analysis of global GDP data.

## What is This?

This platform processes World Bank GDP dataset and produces eight key analytics:

1. **Top 10 / Bottom 10 Countries** by GDP in a given continent and year
2. **Growth Rate** – percent change per country over a date range
3. **Average GDP by Continent** for a given year
4. **Global GDP Trend** – year-by-year aggregate
5. **Fastest Growing Continent** (by absolute change)
6. **Countries with Consistent Decline** (multi-year downturn)
7. **Global Contribution** – each continent's share of world GDP

## Key Features

✅ **Modular Architecture** – Clean separation of concerns (core logic, I/O, configuration)  
✅ **Dependency Inversion** – Core engine is agnostic of file formats and destinations  
✅ **Protocol-Based** – Uses Python typing.Protocol for structural interfaces  
✅ **Pluggable I/O** – Swap data sources and output formats via config.json  
✅ **Well-Documented** – Comprehensive docstrings and this documentation site  
✅ **Production Ready** – Factory patterns, validation, error handling

## Quick Start

### 1. Install Dependencies

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install mkdocs mkdocs-material  # for documentation
```

### 2. Configure Analysis

Edit `config.json`:

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

### 3. Run the Pipeline

```bash
python main.py
```

Results are displayed on console or written to a file (depending on output config).

## Architecture at a Glance

```
main.py (entry point)
  ↓
  ├─→ Loads config.json
  ├─→ Instantiates InputReader (CSVReader or JSONReader)
  ├─→ Instantiates OutputWriter (ConsoleWriter, JSONWriter, etc.)
  ├─→ Creates TransformationEngine and injects the writer
  └─→ Wires reader → engine → writer and executes
```

**Core Design:**
- Engine implements `PipelineService` protocol (inputs call this)
- Engine depends on `DataSink` protocol (outputs implement this)
- Dependencies always point **toward** the core (Dependency Inversion Principle)

## Next Steps

- **[Architecture Overview](architecture/overview.md)** – Deep dive into design
- **[Quick Start Guide](guide/quickstart.md)** – Step-by-step instructions
- **[API Reference](api/contracts.md)** – Detailed class/method documentation
- **[Extending](extend/input_plugins.md)** – Add custom input/output plugins

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Orchestrator & entry point |
| `config.json` | Runtime configuration |
| `core/contracts.py` | Protocol definitions (DataSink, PipelineService) |
| `core/engine.py` | Transformation engine & analytics |
| `plugins/inputs.py` | CSVReader, JSONReader |
| `plugins/outputs.py` | ConsoleWriter, JSONWriter, CSVWriter |

---

**Phase 2**: Modular Orchestration & Dependency Inversion  
Built with Python 3.8+ | Designed for extensibility and maintainability
