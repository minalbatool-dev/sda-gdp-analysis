# SDA GDP Analysis Project (Phase 2)

This repository has been refactored into a **modular architecture** that follows the
Dependency Inversion Principle.  The core business logic is completely decoupled
from data ingestion and persistence.  You can swap input/output implementations
by editing `config.json` alone – no core code needs changing.

---

## Architecture Overview 🏗️

```
main.py       (orchestrator / bootstrap)
│
├─> plugins.inputs   (CSVReader, JSONReader, etc.)
│
├─> core.contracts   (Protocols: `PipelineService`, `DataSink`)
│
├─> core.engine      (TransformationEngine – implements `PipelineService`)
│
└─> plugins.outputs  (ConsoleWriter, JSONWriter, CSVWriter, ...)
```

- **Core** owns the contracts (`Protocol` classes in
  `core/contracts.py`).  All other modules reference these protocols – not
  concrete classes.
- **Inputs** call `PipelineService.execute(...)` with raw rows; the core
  transforms data and passes the result to an injected `DataSink`.
- **Outputs** simply implement `write(records)`; the engine never imports them
  directly.  This is classic outbound abstraction.
- **main.py** reads `config.json`, uses simple dictionary-based factories, and
  wires everything together.

Dependency arrows point *toward* the core; no module leaks business logic.

---

## Running the Pipeline ✅

1. Create and activate a virtual environment (any Python 3.8+):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # see note below
```

2. Edit `config.json` to choose the input/output drivers and analysis
   parameters.  For example:

```json
{
  "input": {
    "type": "csv",
    "path": "data/data.csv"
  },
  "output": {
    "type": "json",
    "path": "out/results.json"
  },
  "parameters": {
    "continent": "Asia",
    "year": 2020,
    "start_year": 2015,
    "end_year": 2020
  }
}
```

3. Launch the orchestrator:

```bash
python main.py
```

Depending on the chosen output driver you'll either see results on the
console or have them written to a file.

> **Tip:** add new reader/writer classes under `plugins/` and register them in
> the factory dictionaries in `main.py` to extend behaviour without touching the
> core.

---

## Supported Drivers

| Module  | Class        | Description                                |
|--------|--------------|--------------------------------------------|
| inputs | `CSVReader`  | Reads CSV files from a path                |
|        | `JSONReader` | Reads JSON arrays                          |
| outputs| `ConsoleWriter` | Pretty‑prints to stdout                   |
|        | `JSONWriter`    | Dumps results to a JSON file              |
|        | `CSVWriter`     | Writes a two‑column CSV (section, payload) |

More can be added – just follow the protocol definitions in
`core/contracts.py`.

---

## Dependencies

This phase only relies on the Python standard library; previous `pandas`
/`matplotlib` dependencies are no longer required unless you intend to
re‑introduce visualizations.  (You can still install them via `pip`.)

---

## Legacy Files

Old scripts from phase‑1 such as `dashboard.py`, `data_loader.py`,
`data_processor.py` etc. remain for reference but are no longer used by
`main.py`.

---

## Next Steps & Testing

- Add unit tests for `TransformationEngine` and the reader/writer plugins.
- Provide a CLI wrapper around `main.bootstrap` to override `config.json`.
- Introduce additional outputs (e.g. chart generator) as separate plugins.

Happy hacking! 🎯
