import csv
import time


class InputReader:

    def __init__(self, config, raw_queue):

        self.config = config
        self.raw_queue = raw_queue

        self.dataset_path = config.get("dataset_path")

        dynamics = config.get("pipeline_dynamics", {})
        self.delay = dynamics.get("input_delay_seconds", 0.01)

        self.schema = config.get("schema_mapping", {}).get("columns", [])

    # ----------------------------------
    # Map CSV row → generic internal record
    # ----------------------------------
    def map_row(self, row):

        mapped_record = {}

        for col_def in self.schema:

            csv_name = col_def.get("source_name", col_def.get("csv_name"))
            internal_name = col_def["internal_mapping"]
            dtype = col_def.get("data_type", col_def.get("type"))

            val = row.get(csv_name)

            if val is None:
                mapped_record[internal_name] = None
                continue

            try:
                if dtype == "float":
                    mapped_record[internal_name] = float(val)

                elif dtype == "integer":
                    mapped_record[internal_name] = int(val)

                else:
                    mapped_record[internal_name] = val

            except:
                mapped_record[internal_name] = None

        return mapped_record

    # ----------------------------------
    # Producer loop
    # ----------------------------------
    def run(self):

        try:

            with open(self.dataset_path, "r", newline="") as f:

                reader = csv.DictReader(f, delimiter=",")

                for row in reader:

                    mapped_record = self.map_row(row)

                    self.raw_queue.put(mapped_record)

                    time.sleep(self.delay)

        except Exception as e:

            print("[INPUT ERROR]", e)

        finally:

            print("[INPUT] Dataset fully streamed.")
