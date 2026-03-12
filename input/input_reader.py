import csv
import time
from typing import Dict, Any
from multiprocessing import Queue

class InputReader:
    """Producer: Reads raw data, maps schema dynamically, and feeds raw_queue."""

    def __init__(self, config: Dict[str, Any], raw_queue: Queue):
        self.config = config
        self.raw_queue = raw_queue

    def run(self):
        """Starts reading the stream and pushing generic packets."""
        dataset_path = self.config["dataset_path"]
        # Fallback to absolute/relative dynamic resolution if needed, but try config relative first
        import os
        if not os.path.exists(dataset_path) and os.path.exists(f"phase3/{dataset_path}"):
            dataset_path = f"phase3/{dataset_path}"
        delay = self.config.get("pipeline_dynamics", {}).get("input_delay_seconds", 0.05)
        schema = self.config.get("schema_mapping", {}).get("columns", [])

        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    mapped_record = self._map_row(row, schema)
                    
                    # Create generic data packet
                    # Sleep to simulate delay and create queue backpressure
                    time.sleep(delay)
                    self.raw_queue.put(mapped_record)

        except Exception as e:
            print(f"InputReader Error: {e}")

        # Signal end of stream by putting Nones
        # Main orchestrator will dictate how many Nones based on parallelism
        # But this is just a single producer, so we will handle poison pills in main.
        
    def _map_row(self, row: Dict[str, str], schema: list) -> Dict[str, Any]:
        """Maps specific column names to generic internal variables with casting."""
        mapped_record = {}
        for col_def in schema:
            source_val = row.get(col_def["source_name"])
            if source_val is None:
                continue

            # Cast data type strictly based on schema config
            val = source_val
            data_type = col_def.get("data_type", "string")
            if data_type == "integer":
                val = int(val)
            elif data_type == "float":
                val = float(val)
            elif data_type == "string":
                val = str(val)

            mapped_record[col_def["internal_mapping"]] = val
            
        return mapped_record
