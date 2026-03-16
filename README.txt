# Phase 3: Generic Concurrent Real-Time Pipeline

## Overview
This is the final phase of the Data Processing Pipeline project. The system has been upgraded to a concurrent, multi-core architecture using Python's `multiprocessing` library. It acts as a real-time data ingestion and processing framework, driven entirely by `config.json`.

## How to Run

1. **Configuration**:
   - The main configuration is stored in `config.json` at the root directory.
   - Specify your input dataset path in `config.json` under `dataset_path`. By default, it looks for `sample_sensor_data.csv` in the root folder.
   
2. **Execution**:
   - Ensure you have Python 3.8+ installed. No external pip packages are strictly required as everything uses the Python Standard Library.
   - Run the main orchestrator script from the root directory:
     ```bash
     python main.py
     ```

## Architecture Notes
- **Input Stream**: Producer reads rows over time and acts on a bounded multiprocessing queue.
- **Core Processing**: Multiple independent worker processes calculate PBKDF2 signatures and utilize the functional core (`processors.py`) to maintain state.
- **Telemetry**: Observer Pattern enables UI visualizers to track real-time queue backpressure without violating the Dependency Inversion Principle.
- **Design Artifacts**: The Class Diagram (`architecture.puml`) and Sequence Diagram (`sequence.puml`), along with their PNG renders, reflect these additions.