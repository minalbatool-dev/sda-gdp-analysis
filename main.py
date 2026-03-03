"""Orchestrator: bootstrap layer for the GDP analysis pipeline.

This module is the entry point. It reads configuration from config.json,
instantiates concrete implementations using dictionary-based factories,
and wires the components together via Dependency Injection.

Key Concepts:
    1. **Factories**: INPUT_DRIVERS and OUTPUT_DRIVERS map config strings to classes
    2. **DI Helper**: _make_sink() instantiates output drivers with config kwargs
    3. **Bootstrap**: bootstrap() orchestrates the full pipeline: load config,
                     create sink, create engine, create input, run

Workflow:
    1. Load config.json (specifies input type, path, output type, parameters)
    2. Call _make_sink(output_cfg) to create the output writer
    3. Create TransformationEngine(sink, parameters)
    4. Create input reader (CSVReader, JSONReader, etc.)
    5. Call reader.read() which feeds data to engine

Design Principle:
    The main module must NOT import core business logic. It wires the system
    using protocols, letting plugins satisfy contracts via duck typing.

Example config.json:
    {
      "input": {"type": "csv", "path": "data/data.csv"},
      "output": {"type": "json", "path": "out/results.json"},
      "parameters": {
        "continent": "Asia",
        "year": 2020,
        "start_year": 2015,
        "end_year": 2020
      }
    }

Extending the System:
    1. To add a new input format: Create a class in plugins/inputs.py,
       register it in INPUT_DRIVERS, and it's ready to use.
    2. To add a new output format: Create a class in plugins/outputs.py,
       register it in OUTPUT_DRIVERS, pass config via output dict in config.json.

See Also:
    - config.json: Configuration file
    - core/contracts.py: Protocol definitions
    - core/engine.py: Business logic
"""

import json
from typing import Any, Dict

from core import TransformationEngine
from plugins import (
    CSVReader,
    JSONReader,
    ConsoleWriter,
    JSONWriter,
    CSVWriter,
)

# Factory registries --------------------------------------------------------
INPUT_DRIVERS = {
    "csv": CSVReader,
    "json": JSONReader,
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter,
    "json": JSONWriter,
    "csv": CSVWriter,
}


def _make_sink(output_cfg: Dict[str, Any]) -> Any:
    """Instantiate an output driver from a configuration dictionary.

    The dict must include a ``type`` key; any other entries are forwarded as
    keyword arguments to the constructor.  This keeps ``main`` generic so new
    writers can expose parameters without changing the orchestrator.
    """

    typ = output_cfg.get("type")
    if typ not in OUTPUT_DRIVERS:
        raise ValueError(f"unknown output type {typ!r}")
    cls = OUTPUT_DRIVERS[typ]
    kwargs = {k: v for k, v in output_cfg.items() if k != "type"}
    return cls(**kwargs)


def bootstrap() -> None:
    # load runtime configuration
    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    input_type = cfg["input"]["type"]
    input_path = cfg["input"]["path"]
    output_cfg = cfg["output"]
    parameters = cfg.get("parameters", {})

    # create sink & core engine
    sink = _make_sink(output_cfg)
    engine = TransformationEngine(sink, parameters)

    # wire input to engine
    reader_cls = INPUT_DRIVERS[input_type]
    reader = reader_cls(input_path, engine)

    # run the pipeline
    reader.read()


if __name__ == "__main__":
    bootstrap()
